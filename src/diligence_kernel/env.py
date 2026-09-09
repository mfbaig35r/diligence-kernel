"""Loading credentials from a `.env` file.

An MCP server is launched by its client, not from a shell, so it inherits none of the
terminal's environment. Rather than write API keys into an MCP config, the kernel reads a
`.env` beside the project or the matter database.

Existing environment variables always win: a value already set is never overwritten.
"""

from __future__ import annotations

import os
from pathlib import Path

FILENAME = ".env"


def parse(text: str) -> dict[str, str]:
    """Parse `KEY=value` lines. Supports `export`, quotes, and `#` comments."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key:
            out[key] = value
    return out


def candidates() -> list[Path]:
    """Where a `.env` may live, nearest first."""
    from .db import db_path

    here = Path(__file__).resolve()
    return [
        Path.cwd() / FILENAME,
        here.parents[2] / FILENAME,  # the project root
        db_path().parent / FILENAME,  # beside the matter database
    ]


def load(path: Path | None = None) -> list[str]:
    """Set any variable not already in the environment. Returns the names it set."""
    paths = [path] if path is not None else candidates()
    applied: list[str] = []
    seen: set[Path] = set()
    for candidate in paths:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.is_file():
            continue
        seen.add(resolved)
        try:
            values = parse(resolved.read_text(encoding="utf-8"))
        except OSError:
            continue
        for key, value in values.items():
            if key not in os.environ:
                os.environ[key] = value
                applied.append(key)
    return applied
