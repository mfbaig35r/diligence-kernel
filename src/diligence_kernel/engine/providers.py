"""Model providers behind one interface.

The engine makes exactly one kind of call: a stable cached prefix, a short varying
instruction, and a schema the answer must satisfy. Both providers support all three; what
differs is how the cache is addressed.

- **OpenAI** caches input prefixes automatically once they exceed a minimum length, and
  `prompt_cache_key` routes identical prefixes to the same cache. The unit-major design is
  exactly what that rewards, so the prefix carries the unit's key.
- **Anthropic** caches only where a `cache_control` breakpoint is placed, so the prefix ends
  with one.

Either way the engine's rule is unchanged: stable content first, volatile content last.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass(slots=True)
class PromptPrefix:
    """The part of a request that is identical for every column of one review unit."""

    text: str
    cache_key: str

    def __len__(self) -> int:
        return len(self.text)


@dataclass(slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0

    def add(self, other: Usage) -> None:
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.cache_read_tokens += other.cache_read_tokens
        self.cache_write_tokens += other.cache_write_tokens


class ProviderUnavailable(RuntimeError):
    """The provider's SDK is missing, or no credentials resolved."""


class Provider(ABC):
    name: str
    default_model: str
    default_effort: str
    #: What a cached input token costs relative to a fresh one.
    cache_read_multiplier: float = 0.1
    #: What writing a token into the cache costs relative to a fresh one.
    cache_write_multiplier: float = 1.0
    #: Prefixes shorter than this are not cached at all, so an estimate must not assume they are.
    min_cacheable_tokens: int = 1024

    @abstractmethod
    def complete(
        self,
        *,
        prefix: PromptPrefix,
        user: str,
        schema: type[BaseModel],
        model: str,
        effort: str,
        max_tokens: int,
    ) -> tuple[BaseModel, Usage]:
        """One structured answer, or raise."""

    @abstractmethod
    def count_tokens(self, model: str, prefix: PromptPrefix, user: str) -> tuple[int, bool]:
        """Input tokens for one request, and whether the count is exact."""

    def pricing(self, model: str) -> tuple[float, float] | None:
        """USD per million (input, output), or None when this model's price is unknown here."""
        return PRICING.get(self.name, {}).get(model)


# ---------------------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------------------


class OpenAIProvider(Provider):
    name = "openai"
    default_model = "gpt-5"
    default_effort = "medium"
    cache_read_multiplier = 0.1
    cache_write_multiplier = 1.0
    min_cacheable_tokens = 1024

    def __init__(self, client: Any | None = None) -> None:
        self._client = client
        self._encoding: Any | None = None

    @property
    def client(self) -> Any:
        if self._client is None:
            try:
                import openai
            except ImportError as exc:
                raise ProviderUnavailable(
                    "The openai SDK is not installed. Install with: pip install openai"
                ) from exc
            self._client = openai.OpenAI()
        return self._client

    def complete(
        self,
        *,
        prefix: PromptPrefix,
        user: str,
        schema: type[BaseModel],
        model: str,
        effort: str,
        max_tokens: int,
    ) -> tuple[BaseModel, Usage]:
        response = self.client.responses.parse(
            model=model,
            instructions=prefix.text,
            input=user,
            text_format=schema,
            reasoning={"effort": effort},
            max_output_tokens=max_tokens,
            # Routes requests that share this prefix to the same cache.
            prompt_cache_key=prefix.cache_key,
            store=False,
        )
        answer = response.output_parsed
        if answer is None:
            raise RuntimeError(
                f"The model returned no parsable answer (status={response.status!r}). "
                "A cell was left unfilled rather than guessed."
            )
        return answer, _openai_usage(response)

    def count_tokens(self, model: str, prefix: PromptPrefix, user: str) -> tuple[int, bool]:
        """Counted locally with tiktoken: free, offline, and needs no credentials.

        Exact for the text; it does not include the few tokens of request scaffolding, so it
        reads slightly low. Reported as approximate for that reason.
        """
        try:
            import tiktoken
        except ImportError:
            return (len(prefix.text) + len(user)) // 4, False
        if self._encoding is None:
            try:
                self._encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                self._encoding = tiktoken.get_encoding("o200k_base")
        return len(self._encoding.encode(prefix.text)) + len(self._encoding.encode(user)), False


def _openai_usage(response: Any) -> Usage:
    raw = getattr(response, "usage", None)
    if raw is None:
        return Usage()
    details = getattr(raw, "input_tokens_details", None)
    cached = int(getattr(details, "cached_tokens", 0) or 0) if details else 0
    written = int(getattr(details, "cache_write_tokens", 0) or 0) if details else 0
    total_in = int(getattr(raw, "input_tokens", 0) or 0)
    return Usage(
        # OpenAI reports cached tokens inside input_tokens; separate them so cost is right.
        input_tokens=max(0, total_in - cached),
        output_tokens=int(getattr(raw, "output_tokens", 0) or 0),
        cache_read_tokens=cached,
        cache_write_tokens=written,
    )


# ---------------------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------------------


class AnthropicProvider(Provider):
    name = "anthropic"
    default_model = "claude-opus-5"
    default_effort = "high"
    cache_read_multiplier = 0.1
    cache_write_multiplier = 1.25
    min_cacheable_tokens = 1024

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:
                raise ProviderUnavailable(
                    "The anthropic SDK is not installed. Install with: pip install anthropic"
                ) from exc
            self._client = anthropic.Anthropic()
        return self._client

    def _system(self, prefix: PromptPrefix) -> list[dict[str, Any]]:
        return [
            {
                "type": "text",
                "text": prefix.text,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    def complete(
        self,
        *,
        prefix: PromptPrefix,
        user: str,
        schema: type[BaseModel],
        model: str,
        effort: str,
        max_tokens: int,
    ) -> tuple[BaseModel, Usage]:
        response = self.client.messages.parse(
            model=model,
            max_tokens=max_tokens,
            system=self._system(prefix),
            messages=[{"role": "user", "content": user}],
            output_format=schema,
            output_config={"effort": effort},
        )
        answer = getattr(response, "parsed_output", None)
        if answer is None:
            raise RuntimeError(
                f"The model returned no parsable answer "
                f"(stop_reason={getattr(response, 'stop_reason', None)!r}). "
                "A cell was left unfilled rather than guessed."
            )
        return answer, _anthropic_usage(response)

    def count_tokens(self, model: str, prefix: PromptPrefix, user: str) -> tuple[int, bool]:
        """Counted by the API's free token-counting endpoint, so it is exact."""
        counted = self.client.messages.count_tokens(
            model=model,
            system=self._system(prefix),
            messages=[{"role": "user", "content": user}],
        )
        return int(getattr(counted, "input_tokens", 0) or 0), True


def _anthropic_usage(response: Any) -> Usage:
    raw = getattr(response, "usage", None)
    if raw is None:
        return Usage()
    return Usage(
        input_tokens=int(getattr(raw, "input_tokens", 0) or 0),
        output_tokens=int(getattr(raw, "output_tokens", 0) or 0),
        cache_read_tokens=int(getattr(raw, "cache_read_input_tokens", 0) or 0),
        cache_write_tokens=int(getattr(raw, "cache_creation_input_tokens", 0) or 0),
    )


# ---------------------------------------------------------------------------------------
# pricing and selection
# ---------------------------------------------------------------------------------------

#: USD per million tokens, (input, output). Deliberately partial: a model absent here
#: reports its cost as unknown rather than being priced from a stale guess. Override for
#: any model with DILIGENCE_KERNEL_PRICE_IN and DILIGENCE_KERNEL_PRICE_OUT.
PRICING: dict[str, dict[str, tuple[float, float]]] = {
    "openai": {
        "gpt-5": (1.25, 10.00),
        "gpt-5-mini": (0.25, 2.00),
        "gpt-5-nano": (0.05, 0.40),
        "gpt-4.1": (2.00, 8.00),
        "gpt-4.1-mini": (0.40, 1.60),
        "gpt-4.1-nano": (0.10, 0.40),
        "o3": (2.00, 8.00),
        "o4-mini": (1.10, 4.40),
    },
    "anthropic": {
        "claude-fable-5-1": (10.00, 50.00),
        "claude-fable-5": (10.00, 50.00),
        "claude-opus-5": (5.00, 25.00),
        "claude-opus-4-8": (5.00, 25.00),
        "claude-sonnet-5": (2.00, 10.00),
        "claude-haiku-4-5": (1.00, 5.00),
    },
}

PROVIDERS: dict[str, type[Provider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
}

DEFAULT_PROVIDER = "openai"


def get_provider(name: str | None = None, *, client: Any | None = None) -> Provider:
    """Resolve the provider, from the argument, then DILIGENCE_KERNEL_PROVIDER, then default."""
    key = (name or os.environ.get("DILIGENCE_KERNEL_PROVIDER") or DEFAULT_PROVIDER).lower()
    cls = PROVIDERS.get(key)
    if cls is None:
        raise ProviderUnavailable(
            f"Unknown provider {key!r}. Known: {', '.join(sorted(PROVIDERS))}."
        )
    return cls(client=client)


def price_override() -> tuple[float, float] | None:
    """A price the operator states for a model this table does not carry."""
    raw_in = os.environ.get("DILIGENCE_KERNEL_PRICE_IN")
    raw_out = os.environ.get("DILIGENCE_KERNEL_PRICE_OUT")
    if raw_in is None or raw_out is None:
        return None
    try:
        return float(raw_in), float(raw_out)
    except ValueError:
        return None


def estimate_cost(
    provider: Provider,
    model: str,
    *,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
) -> float | None:
    """USD for a token profile, or None when the model's price is not known."""
    price = price_override() or provider.pricing(model)
    if price is None:
        return None
    per_in, per_out = price
    return (
        input_tokens * per_in
        + cache_read_tokens * per_in * provider.cache_read_multiplier
        + cache_write_tokens * per_in * provider.cache_write_multiplier
        + output_tokens * per_out
    ) / 1_000_000
