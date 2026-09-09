# Architecture

## Four layers

| Layer | Module | Job |
|---|---|---|
| **Corpus** | `corpus/parser.py`, `corpus/loader.py` | Parse 24 markdown inventories into 591 columns; compute topological stages |
| **Vault** | `vault/` | Extract, clean, chunk, OCR, group into review units, retrieve evidence |
| **Engine** | `engine/` | Fill cells in dependency order, validate against `00a`, persist with evidence |
| **Derive** | `derive/artifacts.py` | Project filled cells into schedules — filters, never fresh questions |

`server.py` is transport; `service.py` is behaviour. `findings.py` holds the one output shape
every tool shares.

## The split with prompt-graph

Two servers, one corpus, a clean seam:

- **diligence-kernel** meets documents and produces evidence. It parses files, runs prompts,
  and validates answers.
- **prompt-graph** holds prompt versions, the cross-table dependency graph, the evaluation
  log, and the change-log discipline `00a` section 11 requires. It never parses files.

**MCP servers cannot call each other** — the client mediates every call. That is why the
kernel holds its own parsed copy of the corpus: an engine filling a thousand cells needs
prompt text, dependency order and retrieved evidence in-process.

It is *not* why the two cannot be connected. `scripts/sync_prompt_graph.py` calls
`prompt_graph.service.table_ingest` directly — the same function the MCP tool of that name
wraps, so the identical lint, `@ref` resolution and versioning run. Calling another project's
library is fine; only server-to-server MCP calls are impossible.

## Data flow

```
review-table-prompts/*.md
        │  parse (deterministic, fence-aware)
        ▼
   review_table ─── column_def ─── column_dep      (derived; rebuildable)
                         │
data room ──ingest──► document ─── chunk (+FTS5, embeddings)
                         │
                 classification  (Table 05 output — the routing record)
                         │
                    review_unit ─── unit_document
                         │
                    run ──► cell ─── cell_evidence
                                       │
                                  derived artifacts
```

## Two ordering rules the engine cannot break

**Within a unit, columns run in topological stage order.** A stage-2 prompt consumes stage-1
answers as established results; filling out of order feeds a prompt an empty upstream.
338 of 591 columns are stage 1.

**Across units, iteration is unit-major.** A unit's documents are the bulk of the tokens and
are identical for every column of that unit, so they go in the cached prefix and are paid for
once per unit rather than once per column.

## Concurrency

Parallel **inside a stage, never across one** — a stage is by definition a set of columns with
no dependency on each other. The run waits at each boundary.

Two details that matter:

- **The first call of a unit runs alone**, to populate the prompt cache. Firing a whole stage
  at once means every request misses it, because nothing has written the prefix yet.
- **Only model calls leave the calling thread.** Every database read happens in `_prepare`
  beforehand and every write after the stage completes, so SQLite sees one writer and cell
  ordering stays deterministic. Tests assert concurrency 1 and 8 produce identical cells.

Measured on Table 05: 1.3–6.3 cells/min sequential and degrading, ~12/min at concurrency 6
and steady.

## Storage

One matter is one SQLite file. It holds client-confidential material — document text,
extracted cells, entity names — so treat it like a matter file and keep the `-wal` and `-shm`
sidecars with it. Extracted email attachments live in an `attachments/` directory beside it.
