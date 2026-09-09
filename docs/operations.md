# Operations

## Install

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev]"        # PDF, DOCX, XLSX, HTML, email
uv pip install --python .venv/bin/python -e ".[dev,all]"    # adds OCR, local embeddings, Anthropic
brew install tesseract poppler                              # OCR, macOS
```

## Credentials

The server is launched by its MCP client, not from a shell, so it inherits nothing from your
terminal. Put the key in `.env` at the project root rather than in the MCP config:

```bash
cp .env.example .env    # then edit
```

`.env` is gitignored, and an environment variable already set always wins over it.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DILIGENCE_KERNEL_DB` | `~/.diligence-kernel/matter.db` | One matter, one file |
| `DILIGENCE_KERNEL_CORPUS` | `review-table-prompts/` | The prompt corpus |
| `DILIGENCE_KERNEL_PROVIDER` | `openai` | `openai` or `anthropic` |
| `DILIGENCE_KERNEL_MODEL` | `gpt-5.6-luna` | Any model the provider offers |
| `DILIGENCE_KERNEL_EFFORT` | `medium` | `low` … `max` |
| `DILIGENCE_KERNEL_CONCURRENCY` | `6` | Model calls in flight, within a stage |
| `DILIGENCE_KERNEL_OCR` | `auto` | `auto`, `tesseract`, `vision`, `off` |
| `DILIGENCE_KERNEL_OCR_DPI` | `300` | Render resolution for OCR |
| `DILIGENCE_KERNEL_PRICE_IN` / `_OUT` | — | Price a model the table does not carry |
| `DILIGENCE_KERNEL_PLAYBOOK` | sibling `diligence-playbook/` | The firm playbook checkout, for the crosswalk only |
| `DILIGENCE_KERNEL_EMBED_CACHE` | `~/.diligence-kernel/embeddings.json` | Crosswalk embedding cache |

## Register with Claude Code

```bash
claude mcp add diligence-kernel \
  -e DILIGENCE_KERNEL_DB=/absolute/path/to/matters/acme.db \
  -e DILIGENCE_KERNEL_CORPUS=/absolute/path/to/review-table-prompts \
  -- /absolute/path/to/diligence-kernel/.venv/bin/diligence-kernel
```

## Scripts

| Script | Purpose |
|---|---|
| `scripts/smoke_test.py` | Verify the live model path on four cells. Safe by default; `--run` spends |
| `scripts/run_table.py` | Run a table with progress and a cost gate. Estimates unless `--run` |
| `scripts/inspect_table.py` | Read a filled table back: values, fallbacks, violations, routing |
| `scripts/score_intake.py` | Score a Table 05 run against the fixture ground truth |
| `scripts/compare_runs.py` | Compare two runs cell by cell, judged against ground truth |
| `scripts/sync_prompt_graph.py` | Replay the corpus into prompt-graph. `--dry-run` writes nothing |
| `scripts/extract_playbook.py` | Extract the playbook's prompts and fields from its PDF |
| `scripts/crosswalk.py` | Crosswalk playbook against corpus. `--calibrate` checks the scorer |
| `tests/fixtures/build_fixtures.py` | Regenerate the binary fixtures (needs `[fixtures]`) |

## The smoke test

```bash
.venv/bin/python scripts/smoke_test.py          # free: credentials + cost estimate
.venv/bin/python scripts/smoke_test.py --run    # spends ~$0.01: fills 4 cells on one row
```

Works on a throwaway database in a temp directory, never a real matter, and refuses to fill
more than 12 cells. `--run` prints each cell's value, the sentences it was drawn from with
their offsets, and any standards violation.

## Running a table for real

```bash
python scripts/run_table.py 05 --db matters/acme.db --room /path/to/dataroom          # estimate
python scripts/run_table.py 05 --db matters/acme.db --room /path/to/dataroom --run    # spend
```

Always read the estimate first. A 27-column table over 40 rows is roughly 1,080 model calls.

## Tests

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check src tests scripts && .venv/bin/ruff format --check src tests scripts
```

189 tests. OCR is off by default in the suite and exercised deliberately through the `ocr_on`
fixture, which keeps the run near 20 seconds. CI installs `tesseract-ocr` and `poppler-utils`.

## The matter database holds client material

Document text, extracted cells, entity names, and extracted email attachments. Treat the file
like a matter file: restrict who can read the directory, back it up with the firm's normal
process, and keep the `-wal` and `-shm` sidecars with it.
