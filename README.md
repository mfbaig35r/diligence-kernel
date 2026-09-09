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

## Tools

**Matter** — `matter_open`, `matter_status`
**Vault** — `vault_ingest`, `vault_search`, `classification_record`
**Rows** — `units_propose`, `units_assemble`
**Execution** — `run_estimate`, `run_table`, `run_status`
**Review** — `table_read`, `cell_evidence`, `cell_review`
**Corpus** — `table_describe`, `column_prompt`, `columns_find`
**Artifacts** — `artifact_list`, `artifact_build`

## A matter, end to end

```
matter_open("Project Cedar", as_of_date="2026-09-01")   # loads 24 tables, 591 columns
vault_ingest("/path/to/dataroom")                        # extract, chunk, offsets, embed
units_assemble("05") ; run_table("05")                   # intake classifies and routes
units_assemble("01") ; run_table("01")                   # a workstream table
table_read("01", only_flagged=True)                      # what breached the standards
cell_evidence(unit_id, "Assignment Language")            # the sentences behind a cell
cell_review(unit_id, "...", review_status="Verified", materiality="Critical")
artifact_build("consent_schedule")                       # a filter, not a fresh question
```

Build order is `00a` section 12: start at 05, then 06, then 01, and stop when the matter is
covered. `table_describe` reports the pairs that must be built together.

## Install

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev,all]"
```

## Smoke test

Verify the live model path on the smallest possible run. Safe by default — with no flags it
checks credentials and estimates cost using the free token-counting endpoint, and spends
nothing.

```bash
.venv/bin/python scripts/smoke_test.py          # free: credentials + cost estimate
.venv/bin/python scripts/smoke_test.py --run    # spends: fills 4 cells on one row
```

It works on a throwaway database in a temp directory, never a real matter, and refuses to
fill more than 12 cells. `--run` prints each cell's value, the sentences it was drawn from
with their offsets, and any standards violation.

For a real run, `run_estimate` reports what `run_table` would cost before you start it,
with and without the cached unit prefix.

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
