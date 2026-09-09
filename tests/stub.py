"""A deterministic stand-in for the model, so the pipeline can be tested without spending."""

from __future__ import annotations

from diligence_kernel.engine.llm import CellAnswer, CellFiller, CellRequest
from diligence_kernel.engine.providers import PromptPrefix, Usage

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


class StubProvider:
    """Implements the Provider surface the filler and estimator use."""

    name = "stub"
    default_model = "stub-1"
    default_effort = "medium"
    cache_read_multiplier = 0.1
    cache_write_multiplier = 1.0
    min_cacheable_tokens = 0

    def pricing(self, model: str) -> tuple[float, float] | None:
        return (1.0, 4.0)


class StubFiller(CellFiller):
    """A CellFiller that answers from a script instead of calling a provider."""

    def __init__(self, script: dict[str, tuple[str, list[str]]] | None = None) -> None:
        self.provider = StubProvider()  # type: ignore[assignment]
        self.model = "stub-1"
        self.effort = "medium"
        self.max_tokens = 4096
        self.script = script if script is not None else SCRIPT
        self.calls: list[CellRequest] = []
        self.systems: list[PromptPrefix] = []

    def fill(self, request: CellRequest, *, system: PromptPrefix) -> tuple[CellAnswer, Usage]:
        self.calls.append(request)
        self.systems.append(system)
        value, evidence = self.script.get(request.column_name, ("Not addressed", []))
        answer = CellAnswer(value=value, evidence=evidence, source_document=None)
        return answer, Usage(input_tokens=100, output_tokens=10)

    def count(self, request: CellRequest, *, system: PromptPrefix) -> tuple[int, bool]:
        return (len(system.text) + len(self.build_user(request))) // 4, False
