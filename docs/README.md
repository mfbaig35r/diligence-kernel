# diligence-kernel — project wiki

A matter-scoped M&A diligence vault and review-table execution engine, over MCP.

| Page | What it covers |
|---|---|
| [Architecture](architecture.md) | The four layers, and the split with `prompt-graph` |
| [The corpus](corpus.md) | 24 tables, 591 prompts, how they are parsed and kept honest |
| [Ingestion](ingestion.md) | PDFs, spreadsheets, email, OCR — and what each nearly broke |
| [Running a table](running-a-table.md) | Units, stages, concurrency, caching, cost |
| [Standards](standards.md) | What `00a` requires, and where each rule is enforced |
| [Findings reference](findings.md) | Every code the server can return, and what to do about it |
| [Operations](operations.md) | Configuration, scripts, the smoke test |
| [Playbook crosswalk](../playbook/README.md) | The firm's M&A playbook mapped against the corpus, both directions |
| [Decisions](../DECISIONS.md) | Why the system is shaped this way |

## What it is

```
files → extract → classify (Table 05) → assemble review units
      → chunk + embed → vault
      → run a table: retrieve in-scope evidence, fill each cell in dependency order
      → persist cells + evidence + provenance
      → derived artifacts: consent schedule, coverage register, issues list
```

The prompt corpus is the **schema**, not the product. The markdown in `review-table-prompts/`
is the source of truth; the database is derived and rebuildable from it.

## What it is not

It does not draft prompts — the `legal-review-table-builder` skill does that. It does not make
legal determinations. It does no arithmetic: `00a` section 7 is enforced, not requested, so
every figure is reported as stated and reconciliation happens outside.

Which document is operative, whether a consent is required, materiality, and deal
consequence all stay human. `00a` section 10 lists them; the human-review columns are where
their answers live.

## The one sentence worth remembering

**A cell the engine filled is a candidate, not a finding.** It does not go in a memo and is not
told to a client until its review status says otherwise.

## Status

19 MCP tools, 189 tests, CI green. The live model path has been exercised end to end on a
ten-document fixture data room; nothing has yet run against a real matter.
