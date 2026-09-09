# Ingestion

A data room is not a folder of text files. PDF, DOCX, XLSX, CSV, HTML and email are read by
default; anything produced but unreadable is **reported**, not skipped in silence, because an
unread file must not look like an absent one — that is exactly what the coverage register
exists to catch.

| Path | Extensions | Handling |
|---|---|---|
| Prose | `.pdf` `.docx` `.txt` `.md` `.html` `.htm` | Extract, strip running headers, chunk by paragraph |
| Tabular | `.xlsx` `.xlsm` `.csv` `.tsv` | Chunk by rows, header restated per chunk |
| Mail | `.eml` `.msg` | Normalize headers, split quoted chain, extract attachments |
| Reported unreadable | `.xls` `.doc` `.rtf` `.ppt(x)` `.zip` `.7z` `.rar` | `DOCUMENT_FORMAT_UNREADABLE`, with what to do about it |

Ingestion is idempotent by content hash. Re-ingesting an unchanged file is a no-op.

## Running headers and footers are removed first

An extractor emits them in reading order, so a clause spanning a page break arrives as:

```
...and any consent
Confidential Page 1 of 3

CEDAR POINT COMMERCE CENTER — LEASE AGREEMENT EXECUTION VERSION
required under Section 4 or Section 5 must be obtained...
```

Boilerplate inside a sentence breaks three things at once: the Verbatim check rejects a
correct quotation, retrieval scores passages on page furniture, and the model reads an
interrupted sentence.

`vault/cleaning.py` drops lines repeating at the top or bottom of most pages, comparing them
with digits masked so `Page 1 of 3` matches `Page 2 of 3`. A one-page document is untouched —
nothing can be shown to repeat. The full text is then **rebuilt from the cleaned pages**, so
character offsets and page attribution are exact by construction rather than by agreement
with the extractor.

## Spreadsheets are read as tables, not prose

`00a` classifies cap tables, stock ledgers, censuses and loss runs as **Records** — they report
facts as at a date, and the as-of date is what makes one usable.

Chunking one by paragraph produced this, on a 40-row census fixture:

```
E1027   Employee 27   Manager   Wilmington, DE   2024-01-15   118450   20   US Citizen
```

The header was two chunks back. Nothing says `118450` is base salary and `20` a bonus
percentage, and a model asked to read it will guess — on a record that feeds the transaction
payments schedule.

So tables are chunked **by rows**, with the sheet name and header restated in every chunk
including continuations, and the repetition written into the stored text so each chunk stays
an exact slice:

```
# Sheet: Employee Census (continued)
Employee ID  Name  Title  Location  Hire Date  Base Salary  Bonus Target %  Visa Status
E1032  Employee 32  Engineer II  Austin, TX  2022-06-15  125200  10  US Citizen
```

## Email is correspondence, and it carries documents

Tables 17, 23 and 25 are built around correspondence, and their review unit is a *matter* of
several communications — so one message is one document, and unit assembly groups them.

- **Headers are normalized** into the text: Table 05 routes on From, Cc, Date and Subject.
- **The quoted chain is separated and labelled**, not deleted. Deleting it loses evidence;
  leaving it inline duplicates every earlier message into every later file, distorting
  retrieval and defeating "the most recently dated document that addresses it".
- **Attachments are ingested in their own right**, linked to the carrier, because in a data
  room the attachment is usually the agreement. Signature images, `.p7s`, `.ics` and `.vcf`
  are recognised as mail furniture.
- **Privilege markings are reported** on every document, not only email. `00a`: report the
  marking and stop, never assess whether privilege applies — "a privileged document reaching
  the wrong reviewer is a handling problem". A column that notices after a run is too late.

## OCR

A PDF page with no text layer is a scan. `DILIGENCE_KERNEL_OCR` takes `auto` (default),
`tesseract`, `vision` or `off`.

**Tesseract is the default, not a vision model.** Both misread; they misread differently.
Tesseract garbles, which a reviewer sees. A vision model transcribes fluently, so a misreading
arrives as ordinary plausible text. When the output feeds a control a partner relies on, a
legible failure beats a convincing one — and tesseract is free, offline, and keeps client
documents on the machine.

**OCR text is a transcription, not the document.** That travels with it:

- `document.text_source` records `ocr` with engine and confidence
- the prompt prefix tags such documents `source="ocr (tesseract, 95% confidence)"` and tells
  the model not to correct a garbled word
- `cell_evidence` reports the source of every quotation
- a **Verbatim** cell in a transcribed unit is flagged `VERBATIM_FROM_OCR`, because matching a
  quotation against OCR output compares one reading with another and cannot show the words are
  the document's

## Evidence provenance

Every chunk carries a character span and page range into the stored text, and every cell names
the sentences it was drawn from. A quote that cannot be located is dropped rather than stored
with a false offset.

## What running it for real found

Each of these came from feeding the pipeline a realistic document, not from reasoning:

| Symptom | Actual cause |
|---|---|
| Verbatim rejected a correct quotation | Ligatures, soft hyphens, hyphenated line breaks, page-break boilerplate |
| A scan became 20 confident cells | Empty text produced a context block; the unit is now reported, not answered |
| Census rows unreadable | Header stranded two chunks back |
| An emailed agreement vanished from intake | Per-file units keyed on content hash collided with the folder copy |
| `Secondary Workstream` returned `None` on 9 of 10 documents, on two models | The parser silently truncated a 20-option list to 2, and the engine presented it as complete |
| 5 of 10 documents routed nowhere | The routing map used invented workstream names, not the corpus's |
| Widespread `Unable to determine` | Table Instructions reached the model with placeholders unbound |
