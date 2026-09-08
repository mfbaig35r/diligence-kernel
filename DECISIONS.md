# Decisions

Why the kernel is shaped this way. Each entry names the constraint that forced it.

## 1. The kernel holds its own parsed copy of the corpus

`prompt-graph` is the authoring and evaluation companion and stays independent. It cannot
be a runtime dependency, because **MCP servers cannot call each other** — Claude mediates
every call. An engine that fills a thousand cells needs prompt text, dependency order, and
retrieved evidence in-process.

The markdown stays the source of truth. The database is derived and rebuilt by
`matter_open`, so the prompts' git history remains the real record and the database never
becomes a second, divergent copy.

## 2. Execution order is unit-major, not column-major

A review unit's documents are the bulk of the tokens and are identical for every column of
that unit, so they go in the cached prefix and the engine iterates unit-major. A 27-column
table pays for its documents once per unit instead of 27 times.

Within a unit, columns run in topological stage order. A stage-2 prompt consumes stage-1
answers as established results; filling out of order would feed a prompt an empty upstream.
Stage is computed from the union of each column's declared `Upstream` and the `@Column`
references detected in its prompt text.

## 3. Verbatim columns take a different retrieval path

`00a`: "The entire spot-check design rests on this." A clause split across a chunk boundary
cannot be quoted exactly, so a unit that fits goes into context whole and only an oversized
unit falls back to per-column retrieval. `validate_verbatim` then confirms the returned text
actually appears in the unit's documents, tolerating line wrapping, smart quotes, and dash
variants but not paraphrase.

## 4. The standards are enforced, not requested

A prompt instruction is a request. `engine/validate.py` turns `00a` into checks that run
before a cell persists: fallback vocabulary, banned synonyms, `Not stated` restricted to
typed columns, Classify answers restricted to configured options, ISO dates with partial
precision, no markdown, no citations, no computed figures. Violations are recorded on the
cell and returned as findings rather than silently accepted, because a wrong cell that looks
right is the failure this system exists to avoid.

## 5. Amendments are matched to their base, not keyed alongside it

The first grouping attempt keyed every document on subject plus counterparty plus type. It
could never work: a base agreement describes itself, while its amendment names the base in
prose (`"Master Services Agreement dated March 14, 2022"`). Those strings never match.

Bases now anchor families and dependents are matched to them — parties gate the candidate
set, reference text scores it. A dependent with no matching base gets its own unit and a
`DEPENDENT_WITHOUT_BASE` finding; a near-tie gets `BASE_MATCH_AMBIGUOUS`. `00a` warns that
a family missing an amendment produces a confidently wrong row and nothing else detects it,
so neither case is resolved silently.

## 6. Derived artifacts filter, never re-ask

`00a` section 2: "Never re-derive a consent schedule by asking Harvey a fresh question.
Filter and carry, so the schedule and its sources cannot disagree." No artifact calls a
model. Each reports how many of its rows are still unreviewed or carry a violation, because
a schedule built from unreviewed candidates is a list of candidates.

## 7. What the engine never does

Which document is operative, whether a consent is required, materiality, deal consequence,
and all arithmetic stay human. `00a` section 10 lists them; the human-review columns are
where their answers live, and a run never overwrites a verified, corrected, or locked cell.

## Open

- **The live model path is unverified.** `messages.parse` is called with `output_format`,
  `output_config`, and a cached system prefix; the shapes match the installed SDK, but no
  request has been made against the API. The first real run is a smoke test, not a batch.
- **Table 05's document-type vocabulary is ~180 values.** `00a` section 8 flags this as
  deciding whether the column is Classify or Free Response. The corpus currently calls it
  Free Response, so the engine does not constrain it.
- **57 columns carry a pre-run verification caveat** on their native type, recorded by the
  parser and surfaced through `table_describe`. Those are `00a` section 8's untested
  fallbacks, and they are untested here too.
