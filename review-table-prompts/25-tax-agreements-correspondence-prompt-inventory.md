# Prompt Inventory — Tax: Agreements and Correspondence

Table 25 of the POC. **This completes the set.**

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Tax`
- Review unit: **one tax matter or instrument** — for an agreement, the agreement
  and its amendments; for an examination or dispute, the initiating notice, the
  responses, any report, adjustment, or assessment, and any closing agreement or
  determination
- Grouping used: **yes**, typically 1–8 documents per unit
- Intended reviewers and downstream use: tax and corporate/M&A teams; feeds the
  tax indemnity and escrow analysis, the deconsolidation analysis, the disclosure
  schedule, and the coverage register
- Inventory version: v1.0

### A deliberate exception to the role rule

**This is the only table in the 25 that carries two document roles.** A tax
sharing agreement is an Instrument read for its allocation and survival terms; an
audit file is Correspondence read for the chronology and the assertion; a ruling or
opinion is Analysis read for scope and reliance.

Splitting them would produce three tables of eight to ten columns each over a
handful of rows, which costs more in build and maintenance than it returns. The
compromise is `Matter Category` as the first routing column, with every substantive
column routed on it — the same technique used in Real Estate — Owned Property,
where the row is the property rather than the document.

**If your matter is heavy on either side** — a target with a substantial audit
history, or one sitting inside a complex group tax sharing arrangement — split it.
The columns divide cleanly at the category boundary and the front matter's table
register should be updated to 26.

### The two questions that matter most

1. **What survives closing, and who bears it?** A tax sharing agreement allocates
   liability between the parties; **it does not remove several liability as against
   the authority.** Where the target has been filing inside the seller's group, both
   facts are live and the agreement is the operative document.
2. **What is open?** An examination in progress, an unpaid assessment, or an
   unexpired appeal is a live exposure with its own timetable, and it may
   constrain the indemnity and the escrow directly.

## Assumptions to confirm before running

1. One row is one matter or one instrument. An examination generating a notice, an
   information request, a response, a report, and a closing agreement is one row.
2. **Returns and filings are the companion table.** A return is a Record.
3. Court or tribunal proceedings are Litigation rows as well as rows here.
   `Escalation Status` records the crossing.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

19 Harvey columns plus 9 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side tax diligence on the target group listed below. This table reviews tax agreements, examinations, disputes, rulings, and correspondence with tax authorities.

One row is one tax matter or instrument. For an agreement, the review unit is the agreement and its amendments. For an examination or dispute, it is the initiating notice, the responses, any report, adjustment, or assessment, and any closing agreement or determination. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the taxpayer or its affairs.
- **Report the position as at the most recently dated document in the unit, and identify that document.** A tax dispute moves, and a cell without a date is not usable.
- **Distinguish what the authority asserts from what the taxpayer accepts.** A proposed adjustment is the authority's position; the response may dispute it. Report both and label each. Do not adopt either.
- **Do not assess the merits of any position, the likely outcome, the size of any exposure, or whether an agreement is enforceable.** All four are legal judgements and all four are human columns.
- Report figures exactly as stated, with the document they come from. **Do not calculate anything** — do not total tax, interest, and penalties, do not accrue, do not net an adjustment against a refund, and do not convert currency.
- **Report privilege and work-product markings where present and do not assess privilege.** Tax advice, opinions, and audit workpapers frequently attract protection, and some material may not be disclosable to a buyer at all.
- Do not report the names or identifying numbers of individual taxpayers or employees. Report entities and roles.
- Use entity and authority names exactly as printed.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Write currency amounts with the currency as printed.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Matter Category
  Taxpayer Entity
  Tax Type and Jurisdiction
  Periods Covered

Stage 2 — Counterparty and status
  Matter Category ──→ Authority or Counterparty
                      Issues or Subject Matter
                      Allocation and Indemnity Terms
                      Reliance and Scope
  Documents in Unit ──→ Status
                        Referenced but Not Produced
  Status ──→ Status As-Of Date
  Initiated or Executed Date

Stage 3 — Dispute substance
  Issues or Subject Matter ──→ Taxpayer Position
  Amount at Issue
  Settlement or Determination

Stage 4 — Transaction effect
  Allocation and Indemnity Terms ──→ Survival on Change of Control
  Continuing Obligations
  Escalation Status
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Matter Category | Classify | — | Authority or Counterparty; Issues or Subject Matter; Allocation and Indemnity Terms; Reliance and Scope | v1.0 | draft |
| 3 | Authority or Counterparty | Free Response | @Matter Category | — | v1.0 | draft |
| 4 | Taxpayer Entity | Free Response | — | — | v1.0 | draft |
| 5 | Tax Type and Jurisdiction | Free Response | — | — | v1.0 | draft |
| 6 | Periods Covered | Free Response | — | — | v1.0 | draft |
| 7 | Initiated or Executed Date | Date | — | — | v1.0 | draft |
| 8 | Status | Classify | @Documents in Unit | Status As-Of Date | v1.0 | draft |
| 9 | Status As-Of Date | Date | @Status | — | v1.0 | draft |
| 10 | Issues or Subject Matter | Free Response | @Matter Category | Taxpayer Position | v1.0 | draft |
| 11 | Taxpayer Position | Free Response | @Issues or Subject Matter | — | v1.0 | draft |
| 12 | Amount at Issue | Free Response | — | — | v1.0 | draft |
| 13 | Settlement or Determination | Free Response | — | — | v1.0 | draft |
| 14 | Allocation and Indemnity Terms | Free Response | @Matter Category | Survival on Change of Control | v1.0 | draft |
| 15 | Survival on Change of Control | Classify | @Allocation and Indemnity Terms | — | v1.0 | draft |
| 16 | Reliance and Scope | Free Response | @Matter Category | — | v1.0 | draft |
| 17 | Continuing Obligations | Free Response | — | — | v1.0 | draft |
| 18 | Escalation Status | Classify | — | — | v1.0 | draft |
| 19 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

19 columns.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Status`, `Referenced but Not Produced`
- Purpose: inventory the matter or instrument, in date order.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- For an agreement: the agreement, every amendment or restatement, any schedule, and any assignment or novation.
- For an examination or dispute: the opening or audit notice, information document requests, the taxpayer's responses and submissions, examination reports, proposed and final adjustments, assessments and notices of deficiency, protests and appeals, settlement or closing agreements, and any final determination or closing letter.
- For a ruling or opinion: the request or submission, the ruling or opinion, and any supplement or withdrawal.
- For a voluntary disclosure: the application, the authority's response, and any agreement reached.
- Treat schedules and exhibits attached to a document as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title and form number where one appears. Where none is printed, describe it in five words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Agreement`, `Amendment`, `Opening notice`, `Information request`, `Taxpayer response`, `Examination report`, `Proposed adjustment`, `Assessment or notice`, `Protest or appeal`, `Settlement or closing agreement`, `Ruling or opinion`, `Determination or closing letter`, or `Other`.
- **For a dispute, state who sent each document — the authority or the taxpayer — since the alternation is the chronology.**
- **Where the most recent document is from the authority and no taxpayer response follows, note that in the evidence field.** An unanswered authority communication is a finding in itself and frequently means a deadline has passed.
- **Where the unit contains an unsigned agreement or an unexecuted settlement, state that.** Neither binds anyone.
- Where a document relates to a different matter, entity, or period, still list it and append ` [relates to [matter, entity, or period]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [from authority | from taxpayer | n/a] — [Title] ([Function])`

Return no more than 15 lines and no more than 130 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Matter Category

- Native type: Classify
- Configured options, in UI order: `Tax sharing or allocation agreement`, `Tax indemnity agreement`, `Examination or audit`, `Proposed adjustment`, `Assessment or notice of deficiency`, `Protest or appeal`, `Settlement or closing agreement`, `Advance ruling or clearance`, `Tax opinion or advice`, `Voluntary disclosure`, `Information request`, `Correspondence, other`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Authority or Counterparty`, `Issues or Subject Matter`, `Allocation and Indemnity Terms`, `Reliance and Scope`
- Purpose: **the routing column that makes a two-role table workable.** Every
  substantive column reads its value.

```markdown
## Task

Classify the nature of this tax matter or instrument. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits, since the order runs from most to least consequential within each role.

1. `Tax sharing or allocation agreement`: an agreement among group members allocating tax liabilities, benefits, and attributes. **Report as such even where the document is titled differently**, since the allocation function is what matters.
2. `Tax indemnity agreement`: an agreement under which one party indemnifies another for tax, whether standalone or arising from a prior transaction. **A prior-transaction tax indemnity may be an asset the buyer acquires**, and it is frequently forgotten.
3. `Settlement or closing agreement`: a concluded agreement with an authority resolving a matter, including a closing agreement, an offer in compromise, or an agreed adjustment. **These bind and they usually preclude reopening the period.**
4. `Assessment or notice of deficiency`: a formal notice of tax due or of a determined deficiency. **Report as such rather than as a proposed adjustment** — an assessment usually starts a hard clock for payment or appeal, and missing it can forfeit the right to contest.
5. `Protest or appeal`: a filed challenge to an adjustment or assessment, whether administrative or before an appeals function.
6. `Proposed adjustment`: the authority has proposed an adjustment which has not become an assessment.
7. `Examination or audit`: an examination is open, with no adjustment yet proposed.
8. `Voluntary disclosure`: the taxpayer has approached an authority to disclose an unreported liability or an unfiled period. **Report as such** — voluntary disclosure usually attracts penalty mitigation and it is also an admission of a prior failure.
9. `Advance ruling or clearance`: a ruling, clearance, or advance pricing agreement obtained from an authority.
10. `Tax opinion or advice`: an opinion or memorandum from an adviser, not from an authority. **Note in the evidence field any privilege marking**, and do not assess privilege.
11. `Information request`: the authority has requested information with no examination or concern stated.

**An information request may be the opening of an examination.** Where the documents indicate a concern behind it, classify on the concern.

## Fallback rules

- Use `Correspondence, other` where the matter is authority correspondence none of the options describes.
- Use `Other` where the document is a tax instrument none of the options describes.
- Use `Unable to determine` where the documents are too fragmentary to identify the matter.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Authority or Counterparty

- Native type: Free Response
- Upstream: `@Matter Category`
- Downstream: none
- Purpose: who the matter is with — an authority for a dispute, a counterparty for
  an agreement, an adviser for an opinion.

```markdown
## Established result

- Matter Category: @Matter Category

## Task

State the authority, counterparty, or adviser this matter is with.

## Rules by matter category

- For `Examination or audit`, `Proposed adjustment`, `Assessment or notice of deficiency`, `Protest or appeal`, `Settlement or closing agreement`, `Advance ruling or clearance`, `Voluntary disclosure`, `Information request`, and `Correspondence, other`: report the **authority** exactly as printed, with its division, office, or examination team where stated, and its level — federal or national, state or provincial, or local. Report any case, docket, or examination reference exactly as printed, since it is the key for any enquiry. Report any case officer by role rather than by name.
- For `Tax sharing or allocation agreement` and `Tax indemnity agreement`: report **every party** exactly as named, and **state for each whether it is inside or outside the acquired group**, using the review-subject list. **This is the critical fact** — an agreement whose counterparty is the seller's group is the operative document at deconsolidation, and one entirely within the acquired group simply comes along.
- For `Tax opinion or advice`: report the **adviser** firm exactly as printed, and whether the adviser is external or internal.

## Rules

- **Where more than one authority is involved — a state adjustment following a federal one, or a joint examination — report each and label its role.** A federal adjustment frequently cascades to every state return for the same period, and that cascade is a larger exposure than the federal adjustment alone.
- **Report the reference exactly**, since it is what a status enquiry is made against.

## Fallback rules

- Return `Unable to determine` where the authority, counterparty, or adviser cannot be identified.

## Output format

For a dispute: `[Authority as printed] — [office]; level: [as stated]; reference: [as printed]`.
For an agreement: `[Party as named] ([inside | outside] acquired group)` per party.
For an opinion: `[Adviser as printed] — [external | internal]`.

Return no more than 55 words.
```

---

### 4. Taxpayer Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity carries the matter. **Determines whether the exposure
  or the benefit follows the business.**

```markdown
## Task

State the target-group entity or entities this matter concerns.

## Rules

- Use the review-subject list in the Table Instructions to determine which named entities are group entities.
- Report each name exactly as printed, including entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- Where more than one group entity is concerned, list each.
- **Where the matter concerns a consolidated or combined group, report the entity examined or assessed and note in the evidence field that it is a group matter.** An adjustment at group level can affect every member.
- **Where the matter is directed at the seller's group but concerns periods in which a target entity was a member, report both and label each.** This is the deconsolidation case: **the target may remain severally liable for the group's tax for its membership years even though the matter is being run by the seller.**
- **Where an individual — a director, officer, or responsible person — is a subject of the matter, report the entity and note the individual's role in the evidence field.** Do not report the name. Personal liability for tax, particularly for withheld payroll taxes, is a real feature of several regimes.
- Where the entity named is not on the review-subject list, report the name and append ` (not a listed entity)`.

## Fallback rules

- Return `Unable to determine` where the subject cannot be identified.

## Output format

`[Exact legal name]` per entity, with any qualifier appended. Return no more than 45 words. Do not name individuals.
```

---

### 5. Tax Type and Jurisdiction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which tax and which authority, which is the join key to the companion
  table.

```markdown
## Task

State the tax or taxes and the jurisdiction this matter concerns.

## Rules

- Report the tax type as the documents describe it — income, franchise, sales and use, value added, payroll, withholding, property, excise, or other.
- Report the jurisdiction and the level.
- **Where the matter concerns more than one tax type, list each.** An examination frequently spans income and payroll, and the exposures behave differently.
- **Where the matter concerns a tax on a cross-border basis or under a treaty, say so** and name the treaty where stated.
- **Where the matter concerns a tax type or jurisdiction for which no return appears in the companion table, note that in the evidence field.** An examination of an unfiled period is a distinct and more serious exposure than an examination of a filed one.
- For an agreement, report the taxes it covers, and **note where it covers all taxes generally rather than named ones**, since the breadth determines the indemnity's reach.

## Fallback rules

- Return `Not stated` where the documents do not identify the tax.
- Return `Unable to determine` where the tax or jurisdiction is illegible.

## Output format

`[Tax type] — [jurisdiction], [level]` per tax, with any qualifier appended. Return no more than 45 words.
```

---

### 6. Periods Covered

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which periods are exposed. **The axis on which the exposure window and
  the indemnity tail are set.**

```markdown
## Task

State the tax periods this matter covers.

## Rules

- Report each period exactly as stated, with its start and end where given.
- **Where the matter covers a range of periods, report the earliest and latest**, and the count.
- **Report any period the documents state has been added to, or removed from, the scope of an examination during its course.** Scope expansion is common and it is the clearest signal that an examination is going badly.
- For an agreement, report the periods it applies to, **and where it applies to all periods during which an entity was a group member, say so and report the membership period where stated.**
- For a ruling or opinion, report the periods or transactions it addresses, and any stated period of validity.
- **Where any period covered is one for which no return appears in the companion table, note that in the evidence field.**
- **Where any period covered is stated to be one for which the limitation period has been waived or extended, note that**, since the companion table's limitation column depends on it.
- Report periods as stated. **Do not calculate a range or infer periods from a date.**

## Fallback rules

- Return `Not stated` where the documents do not identify the periods.
- Return `Unable to determine` where periods conflict or are illegible.

## Output format

`[Periods as stated][; count: [N]][; scope changed: [as stated]]`. Return no more than 45 words.
```

---

### 7. Initiated or Executed Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the matter began or the instrument was made.

```markdown
## Task

Identify the date this matter was initiated or this instrument was executed.

## Date-selection hierarchy

### For an agreement, ruling, or opinion

1. Use the effective date the document states for itself.
2. If none, use the date of the last party signature or the issue date.
3. If neither, use the date printed in the preamble.

### For an examination, dispute, or correspondence

1. Use the date of the earliest communication from the authority in the unit.
2. Where the matter is a voluntary disclosure, use the date of the taxpayer's approach.
3. Where the earliest document refers to an earlier communication not in the unit, use that earlier date as stated and note that it is taken from a reference.

## Excluded dates

- The periods under examination or covered by the agreement
- The date of the taxpayer's response
- The date of an amendment, which is noted in the evidence field
- File name and metadata dates, and transmittal and scan dates

## Rules

- **For an agreement, report whether it is signed** and note any unsigned party in the evidence field. An unsigned tax sharing agreement allocates nothing.
- **For a dispute, report the periods under examination in the evidence field**, since the gap between the periods and the examination date bears on limitation.
- Compare the date to the diligence as-of date. **Where the matter is a dispute, is not concluded, and was initiated more than eighteen months before that date, append ` [open over 18 months]`.**
- **For an agreement, note in the evidence field whether it predates a prior acquisition of the target**, since an old tax sharing agreement may bind parties nobody has thought about for years.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 8. Status

- Native type: Classify
- Configured options, in UI order: `Agreement in force`, `Agreement terminated or superseded`, `Examination open`, `Adjustment proposed, response pending`, `Assessment issued, unpaid`, `Assessment issued, paid`, `Under appeal or protest`, `Settled or closed by agreement`, `Closed, no change`, `Ruling in force`, `Advice given, no action`, `Dormant`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Status As-Of Date`
- Purpose: where the matter stands.

**Closure must be evidenced.** A tax matter believed closed with no closing letter
or determination is not closed, and tax authorities routinely revisit periods years
after an examination appears to have ended.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document and who sent it. Confirm the status against that document.

## Task

Classify the status of this matter or instrument as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Settled or closed by agreement`: a settlement, closing agreement, offer in compromise, or agreed adjustment concludes the matter. **Report in the evidence field whether it precludes reopening**, since a closing agreement usually does and an agreed adjustment may not.
2. `Closed, no change`: the authority closed the examination with no adjustment, evidenced by a closing letter or determination.
3. `Under appeal or protest`: a challenge has been filed and is pending. Note the forum and any deadline in the evidence field.
4. `Assessment issued, unpaid`: an assessment or deficiency notice has issued and the documents do not evidence payment. **Report any payment or appeal deadline in the evidence field** — these deadlines are usually short and hard, and missing one can forfeit the right to contest or trigger collection.
5. `Assessment issued, paid`: an assessment issued and payment is evidenced.
6. `Adjustment proposed, response pending`: an adjustment has been proposed and the taxpayer's response is outstanding or unanswered.
7. `Examination open`: an examination is open with no adjustment proposed.
8. `Agreement terminated or superseded`: a tax sharing, indemnity, or similar agreement has been terminated, replaced, or has expired by its terms.
9. `Agreement in force`: an agreement remains in force on the face of the documents.
10. `Ruling in force`: a ruling, clearance, or advance pricing agreement remains in force. Note any expiry or condition in the evidence field.
11. `Advice given, no action`: an opinion or memorandum with no consequent matter recorded.
12. `Dormant`: a dispute where the most recent document is more than two years before the diligence as-of date with no conclusion recorded. **Do not treat this as closed** — tax matters do not lapse through inactivity and the file may be incomplete.

**Closure must be evidenced by an authority document.** Do not infer closure from the passage of time, from a payment, or from an internal note.

## Fallback rules

- Use `Unable to determine` where documents of the same date conflict, or where the most recent document is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Status As-Of Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Status`
- Downstream: none
- Purpose: the date the status speaks as of.

```markdown
## Established result

- Status: @Status

## Task

Identify the date of the most recently dated document in the review unit, which is the date as of which the status is reported.

## Rules

- Report the date of the most recent document, and state in the evidence field who sent it.
- **Prefer the most recent document bearing on the status** — an authority communication, a taxpayer response, an assessment, a settlement, or a determination — over routine acknowledgements of a later date.
- **For an agreement, report the date of the most recent amendment or the agreement itself**, and note in the evidence field that an agreement's status does not go stale in the way a dispute's does.
- Compare the reported date to the diligence as-of date and flag the gap:
  - more than six months: append ` [status over 6 months old]`
  - more than eighteen months: append ` [status over 18 months old]`
- **Where Status is any open or pending state and the flag is `[status over 18 months old]`, the row needs verification with the target's tax function or the authority before it can be relied on.** An open examination reported from a two-year-old document may have concluded, escalated, or produced an assessment nobody has produced.

## Fallback rules

- Return `Not stated` where no document in the unit bears a date.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended.
```

---

### 10. Issues or Subject Matter

- Native type: Free Response
- Upstream: `@Matter Category`
- Downstream: `Taxpayer Position`
- Purpose: what the matter is actually about.

```markdown
## Established result

- Matter Category: @Matter Category

## Task

Report the issues this matter concerns.

## Rules by matter category

- For `Examination or audit`, `Proposed adjustment`, `Assessment or notice of deficiency`, `Protest or appeal`: report each issue the authority has raised, in twelve words or fewer, **with the tax treatment challenged and the period it affects.** Report the authority's stated basis where given.
- For `Settlement or closing agreement`: report the issues resolved and any issue expressly reserved or excluded.
- For `Advance ruling or clearance`, `Tax opinion or advice`: report the transaction, structure, or position addressed, and the conclusion reached, in the document's own terms.
- For `Voluntary disclosure`: report the liability or failure disclosed, and the periods.
- For `Tax sharing or allocation agreement`, `Tax indemnity agreement`: report the subject matter and scope in outline; the operative terms are in the Allocation and Indemnity Terms column.
- For `Information request`: report what was requested, and any concern the request indicates.

## Rules

- **Report issues as the authority's assertions**, using `the authority proposes` or `the notice asserts`. **The taxpayer's position is a separate column.**
- **Report any issue described as recurring, or as also affecting other periods, and flag it.** A single-issue adjustment that recurs across open periods multiplies, and the authority frequently says so.
- **Report any issue the documents state has been referred to a specialist, technical, or appeals function**, since it signals the authority is taking it seriously.
- **Report any penalty asserted separately from the tax issue**, since penalty exposure turns on different considerations and is often more negotiable.
- Report no more than eight issues. Where more exist, report the eight largest and append ` and [N] further issues`.
- **Do not assess the merits of any issue or the likely outcome.**

## Fallback rules

- Return `Not stated` where the documents do not identify the issues.
- Return `Unable to determine` where the issues are illegible.

## Output format

One line per issue:

`[Issue] — [treatment challenged] — [periods affected] — [authority's basis or "not stated"]`

Return no more than 8 lines and no more than 100 words.
```

---

### 11. Taxpayer Position

- Native type: Free Response
- Upstream: `@Issues or Subject Matter`
- Downstream: none
- Purpose: what the taxpayer said back. **A conceded issue and a contested one are
  entirely different exposures.**

```markdown
## Established result

- Issues or subject matter: @Issues or Subject Matter

## Task

If Issues or Subject Matter reported issues raised by an authority, report the taxpayer's position on them.

If the matter is an agreement, ruling, or opinion with no authority-raised issue, return exactly `Not applicable`.

If it returned `Not stated` or `Unable to determine`, return exactly `Unable to determine`.

## Include where expressly stated

- Which issues the taxpayer conceded, in whole or in part
- **Which issues the taxpayer contested, and on what basis in ten words or fewer**
- Any authority relied on, described generically rather than cited
- Any opinion or advice relied on, and from whom. **The opinion is a document that should be produced and it is a row in this table**
- Any statement that the position was disclosed on the return
- Any penalty defence asserted — reasonable cause, reliance on advice, substantial authority, or an equivalent
- Any request for an extension, a conference, a technical advice referral, or a meeting
- Any alternative position advanced
- Whether the response was made by the taxpayer, by counsel, or by an accountant
- The date of the response

## Rules

- **Report concession and contest separately, issue by issue where the documents allow it.** A conceded issue is a quantified liability; a contested one is a contingency, and the buyer prices them differently.
- **Report any penalty defence asserted**, since penalties are frequently the larger part of an assessment and reliance on professional advice is a recognised defence in many regimes.
- **Report where the taxpayer relied on an opinion**, since it both supports the position and identifies a document to obtain.
- **Report where no response appears and one was required.** That is either a missed deadline or a production gap, and Status carries the flag.
- Report the position as made. **Do not assess whether it is likely to succeed** and do not adopt it.

## Output format

`Conceded: [issues or "none"]; contested: [issues and basis, or "none"]; advice relied on: [adviser or "none"]; penalty defence: [as stated or "none"]; responded by: [taxpayer | counsel | accountant]; dated [YYYY-MM-DD]`

Return no more than 90 words.
```

---

### 12. Amount at Issue

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the matter is worth, reported as stated so the tax advisers can
  size it.

```markdown
## Task

Report the amounts at issue in this matter.

## Rules

- **Report each amount with its source, its date, and what it measures** — tax proposed, tax assessed, interest, penalties, tax conceded, tax settled, or a refund claimed. **These are very different figures and reporting them without labels is misleading.**
- **Report tax, interest, and penalties separately, exactly as stated. Do not total them.** Interest and penalties frequently exceed the tax on an old period, and the components are negotiated differently.
- **Report any amount stated as accruing, with its as-of date and rate as stated. Do not accrue anything yourself.**
- Report the amount by period where the documents break it down.
- **Report any amount the taxpayer has conceded separately from the amount in dispute.**
- Where an amount has been reduced during the matter, report the current figure and append ` (reduced from [figure], [YYYY-MM-DD])`. **Proposed tax adjustments are very frequently reduced substantially, so a proposed figure treated as a liability overstates the exposure.**
- **Report any amount paid, deposited, or bonded to stop interest running or to preserve an appeal right.**
- For an agreement, report any cap, threshold, or deductible on the indemnity; the terms are in the Allocation column.
- **Do not compute a total exposure, do not gross up for other periods or jurisdictions, and do not estimate an outcome.**

## Fallback rules

- Return `Unquantified` where the matter has no stated amount, which is expected for an open examination with no adjustment proposed.
- Return `Not applicable` where no amount could arise, as for an opinion.
- Return `Unable to determine` where amounts of the same date conflict.

## Output format

One line per amount:

`[Tax | interest | penalty | refund] — [figure] [currency] — [what it measures] — per [document], [YYYY-MM-DD]`

Return no more than 8 lines and no more than 95 words. Do not include any figure you calculated.
```

---

### 13. Settlement or Determination

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what was actually agreed or determined, and what it closes.

```markdown
## Task

Report the terms of any settlement, closing agreement, or final determination in this review unit.

## Include where expressly stated

- The amount agreed or determined, split between tax, interest, and penalties as stated
- The issues resolved, and **any issue expressly reserved, excluded, or left open**
- The periods covered, and **any period expressly excluded**
- **Whether the agreement precludes the authority from reopening the periods**, and any exception — commonly fraud, misrepresentation, or a subsequent adjustment by another authority
- Any concession by the authority on penalties, and the basis
- **Any agreed treatment of an issue for future periods**, and whether it binds either party going forward
- Any agreed adjustment to attributes, basis, or carryforwards
- Any payment schedule agreed, and any instalments outstanding
- **Any requirement to make a corresponding adjustment in another jurisdiction**, and whether it has been made
- Whether the agreement is signed by all parties, and whether any approval is required
- Any provision on the effect for other group members

## Rules

- **Report the reopening position prominently.** A closing agreement that precludes reopening converts an open exposure into a closed one, and that is precisely the fact a buyer needs — a settlement that leaves the period open does much less.
- **Report any agreed future treatment**, since it binds the business after closing and may constrain a position the buyer intended to take.
- **Report any required corresponding adjustment elsewhere, and whether it was made.** A federal settlement usually requires amended state returns, and **an unmade corresponding adjustment is a live exposure created by the settlement itself.**
- **Report whether the agreement is executed.** An unsigned settlement resolves nothing.
- Report amounts as stated. **Do not total or net anything.**

## Fallback rules

- Return exactly `Not settled` where the matter is unresolved.
- Return `Referenced but not produced` where a settlement is referenced and the document is absent. **A matter believed settled with no agreement produced is a significant coverage gap**, since neither the scope of the release nor the reopening position can be read.
- Return `Not applicable` where the matter category admits of no settlement.
- Return `Unable to determine` where terms conflict or are illegible.

## Output format

`Amount: [tax, interest, penalty as stated]; issues resolved: [list]; reserved: [list or "none"]; periods: [as stated]; reopening: [precluded | permitted | Not addressed]; future treatment: [as stated or "none"]; corresponding adjustment: [required and made | required not made | none]; executed: [yes | no]`

Return no more than 100 words.
```

---

### 14. Allocation and Indemnity Terms

- Native type: Free Response
- Upstream: `@Matter Category`
- Downstream: `Survival on Change of Control`
- Purpose: **the operative terms of a tax sharing or indemnity agreement.**

Where the target has been filing inside the seller's group, this is the document
that determines who pays for pre-closing tax — and its interaction with the SPA's
own tax indemnity is a drafting point the corporate team has to get right.

```markdown
## Established result

- Matter Category: @Matter Category

## Task

If Matter Category is `Tax sharing or allocation agreement` or `Tax indemnity agreement`, report the operative allocation and indemnity terms.

If Matter Category is `Settlement or closing agreement`, report any allocation among parties or group members the agreement provides, and otherwise return `Not applicable`.

For all other categories, return exactly `Not applicable`.

## Include where expressly stated

- **The allocation method** — separate return basis, pro rata by income, by an agreed formula, or by the parent's determination
- **Which party bears pre-closing tax, and which bears post-closing tax**, and how a straddle period is split
- **Who is entitled to a refund of pre-closing tax**, and whether a refund arising from a post-closing carryback belongs to the seller or the buyer. **This is a standard and frequently contested point**
- The treatment of tax attributes on a member leaving the group
- **Any indemnity given, by whom to whom, and its scope**
- Any cap, threshold, deductible, or basket on the indemnity
- **Any time limit on claiming under the indemnity**, and how it relates to the limitation periods for the taxes covered
- Any procedural requirements for a claim — notice periods, control of any contest, and rights of participation
- **Who controls the conduct of a pre-closing tax audit or dispute**, and any obligation to cooperate or to consult
- Any obligation to file, amend, or refrain from amending a pre-closing return
- Any exclusion — commonly for tax arising from the buyer's own post-closing actions
- Any security, escrow, or guarantee supporting the indemnity

## Rules

- **Report the control-of-contest provision prominently.** Whoever controls a pre-closing audit controls an outcome the other party pays for, and it is one of the most negotiated provisions in any tax indemnity.
- **Report the refund and carryback treatment**, since it is frequently the only place a real economic entitlement is allocated.
- **Report the time limit on claims against the limitation periods for the taxes covered.** An indemnity expiring before the tax limitation period leaves an uncovered window, and that window is exactly what the SPA needs to address.
- **Report any obligation restricting amendment of a pre-closing return**, since it can prevent the buyer from correcting an error it discovers.
- Report the terms as stated. **Do not assess enforceability, do not compute any allocation, and do not conclude who bears any particular liability.**

## Fallback rules

- Return `Not applicable` where the matter category is not an allocation or indemnity instrument.
- Return `Unable to determine` where terms conflict or are illegible.

## Output format

`Allocation method: [as stated]; pre-closing tax borne by: [party]; straddle split: [as stated]; refunds: [as stated]; indemnity: [by whom, scope]; cap: [as stated or "none"]; claim period: [as stated]; contest control: [party]; amendment restriction: [as stated or "none"]; security: [as stated or "none"]`

Return no more than 110 words.
```

---

### 15. Survival on Change of Control

- Native type: Classify
- Configured options, in UI order: `Survives, binds the target after closing`, `Survives, binds the seller only`, `Terminates on the target leaving the group`, `Terminates on notice or by agreement`, `Assignment or consent required`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Allocation and Indemnity Terms`
- Downstream: none
- Purpose: **whether the agreement follows the target out of the seller's group.**

An agreement that survives and binds the target is an obligation the buyer
inherits — possibly to indemnify the seller's group. One that terminates leaves
pre-closing tax to be dealt with entirely in the SPA. Either answer is workable;
not knowing which is not.

```markdown
## Established result

- Allocation and indemnity terms: @Allocation and Indemnity Terms

## Task

If Allocation and Indemnity Terms reported terms, classify what happens to this agreement when the target ceases to be a member of the group or its ownership changes.

If it returned `Not applicable`, return `Not applicable`.

If it returned `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Survives, binds the target after closing`: the agreement continues to bind the target entity after it leaves the group. **The most consequential state** — the buyer inherits the entity together with its obligations under the agreement, which may include indemnifying the seller's group for tax attributable to the target's pre-closing periods. **This must be reconciled with the SPA's own tax indemnity**, and the two can conflict.
2. `Survives, binds the seller only`: the agreement continues but its obligations after departure fall on the seller or the remaining group. Generally favourable to the buyer, and the seller's covenant is the asset.
3. `Terminates on the target leaving the group`: the agreement ceases to apply to the departing entity, whether automatically or on a stated event. **Report in the evidence field whether accrued rights and obligations survive termination** — they very often do, and a termination that preserves accrued items is not a clean break.
4. `Terminates on notice or by agreement`: termination requires an act by a party.
5. `Assignment or consent required`: the agreement addresses assignment or change of control and requires consent for it to continue or transfer.
6. `Not addressed`: the agreement says nothing about a member leaving the group or a change of control. **This is common in older tax sharing agreements and it is not benign** — the position then depends on construction, and **the several liability of former group members as against the authority is unaffected by anything the agreement says.**

Report in the evidence field whether the agreement expressly binds successors and assigns.

## Fallback rules

- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Reliance and Scope

- Native type: Free Response
- Upstream: `@Matter Category`
- Downstream: none
- Purpose: for a ruling or an opinion, what it actually covers and who can rely on
  it. **An opinion addressed to the seller, on assumed facts, may support nothing
  the buyer needs.**

```markdown
## Established result

- Matter Category: @Matter Category

## Task

If Matter Category is `Advance ruling or clearance` or `Tax opinion or advice`, report the scope, assumptions, and reliance terms.

For all other categories, return exactly `Not applicable`.

## Include where expressly stated

- The party the ruling or opinion is addressed to or issued for
- **The transaction, structure, or position it addresses, and any part expressly not addressed**
- **The level of assurance expressed** — will, should, more likely than not, reasonable basis, or an equivalent formulation. **The words are the finding**: the gradation is a term of art and each level carries a different penalty-protection effect
- **The factual assumptions the conclusion depends on, and any statement that the adviser did not verify them**
- Any representation the taxpayer gave that the conclusion relies on
- Any statement that the conclusion is not binding on the authority
- **For a ruling: whether it is binding on the authority, its period of validity, and any condition on which it ceases to apply** — commonly a change in the facts, the law, or the ownership of the taxpayer
- **Any statement that the ruling or opinion ceases to apply on a change of control or a change in the structure**
- Any reliance restriction, and whether a third party or a purchaser may rely
- Any limitation of the adviser's liability, with the amount
- Any confidentiality or disclosure restriction

## Rules

- **Report the assurance level using the document's own words.** Do not translate between formulations and do not characterise a conclusion as stronger or weaker than it states.
- **Report the factual assumptions prominently.** An opinion is only as good as its assumptions, and **an assumption that has since ceased to be true means the opinion no longer supports the position** — which is a real and common finding.
- **Report any condition on which a ruling ceases to apply, particularly a change of ownership.** A ruling the transaction invalidates is worth nothing after closing, and that is precisely when the buyer would want it.
- **Report the reliance position.** Advice addressed to the seller does not protect the buyer, and reliance is sometimes extendable.
- Report the terms as stated. **Do not assess whether the conclusion is correct or whether penalty protection is available.**

## Fallback rules

- Return `Not applicable` where the matter category is not a ruling or an opinion.
- Return `Unable to determine` where the scope or reliance terms are illegible.

## Output format

`Addressed to: [as printed]; addresses: [subject]; not addressed: [as stated or "none"]; assurance: [as printed]; assumptions: [brief]; binding on authority: [yes | no | n/a]; validity: [period or conditions]; ceases on change of control: [yes | Not addressed]; third-party reliance: [as stated]; liability cap: [as stated or "none"]`

Return no more than 100 words.
```

---

### 17. Continuing Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what survives the matter's resolution.

```markdown
## Task

Report any obligation arising from this matter or instrument that continues after its resolution or after closing.

## Include where expressly stated

- Any obligation to file, amend, or refrain from amending a return
- **Any agreed treatment of an issue binding for future periods**
- Any instalment payment schedule with amounts outstanding
- Any obligation to make a corresponding adjustment in another jurisdiction, and its deadline
- **Any ongoing reporting, disclosure, or certification obligation to an authority**
- Any obligation to maintain records for a stated period
- **Any obligation to cooperate with, or to permit another party to control, a future audit of a pre-closing period**
- Any indemnity obligation continuing, with its expiry
- Any obligation to preserve or not to use a tax attribute
- Any condition on which a ruling or an agreed treatment ceases to apply
- **Any provision stating that the obligations bind successors and assigns**
- Any escrow, security, or retention supporting a continuing obligation

## Rules

- **Report the duration of each obligation, and where none is stated say so.**
- **Report any successor-binding provision prominently**, since it is what makes the obligation the buyer's.
- **Report any obligation to cooperate on a pre-closing audit, with the control position.** These obligations run for years, they consume management time the buyer pays for, and they sit alongside whatever the SPA says about the same subject.
- **Report any agreed treatment binding future periods**, since it constrains positions the buyer may have intended to take.
- **Report any outstanding instalment**, since it is a debt.
- Report the obligations as stated. **Do not assess their burden or estimate their cost.**

## Fallback rules

- Return exactly `None` where the matter leaves no continuing obligation.
- Return `Not applicable` where the matter is not resolved, so continuing obligations cannot yet arise.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

One line per obligation:

`[Obligation] — [duration or "no end date stated"] — [party bearing it]`

then a final line: `Binds successors: [yes | Not addressed]; security: [as stated or "none"]`

Return no more than 8 lines and no more than 90 words.
```

---

### 18. Escalation Status

- Native type: Classify
- Configured options, in UI order: `No escalation`, `Referred to specialist or technical function`, `Referred to appeals`, `Referred to another jurisdiction or authority`, `Referred to criminal investigation`, `Court or tribunal proceedings commenced`, `Competent authority or treaty procedure invoked`, `Escalation threatened, not effected`, `De-escalated or withdrawn`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the matter has moved beyond routine examination. **Also the
  boundary marker with the Litigation table.**

```markdown
## Task

Classify whether this matter has been escalated beyond routine examination. Choose exactly one configured option.

## Scope

- Consider referrals within the authority, referrals to other authorities or jurisdictions, criminal referrals, treaty procedures, and the commencement of proceedings.
- Consider any statement by the authority that escalation is contemplated.
- For an agreement, ruling, or opinion with no dispute, return `Not applicable`.

## Classification rules

Apply the first rule that fits.

1. `Referred to criminal investigation`: the documents record a referral for criminal investigation or prosecution, or the involvement of a criminal investigation function. **The most serious state available.** Report in the evidence field whether individuals are within the referral, described by role. **Tax fraud and evasion carry personal criminal exposure in every major regime**, and a criminal referral changes the disclosure, the indemnity, and sometimes the deal.
2. `Court or tribunal proceedings commenced`: proceedings have been commenced in a tax court, tribunal, or general court. **This matter is also a Litigation row**, and the reviewer should confirm it appears there.
3. `Competent authority or treaty procedure invoked`: a mutual agreement procedure or competent authority process has been invoked under a double tax treaty. **These take years and they suspend the practical finality of the matter in both jurisdictions.**
4. `Referred to another jurisdiction or authority`: the matter has been referred or reported to another authority, or an adjustment in one jurisdiction has triggered an examination in another. **A federal adjustment commonly cascades to every state return for the same periods**, and the cascade is frequently larger than the original.
5. `Referred to appeals`: the matter has moved to an appeals or review function within the authority.
6. `Referred to specialist or technical function`: the matter has been referred for technical advice, to a specialist team, or to a transfer pricing or valuation function. **A signal that the authority is taking the issue seriously.**
7. `Escalation threatened, not effected`: the authority has stated it may escalate or take formal action if a condition is not met. **Report the condition and any deadline in the evidence field.**
8. `De-escalated or withdrawn`: an adjustment was withdrawn, a referral closed, or the matter returned to routine handling.
9. `No escalation`: the matter has remained within routine examination.

## Fallback rules

- Use `Not applicable` where the matter is an agreement, ruling, or opinion with no dispute element.
- Use `Unable to determine` where references to escalation are too incomplete to classify.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this matter refers to that is not present. Feeds
  the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this matter that the documents in this unit refer to and that is not present.

## Scope

- **Include any settlement, closing agreement, or determination referenced but not produced.**
- **Include any assessment, notice of deficiency, or adjustment referenced but not produced.**
- Include examination reports and information document requests referenced.
- Include the taxpayer's responses and submissions referenced.
- **Include any waiver or extension of the limitation period referenced.**
- **Include the tax sharing or indemnity agreement referenced by an examination or a return.**
- Include any amendment to an agreement referenced but absent.
- Include any ruling, clearance, or advance pricing agreement referenced.
- **Include any opinion or memorandum referenced as relied on**, noting that these may be privileged; report the reference and do not assess privilege.
- Include the returns for the periods under examination, where not in the companion table's units.
- Include any corresponding adjustment filing in another jurisdiction referenced as required.
- Include any protest, appeal, or petition referenced.
- Include any prior examination of the same issue referenced.
- Include any payment record, instalment agreement, or lien notice referenced.
- Exclude statutes, regulations, and published guidance.

## Rules

- Name each document as the referencing document names it, with its form number and date where stated.
- **Where a settlement or determination is referenced and absent, add `; resolution scope unreadable`.** Filter these first — neither the issues resolved nor the reopening position can be assessed without it, and a matter believed closed may not be.
- **Where a tax sharing or indemnity agreement is referenced and absent, add `; allocation terms unreadable`.** In a deconsolidation this is the operative document and the SPA drafting depends on it.
- **Where a waiver or extension of the limitation period is referenced and absent, add `; limitation position uncertain`.**
- Where an opinion relied on is absent, add `; penalty defence unevidenced`.
- Where a required corresponding adjustment filing is absent, add `; corresponding adjustment unevidenced`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; flag]`

Return no more than 15 lines and no more than 130 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Status verified with tax function or authority** | Yes (date) / No / Not required |
| **Exposure estimate** | Free text |
| **Bears on deconsolidation** | Yes / No / Unassessed |
| **Interaction with SPA tax indemnity** | Reconciled / Conflict identified / Unassessed |
| **Recovery route** | Prior-transaction indemnity / Seller covenant / None / Unassessed |
| **Disclosure schedule item** | Yes / No |
| **Special indemnity or escrow candidate** | Yes / No / Unassessed |
| **Continuing obligations post-closing** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** These rows are few and each either allocates a liability,
records one, or protects against one.

### Reconciliation work that never belongs in a column

- **The deconsolidation analysis.** Every `Tax sharing or allocation agreement`
  row, read with the companion table's `Consolidated or Combined Group` rows.
  **Several liability for group tax commonly survives leaving the group**, and the
  agreement allocates it between the parties without removing it as against the
  authority. **The SPA has to address both**, and the `Survives, binds the target
  after closing` rows are where the agreement and the SPA indemnity can conflict.
- **The indemnity gap analysis.** Every indemnity claim period from
  `Allocation and Indemnity Terms` against the limitation periods from the
  companion table's `Statute of Limitations` column. **An indemnity expiring
  before the tax limitation period leaves an uncovered window**, and that window is
  what the SPA survival period must cover.
- **Open matter quantification.** Every open examination, proposed adjustment, and
  assessment, sized by tax advisers with interest and penalties, and stress-tested
  for the periods and jurisdictions the same issue could reach. **Never a Harvey
  column**, and the cascade to other periods and jurisdictions is usually larger
  than the matter as raised.
- **The cascade check.** Every adjustment or settlement, checked for required
  corresponding adjustments in other jurisdictions and for whether they were made.
  **An unmade corresponding adjustment is an exposure created by the settlement
  itself.**
- **Opinion currency.** Every `Tax opinion or advice` row, with its assumptions
  tested against the current facts, and every ruling checked for a change-of-control
  condition. **An opinion resting on an assumption that has ceased to be true, or a
  ruling the transaction invalidates, supports nothing.**
- **Recovery routes.** Every `Tax indemnity agreement` from a prior transaction,
  with its limits and expiry. **These are assets, they are routinely forgotten, and
  the transaction should preserve rather than lose them.**
- **Criminal exposure.** Every criminal referral, with counsel, including the
  position of individuals and the availability of indemnification and D&O cover.
- **Continuing obligations register.** Every entry from `Continuing Obligations`,
  consolidated with the Litigation settlement obligations, the Contracts survival
  terms, the Regulatory undertakings, and the Environmental controls, into one
  post-closing register with named owners.
- **Status verification.** Every row with a `[status over 18 months old]` flag,
  checked with the target's tax function. **An open examination reported from a
  two-year-old document may have produced an assessment nobody has produced.**

---

## Test set

- [ ] Tax sharing agreement among members of the seller's consolidated group
- [ ] Tax sharing agreement entirely within the acquired group
- [ ] Tax sharing agreement silent on a member leaving the group
- [ ] Tax sharing agreement terminating on departure with accrued rights preserved
- [ ] Tax sharing agreement expressly binding successors and assigns
- [ ] Tax indemnity from a prior acquisition of the target
- [ ] Tax indemnity with a claim period shorter than the limitation period
- [ ] Tax indemnity with the seller controlling pre-closing contests
- [ ] Unsigned tax sharing agreement
- [ ] Open federal income examination with no adjustment proposed
- [ ] Examination with scope expanded to further periods
- [ ] Proposed adjustment with the taxpayer response outstanding
- [ ] Proposed adjustment with issues partly conceded and partly contested
- [ ] Notice of deficiency unpaid with an appeal deadline stated
- [ ] Assessment paid with an appeal preserved by deposit
- [ ] Protest filed with an appeals function
- [ ] Closing agreement precluding reopening of the periods
- [ ] Agreed adjustment leaving the periods open
- [ ] Settlement requiring a corresponding state adjustment, not evidenced as made
- [ ] Settlement with an agreed treatment binding future periods
- [ ] Settlement with an instalment schedule outstanding
- [ ] Examination referred to a transfer pricing specialist function
- [ ] Matter referred to a criminal investigation function
- [ ] Matter with a mutual agreement procedure invoked under a treaty
- [ ] Federal adjustment with a state examination following
- [ ] Matter where escalation was threatened if a deadline was missed
- [ ] Matter where a proposed adjustment was withdrawn
- [ ] Matter whose latest document is three years old with no conclusion
- [ ] Matter referenced as settled with the closing agreement not produced
- [ ] Advance ruling with a validity period and a change-of-control condition
- [ ] Advance pricing agreement with a stated term
- [ ] Tax opinion at a "should" level with stated assumptions
- [ ] Tax opinion at a "more likely than not" level relied on for penalty protection
- [ ] Tax opinion addressed to the seller with third-party reliance excluded
- [ ] Tax opinion whose stated assumption has ceased to be true
- [ ] Voluntary disclosure for unfiled state returns
- [ ] Information request with no stated concern
- [ ] Matter naming an officer individually for unremitted payroll tax
- [ ] Matter open with the latest document an authority request and no response
- [ ] Matter file marked privileged and confidential
- [ ] Unit mistakenly containing two matters

Then test the dependencies: change `Matter Category` from
`Tax sharing or allocation agreement` to `Examination or audit` and confirm
`Allocation and Indemnity Terms` and `Reliance and Scope` move to
`Not applicable` while `Issues or Subject Matter` re-runs against the examination
rules and `Survival on Change of Control` follows its upstream. Change
`Issues or Subject Matter` to `Not stated` and confirm `Taxpayer Position` returns
`Unable to determine`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
