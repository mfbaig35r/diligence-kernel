# The corpus

`review-table-prompts/` holds 24 table inventories: **591 columns, 591 prompts**, plus front
matter (`00a` standards, `00b` rationale) and one specification (`06` coverage register).

## The markdown is the source of truth

It is what git tracks, what a partner redlines, and what `00a` section 11 calls "the history
and the reasons". Everything else is derived:

- The kernel's database is rebuilt by `matter_open`.
- prompt-graph's record is rebuilt by `scripts/sync_prompt_graph.py`.

Re-syncing unchanged markdown reports every column unchanged and writes nothing. That
property is what makes the arrangement safe — edits cannot originate in two places.

## What the parser reads

The corpus is mechanically regular, and the parser never guesses. Anything it cannot resolve
becomes a finding.

| From the inventory | Into |
|---|---|
| `## Table` bullets | review unit, grouping, max docs per unit, vault project |
| `## Table Instructions` fenced block | the table's shared rules |
| `## Column index` table | cross-check against the column records |
| `### N. Name` records | name, native type, options, purpose, upstream, downstream |
| The fenced prompt in each record | the prompt text |
| `## Test set` checkboxes | test cases |

**One subtlety runs through all of it:** prompt sections like `## Task` live *inside* fenced
blocks. Every scan is fence-aware, or the parser would read a prompt's own headings as the
document's structure.

## Type distribution

371 Free Response, 152 Classify, 44 Date, 22 Verbatim, 2 Duration — and **zero Number or
Currency**. That is `00a` section 7's "report, never compute" visible in the schema itself.

Stages: 338 stage-1, 219 stage-2, 32 stage-3, 2 stage-4. No dependency cycles.

## Two things the parser records rather than smooths over

**Type caveats.** 57 columns carry a note after the native type — `Date — confirm the type
accepts \`Not stated\``. `00a` section 8 calls those load-bearing untested unknowns, so they
are kept and surfaced through `table_describe`.

**Unenumerated option lists.** A bullet reading `the same 18 workstream values, plus \`None\``
names a vocabulary it does not spell out. The parser raises `OPTIONS_NOT_ENUMERATED` and the
engine stops asserting the list is complete, because a truncated controlled list presented as
whole makes the model comply with the truncation. This was found the hard way — see
[Ingestion](ingestion.md#what-running-it-for-real-found).

## Routing vocabulary is checked at load

`constants.WORKSTREAM_TABLES` maps Table 05's `Workstream` options to the tables that serve
them. Its keys are **the corpus's own option strings, verbatim**. `load_corpus` compares the
map against the corpus and raises `WORKSTREAM_NOT_ROUTED` or `WORKSTREAM_ROUTE_STALE` if they
diverge — because a workstream with no routing entry means documents classified into it reach
no table and vanish while looking correctly classified.

`WORKSTREAMS_WITHOUT_TABLES` records the values that legitimately route nowhere
(`Privacy and Cybersecurity`, `Benefits and Pensions`, `Compliance` — `00a` section 2's open
scope question — plus `Deal Documents`, `Related-Party` and `Unable to determine`), so an
empty result is a stated fact rather than a silent miss.

## Parameters must be bound before a run

The inventories ship **templates**: `[Project name]`, `[Exact legal name] ([jurisdiction and
entity type]; [role in the group])`, `[YYYY-MM-DD]`. Sent unchanged, they ask the model to
decide whether a document's party is a "review subject" against a list of square brackets.

`matter_parameters_set` records the entities; `binding.py` substitutes them; any run against
unbound instructions raises `UNBOUND_PARAMETERS`.

Only the eight known matter placeholders are bound. Table Instructions also contain
output-format tokens — Table 14 has `[answer]` and `[document title]` in a response template —
which are instructions about the shape of an answer, not values to substitute.

## Corpus linting belongs to prompt-graph

The kernel validates **answers**, not prompts. On the same corpus prompt-graph reports 270
per-prompt findings and 113 suite-level ones, including categories a per-column lint cannot
see: concept drift across tables, and narrative columns acting as a control plane for many
dependents.

The decisive argument: a lint built on the kernel's own parse cannot catch the kernel's own
parsing bug, because it compares a prompt against *the options the parser produced*.
