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

## 2a. Providers sit behind one interface, OpenAI by default

The engine makes exactly one kind of call, so the provider surface is small: a cached
prefix, a varying instruction, a schema. What differs is only how the cache is addressed.
OpenAI caches input prefixes automatically above a minimum length and `prompt_cache_key`
routes identical prefixes to one cache; Anthropic caches only at an explicit
`cache_control` breakpoint. Decision 2 is unchanged by either — stable content first,
volatile last, is what both reward.

Two consequences worth knowing:

- **OpenAI estimates need no credentials.** tiktoken counts locally, so `run_estimate` works
  offline. Anthropic's count is exact but needs a network call, so its estimates degrade to
  a character approximation without a key.
- **Structured outputs made every field of `CellAnswer` required.** OpenAI strict mode
  requires it; an optional field becomes required-and-nullable. That is stricter than what
  Anthropic needed and is the better contract anyway — the model must state a source
  document or explicitly say there is none.

A model absent from the built-in price table reports cost as unknown rather than being
priced from a guess. `DILIGENCE_KERNEL_PRICE_IN` / `_OUT` price it.

## 3. Verbatim columns take a different retrieval path

`00a`: "The entire spot-check design rests on this." A clause split across a chunk boundary
cannot be quoted exactly, so a unit that fits goes into context whole and only an oversized
unit falls back to per-column retrieval. `validate_verbatim` then confirms the returned text
actually appears in the unit's documents, tolerating line wrapping, smart quotes, and dash
variants but not paraphrase.

## 3a. Running headers and footers are removed before anything reads the text

Every legal PDF carries them, and an extractor emits them in reading order — so a clause
spanning a page break comes out with `Confidential Page 1 of 3` wedged into the middle of a
sentence. Observed on the fixture lease, not imagined.

That breaks three things at once: the Verbatim check rejects a correct quotation, retrieval
scores a passage on boilerplate, and the model reads an interrupted sentence. `vault/cleaning.py`
drops lines that repeat at the top or bottom of most pages, comparing them with digits
masked so `Page 1 of 3` matches `Page 2 of 3`. A one-page document is left untouched,
because nothing can be shown to repeat.

The full text is then rebuilt from the cleaned pages, so character offsets and page
attribution are exact by construction rather than by agreement with the extractor.

## 3b. The Verbatim comparison form absorbs extraction artefacts, not paraphrase

Each of these was observed on a real PDF extraction and each rejected a correct quotation
before it was handled: ligatures (`oﬃce`), soft hyphens, hyphenated line breaks
(`non-\nexclusive`), line wrapping, smart quotes, en and em dashes, non-breaking spaces.

Hyphens are dropped entirely, so `non-compete` and `noncompete` compare equal. That is a
deliberate loosening. The check exists to catch paraphrase, and paraphrase differs by words,
not by punctuation — the tests assert that three plausible paraphrases of the fixture lease's
assignment clause are still rejected.

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

- **The live model path is unverified on both providers.** The request shapes match the
  installed SDKs (`responses.parse` with `text_format`; `messages.parse` with
  `output_format`), and the whole pipeline passes against a stub, but no request has been
  made against either API. The first real run is a smoke test, not a batch.
- **Cost per cell is known only for fixture-sized documents.** The estimate on the three
  fixture agreements is ~$0.0023 a cell on `gpt-5`. Real diligence documents are ten to
  fifty times larger, and the prefix is the bulk of a request, so a real matter scales up
  from that number rather than matching it.
- **Scanned documents have no OCR path.** A PDF with no text layer ingests, reports
  `DOCUMENT_EMPTY`, and is skipped by any run rather than answered from an empty page — but
  it is invisible to every table until someone OCRs it. In a real data room that is routinely
  a tenth of the files.
- **Table 05's document-type vocabulary is ~180 values.** `00a` section 8 flags this as
  deciding whether the column is Classify or Free Response. The corpus currently calls it
  Free Response, so the engine does not constrain it.
- **57 columns carry a pre-run verification caveat** on their native type, recorded by the
  parser and surfaced through `table_describe`. Those are `00a` section 8's untested
  fallbacks, and they are untested here too.
