# Coverage Register — Construction Specification

Table 6 of the POC. **This one is not a Review Table**, and the reason matters.

Shared conventions are in `00-build-plan-and-standards.md`.

---

## 1. Why this is not a Review Table

`harvey-diligence-spec.md` §2 calls the row inversion "the single most useful move
available in a UI-only world," and it is right about that. Rows are request-list
items rather than documents, so the empty cells become the gap register. Filter to
them and that filter is your supplemental request list.

The mechanism it proposes does not work, though. §5.3 says to build rows from the
diligence request list and then run the table against the project. But a Review
Table column analyses **the review unit in its row**. A row representing a request
item has no review unit. There is nothing for a column to read, so a column asking
"is there a responsive document in this project?" has no document to answer from.

Whether Harvey permits manually created rows at all is unverified — it is in the
shared pre-run checklist. But even if it does, the column would still have nothing
to analyse. The obstacle is the execution model, not row creation.

**The fix keeps the insight and changes the direction of the inversion.** Harvey
maps documents to request items, one row per document, which is exactly what a
Review Table does well. Then you invert in Excel, where request items with no
responsive document are the gaps. Same artifact, one pivot table later.

That is a correction to the source spec, and worth recording as one.

---

## 2. Architecture

```
INPUT 1 — Diligence request list (DDRL)
   Typed by the team, outside Harvey. One row per item.
                    │
INPUT 2 — Intake table, two added columns          [HARVEY]
   Per document: which DDRL items it responds to, and how fully
                    │
INPUT 3 — Referenced but Not Produced              [HARVEY]
   Aggregated from every table's coverage column
                    │
                    ▼
        Excel: pivot documents → request items
                    │
                    ▼
        COVERAGE REGISTER
   Rows: request items + referenced-but-absent documents
   Empty responsive-document cells = the gap register
```

Only Input 2 needs new prompts. Input 3 already exists in every inventory. The
pivot and the register are Excel.

---

## 3. Input 1 — the request list

Typed by the team before anything is produced. One row per item, at the
granularity you would actually request at.

| Field | Populated by | Notes |
|---|---|---|
| Item ID | Human | `CORP-04`, `EMP-11`. The join key; keep it stable |
| Workstream | Human | Matches the Intake workstream vocabulary exactly |
| Request text | Human | As sent to the seller, verbatim |
| Round requested | Human | Initial, supplemental 1, supplemental 2 |
| Expected document types | Human | From the Intake vocabulary. **This is what makes matching possible** |
| Priority | Human | Closing-critical / Material / Standard |

**Seed the list from the missing-document tests**, not only from the DDRL.
`review-tables.md` §2–11 lists them per workstream — good standing certificates
for every entity, board approvals for every issuance, invention assignments for
every technical employee, UCC searches for every jurisdiction of organisation,
leases for every operating location. Those are what the team knows to look for
before the seller produces anything, and they belong in the register as rows from
day one.

---

## 4. Input 2 — two columns added to the Intake table

These go in the Intake Classification inventory as columns 21 and 22. Intake
already runs over the whole data room, so the mapping comes free rather than
needing its own pass.

### 21. Request Items Responded To

- Native type: Free Response
- Upstream: `@Document Type`, `@Workstream`, `@Subject Entity`
- Downstream: `Responsiveness`
- Purpose: identify which request-list items this document responds to, so the
  register can be built by pivoting rather than by matching document names to
  request text by hand.

**Maintenance warning.** The request list is pasted into this prompt, so the
prompt is matter-specific and changes every time a supplemental request goes out.
Version it in the inventory on every change and rerun the column. This is the
only matter-specific prompt in the whole set.

```markdown
## Established results

- Document type: @Document Type
- Workstream: @Workstream
- Subject entity: @Subject Entity

Use these to narrow which request items could apply. Confirm responsiveness against the document itself.

## Task

Identify every request-list item below that this document responds to, in whole or in part.

## Request list

Match only against items in this list. Use the item ID exactly as written.

- `[ITEM-ID]` — [request text as sent] — expects: [document types]
- `[ITEM-ID]` — [request text as sent] — expects: [document types]
- `[ITEM-ID]` — [request text as sent] — expects: [document types]

[Paste the full list. Keep the ID, the request text, and the expected document types for each item.]

## Matching rules

- A document responds to an item where it is of a type the item expects **and** it concerns the subject the item asks about. Both are required. A lease responds to a request for leases only if it is a lease for a property the request covers.
- Match on the document's content, not on the workstream assignment alone. The workstream narrows the candidates; it does not decide the match.
- Where the item asks about a specific entity, property, individual, or counterparty, match only if this document concerns that subject. Use the Subject Entity result to check.
- **A document may respond to more than one item.** List every item it responds to. An employment agreement with an IP assignment clause responds to both the employment item and the invention-assignment item.
- Match a document that partially responds. Partial responsiveness is reported in the next column, not resolved here by excluding it.
- Do not match a document merely because it mentions the subject. A board consent referring to a lease does not respond to a request for the lease.
- Do not match on the file name.

## Fallback rules

- Return exactly `No matching item` where the document responds to no item in the list. **This is a meaningful answer**: it means the seller produced something nobody asked for, which is worth a look, and it may mean the request list has a gap.
- Return `Unable to determine` where the document cannot be read well enough to assess responsiveness.

## Output format

`[ITEM-ID]` per line, in list order. Return no more than 8 lines. Where a document responds to more than 8 items, list the first 8 and end with `and [N] further items`. Do not include the request text, explanation, or citation markers.
```

### 22. Responsiveness

- Native type: Classify
- Configured options, in UI order: `Fully responsive`, `Partially responsive`, `Responsive but superseded`, `Responsive but unexecuted`, `Not responsive`, `Unable to determine`
- Upstream: `@Request Items Responded To`, `@Execution Status`, `@Completeness`
- Purpose: whether the produced document actually satisfies the request. **A
  document produced is not a request satisfied**, and this is the column that
  keeps the register honest about the difference.

```markdown
## Established results

- Request items responded to: @Request Items Responded To
- Execution status: @Execution Status
- Completeness: @Completeness

Use these for routing. Confirm the assessment against the document itself.

## Task

Classify how fully this document satisfies the request items it responds to. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Not responsive`: Request Items Responded To returned `No matching item`.
2. `Unable to determine`: Request Items Responded To returned `Unable to determine`.
3. `Responsive but unexecuted`: Execution Status is `Unsigned draft` or `Form or template`. **A draft does not satisfy a request for an agreement**, and treating it as satisfied is the failure this register exists to prevent.
4. `Partially responsive`: Completeness is `Fragment only`, `Pages missing`, `Signature page missing`, or `Exhibits or schedules missing`; or the document covers only part of what the item asks about — one entity of several, one property of several, one year of a requested period.
5. `Responsive but superseded`: the document states on its face that it has been amended, restated, replaced, or terminated by a document dated later. Whether the later version governs is a legal question; this cell reports only that the document says it is not the current version.
6. `Fully responsive`: the document is complete, executed where execution is expected, and covers what the item asks about.

Where a document responds to several items and its adequacy differs between them, classify on the **least** satisfied and note which item in the evidence field. The register should overstate a gap rather than hide one.

## Fallback rules

- Do not use `Unable to determine` because the document only partly answers. That is `Partially responsive`.

## Output format

Return only the exact configured option and no explanation.
```

---

## 5. Input 3 — referenced but not produced

Already built. Every inventory in this set carries a `Referenced but Not Produced`
column with the same output format:

`[Name as referenced] — [date or "date not stated"][; authorizes: [action]]`

Export all of them, stack the columns in one sheet, and de-duplicate on name and
date. Each surviving line becomes a register row with no Item ID — these are the
gaps nobody asked for because nobody knew the documents existed, and they are
where the real exposure hides.

Two things to keep when stacking: the source table and row, so a reviewer can see
which document referenced the missing one; and the `authorizes:` clause, because
an action with no producible approval is a stronger finding than a missing exhibit.

---

## 6. The register itself

Built in Excel. Two row populations in one sheet.

| Column | Populated by | Notes |
|---|---|---|
| Item ID | Human | Blank for referenced-but-absent rows |
| Workstream | Human / carried | |
| Request text or document name | Human / carried | Request text for DDRL rows; the name as referenced for absent-document rows |
| Priority | Human | |
| **Responsive documents** | **Pivot** | File names from the Intake export where `Request Items Responded To` contains this Item ID |
| **Responsiveness** | **Pivot** | Best value across the responsive documents |
| Referenced in | Carried | For absent-document rows: which document referenced it |
| **Disposition** | **Human** | `Satisfied` / `Gap, outstanding` / `Gap, waived` / `Assumed` / `Carried to SPA` |
| Round requested | Human | |
| Owner | Human | |
| Waiver name and reason | Human | Required whenever Disposition is `Gap, waived` |
| Notes | Human | |

### The pivot

From the Intake export: split `Request Items Responded To` on line breaks, so one
document with four item IDs becomes four rows, then pivot with Item ID as the row
field and file name as the value. Any item ID from the request list that does not
appear in the pivot has no responsive document.

**The empty cells are the deliverable.** Filter `Responsive documents` to blank
and that filter is your supplemental request list.

### The four filters to work

1. `Responsive documents` blank, `Priority` = closing-critical — the gaps that
   stop a closing
2. `Responsiveness` = `Responsive but unexecuted` — produced but worthless, and
   the failure mode most often mistaken for satisfaction
3. Referenced-but-absent rows with an `authorizes:` clause — an action with no
   producible approval
4. `Disposition` = `Gap, waived` with no name and reason — **the failure this
   whole structure exists to prevent**

---

## 7. Completion means dispositions, not documents

"We reviewed everything in the data room" is not a completeness statement, because
the data room is what the seller chose to produce.

A workstream is done when every row has a disposition. A gap closed without a
named waiver and a reason is not closed.

---

## 8. What to verify

- [ ] Whether Harvey permits manually created rows in a Review Table. If it does,
      revisit whether any part of this can move in-product. The execution-model
      obstacle in §1 stands either way, so expect the answer not to change the
      design.
- [ ] Whether `Request Items Responded To` stays under the character limit with
      your actual request list pasted in. A 60-item list at 25 words each is
      roughly 4,500 characters before the rules. If it overruns, split the column
      by workstream — one column per workstream, each carrying only its own items,
      routed on `@Workstream`.
- [ ] Whether re-running the column after a supplemental request preserves the
      earlier matches. It should, but the whole register depends on it.

---

## 9. Change log

| Date | Item | Change | Notes |
|---|---|---|---|
| | v1.0 | Initial specification | Corrects `harvey-diligence-spec.md` §5.3: the inversion happens in Excel, not in a Review Table |
