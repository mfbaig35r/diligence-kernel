# Running a table

## The order of operations

```
matter_open("Project Cedar", as_of_date="2026-09-08")   # loads 24 tables, 591 columns
matter_parameters_set([...entities...])                  # bind the templates — do not skip
vault_ingest("/path/to/dataroom")                        # extract, chunk, offsets, OCR
units_assemble("05") ; run_table("05")                   # intake classifies and routes
units_assemble("01") ; run_table("01")                   # a workstream table
table_read("01", only_flagged=True)                      # what breached the standards
cell_evidence(unit_id, "Assignment Language")            # the sentences behind a cell
cell_review(unit_id, "...", review_status="Verified", materiality="Critical")
artifact_build("consent_schedule")                       # a filter, not a fresh question
```

Build order is `00a` section 12: start at 05, then 06, then 01, and stop when the matter is
covered. `table_describe` reports the pairs that must be built together.

## Review units

What one row is. `00a` is emphatic that grouping surfaces differences among documents but does
**not** establish which one controls — that stays a human column.

- **Per-file tables** (Table 05) make one unit per produced file, keyed on where the file was
  produced rather than its content. The same agreement in a folder and attached to an email is
  two produced files and two rows; Table 05 carries a `Duplicate Indicators` column to say so.
- **Grouped tables** anchor a family on its base instrument. Dependents name their base in
  prose, so they are *matched* to it — parties gate the candidate set, reference text scores
  it. `DEPENDENT_WITHOUT_BASE` and `BASE_MATCH_AMBIGUOUS` report what could not be resolved,
  because `00a` warns a family missing an amendment produces a confidently wrong row that
  nothing else detects.

## Estimating before spending

`run_estimate` builds the exact requests a run would send and prices them, without sending
any. It excludes cells a run would skip — already filled, locked, or reviewed.

On OpenAI this needs no credentials and no network: tiktoken counts locally.

```
plan: 200 cells over 10 rows on openai/gpt-5.6-luna (effort medium, concurrency 6)
estimate: 309,850 in, 220,000 out, $0.42
```

## What a run costs

Output dominates. A cell spends far more on reasoning than the visible answer suggests, and the
spend tracks how *ambiguous* a document is rather than how long it is — a 1,066-character email
reasoned 34% harder than a 3,608-character workbook.

`OUTPUT_TOKENS_PER_CELL` is a measured constant, not a guess. Re-measure it when the default
model or effort changes.

Cost per document for intake alone (Table 05 runs over every file, 20 columns each):

| Model | Per document | 500 documents |
|---|---|---|
| `gpt-5.6-luna` | $0.031 | $24 |
| `gpt-5.4` | $0.384 | $298 |
| `gpt-6-astra` | $1.308 | $1,021 |

Only Table 05 scales linearly with document count. Every other table runs over *units*, which
are always fewer than documents because grouping collapses a family into one row.

## Durability

A run is a row in `run` and a set of cells. Every cell commits as it is filled, so calling
again after a failure resumes rather than restarts. Already-filled cells are skipped unless
`refill` is set, and a locked or human-corrected cell is **never** overwritten — locking
preserves work, it does not refresh it.

## Model choice

Measured on Table 05 over the fixture data room, scored against 89 ground-truth expectations:

| | score | cost |
|---|---|---|
| `gpt-5.6-luna` | 86/89 (97%) | $0.21 |
| `gpt-5.4` | 82/89 (92%) | $3.06 |

luna is the default on that evidence. It is **untested on the extraction tables**, where
Verbatim and judgment matter more than classification into a fixed option list — which is
where a cheaper model is most likely to break. Raise the model per table rather than globally.
