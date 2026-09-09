"""Binding a matter's real parameters into the corpus's Table Instructions.

The inventories ship **templates**. Their Table Instructions read:

    ## Matter
    [Project name]. Buyer-side legal diligence on the target group listed below.
    Diligence as-of date: `[YYYY-MM-DD]`.

    ## Review subjects
    - [Exact legal name] ([jurisdiction and entity type]; [role in the group])

Sending that to a model unchanged asks it to decide whether a document's party is a "review
subject" against a list of square brackets. It cannot, and it is right not to: an
`Unable to determine` returned against unbound instructions is a correct answer to the wrong
question, and it looks exactly like a model failing.

So parameters are bound before a run, and anything left unbound is reported loudly.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass

#: The matter parameters the corpus's templates carry. Only these are bound.
#:
#: Table Instructions also contain output-format tokens — Table 14 has `[answer]` and
#: `[document title]` inside a response template. Those are instructions to the model about
#: the shape of its answer, not values to substitute; binding them would corrupt the prompt,
#: and reporting them as unbound would cry wolf on every run.
MATTER_PLACEHOLDERS: tuple[str, ...] = (
    "[Project name]",
    "[YYYY-MM-DD]",
    "[Exact legal name]",
    "[jurisdiction and entity type]",
    "[role in the group]",
    "[Buyer legal name]",
    "[Seller or parent legal name]",
    "[Adviser names]",
)

#: A template line listing one review subject, which expands to one line per entity.
ENTITY_LINE = re.compile(r"^- \[Exact legal name\][^\n]*$", re.MULTILINE)


@dataclass(slots=True)
class Entity:
    name: str
    jurisdiction: str | None = None
    role: str | None = None
    is_subject: bool = True

    def rendered(self) -> str:
        detail = "; ".join(p for p in (self.jurisdiction, self.role) if p)
        return f"- {self.name}" + (f" ({detail})" if detail else "")


def entities_of(conn: sqlite3.Connection) -> list[Entity]:
    return [
        Entity(r["name"], r["jurisdiction"], r["role"], bool(r["is_subject"]))
        for r in conn.execute(
            "SELECT name, jurisdiction, role, is_subject FROM entity ORDER BY is_subject DESC, id"
        )
    ]


def bind(text: str, *, matter: sqlite3.Row | None, entities: list[Entity]) -> str:
    """Substitute a matter's parameters into Table Instructions."""
    if not text:
        return text
    subjects = [e for e in entities if e.is_subject]
    by_role = {(e.role or "").strip().lower(): e for e in entities if not e.is_subject}

    # The subject list first: one template line becomes one line per entity.
    if subjects and ENTITY_LINE.search(text):
        block = "\n".join(e.rendered() for e in subjects)
        text = ENTITY_LINE.sub(lambda _m: "\x00BLOCK\x00", text, count=1)
        text = ENTITY_LINE.sub("", text)
        text = text.replace("\x00BLOCK\x00", block)

    replacements = {
        "[Project name]": (matter["name"] if matter else None),
        "[YYYY-MM-DD]": (matter["as_of_date"] if matter else None),
        "[Buyer legal name]": _named(by_role, "buyer"),
        "[Seller or parent legal name]": _named(by_role, "seller", "parent"),
        "[Adviser names]": _joined(by_role, "adviser", "advisor"),
    }
    for token, value in replacements.items():
        if value:
            text = text.replace(token, str(value))
    return re.sub(r"\n{3,}", "\n\n", text)


def _named(by_role: dict[str, Entity], *roles: str) -> str | None:
    for role in roles:
        for key, entity in by_role.items():
            if role in key:
                return entity.name
    return None


def _joined(by_role: dict[str, Entity], *roles: str) -> str | None:
    names = [e.name for key, e in by_role.items() if any(role in key for role in roles)]
    return ", ".join(names) or None


def unbound(text: str) -> list[str]:
    """Matter parameters still present, in the order the corpus declares them."""
    body = text or ""
    return [p for p in MATTER_PLACEHOLDERS if p in body]
