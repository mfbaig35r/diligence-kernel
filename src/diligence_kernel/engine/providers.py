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

    def pricing(self, model: str) -> Price | None:
        """The model's published rates, or None when they are not recorded here."""
        return PRICING.get(self.name, {}).get(model)


# ---------------------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------------------


class OpenAIProvider(Provider):
    name = "openai"
    # Measured on Table 05 over the fixture data room: gpt-5.6-luna scored identically to
    # gpt-5.4 (30/34 each, zero disagreements either way) at a fifteenth of the cost. Raise
    # the model per table where judgment matters more than classification does.
    default_model = "gpt-5.6-luna"
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


@dataclass(frozen=True, slots=True)
class Price:
    """USD per million tokens for one model.

    Cached input and cache writes are separate line items and vary by model, so they are not
    a single provider-wide multiplier. Some models bill nothing for a cache write; on others
    it is a premium over fresh input. `long_*` applies above `LONG_CONTEXT_THRESHOLD`.
    """

    input: float
    output: float
    cached_input: float | None = None
    #: None means a cache write is not separately charged.
    cache_write: float | None = None
    long_input: float | None = None
    long_output: float | None = None
    long_cached_input: float | None = None
    long_cache_write: float | None = None

    def at(self, tokens: int) -> tuple[float, float, float, float]:
        """(input, cached input, cache write, output) rates for a request of this size."""
        long = tokens >= LONG_CONTEXT_THRESHOLD and self.long_input is not None
        if long:
            return (
                self.long_input or self.input,
                self.long_cached_input
                if self.long_cached_input is not None
                else (self.long_input or self.input) * 0.1,
                self.long_cache_write or 0.0,
                self.long_output or self.output,
            )
        return (
            self.input,
            self.cached_input if self.cached_input is not None else self.input * 0.1,
            self.cache_write or 0.0,
            self.output,
        )


#: Where a request moves onto long-context rates. **Assumed**, not confirmed against the
#: price list: correct it if OpenAI publishes a different boundary. Review units in this
#: corpus run a few thousand tokens, so it rarely binds — but a large lease could.
LONG_CONTEXT_THRESHOLD = 128_000

#: Deliberately partial: a model absent here reports its cost as unknown rather than being
#: priced from a stale guess. Override any model with DILIGENCE_KERNEL_PRICE_IN / _OUT.
PRICING: dict[str, dict[str, Price]] = {
    "openai": {
        "gpt-6-astra": Price(10.00, 50.00, 1.00, 12.50, 20.00, 75.00, 2.00, 25.00),
        "gpt-5.6-sol": Price(4.00, 20.00, 0.40, 5.00, 8.00, 30.00, 0.80, 10.00),
        "gpt-5.6-terra": Price(2.00, 12.00, 0.20, 2.50, 4.00, 18.00, 0.40, 5.00),
        "gpt-5.6-luna": Price(0.20, 1.20, 0.02, 0.25, 0.40, 1.80, 0.04, 0.50),
        "gpt-5.5": Price(5.00, 30.00, 0.50, None, 10.00, 45.00, 1.00, None),
        "gpt-5.5-pro": Price(30.00, 180.00, None, None, 60.00, 270.00, None, None),
        "gpt-5.4": Price(2.50, 15.00, 0.25, None, 5.00, 22.50, 0.50, None),
        "gpt-5.4-pro": Price(30.00, 180.00, None, None, 60.00, 270.00, None, None),
        # Not on the current published price list. These rates are from an earlier one and
        # are unverified; treat any figure derived from them as indicative.
        "gpt-5": Price(1.25, 10.00, 0.125),
        "gpt-5-mini": Price(0.25, 2.00, 0.025),
        "gpt-5-nano": Price(0.05, 0.40, 0.005),
    },
    "anthropic": {
        "claude-fable-5-1": Price(10.00, 50.00),
        "claude-fable-5": Price(10.00, 50.00),
        "claude-opus-5": Price(5.00, 25.00, cache_write=6.25),
        "claude-opus-4-8": Price(5.00, 25.00, cache_write=6.25),
        "claude-sonnet-5": Price(2.00, 10.00, cache_write=2.50),
        "claude-haiku-4-5": Price(1.00, 5.00, cache_write=1.25),
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
    """USD for a token profile, or None when the model's price is not known.

    Cached input and cache writes are billed at their own published rates, which differ by
    model — on some, a cache write costs nothing; on others it is a premium over fresh input.
    """
    override = price_override()
    price = Price(*override) if override else provider.pricing(model)
    if price is None:
        return None
    per_in, per_cached, per_write, per_out = price.at(
        input_tokens + cache_read_tokens + cache_write_tokens
    )
    return (
        input_tokens * per_in
        + cache_read_tokens * per_cached
        + cache_write_tokens * per_write
        + output_tokens * per_out
    ) / 1_000_000
