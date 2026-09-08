"""A deterministic stand-in for the model, so the pipeline can be tested without spending."""

from __future__ import annotations

from diligence_kernel.engine.llm import CellAnswer, CellRequest, Usage

#: Column name -> (value, evidence quotes). Anything unlisted returns `Not addressed`.
SCRIPT: dict[str, tuple[str, list[str]]] = {
    "Governing Law": (
        "New York",
        ["This Agreement shall be governed by and construed in accordance with the"],
    ),
    "Chain Completeness": (
        "Amendment referenced but absent",
        [
            "WHEREAS, the parties previously entered into that certain Side Letter dated June 2, 2023"
        ],
    ),
    "Execution Status": ("All documents executed", ["By: /s/ Dana Ruiz"]),
    "Effective Date": ("2022-03-14", []),
    "Assignment Language": (
        "Neither party may assign this Agreement without the prior written consent\nof the other party",
        [],
    ),
    "Counterparty": ("Northwind Logistics Inc.", []),
}


class StubFiller:
    """Implements the CellFiller surface the runner uses."""

    def __init__(self, script: dict[str, tuple[str, list[str]]] | None = None) -> None:
        self.script = script if script is not None else SCRIPT
        self.calls: list[CellRequest] = []
        self.systems: list[list[dict]] = []
        self.model = "stub"
        self.effort = "n/a"

    def build_system(self, *, table_instructions: str, unit_label: str, evidence_blocks):
        from diligence_kernel.engine.llm import CellFiller

        return CellFiller.build_system(
            self,  # type: ignore[arg-type]
            table_instructions=table_instructions,
            unit_label=unit_label,
            evidence_blocks=evidence_blocks,
        )

    def build_user(self, request: CellRequest) -> str:
        from diligence_kernel.engine.llm import CellFiller

        return CellFiller.build_user(self, request)  # type: ignore[arg-type]

    def fill(self, request: CellRequest, *, system):
        self.calls.append(request)
        self.systems.append(system)
        value, evidence = self.script.get(request.column_name, ("Not addressed", []))
        return CellAnswer(value=value, evidence=evidence), Usage(input_tokens=100, output_tokens=10)
