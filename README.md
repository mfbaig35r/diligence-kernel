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

PDF, DOCX, XLSX, CSV, HTML and email (`.eml`, `.msg`) are read by default — a data room is
not a folder of text files. Anything produced but unreadable (`.xls`, `.doc`, `.pptx`,
archives) is **reported**, not skipped in silence: an unread file must not look like an
absent one. Three things happen on the way in that matter more than they sound:

- **Running headers and footers are stripped.** An extractor emits them in reading order, so
  a clause spanning a page break arrives with `Confidential Page 1 of 3` inside the sentence.
  Lines repeating at the top or bottom of most pages are removed, with page numbers masked so
  `Page 1 of 3` and `Page 2 of 3` count as the same line.
- **Offsets survive.** The full text is rebuilt from the cleaned pages, so every chunk's
  character span and page range is exact, and evidence can point at it.
- **Scans are read by OCR.** A PDF page with no text layer is transcribed locally with
  tesseract, so nothing leaves the machine. Set `DILIGENCE_KERNEL_OCR` to `tesseract`
  (default), `vision`, or `off`. Without OCR available, the file still ingests and reports
  itself rather than disappearing.

### Spreadsheets are read as tables, not prose

`00a` classifies cap tables, stock ledgers, employee censuses and loss runs as **Records** —
they report facts as at a date, and the as-of date is what makes one usable. Flattening a
sheet into prose loses two things a reader cannot recover:

- **Column headers.** A chunk holding rows 27 to 52 of a census, with the header left behind
  in an earlier chunk, is a grid of unlabelled numbers — nothing can tell salary from bonus.
- **Sheet boundaries.** A cap table followed by a census reads as one table that changes
  shape halfway through.

So a table is chunked by rows, and every chunk restates its sheet name and header:

```
# Sheet: Employee Census (continued)
Employee ID  Name         Title        Location        Hire Date   Base Salary  ...
E1032        Employee 32  Engineer II  Austin, TX      2022-06-15  125200       ...
```

The repetition is written into the stored text too, the way a printed schedule repeats its
headings on each page, which keeps every chunk an exact slice and offsets true.

### Email is correspondence, and it carries documents

Tables 17, 23 and 25 are built around correspondence, and their review unit is a *matter* of
several communications — so one message is one document, and unit assembly groups them.

- **Headers are normalized** into the text, because From, Cc, Date and Subject are what
  Table 05 routes on.
- **The quoted chain is separated and labelled.** A reply carrying twelve earlier messages
  otherwise duplicates their text into every later file, which distorts retrieval and makes
  "the most recently dated document" meaningless. The history is kept — it is evidence — but
  marked as repeated.
- **Attachments are extracted and ingested in their own right**, linked back to the message
  that carried them, because in a data room the attachment is usually the agreement.
  Signature images, calendar items and `smime.p7s` are recognised as mail furniture.
- **Privilege markings are reported.** `00a`: report the marking and stop, never assess
  whether privilege applies — "a privileged document reaching the wrong reviewer is a
  handling problem." Detection runs on every document, not only email.

The Verbatim check tolerates what extraction does to text — ligatures, soft hyphens,
hyphenated line breaks, wrapping, smart quotes, dashes, non-breaking spaces — while still
rejecting paraphrase.

### OCR text is a transcription, not the document

A document read by OCR records that fact, its engine and its confidence, and the whole
system stays honest about it:

- the model is told which documents are transcriptions, and not to correct a garbled word
- `cell_evidence` reports the source of every quotation it shows a reviewer
- a **Verbatim** cell drawn from a transcribed unit is flagged `VERBATIM_FROM_OCR`, because
  matching a quotation against OCR output compares one reading with another and cannot show
  the words are the document's

`tesseract` is the default rather than `vision` for a specific reason: tesseract garbles,
which is visible, while a vision model transcribes fluently, so its misreadings look like
ordinary text. On a control that a partner will rely on, a legible failure beats a
plausible one.

```bash
brew install tesseract poppler          # macOS
uv pip install -e ".[ocr]"
```

## Providers

OpenAI by default; Anthropic behind the same interface. Both make the identical call — a
cached prefix, a short varying instruction, and a schema the answer must satisfy — so
switching is one environment variable.

```bash
export DILIGENCE_KERNEL_PROVIDER=openai        # or anthropic
export DILIGENCE_KERNEL_MODEL=gpt-5            # default: gpt-5
export DILIGENCE_KERNEL_EFFORT=medium          # low | medium | high | xhigh | max
export DILIGENCE_KERNEL_CONCURRENCY=6          # model calls in flight, within a stage
```

Columns of the same stage are filled concurrently and the run waits at each stage boundary,
so a downstream prompt always sees its upstream answers. 338 of the 591 columns are stage 1.
The first call of each unit runs alone to populate the prompt cache; firing a whole stage at
once would make every request miss it.

The default is `gpt-5.4`. Cost is modelled from the published rates: cached input at a tenth
of fresh, cache writes at each model's own rate (free on `gpt-5.4` and `gpt-5.5`, a premium on
the `gpt-5.6` family), and the long-context tier at roughly double above ~128k tokens.

Output dominates this workload — a cell spends ~1,145 output tokens against ~693 fresh input
— so the output rate is what you are really choosing between. The spread is wide:
`gpt-5.6-luna` runs the same work for about a twelfth of `gpt-5.4`.

Anything absent from the built-in price table reports its cost as unknown rather than
guessing; price it yourself with:

```bash
export DILIGENCE_KERNEL_PRICE_IN=1.25          # USD per million input tokens
export DILIGENCE_KERNEL_PRICE_OUT=10.00        # USD per million output tokens
```

On OpenAI, `run_estimate` needs no credentials and no network — tiktoken counts locally.

## Credentials

The server is launched by its MCP client, not from a shell, so it inherits nothing from your
terminal. Put the key in a `.env` at the project root rather than in the MCP config:

```bash
cp .env.example .env      # then edit it
```

`.env` is gitignored, and an environment variable already set always wins over it.

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
