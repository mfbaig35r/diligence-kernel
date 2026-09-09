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

## Real documents

PDF, DOCX, XLSX and HTML extraction is installed by default — a data room is not a folder of
text files. Three things happen on the way in that matter more than they sound:

- **Running headers and footers are stripped.** An extractor emits them in reading order, so
  a clause spanning a page break arrives with `Confidential Page 1 of 3` inside the sentence.
  Lines repeating at the top or bottom of most pages are removed, with page numbers masked so
  `Page 1 of 3` and `Page 2 of 3` count as the same line.
- **Offsets survive.** The full text is rebuilt from the cleaned pages, so every chunk's
  character span and page range is exact, and evidence can point at it.
- **Scans report themselves.** A PDF with no text layer ingests, raises `DOCUMENT_EMPTY`, and
  is skipped by any run — never answered from an empty page. There is no OCR path yet.

The Verbatim check tolerates what extraction does to text — ligatures, soft hyphens,
hyphenated line breaks, wrapping, smart quotes, dashes, non-breaking spaces — while still
rejecting paraphrase.

## Providers

OpenAI by default; Anthropic behind the same interface. Both make the identical call — a
cached prefix, a short varying instruction, and a schema the answer must satisfy — so
switching is one environment variable.

```bash
export DILIGENCE_KERNEL_PROVIDER=openai        # or anthropic
export DILIGENCE_KERNEL_MODEL=gpt-5            # default: gpt-5
export DILIGENCE_KERNEL_EFFORT=medium          # low | medium | high | xhigh | max
```

The default is `gpt-5` because its price and behaviour can be stated. Newer models the SDK
knows about — `gpt-5.4`, `gpt-5.5`, `gpt-6-astra` and the rest — work by setting
`DILIGENCE_KERNEL_MODEL`. Anything absent from the built-in price table reports its cost as
unknown rather than guessing; price it yourself with:

```bash
export DILIGENCE_KERNEL_PRICE_IN=1.25          # USD per million input tokens
export DILIGENCE_KERNEL_PRICE_OUT=10.00        # USD per million output tokens
```

On OpenAI, `run_estimate` needs no credentials and no network — tiktoken counts locally.

## Install

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev,all]"      # OpenAI
uv pip install --python .venv/bin/python -e ".[dev,anthropic]" # adds Anthropic
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
  -e OPENAI_API_KEY=... \
  -- /absolute/path/to/diligence-kernel/.venv/bin/diligence-kernel
```

The database holds client-confidential material: document text, extracted cells, entity
names. Treat the file like a matter file, and keep the `-wal` and `-shm` sidecars with it.
