"""The one output shape every tool shares.

Borrowed from prompt-graph deliberately: a finding is a factual observation with a stable
code. It carries no advice, no severity adjective, and no suggested rewrite. Claude
supplies the interpretation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

SubjectType = (
    str  # matter | corpus | table | column | prompt | document | unit | cell | run | artifact
)


@dataclass(slots=True)
class Finding:
    code: str
    subject_type: SubjectType
    subject_id: int | str | None
    subject_name: str
    observation: str  # one factual sentence
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def dump(findings: list[Finding]) -> list[dict[str, Any]]:
    return [f.to_dict() for f in findings]


class KernelError(Exception):
    """Input the server cannot act on. The message is written for the model."""
