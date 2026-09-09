# Findings reference

Every tool returns findings: `{code, subject_type, subject_id, subject_name, observation,
evidence}`. An observation is one factual sentence — it carries no advice, no severity
adjective and no suggested rewrite.

A **finding** is an observation about the matter. A **violation** is a standards breach
recorded on a cell; those are listed in [Standards](standards.md).


## Corpus

| Code | Means | What to do |
|---|---|---|
| `INVENTORY_UNPARSED` | An inventory file could not be parsed at all. | Read the file; the parser reports the exception. |
| `PROMPT_MISSING` | A column record has no fenced prompt block. | Add the prompt, or the column cannot be filled. |
| `NATIVE_TYPE_MISSING` | A column record states no native type. | Add it; the loader defaults to Free Response. |
| `NATIVE_TYPE_DISAGREES` | The column index and the column record disagree on the type. | Correct one of them. |
| `CLASSIFY_OPTIONS_ABSENT` | A Classify column lists no configured options. | Add the option list. |
| `OPTIONS_NOT_ENUMERATED` | The options bullet names a vocabulary it does not spell out. | Enumerate it. Until then the engine does not assert the list is complete. |
| `INDEX_COLUMN_WITHOUT_RECORD` | The index lists a column no record defines. | Add the record or remove the index row. |
| `RECORD_COLUMN_WITHOUT_INDEX` | A record defines a column the index omits. | Add the index row. |
| `AT_REF_UNRESOLVED` | A prompt references an @Column that does not exist in its table. | Fix the reference; it currently resolves to nothing. |
| `DEPENDENCY_CYCLE` | Columns could not be staged because their references form a cycle. | Break the cycle; those columns cannot run. |
| `WORKSTREAM_NOT_ROUTED` | A Workstream option has no routing entry. | Documents classified into it reach no table. Add it to WORKSTREAM_TABLES or WORKSTREAMS_WITHOUT_TABLES. |
| `WORKSTREAM_ROUTE_STALE` | A routing entry names a workstream the corpus no longer offers. | Remove it. |
| `TABLE_MUST_PAIR` | 00a pairs this table with another that resolves its `Incorporated terms`. | Build both or neither. |

## Matter

| Code | Means | What to do |
|---|---|---|
| `UNBOUND_PARAMETERS` | Table Instructions reach the model with placeholders unbound. | Call matter_parameters_set. Answers depending on them cannot be right. |
| `DOCUMENTS_UNROUTED` | Extracted documents carry no classification. | Run Table 05; no workstream table can see them. |
| `DOCUMENT_WITHOUT_WORKSTREAM` | Table 05 returned no workstream for a file. | A human decides. The file is invisible to every workstream table until then. |

## Ingestion

| Code | Means | What to do |
|---|---|---|
| `EXTRACT_FAILED` | The file could not be extracted. | Check the format; the exception is recorded on the document. |
| `DOCUMENT_FORMAT_UNREADABLE` | A produced file is in a format the vault cannot read. | Convert it. It is reported so it does not look absent. |
| `DOCUMENT_EMPTY` | The file yielded no text. | Enable OCR, or accept it as produced-but-unreadable. |
| `DOCUMENT_OCRED` | Pages with no text layer were transcribed. | The text is a reading of the document, not the document. |
| `OCR_LOW_CONFIDENCE` | The transcription averaged below 70% confidence. | Treat every cell drawn from it as unverified. |
| `OCR_UNAVAILABLE` | Pages need OCR and no engine is available. | Install tesseract and poppler, or set DILIGENCE_KERNEL_OCR. |
| `OCR_FAILED` | OCR produced no usable text. | Check the engine; the error is reported. |
| `WORKBOOK_READ` | A spreadsheet was read as tables. | Informational: names each sheet and its row count. |
| `SHEET_WITHOUT_HEADER` | No header row could be identified in a sheet. | Its columns are unlabelled and cannot be relied on. |
| `SHEET_EMPTY` | A sheet holds no rows. | Informational. |
| `PRIVILEGE_MARKING` | A document carries a privilege marking. | Confirm who may see it. The marking is reported, never assessed. |
| `ATTACHMENT_INGESTED` | An email attachment was ingested as its own document. | Informational: it is classified and routed on its own merits. |
| `ATTACHMENTS_NOT_DOCUMENTS` | Attachments were mail furniture rather than documents. | Informational. |
| `EMBEDDING_FAILED` | Chunks were stored without embeddings. | Retrieval falls back to keyword matching. |

## Units

| Code | Means | What to do |
|---|---|---|
| `NO_DOCUMENTS_IN_SCOPE` | No classified document routes to this table. | Run Table 05 first, or check the workstream mapping. |
| `DEPENDENT_WITHOUT_BASE` | A document names a base instrument that is not in scope. | It was placed in a unit of its own; confirm the family. |
| `BASE_MATCH_AMBIGUOUS` | A dependent matched more than one candidate base about equally. | Confirm the family before relying on the row. |
| `UNIT_EXCEEDS_GROUPING_CAP` | A unit holds more documents than the table's stated cap. | Split it, or confirm the cap. |
| `UNIT_KEY_UNRESOLVED` | Documents could not be grouped by subject. | They were collected into one unassigned unit. |
| `UNIT_HAS_NO_TEXT` | A unit's documents hold no extracted text. | Its cells were skipped rather than answered from an empty page. |

## Runs

| Code | Means | What to do |
|---|---|---|
| `NOTHING_TO_RUN` | No cell is in scope. | Every cell is filled, locked or reviewed, or the table has no rows. |
| `CELL_FILL_FAILED` | A cell could not be filled. | The provider error is recorded; the rest of the stage continued. |
| `CELL_LOCKED_NOT_REFILLED` | A locked or reviewed cell was left as it stands. | Expected. Locking preserves work; it does not refresh it. |
| `PREFIX_BELOW_CACHE_MINIMUM` | A unit's prefix is too short to cache. | Priced without the discount. Small documents only. |
| `MODEL_PRICE_UNKNOWN` | No price is recorded for the model. | Set DILIGENCE_KERNEL_PRICE_IN / _OUT. |
| `TOKENS_ESTIMATED_NOT_COUNTED` | Tokens could not be counted; figures are approximate. | Usually a missing credential. |

## Artifacts

| Code | Means | What to do |
|---|---|---|
| `ARTIFACT_EMPTY` | No filled cell matches the artifact's source columns. | Run the tables that feed it. |
| `ARTIFACT_CARRIES_UNREVIEWED_CELLS` | Rows carry cells still Unreviewed. | A schedule built from candidates is a list of candidates. |
| `ARTIFACT_CARRIES_FLAGGED_CELLS` | Rows carry cells with a standards violation. | Read them before circulating. |
| `NO_MATERIALITY_RECORDED` | No cell carries a materiality value. | The issues list is built from a human column nobody has filled. |
