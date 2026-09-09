"""The model call that fills one cell, independent of which provider makes it.

Structure of a request, and why:

    prefix = the cell contract + the table's Table Instructions + the review unit's documents
    user   = established upstream results + the column prompt

The unit's documents are the bulk of the tokens and are identical for every column of that
unit, so they go in the prefix and the engine iterates unit-major. A 27-column table then
pays for its documents once per unit instead of 27 times. Both providers cache a stable
prefix; `providers.py` handles how each one is told to.

The column prompt goes last because 00a section 6 orders a prompt so the final instruction
is the output contract.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from .providers import (  # noqa: F401  (re-exported for callers)
    PromptPrefix,
    Provider,
    ProviderUnavailable,
    Usage,
    estimate_cost,
    get_provider,
)

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
        description="Sentences quoted verbatim from the documents in this review unit that "
        "support the value. Empty when the documents are silent.",
    )
    source_document: str | None = Field(
        description="Printed title or filename of the document the value was read from, or "
        "null when no single document supplied it.",
    )


@dataclass(slots=True)
class CellRequest:
    column_name: str
    prompt_text: str
    native_type: str
    configured_options: list[str] = field(default_factory=list)
    established: dict[str, str] = field(default_factory=dict)


class CellFiller:
    """Fills cells for one review unit, reusing that unit's cached prefix."""

    def __init__(
        self,
        *,
        provider: Provider | str | None = None,
        model: str | None = None,
        effort: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> None:
        self.provider = provider if isinstance(provider, Provider) else get_provider(provider)
        self.model = model or os.environ.get("DILIGENCE_KERNEL_MODEL", self.provider.default_model)
        self.effort = effort or os.environ.get(
            "DILIGENCE_KERNEL_EFFORT", self.provider.default_effort
        )
        self.max_tokens = max_tokens

    # -- prompt assembly ---------------------------------------------------------------

    def build_system(
        self,
        *,
        table_instructions: str,
        unit_label: str,
        evidence_blocks: list[dict[str, object]],
        cache_key: str | None = None,
    ) -> PromptPrefix:
        """The cached prefix: the contract, the table's instructions, and the unit."""
        documents = "\n\n".join(
            f"<document title={d.get('filename')!r} role={d.get('role') or 'unstated'!r}"
            f"{' truncated=true' if d.get('truncated') else ''}>\n{d.get('text', '')}\n</document>"
            for d in evidence_blocks
        )
        text = CELL_CONTRACT
        if table_instructions:
            text += "\n\n## Table Instructions\n\n" + table_instructions
        text += f"\n\n## Review unit: {unit_label}\n\n{documents}"
        return PromptPrefix(text=text, cache_key=cache_key or unit_label)

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

    def fill(self, request: CellRequest, *, system: PromptPrefix) -> tuple[CellAnswer, Usage]:
        """One cell. Raises for transport errors; the SDKs retry 429 and 5xx themselves."""
        answer, usage = self.provider.complete(
            prefix=system,
            user=self.build_user(request),
            schema=CellAnswer,
            model=self.model,
            effort=self.effort,
            max_tokens=self.max_tokens,
        )
        return answer, usage  # type: ignore[return-value]

    def count(self, request: CellRequest, *, system: PromptPrefix) -> tuple[int, bool]:
        return self.provider.count_tokens(self.model, system, self.build_user(request))
