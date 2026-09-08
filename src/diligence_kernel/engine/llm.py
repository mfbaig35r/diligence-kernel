"""The model call that fills one cell.

Structure of a request, and why:

    system   = [ Table Instructions (cached) , the review unit's evidence (cached) ]
    messages = [ established upstream results + the column prompt ]

The unit's documents are the bulk of the tokens and are identical for every column of
that unit, so they go in the cached prefix and the engine iterates unit-major. A 27-column
table then pays for its documents once per unit instead of 27 times.

The column prompt goes last because 00a section 6 orders a prompt so the final instruction
is the output contract.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

DEFAULT_MODEL = "claude-opus-5"
DEFAULT_EFFORT = "high"
DEFAULT_MAX_TOKENS = 4096

#: 00a's shared rules, restated as the operator contract for a cell.
CELL_CONTRACT = """You are filling one cell of a legal diligence review table.

Return the normalized answer only. Reasoning, section numbers, and citations belong in the
evidence you cite, never in the cell value.

- Analyze only the documents in the current review unit. Do not use other rows, file names,
  or outside knowledge of the parties.
- Report, never compute. State every figure as the document states it. Do not add, subtract,
  net, reconcile, or derive anything.
- Filed is not adopted; adopted is not current; signed is not effective. Where the evidence
  does not support a completed act, write `purports to`, `would`, or `proposed`.
- Use only these fallback states, with the meaning the column defines: `Not addressed`,
  `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`. A fallback
  state never replaces a value the document states, and a silent document is
  `Not addressed`, never `Unable to determine`.
- Do not use markdown in the cell value.

Cite the exact sentences you relied on in `evidence`, quoted verbatim from the documents in
this unit. If you relied on no text because the documents are silent, return an empty list.
"""


class CellAnswer(BaseModel):
    """The shape every cell response must take."""

    value: str = Field(
        description="The cell value alone: an option, a date, a figure as "
        "stated, a short answer, or one of the fallback states."
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Sentences quoted verbatim from the documents in this review unit that "
        "support the value. Empty when the documents are silent.",
    )
    source_document: str | None = Field(
        default=None,
        description="Printed title or filename of the document the value was read from.",
    )


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


@dataclass(slots=True)
class CellRequest:
    column_name: str
    prompt_text: str
    native_type: str
    configured_options: list[str] = field(default_factory=list)
    established: dict[str, str] = field(default_factory=dict)


class LLMUnavailable(RuntimeError):
    """No API credentials, or the SDK is not installed."""


class CellFiller:
    """Fills cells for one review unit, reusing that unit's cached evidence prefix."""

    def __init__(
        self,
        *,
        model: str | None = None,
        effort: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        client: Any | None = None,
    ) -> None:
        self.model = model or os.environ.get("DILIGENCE_KERNEL_MODEL", DEFAULT_MODEL)
        self.effort = effort or os.environ.get("DILIGENCE_KERNEL_EFFORT", DEFAULT_EFFORT)
        self.max_tokens = max_tokens
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - dependency is declared
                raise LLMUnavailable("The anthropic SDK is not installed.") from exc
            self._client = anthropic.Anthropic()
        return self._client

    # -- prompt assembly ---------------------------------------------------------------

    def build_system(
        self,
        *,
        table_instructions: str,
        unit_label: str,
        evidence_blocks: list[dict[str, object]],
    ) -> list[dict[str, Any]]:
        """The cached prefix: the contract, the table's instructions, and the unit."""
        documents = "\n\n".join(
            f"<document title={d.get('filename')!r} role={d.get('role') or 'unstated'!r}"
            f"{' truncated=true' if d.get('truncated') else ''}>\n{d.get('text', '')}\n</document>"
            for d in evidence_blocks
        )
        head = CELL_CONTRACT
        if table_instructions:
            head += "\n\n## Table Instructions\n\n" + table_instructions
        return [
            {"type": "text", "text": head},
            {
                "type": "text",
                "text": f"## Review unit: {unit_label}\n\n{documents}",
                "cache_control": {"type": "ephemeral"},
            },
        ]

    def build_user(self, request: CellRequest) -> str:
        parts: list[str] = []
        if request.established:
            lines = "\n".join(f"- {k}: {v}" for k, v in request.established.items())
            parts.append(
                "## Established results\n\n"
                "These are answers already recorded for this row. Treat them as given.\n\n" + lines
            )
        if request.native_type == "Classify" and request.configured_options:
            options = "\n".join(f"- {o}" for o in request.configured_options)
            parts.append(f"## Configured options\n\nReturn exactly one of these:\n\n{options}")
        parts.append(f"## Column: {request.column_name}\n\n{request.prompt_text}")
        return "\n\n---\n\n".join(parts)

    # -- the call ------------------------------------------------------------------------

    def fill(
        self,
        request: CellRequest,
        *,
        system: list[dict[str, Any]],
    ) -> tuple[CellAnswer, Usage]:
        """One cell. Raises for transport errors; the SDK retries 429 and 5xx itself."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": self.build_user(request)}],
            "output_format": CellAnswer,
            "output_config": {"effort": self.effort},
        }
        response = self.client.messages.parse(**kwargs)
        usage = _usage_of(response)
        answer = getattr(response, "parsed_output", None)
        if answer is None:
            raise RuntimeError(
                f"The model returned no parsable answer for {request.column_name!r} "
                f"(stop_reason={getattr(response, 'stop_reason', None)})."
            )
        return answer, usage


def _usage_of(response: Any) -> Usage:
    raw = getattr(response, "usage", None)
    if raw is None:
        return Usage()
    return Usage(
        input_tokens=getattr(raw, "input_tokens", 0) or 0,
        output_tokens=getattr(raw, "output_tokens", 0) or 0,
        cache_read_tokens=getattr(raw, "cache_read_input_tokens", 0) or 0,
        cache_write_tokens=getattr(raw, "cache_creation_input_tokens", 0) or 0,
    )
