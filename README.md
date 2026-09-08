# diligence-kernel

A matter-scoped M&A diligence vault and review-table execution engine, over MCP.

It ingests a data room, classifies and tags every file, assembles review units, and then
runs the review-table prompt corpus against them — filling cells with evidence attached,
so the analysis persists for higher-level M&A work and drafting.

## What it is

```
files → extract → classify (Table 05) → assemble review units
      → chunk + embed → vault
      → run a table: retrieve in-scope evidence, fill each cell in dependency order
      → persist cells + evidence + provenance
      → derived artifacts: consent schedule, coverage register, issues list
```

The prompt corpus in `review-table-prompts/` is the schema: 24 table inventories,
591 columns, 591 prompts. The markdown is the source of truth. The database is derived and
rebuildable from it.

## What it is not

It does not draft prompts — the `legal-review-table-builder` skill does that. It does not
make legal determinations. It does no arithmetic: `00a` section 7 is enforced, not
requested, so every figure is reported as stated and reconciliation happens outside.

`prompt-graph` remains the authoring and evaluation companion. This engine holds its own
parsed copy of the corpus because it needs prompt text, dependency order, and retrieved
evidence in-process; MCP servers cannot call each other.

## Standards it enforces

From `00a-build-plan-and-standards.md`, checked on every cell before it persists:

- the five-state fallback vocabulary, and the banned synonyms (`N/A`, `None`, `Silent`, …)
- `Not stated` restricted to Date, Number, Currency and Duration columns
- Classify answers restricted to configured options
- ISO dates with partial precision preserved
- no markdown, no citations, and no computed figures in a cell
- Verbatim cells must reproduce text that actually appears in the review unit

## Install

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev,all]"
```

## Configure

One matter is one database file.

```bash
claude mcp add diligence-kernel \
  -e DILIGENCE_KERNEL_DB=/absolute/path/to/matters/acme.db \
  -e DILIGENCE_KERNEL_CORPUS=/absolute/path/to/review-table-prompts \
  -e ANTHROPIC_API_KEY=... \
  -- /absolute/path/to/diligence-kernel/.venv/bin/diligence-kernel
```

The database holds client-confidential material: document text, extracted cells, entity
names. Treat the file like a matter file, and keep the `-wal` and `-shm` sidecars with it.
