"""Where the firm's playbook lives.

The playbook carries the practice's own methodology — prompt text and the field lists behind
it — which is a different class of material from the engine that runs it, so it is held in its
own repository and referenced by path.

Set `DILIGENCE_KERNEL_PLAYBOOK` to that checkout. Everything here degrades to None rather than
raising, so the kernel runs perfectly well without it: the crosswalk is analysis, not runtime.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_VAR = "DILIGENCE_KERNEL_PLAYBOOK"
#: Checked when the variable is unset, so a sibling checkout is found without configuration.
SIBLING = Path(__file__).resolve().parents[2].parent / "diligence-playbook"
FIELDS_FILE = "corporate-ma-3.4.json"


def playbook_dir() -> Path | None:
    """The playbook checkout, or None when it is not present."""
    raw = os.environ.get(ENV_VAR)
    if raw:
        candidate = Path(raw).expanduser()
        return candidate if candidate.is_dir() else None
    return SIBLING if SIBLING.is_dir() else None


def fields_path() -> Path | None:
    """The extracted field inventory, or None."""
    directory = playbook_dir()
    if directory is None:
        return None
    path = directory / FIELDS_FILE
    return path if path.is_file() else None


def require_fields() -> Path:
    """The field inventory, or an error saying how to point at it."""
    path = fields_path()
    if path is None:
        raise FileNotFoundError(
            f"No playbook found. Set {ENV_VAR} to a diligence-playbook checkout, "
            f"or place one beside this repository at {SIBLING}."
        )
    return path
