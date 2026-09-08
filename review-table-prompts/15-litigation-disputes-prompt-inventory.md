# Prompt Inventory — Litigation and Disputes

Table 15 of the POC.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Litigation`
- Review unit: **one dispute** — every pleading, order, judgment, award,
  correspondence, settlement document, and insurance notice produced for that
  dispute
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: litigation and corporate/M&A teams;
  feeds the disclosure schedule, the special indemnity and escrow analysis, the
  insurance cross-check, and the coverage register
- Inventory version: v1.0

### Why the matter is the row, and why this is a change

The original workbook was one row per document, with a Document Type column
classifying Complaint, Answer, and Motion. `review-tables.md` §8 specifies one row
per matter with pleadings collapsed, and it is right: the deal team asks what a
dispute is worth and where it stands, and neither question can be answered from a
single pleading.

**The two designs need different columns entirely.** Per-matter needs the target's
role, the procedural stage as at the latest document, settlement terms, and the
insurance position. Per-document can answer none of those. This inventory
implements per-matter.

### The three questions

1. **What is the exposure?** Amount claimed, unquantified relief, class status,
   and any dispositive ruling that has already narrowed or expanded it.
2. **Who pays?** Insurance tendered, the carrier's coverage position, and any
   reserve the documents disclose.
3. **What does the SPA have to say?** Disclosure schedule item, special indemnity
   candidate, escrow candidate — all human columns fed by the rest.

## Assumptions to confirm before running

1. One row is one dispute. Related matters between the same parties are separate
   rows unless consolidated, in which case the consolidation order determines the
   unit.
2. **Threatened disputes are rows.** A demand letter with no proceedings is a
   dispute, and it is often the most useful row in the table because it is the one
   the seller has not yet disclosed as litigation.
3. Regulatory enforcement is a Regulatory — Correspondence row, not a Litigation
   row, unless proceedings have been commenced in a court or tribunal.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

30 Harvey columns plus 10 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side litigation diligence on the target group listed below.

One row is one dispute: every pleading, order, judgment, award, correspondence, settlement document, and insurance notice produced for that dispute. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the dispute or the parties.
- **Report the position as at the most recently dated document in the unit, and identify that document.** A dispute moves, and a cell without a date is not usable.
- **A pleading states a party's allegations, not facts.** Report allegations as allegations. Do not describe a claim as established, and do not adopt either party's account.
- **Do not assess the merits, the likely outcome, the quantum of any exposure, or whether insurance responds.** All four are legal judgements and all four are human columns.
- Report figures only as the documents state them. Do not calculate, total, convert currency, or add interest.
- Use party names exactly as printed; do not shorten, expand, or correct them.
- **Do not report the names of individual claimants in a consumer, employment, or personal injury matter beyond what is necessary to identify the matter.** Report the matter name as captioned and describe the claimant by category.
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
  Matter Name
  Target Entity Party
  Adverse Party
  Forum
  Case Number
  Jurisdiction and Governing Law
  Commenced Date

Stage 2 — Parties and posture
  Target Entity Party ──→ Target's Role
  Adverse Party       ──→ Adverse Party Type
  Documents in Unit   ──→ Matter Status on Record
                          Referenced but Not Produced
  Matter Status on Record ──→ Status As-Of Date

Stage 3 — Claims and exposure
  Claims Asserted, Factual Subject, Class or Representative,
  Amount Claimed, Unquantified Relief, Counterclaims

Stage 4 — Procedure
  Procedural Stage, Next Deadline or Hearing, Trial or Hearing Date,
  Dispositive Rulings

Stage 5 — Resolution and recovery
  Settlement Terms  ──→ Release Scope
  Insurance Tendered ──→ Carrier and Coverage Position
  Reserve or Accrual Referenced

Stage 6 — Links
  Related Contract, Asset, or Property
  Litigation Hold and Preservation
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Matter Status on Record; Referenced but Not Produced | v1.0 | draft |
| 2 | Matter Name | Free Response | — | — | v1.0 | draft |
| 3 | Target Entity Party | Free Response | — | Target's Role | v1.0 | draft |
| 4 | Target's Role | Classify | @Target Entity Party | — | v1.0 | draft |
| 5 | Adverse Party | Free Response | — | Adverse Party Type | v1.0 | draft |
| 6 | Adverse Party Type | Classify | @Adverse Party | — | v1.0 | draft |
| 7 | Forum | Free Response | — | — | v1.0 | draft |
| 8 | Case Number | Free Response | — | — | v1.0 | draft |
| 9 | Jurisdiction and Governing Law | Free Response | — | — | v1.0 | draft |
| 10 | Commenced Date | Date | — | — | v1.0 | draft |
| 11 | Matter Status on Record | Classify | @Documents in Unit | Status As-Of Date | v1.0 | draft |
| 12 | Status As-Of Date | Date | @Matter Status on Record | — | v1.0 | draft |
| 13 | Claims Asserted | Free Response | — | — | v1.0 | draft |
| 14 | Factual Subject | Free Response | — | — | v1.0 | draft |
| 15 | Class or Representative | Classify | — | — | v1.0 | draft |
| 16 | Amount Claimed | Free Response | — | — | v1.0 | draft |
| 17 | Unquantified Relief | Free Response | — | — | v1.0 | draft |
| 18 | Counterclaims | Free Response | — | — | v1.0 | draft |
| 19 | Procedural Stage | Free Response | — | — | v1.0 | draft |
| 20 | Next Deadline or Hearing | Date | — | — | v1.0 | draft |
| 21 | Trial or Hearing Date | Date | — | — | v1.0 | draft |
| 22 | Dispositive Rulings | Free Response | — | — | v1.0 | draft |
| 23 | Settlement Terms | Free Response | — | Release Scope | v1.0 | draft |
| 24 | Release Scope | Free Response | @Settlement Terms | — | v1.0 | draft |
| 25 | Insurance Tendered | Classify | — | Carrier and Coverage Position | v1.0 | draft |
| 26 | Carrier and Coverage Position | Free Response | @Insurance Tendered | — | v1.0 | draft |
| 27 | Reserve or Accrual Referenced | Free Response | — | — | v1.0 | draft |
| 28 | Related Contract, Asset, or Property | Free Response | — | — | v1.0 | draft |
| 29 | Litigation Hold and Preservation | Classify | — | — | v1.0 | draft |
| 30 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Matter Status on Record`, `Referenced but Not Produced`
- Purpose: inventory the matter file in date order, which is also the chronology
  the reviewer reads the row against.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include demand and pre-action letters, complaints and petitions, answers, counterclaims, motions and responses, orders, judgments, arbitral awards, settlement agreements, releases, dismissal notices, discovery correspondence, insurance notices and coverage letters, and litigation hold notices.
- Treat exhibits attached to a pleading as part of that pleading.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title or caption description. Where none is printed, describe it in five words or fewer and add `(untitled)`.
- Give each document's own stated or filed date.
- State the function as one of `Demand letter`, `Complaint`, `Answer`, `Counterclaim`, `Motion`, `Response`, `Order`, `Judgment`, `Award`, `Settlement`, `Release`, `Dismissal`, `Discovery`, `Insurance notice`, `Coverage letter`, `Hold notice`, or `Other`.
- **Where a document relates to a different dispute than the subject of this row, still list it and append ` [relates to [matter]]`.** A unit mixing two disputes produces a merged row.
- Where the unit's most recent document is a pleading rather than an order, note that in the evidence field. It usually means the file has not been updated.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 25 lines and no more than 150 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Matter Name

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how the dispute is identified, which is the join key to the disclosure
  schedule, the insurance claim records, and the accounts.

```markdown
## Task

State the name or caption of this dispute.

## Rules

- Report the case caption exactly as printed, in the form the documents use.
- Where the dispute is threatened but not commenced, report the parties in the form `[Claimant] v. [Respondent] (threatened)`, using the names as printed.
- Where an arbitration has no caption, report the parties and the administering body's case reference.
- **Where the matter involves an individual claimant in an employment, consumer, or personal injury dispute, report the caption as printed but do not add personal details beyond it.**
- Where a matter has been consolidated, report the lead caption and note the consolidated matters in the evidence field.
- Where the documents use an internal matter reference or claim number, report it in addition to the caption.

## Fallback rules

- Return `Unable to determine` where the documents do not identify the dispute or its parties.

## Output format

`[Caption as printed][; internal reference: [as stated]]`. Return no more than 35 words.
```

---

### 3. Target Entity Party

- Native type: Free Response
- Upstream: none
- Downstream: `Target's Role`
- Purpose: which group entity is exposed. **Decisive in a carve-out**, where a
  dispute against an entity left behind may or may not follow the business.

```markdown
## Task

State the target-group entity or entities party to this dispute.

## Rules

- Use the review-subject list in the Table Instructions to determine which named parties are group entities.
- Report each name exactly as printed in the caption or the pleadings, including entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- Where more than one group entity is a party, list each on its own line.
- **Where a target entity is named as a party but the documents indicate it was dismissed, report it and append ` (dismissed [YYYY-MM-DD])`.**
- **Where no target entity is a party but the documents indicate a target entity is otherwise exposed** — as an indemnitor, a guarantor, an insured, a successor to a named party, or a party to be added — report the exposure and append ` (not a named party)`. This surfaces disputes that will not appear in a party search.
- Where a director, officer, or employee of a target entity is named individually, report the entity and note in the evidence field that an individual is named, since it engages the indemnification and D&O columns elsewhere.
- Where the entity named is not on the review-subject list, report the name and append ` (not a listed entity)`.

## Fallback rules

- Return `Not applicable — no target entity exposed` where the dispute does not involve the target group at all.
- Return `Unable to determine` where the parties cannot be identified.

## Output format

`[Exact legal name]` per line, with any qualifier appended. Return no more than 45 words.
```

---

### 4. Target's Role

- Native type: Classify
- Configured options, in UI order: `Defendant or respondent`, `Plaintiff or claimant`, `Both, with counterclaim`, `Third party or intervenor`, `Non-party with exposure`, `Appellant`, `Appellee`, `Unable to determine`
- Upstream: `@Target Entity Party`
- Downstream: none
- Purpose: which side the target is on. **Absent from the original schema, and it
  inverts the entire reading of every exposure column.**

```markdown
## Established result

- Target entity party: @Target Entity Party

Use this to identify whose role to classify. Confirm the role against the pleadings and orders in the unit.

## Task

Classify the target group's procedural role in this dispute. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Non-party with exposure`: no target entity is a named party, but a target entity is exposed as indemnitor, guarantor, insured, or successor. **Report the basis in the evidence field.**
2. `Both, with counterclaim`: a target entity is a defendant and has asserted a counterclaim, or is a claimant facing one. **The exposure runs both ways** and the amount columns must be read accordingly.
3. `Appellant`: the target has appealed an adverse decision. Note in the evidence field whether the judgment below is stayed, since an unstayed money judgment is immediately enforceable.
4. `Appellee`: the target won below and the other side has appealed.
5. `Third party or intervenor`: the target was joined as a third party, impleaded, or intervened.
6. `Plaintiff or claimant`: a target entity commenced the proceedings and asserts the claims. **This is a potential asset**, not a liability, and it should never be filtered together with defence matters.
7. `Defendant or respondent`: a target entity is defending.

Where different target entities hold different roles in the same dispute, classify on the role carrying the greater exposure and report the others in the evidence field.

Where the target is a nominal defendant only — a garnishee, a custodian, or a party joined for procedural reasons — classify as `Defendant or respondent` and note the nominal status in the evidence field.

## Fallback rules

- Use `Unable to determine` where the pleadings are absent and no order identifies the parties' roles.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Adverse Party

- Native type: Free Response
- Upstream: none
- Downstream: `Adverse Party Type`
- Purpose: who is on the other side, by exact name. The join key to the contracts,
  customer, and employment populations.

```markdown
## Task

State the party or parties adverse to the target group in this dispute.

## Rules

- Report each name exactly as printed, including entity suffix. Do not correct or expand.
- Where there are more than five adverse parties, report the first five as printed and end with `and [N] further parties`.
- **Where the adverse party is an individual in an employment, consumer, or personal injury matter, report the name as it appears in the caption and add the category in three words or fewer**, for example `(former employee)`. Do not add other personal details.
- **Where the adverse parties are a class or a group of similarly situated individuals, report the named representative and the class as described**, rather than listing individuals.
- Where the adverse party is a public body, regulator, or prosecutor, report it as named.
- Where the documents identify the adverse party's counsel, do not report it here.
- Where an adverse party has been dismissed, report it and append ` (dismissed [YYYY-MM-DD])`.

## Fallback rules

- Return `Unable to determine` where the adverse party cannot be identified from the documents.

## Output format

`[Exact name][ ([category])]` per line, with any qualifier appended. Return no more than 50 words.
```

---

### 6. Adverse Party Type

- Native type: Classify
- Configured options, in UI order: `Customer`, `Supplier or vendor`, `Current employee`, `Former employee`, `Competitor`, `Shareholder or investor`, `Landlord or tenant`, `Insurer`, `Regulator or public body`, `Consumer or class of consumers`, `IP rights holder`, `Other`, `Unable to determine`
- Upstream: `@Adverse Party`
- Downstream: none
- Purpose: the population the dispute comes from, which is what makes pattern
  detection possible and links the row to another workstream.

```markdown
## Established result

- Adverse party: @Adverse Party

Use this to identify the party being classified. Determine the relationship from the documents in the unit.

## Task

Classify the adverse party's relationship to the target group. Choose exactly one configured option.

## Classification rules

- Classify on the relationship the documents describe, not on the nature of the claim. A supplier suing for unpaid invoices is `Supplier or vendor`.
- `Former employee`: the documents describe employment that has ended. **Distinguished from `Current employee` because a claim by a serving employee is also a live retention and culture issue**, not only a legal one.
- `Consumer or class of consumers`: individual purchasers or users, whether or not a class has been certified.
- `Competitor`: a market rival, including in an IP, trade secret, or unfair competition dispute. Where the claim is IP infringement and the claimant is a non-competing rights holder or a licensing entity, use `IP rights holder`.
- `Shareholder or investor`: a holder or former holder of securities of a target entity, including in an appraisal or dissenters' rights proceeding.
- `Regulator or public body`: use only where proceedings have been commenced in a court or tribunal. **Regulator correspondence and enforcement short of proceedings belongs in the Regulatory — Correspondence table**, not here.

Where more than one type of adverse party is involved, classify on the party asserting the largest or most consequential claim and report the others in the evidence field.

## Fallback rules

- Use `Other` where the relationship is identifiable but none of the options describes it.
- Use `Unable to determine` where the documents do not describe the relationship.

## Output format

Return only the exact configured option and no explanation.
```

---

### 7. Forum

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the dispute is being heard, which drives cost, timetable, and
  the character of the exposure.

```markdown
## Task

State the court, tribunal, arbitral body, or forum in which this dispute is proceeding.

## Rules

- Report the forum exactly as printed, including the division, district, or chamber.
- **For an arbitration, report the administering body, the seat, and the rules applied where stated**, since an institutional arbitration under named rules is a very different proposition from an ad hoc one.
- Report the panel composition where stated — a single arbitrator or three.
- **Where the dispute is threatened and no forum has been engaged, return `None — threatened only`**, and report any forum the demand letter identifies as intended in the evidence field.
- Where the matter is before a mediator or in a court-ordered mediation, report the underlying forum and note the mediation.
- Where the matter has moved — removed, transferred, remanded, or appealed — report the current forum and append ` (from [prior forum], [YYYY-MM-DD])`.
- Do not report the governing law here; it has its own column.

## Fallback rules

- Return `Unable to determine` where no document identifies the forum.

## Output format

`[Forum as printed][; seat: [as stated]][; rules: [as stated]][; panel: [as stated]]`, with any qualifier appended.

Return no more than 40 words.
```

---

### 8. Case Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the docket reference, which is the key for verifying status
  independently against the court record.

```markdown
## Task

State the case, docket, or reference number for this dispute.

## Rules

- **Report the number exactly as printed, including any prefix, year, division code, slashes, and punctuation. Do not reformat.** Docket searches fail on reformatted numbers, and this cell is what a verification search is run from.
- Where the matter carries more than one number — a trial court number and an appellate number, or a consolidated lead number — report each and label it.
- Where an arbitration has an administering body reference, report it.
- Where a matter has been transferred and renumbered, report the current number and append ` (previously [number])`.
- Return `Not applicable — threatened only` where no proceedings have been commenced.

## Fallback rules

- Return `Not stated` where proceedings exist and no number appears in the documents.

## Output format

`[Label] [number]` per number, separated by semicolons. Return no more than 30 words.
```

---

### 9. Jurisdiction and Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the law applied and the basis of jurisdiction, which bear on both
  outcome and enforceability.

```markdown
## Task

Report the governing law applied to this dispute and the stated basis of the forum's jurisdiction.

## Rules

- Report the governing or substantive law as stated in the pleadings, an order, or a contractual choice-of-law provision the documents recite.
- Report the basis of jurisdiction where the documents state it — federal question, diversity, a contractual submission, an arbitration agreement, or the situs of the subject matter.
- **Report any pending or decided challenge to jurisdiction, venue, or arbitrability**, and its outcome where the documents show it. A successful challenge can end a dispute without touching the merits, and it is the cheapest possible outcome.
- Where the law of more than one jurisdiction is stated to apply to different claims, report each with the claim in four words or fewer.
- Where the dispute is threatened only, report any governing law the demand letter asserts.

## Fallback rules

- Return `Not stated` where the documents do not identify the governing law.
- Return `Unable to determine` where assertions conflict.

## Output format

`Governing law: [as stated]; jurisdictional basis: [as stated or "Not addressed"]; challenge: [brief and outcome, or "none"]`

Return no more than 50 words.
```

---

### 10. Commenced Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the dispute began, which drives limitation analysis and tells a
  reviewer how long the target has been carrying it.

```markdown
## Task

Identify the date this dispute was commenced.

## Date-selection hierarchy

1. Use the filing date stamped on the initiating pleading — complaint, petition, statement of claim, or request for arbitration.
2. If no stamp, use the date the initiating pleading states for itself.
3. If no proceedings have been commenced, use the date of the earliest demand or pre-action letter in the unit, and note in the evidence field that the date is of the demand rather than a filing.

## Excluded dates

- The date of service, where distinct from filing
- The date of the underlying events complained of. **Report that in the evidence field where the documents state it**, since the gap between the events and the filing is what a limitation argument turns on
- The date of an amended pleading, unless the amendment added the target as a party, in which case report the original commencement and note the joinder date
- The date of a litigation hold notice
- File name and metadata dates, and transmittal and scan dates

## Rules

- **Where the target was added by an amended pleading, report the original commencement date and append ` (target joined [YYYY-MM-DD])`.**
- Compare the commenced date to the diligence as-of date. **Where the dispute has been pending more than three years, append ` [pending over 3 years]`**, since a long-running matter usually means either a substantial dispute or a stalled one, and either is worth a look.

## Output format

`YYYY-MM-DD`, with any qualifier appended. Preserve partial precision as printed. Return `Not stated` where no commencement date can be selected.
```

---

### 11. Matter Status on Record

- Native type: Classify
- Configured options, in UI order: `Active`, `Stayed or suspended`, `Settled, terms performed`, `Settled, obligations continuing`, `Judgment or award entered`, `Dismissed with prejudice`, `Dismissed without prejudice`, `Threatened only`, `Abandoned or dormant`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Status As-Of Date`
- Purpose: where the dispute stands on the documents.

**Scope discipline.** This reports what the file shows as at its most recent
document. It does not report the current position, and the two are frequently
different because litigation files in data rooms are stale. `Status As-Of Date`
carries the caveat.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document. Confirm the status against that document.

## Task

Classify the status of this dispute as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Threatened only`: the unit contains a demand or pre-action letter and no evidence that proceedings were commenced.
2. `Dismissed with prejudice`: an order or stipulation dismissing the claims with prejudice, or a final judgment on the merits in the target's favour. **The best outcome and the only one that closes the matter.**
3. `Dismissed without prejudice`: dismissal that does not bar refiling. **This is not a resolution** — the claim can return, often within a limitation period the documents do not state, and it should never be filtered together with a dismissal with prejudice.
4. `Judgment or award entered`: a money judgment, declaratory judgment, or arbitral award has been entered. Note in the evidence field whether it is against the target or in its favour, whether it is final, and whether an appeal or a stay is recorded.
5. `Settled, obligations continuing`: a settlement is recorded and it imposes obligations extending beyond the date of the most recent document — instalment payments, ongoing covenants, injunctive undertakings, or reporting. **These follow the business to the buyer.**
6. `Settled, terms performed`: a settlement is recorded and the documents evidence full performance and release.
7. `Stayed or suspended`: proceedings are stayed, suspended, or abated by order or agreement, including a stay pending arbitration, appeal, or a related matter.
8. `Abandoned or dormant`: proceedings were commenced and the most recent document in the unit is more than two years before the diligence as-of date, with no disposition recorded. **Do not treat this as resolved** — it may simply mean the file was not produced in full.
9. `Active`: none of the above applies.

Where a settlement was agreed but the documents show it unsigned, classify as `Active` and note the unexecuted settlement in the evidence field. **An unsigned settlement resolves nothing.**

## Fallback rules

- Use `Unable to determine` where documents of the same date conflict about the status, or where the most recent document is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Status As-Of Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Matter Status on Record`
- Downstream: none
- Purpose: the date the status statement speaks as of. **Without it the status
  column is unusable**, because a litigation file in a data room is routinely
  months out of date.

```markdown
## Established result

- Matter status on record: @Matter Status on Record

## Task

Identify the date of the most recently dated document in the review unit, which is the date as of which the status is reported.

## Rules

- Report the date of the most recent document, whatever its function.
- **Prefer the most recent document that bears on the status** — an order, judgment, settlement, dismissal, or substantive pleading — over routine correspondence or a discovery document of a later date. Where a later routine document exists, report the substantive document's date and note the later document in the evidence field.
- Compare the reported date to the diligence as-of date in the Table Instructions and flag the gap:
  - more than three months: append ` [status over 3 months old]`
  - more than twelve months: append ` [status over 12 months old]`
- **Where Matter Status on Record is `Active` and the flag is `[status over 12 months old]`, the row needs verification against the court record before it can be relied on.** That combination is the most common reason a litigation schedule is wrong.

## Fallback rules

- Return `Not stated` where no document in the unit bears a date.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended.
```

---

### 13. Claims Asserted

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the causes of action, which is what pattern detection across the table
  is run on.

```markdown
## Task

Report the claims or causes of action asserted against, and by, the target group.

## Rules

- **Report claims asserted against the target separately from claims asserted by it**, labelling each. Counterclaims are reported in their own column, but a target that is a plaintiff has claims of its own and they belong here.
- Report each claim by its legal label as pleaded, in five words or fewer — breach of contract, negligence, wrongful termination, discrimination, patent infringement, trade secret misappropriation, unfair competition, breach of fiduciary duty, unjust enrichment, statutory claim under a named statute.
- **Where a claim is brought under a statute, name the statute as printed.** A statutory claim may carry fee-shifting, statutory or treble damages, or personal liability, and the statute is the only way to know.
- Report no more than eight claims per direction. Where more are pleaded, report the eight with the widest exposure and append ` and [N] further claims`.
- Report any claim the documents show as dismissed, withdrawn, or struck, and append ` (dismissed [YYYY-MM-DD])`. **A narrowed pleading is a materially different exposure from the one originally filed.**
- **Report claims as pleaded. Do not assess their merit, their strength, or whether they are properly pleaded.**

## Fallback rules

- Return `Not stated` where the documents describe a dispute without identifying causes of action, which is common where only a demand letter is present.
- Return `Unable to determine` where the pleadings are absent or illegible.

## Output format

`Against target: [claims]` and, where applicable, `By target: [claims]`, with any dismissal qualifiers appended.

Return no more than 80 words.
```

---

### 14. Factual Subject

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the dispute is actually about, in enough detail for a reviewer to
  recognise a pattern or a link to another workstream.

```markdown
## Task

Describe the subject matter of this dispute in two sentences or fewer.

## Rules

- **Describe the allegations neutrally, as allegations.** Use language such as `alleges`, `claims`, or `asserts`. Do not adopt either party's account and do not describe alleged conduct as having occurred.
- Identify what happened, when the events are said to have occurred, and what the target is said to have done or failed to do.
- **Report the period the events span where the documents state it**, since a single incident and a course of conduct over four years are very different exposures.
- Name the product, service, contract, site, or business line involved, so the row can be linked to the commercial workstream.
- Do not name individual employees or claimants. Describe them by role or category.
- Do not summarise the procedural history; that is in Procedural Stage.
- **Do not assess the merits, apportion fault, or state what a court is likely to find.**

## Fallback rules

- Return `Unable to determine` where the documents do not describe the underlying dispute.

## Output format

Two sentences or fewer, no more than 60 words. Do not include quotations, section numbers, or citation markers.
```

---

### 15. Class or Representative

- Native type: Classify
- Configured options, in UI order: `Individual claim`, `Putative class, not certified`, `Class certified`, `Class certification denied`, `Collective or opt-in action`, `Representative or derivative action`, `Multiple individual claims, coordinated`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the exposure is one claim or thousands. **Changes the number by
  orders of magnitude**, and certification is the single largest inflection point
  in any dispute.

```markdown
## Task

Classify the aggregate character of this dispute. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Class certified`: a court has certified a class, in whole or in part. **This is the most consequential state in the table**, because certification converts an individual dispute into an aggregate one and usually drives settlement.
2. `Class certification denied`: certification has been sought and refused. Note in the evidence field whether an appeal of that ruling is recorded, since the position is not final.
3. `Putative class, not certified`: the pleading asserts class claims and no certification ruling appears in the unit. **The pleaded class is the claimant's assertion, not an established fact**, and the amount claimed should be read with that in mind.
4. `Collective or opt-in action`: an action proceeding on an opt-in basis, common in wage and hour claims. Report any stated number of opt-in participants in the evidence field.
5. `Representative or derivative action`: a claim brought on behalf of an entity or a wider group by a representative claimant, including a shareholder derivative claim.
6. `Multiple individual claims, coordinated`: separate individual claims consolidated, coordinated, or managed together without class treatment.
7. `Individual claim`: a single claimant or a small group of named claimants suing on their own behalf.

Report in the evidence field the class as defined or proposed, and any stated class size or number of claimants. **Report those figures exactly as stated and do not estimate a class size.**

## Fallback rules

- Use `Unable to determine` where the pleadings are absent, or where the aggregate character cannot be established.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Amount Claimed

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the monetary exposure as the documents state it, reported so a human can
  assess it. **The amount claimed is not the exposure**, and the column is
  designed to make that visible rather than to hide it.

```markdown
## Task

Report the monetary amounts claimed in this dispute, and by whom.

## Rules

- **Report each amount with its source and its basis**: the amount pleaded in the complaint, the amount demanded in a letter, the amount awarded in a judgment, the amount agreed in a settlement, or the amount stated in a coverage notice. These are very different figures and reporting them without labels is misleading.
- Report amounts claimed **against** the target separately from amounts claimed **by** it.
- Report the components as stated where the documents break them down: compensatory, consequential, statutory, punitive or exemplary, interest, and costs or fees.
- **Report any claim for statutory, multiplied, or treble damages, and any fee-shifting claim, separately and prominently.** A modest compensatory claim under a fee-shifting statute can produce an exposure many times the principal, and it will not be visible from the headline figure.
- **Where a pleading claims an unspecified amount, or an amount "to be proven at trial", say so** rather than returning nothing.
- **Do not calculate.** Do not total the components, do not sum across claimants, do not add interest, do not convert currency, and **do not multiply a per-claimant figure by a class size**. Every one of those is an exposure estimate and it belongs to the human column.
- Where an amount claimed was later reduced by amendment or by a ruling, report the current figure and append ` (reduced from [figure], [YYYY-MM-DD])`.

## Fallback rules

- Return `Unquantified` where the documents claim monetary relief without stating an amount. **This is common and it is not a gap in the extraction.**
- Return `Not applicable` where no monetary relief is sought.
- Return `Unable to determine` where amounts stated in documents of the same date conflict.

## Output format

One line per amount:

`[Against target | By target] — [figure] [currency] — [basis] — per [document title], [YYYY-MM-DD]`

Return no more than 6 lines and no more than 90 words. Do not include any figure you calculated.
```

---

### 17. Unquantified Relief

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the relief that has no number. **Frequently the more serious exposure**,
  because an injunction can stop the business doing something it needs to do and no
  amount of money resolves it.

```markdown
## Task

Report the non-monetary relief sought or granted in this dispute.

## Include where expressly stated

- Injunctive relief, whether interim, preliminary, or permanent, and what it would require or prohibit
- Specific performance, rescission, or reformation of a contract
- Declaratory relief, and what it would declare
- **Any relief affecting the target's ability to sell, use, or license a product, service, or asset** — a product recall, a withdrawal, a delisting, or an order to cease a use
- Any relief affecting employment or personnel, including reinstatement
- Any order for an accounting, disgorgement, or constructive trust
- Any request for the appointment of a receiver, monitor, or examiner
- Any winding-up, dissolution, or appraisal remedy
- Whether any interim or preliminary relief has been granted, refused, or is pending, with dates

## Rules

- **Report interim relief already granted separately and prominently.** An existing injunction is a present constraint on the business, not a contingent risk, and it is the kind of thing a buyer must know before signing.
- Report what the relief would actually require the target to do or stop doing, in eight words or fewer per item.
- Report any undertaking the target has given to a court or to the other side, since undertakings bind and they survive closing.
- **Do not assess the likelihood of any relief being granted, and do not estimate its business impact.**

## Fallback rules

- Return exactly `None sought` where only monetary relief is sought.
- Return `Unable to determine` where the relief sought cannot be identified.

## Output format

One line per item:

`[Relief] — [what it requires or prohibits] — [sought | granted [YYYY-MM-DD] | refused | pending]`

Return no more than 6 lines and no more than 85 words.
```

---

### 18. Counterclaims

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: claims running the other way, which offset the exposure or create one.

```markdown
## Task

Report any counterclaim, cross-claim, third-party claim, or set-off asserted in this dispute.

## Rules

- **Report who asserts each counterclaim and against whom.** A counterclaim by the target reduces or reverses the exposure; a counterclaim against the target adds to it, and the direction is the whole point.
- Report the claims by legal label, in five words or fewer each.
- Report any amount claimed, with the currency, as stated. Do not net it against the principal claim and do not calculate a balance.
- Report any third-party claim by which the target seeks to pass liability to a supplier, contractor, insurer, or indemnitor. **This is a recovery route and it belongs alongside the insurance columns.**
- Report any set-off asserted, and whether the documents show it as allowed or disputed.
- Report the status of each counterclaim where the documents show it — pending, dismissed, or determined.
- Do not assess the merit of any counterclaim.

## Fallback rules

- Return exactly `None` where no counterclaim, cross-claim, or third-party claim is asserted.
- Return `Unable to determine` where the pleadings are absent or illegible.

## Output format

One line per claim:

`[Asserted by] against [party] — [claims] — [amount or "unquantified"] — [status]`

Return no more than 5 lines and no more than 80 words.
```

---

### 19. Procedural Stage

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how far the dispute has progressed, which drives both cost to
  completion and how much is known about the merits.

```markdown
## Task

Report the procedural stage of this dispute as at the most recently dated document in the unit.

## Include where expressly stated

- The stage reached: pre-action, pleadings, motions, discovery or disclosure, expert phase, pre-trial, trial, post-trial, or appeal
- **Whether discovery has begun, is substantially complete, or is closed.** Discovery status is the best available proxy for how much either side actually knows, and it drives cost to completion more than anything else
- Whether depositions or witness statements have been taken or exchanged
- Whether expert reports have been served
- Any dispositive motion pending, and what it seeks
- Any mediation or settlement conference held or scheduled, and its outcome where stated
- Any case management order and the schedule it sets
- Any appeal pending, and at what stage
- Any stay in place and its basis

## Rules

- **Identify the document the stage statement comes from and its date.** The stage as at a two-year-old pleading is not the stage today.
- Report the stage as the documents describe it. Do not infer a stage from the elapsed time or the volume of documents.
- Report any pending dispositive motion prominently, since its outcome can end the matter.
- Report any mediation outcome as stated, including an impasse.
- Do not estimate remaining cost, duration, or the likely outcome.

## Fallback rules

- Return `Not applicable — threatened only` where no proceedings have been commenced.
- Return `Not stated` where proceedings exist and the documents do not indicate the stage.
- Return `Unable to determine` where documents conflict about the stage.

## Output format

`Stage: [as stated]; discovery: [as stated]; dispositive motion pending: [brief or "none"]; mediation: [brief or "none"]; stay: [brief or "none"] — per [document title], [YYYY-MM-DD]`

Return no more than 75 words.
```

---

### 20. Next Deadline or Hearing

- Native type: Date — confirm the type accepts `Not stated` and `Not applicable`
- Upstream: none
- Downstream: none
- Purpose: the next thing that has to happen. **A deadline falling in the deal
  period is a task with an owner**, and a deadline that has already passed with no
  evidence of action is a finding.

```markdown
## Task

Identify the next deadline, hearing, or required step in this dispute after the diligence as-of date.

## Rules

- Report the earliest such date the documents state, with what it is for in five words or fewer.
- Include response and answer deadlines, discovery cut-offs, expert deadlines, motion hearings, case management conferences, mediation dates, appeal deadlines, and settlement instalment dates.
- **Where a deadline stated in the documents falls before the diligence as-of date and no document shows it was met, report that date and append ` [deadline passed, no action evidenced]`.** A missed response deadline can mean a default judgment, and it is the highest-consequence thing this column can find.
- Report only dates the documents state. **Do not calculate a deadline from a rule, a period, or the date of a pleading**, even where the applicable period is standard.
- Where several dates are stated, report the earliest after the as-of date and note the count of later dates in the evidence field.
- Where the matter is stayed, report `Not applicable — stayed` and note any review date.

## Fallback rules

- Return `Not applicable` where the matter is resolved and no continuing obligation has a date.
- Return `Not stated` where the matter is live and the documents state no forward date. **This is common in a stale file** and it pairs with the Status As-Of Date flag.

## Output format

`YYYY-MM-DD — [what it is for]`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 21. Trial or Hearing Date

- Native type: Date — confirm the type accepts `Not stated` and `Not applicable`
- Upstream: none
- Downstream: none
- Purpose: the date the matter is set for determination, which is the single most
  useful timetable fact for a buyer. **A trial date inside the first year
  post-closing changes how the matter is priced.**

```markdown
## Task

Identify the date this dispute is set for trial, final hearing, or arbitral hearing.

## Rules

- Report the date as stated in a scheduling order, case management order, notice of trial, or hearing notice.
- **State whether the date is firm, provisional, or a trial window**, as the documents describe it. A provisional date is routinely moved and should not be relied on.
- Where a window or period is set rather than a single date, report the start of the window and note the period in the evidence field.
- Where a previously set date has been vacated or adjourned, report the current date and append ` (adjourned from [date])`. **Repeated adjournments are worth noting** and belong in the evidence field.
- **Do not estimate a trial date from the procedural stage or from typical timetables.**
- Compare the date to the diligence as-of date. Where it falls within twelve months after it, append ` [within 12 months]`.

## Fallback rules

- Return `Not applicable` where the matter is resolved, dismissed, or threatened only.
- Return `Not stated` where the matter is live and no trial or hearing date has been set on the documents. **This is the normal position in the early stages** and it is not a gap.

## Output format

`YYYY-MM-DD — [firm | provisional | window]`, with any qualifier or flag appended, or one of the exact fallback values above.
```

---

### 22. Dispositive Rulings

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what has already been decided. **The most reliable evidence of a
  dispute's real shape**, because a ruling is a court's view rather than a party's
  assertion, and it usually narrows or confirms the exposure.

```markdown
## Task

Report every order or ruling in this dispute that determined an issue, narrowed the claims, or established a party's position.

## Include where expressly stated

- Rulings on motions to dismiss or strike, in whole or in part, and which claims survived
- Summary judgment rulings, and on which claims or issues
- **Class certification rulings, granted or denied**
- Rulings on jurisdiction, venue, arbitrability, or standing
- Rulings on limitation or time bar
- Rulings admitting or excluding expert evidence, where they bear on a claim's viability
- Sanctions, adverse inference rulings, or findings of spoliation
- Default judgments, and any order setting one aside
- Interim or preliminary injunctions granted or refused
- Findings of liability with quantum to be determined
- Any appellate ruling and its effect

## Rules

- **Report what each ruling decided and its effect on the claims, with its date.** A partial dismissal that removed the statutory claims from a case is the single most useful fact about that case, and it is invisible from the original pleading.
- **Report any sanctions or spoliation finding prominently.** Beyond its own consequence, it bears on how the target has conducted the litigation and on what a court will infer.
- Report any finding of liability separately from any determination of quantum, since a matter can be lost on liability with the number still open.
- Report the ruling as recorded. **Do not interpret its wider effect, do not predict what follows from it, and do not assess whether it was correct.**

## Fallback rules

- Return exactly `None in unit` where no dispositive ruling appears.

Note: this is a positive finding, not a fallback state. **It means none was produced**, which for a matter pending several years is itself worth asking about.

- Return `Not applicable` where the dispute is threatened only.
- Return `Unable to determine` where orders are illegible or their effect cannot be read.

## Output format

One line per ruling:

`[YYYY-MM-DD] — [ruling] — [effect on claims]`

Return no more than 8 lines and no more than 100 words.
```

---

### 23. Settlement Terms

- Native type: Free Response
- Upstream: none
- Downstream: `Release Scope`
- Purpose: what a settlement actually commits the business to. **The payment is
  usually the least important part**; the continuing obligations are what the buyer
  inherits.

```markdown
## Task

Report the terms of any settlement, compromise, or resolution agreement in this review unit.

## Include where expressly stated

- The payment amount, the payer, and the payment schedule, including any instalments still to fall due
- **Any obligation continuing after the settlement date**: covenants not to compete or solicit, licensing or royalty obligations, product changes, process or policy changes, reporting or monitoring, or an obligation to cooperate
- Any injunctive or behavioural undertaking given
- **Any confidentiality or non-disparagement obligation, and any carve-out permitting disclosure to a purchaser or a lender.** Where none exists, disclosing the settlement in diligence may itself breach it
- Any admission or express denial of liability
- Any most-favoured-settlement or parity provision
- Any provision on costs and fees
- Any condition precedent to the settlement taking effect, and whether the documents show it satisfied
- Whether the settlement is court-approved where approval is required, and whether approval has been given
- Whether the settlement document is signed by all parties

## Rules

- **Report every continuing obligation, with its duration.** These are the terms that follow the business to the buyer and they are routinely missed because the row looks closed.
- **Report whether the settlement is executed and, where required, approved.** An unsigned or unapproved settlement resolves nothing.
- **Report any instalment still outstanding as at the diligence as-of date**, with the remaining schedule as stated. Do not total the remaining payments.
- Report amounts as stated. Do not calculate.
- Do not assess whether the settlement was favourable.

## Fallback rules

- Return exactly `Not settled` where the unit contains no settlement document.
- Return `Referenced but not produced` where a settlement is referenced and the document is absent. **A settled matter whose settlement agreement was not produced is a significant coverage gap**, because the continuing obligations cannot be read.
- Return `Unable to determine` where settlement terms conflict or are illegible.

## Output format

`Payment: [amount, payer, schedule]; outstanding: [as stated or "none"]; continuing obligations: [list with durations]; confidentiality: [brief]; admission: [as stated]; executed: [yes | no]; approval: [as stated or "not required"]`

Return no more than 110 words.
```

---

### 24. Release Scope

- Native type: Free Response
- Upstream: `@Settlement Terms`
- Downstream: none
- Purpose: what the settlement actually resolved. **A narrow release leaves live
  exposure**, and it is the difference between a matter that is closed and one that
  merely looks closed.

```markdown
## Established result

- Settlement terms: @Settlement Terms

## Task

If Settlement Terms reported a settlement, report the scope of the release given.

If it returned `Not settled`, return exactly `Not applicable`.

If it returned `Referenced but not produced`, return `Unable to determine — settlement document not produced`.

If it returned `Unable to determine`, return exactly `Unable to determine — upstream settlement terms unresolved`.

## Include where expressly stated

- **Who is released**: the named party only, or also its affiliates, subsidiaries, parents, officers, directors, employees, insurers, successors, and assigns
- Whether the release extends to a purchaser or successor of the business
- **What is released**: the pleaded claims only, all claims arising from the described events, or all claims of any kind whether known or unknown
- Whether the release covers unknown or future claims, and whether any statutory waiver of unknown claims is given
- The temporal cut-off: claims arising up to the settlement date, up to a stated date, or without limit
- Any claim expressly carved out of the release
- Whether the release is mutual
- Any covenant not to sue, distinct from the release
- Whether dismissal is with prejudice

## Rules

- **Report whether the release covers the target's affiliates and successors.** A release naming only the defendant entity leaves affiliates exposed, and a release that does not extend to a successor may not protect the buyer at all.
- **Report whether unknown claims are released.** A release limited to pleaded claims leaves everything else arising from the same events live, which is the most common way a settled matter is not settled.
- Report any carve-out, since a carve-out is by definition the part that was not resolved.
- Report the scope as stated. **Do not assess whether the release would be effective against any particular claim.**

## Output format

`Released parties: [as stated]; extends to successors: [yes | no | Not addressed]; claims released: [as stated]; unknown claims: [released | not released | Not addressed]; cut-off: [as stated]; carve-outs: [brief or "none"]; mutual: [yes | no]`

Return no more than 90 words.
```

---

### 25. Insurance Tendered

- Native type: Classify
- Configured options, in UI order: `Tendered and accepted`, `Tendered, defence under reservation of rights`, `Tendered, coverage disputed`, `Tendered, coverage denied`, `Tendered, position not stated`, `Not tendered`, `No coverage identified`, `Unable to determine`
- Upstream: none
- Downstream: `Carrier and Coverage Position`
- Purpose: whether someone other than the business is paying. **The difference
  between a covered and an uncovered matter is often the whole exposure**, and a
  matter never tendered may have lost coverage for late notice.

```markdown
## Task

Classify the insurance position for this dispute as the documents show it. Choose exactly one configured option.

## Scope

- Consider claim notices, tender letters, acknowledgements, reservation of rights letters, coverage position letters, denials, and any reference to a carrier or a claim number.
- Consider coverage under any policy: general liability, professional or errors and omissions, directors and officers, employment practices, cyber, or product liability.
- Exclude the target's indemnity claims against contractual counterparties, which are reported in Counterclaims.

## Classification rules

Apply the first rule that fits.

1. `Tendered, coverage denied`: a carrier has declined coverage. Report the stated grounds in the next column.
2. `Tendered, coverage disputed`: the carrier disputes coverage in whole or in part without a final denial, or the documents show a dispute in progress.
3. `Tendered, defence under reservation of rights`: the carrier is defending while reserving the right to deny indemnity later. **This is not the same as accepted coverage** — the defence costs are being met and the indemnity remains open — and the two should never be filtered together.
4. `Tendered and accepted`: the carrier has confirmed coverage without material reservation.
5. `Tendered, position not stated`: notice was given and the documents record no response.
6. `Not tendered`: a policy that might respond is identified or referenced and the documents show no notice given. **Late notice can forfeit coverage entirely**, and this is the most actionable state in the column.
7. `No coverage identified`: the documents identify no policy that might respond.

## Fallback rules

- Use `Unable to determine` where the documents refer to insurance in terms too incomplete to establish the position.

## Output format

Return only the exact configured option and no explanation.
```

---

### 26. Carrier and Coverage Position

- Native type: Free Response
- Upstream: `@Insurance Tendered`
- Downstream: none
- Purpose: the detail behind the classification, and the join key to the Insurance
  table.

```markdown
## Established result

- Insurance tendered: @Insurance Tendered

## Task

If Insurance Tendered is any value other than `No coverage identified` or `Unable to determine`, report the carrier and the coverage particulars.

If it is `No coverage identified`, return exactly `Not applicable`.

If it is `Unable to determine`, return exactly `Unable to determine — upstream position unresolved`.

## Include where expressly stated

- The carrier's exact name, the policy number, and the policy period
- The coverage line — general liability, professional, directors and officers, employment practices, cyber, product
- The claim or reference number the carrier has assigned
- The date notice was given, and the date of any carrier response
- **The grounds of any denial, dispute, or reservation, as stated by the carrier** — late notice, a policy exclusion, a prior-acts limitation, the claims-made trigger, or the absence of an occurrence within the period
- Any deductible, self-insured retention, or co-insurance stated
- Whether defence costs are stated to erode the limit
- Any allocation between covered and uncovered claims
- Any reference to excess or umbrella layers, and whether they have been notified
- Any appointment of defence counsel by the carrier

## Rules

- **Report the stated grounds of any denial or reservation verbatim in substance, in ten words or fewer.** The ground determines whether the position is arguable and it is what coverage counsel needs.
- **Report whether excess layers have been notified where the claim could reach them.** Failure to notify an excess carrier is a common and avoidable forfeiture.
- Report the carrier and policy number exactly, since they are the join key to the Insurance table.
- Report the position as stated. **Do not assess whether coverage responds or whether a denial is well founded.**

## Output format

`Carrier: [name]; policy: [number], [period]; line: [as stated]; notice given: [YYYY-MM-DD]; position: [as stated] — grounds: [brief]; retention: [as stated]; defence costs erode limit: [yes | no | Not addressed]; excess notified: [yes | no | Not applicable]`

Return no more than 90 words.
```

---

### 27. Reserve or Accrual Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any figure the target itself has put on the matter. **The target's own
  reserve is the most informative number in the row**, because it reflects what
  the people closest to the dispute actually expect.

```markdown
## Task

Report any reserve, accrual, provision, or internal estimate for this dispute that the documents in this unit state.

## Scope

- Include reserves or accruals stated in the documents, in correspondence with auditors, in a litigation status report, or in a management summary.
- Include any range of reasonably possible loss stated.
- Include any statement that no reserve has been taken, and any stated reason.
- Include any figure the target has offered in settlement negotiations, where the documents disclose it.
- Include any carrier's reserve where the documents state it.
- Exclude the amount claimed by the other side, which has its own column.

## Rules

- Report each figure with its source, its date, and what it purports to measure.
- **Report any statement that a loss is probable, reasonably possible, or remote, using the documents' own words.** Those characterisations are accounting conclusions with defined meanings and they should not be paraphrased.
- **Report any statement that no reserve was taken and why**, since it is as informative as a figure.
- Report figures as stated. **Do not calculate, total across matters, or reconcile against the accounts.**
- **Be aware that a document containing a litigation reserve or an audit response may be privileged.** Report the figure as stated and note any privilege marking in the evidence field; do not assess privilege.

## Fallback rules

- Return exactly `None stated` where the documents state no reserve, accrual, or estimate. **This is the expected answer for most rows**, since reserves usually sit in the financial workstream rather than the litigation file.
- Return `Unable to determine` where figures conflict or are illegible.

## Output format

One line per figure:

`[Figure] [currency] — [what it measures] — [characterisation as stated] — per [document title], [YYYY-MM-DD]`

Return no more than 4 lines and no more than 70 words.
```

---

### 28. Related Contract, Asset, or Property

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the dispute concerns, so the row links to the workstream that
  holds the underlying document. **A pattern of disputes under one contract form is
  a drafting finding, not a litigation finding.**

```markdown
## Task

Report any contract, intellectual property asset, property, product, or business line this dispute concerns.

## Scope

- Include any agreement the dispute arises under or concerns, named as the documents name it, with its date and counterparty where stated.
- Include any IP asset, registration, or application in issue, with its number where stated.
- Include any real property in issue, with its address.
- Include any product, service, or product line in issue.
- Include any employment or consulting relationship in issue, described by role rather than by name.
- Include any securities issuance, transaction, or corporate action in issue.
- Include any regulatory licence or permit in issue.

## Rules

- **Name each item as the documents name it**, so the row can be joined to the Contracts, IP, Real Estate, Employment, or Regulatory table.
- **Where the dispute concerns a standard form, template, or terms of business rather than a negotiated agreement, say so.** A claim under a standard customer form implies exposure across every customer on that form, and that is the finding rather than the single dispute.
- Where the dispute concerns a category rather than an identified item — a product range, a class of employees, a group of sites — describe the category as stated.
- Do not identify individuals by name.
- Do not assess the wider exposure or count the affected population.

## Fallback rules

- Return exactly `None identified` where the dispute concerns no identifiable contract, asset, or property.
- Return `Unable to determine` where the subject cannot be identified.

## Output format

One line per item:

`[Type] — [name or identifier as stated][; standard form]`

Return no more than 6 lines and no more than 75 words.
```

---

### 29. Litigation Hold and Preservation

- Native type: Classify
- Configured options, in UI order: `Hold notice in unit`, `Hold referenced, notice not produced`, `Preservation obligation referenced, no hold evidenced`, `Spoliation alleged or found`, `No hold evidenced`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether evidence was preserved. **A preservation failure creates
  exposure independent of the merits**, through sanctions and adverse inferences,
  and it is a live obligation the buyer inherits along with the matter.

```markdown
## Task

Classify what the documents show about preservation of evidence in this dispute. Choose exactly one configured option.

## Scope

- Consider litigation hold notices, preservation letters received from the other side, discovery correspondence about preservation, and any allegation or finding of spoliation.
- Consider any statement that documents were deleted, systems were decommissioned, or a retention policy continued to operate after the dispute arose.

## Classification rules

Apply the first rule that fits.

1. `Spoliation alleged or found`: the documents record an allegation of spoliation, a motion for sanctions on preservation grounds, or a finding or sanction. **This is a substantive exposure in its own right** and it also appears in Dispositive Rulings.
2. `Hold notice in unit`: a litigation hold or preservation notice issued by the target is present. Note in the evidence field its date and whether it identifies custodians and data sources.
3. `Hold referenced, notice not produced`: the documents refer to a hold having been issued and the notice is not present.
4. `Preservation obligation referenced, no hold evidenced`: the target has received a preservation demand from the other side, or the documents otherwise show the obligation arose, and nothing evidences a hold being issued. **The gap between the two is where preservation failures happen.**
5. `No hold evidenced`: proceedings or a credible threat exist and the documents show nothing about preservation.
6. `Not applicable`: the matter is fully resolved with obligations performed, so preservation is no longer live.

**Where a hold notice is present, compare its date to the Commenced Date and to the date of any earlier demand letter in the unit.** Where the hold postdates the earliest indication of a dispute by more than sixty days, note the gap in the evidence field.

## Fallback rules

- Use `Unable to determine` where references to preservation are too incomplete to classify.

## Output format

Return only the exact configured option and no explanation.
```

---

### 30. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this matter file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this dispute that the documents in this unit refer to and that is not present.

## Scope

- **Include the initiating pleading where it is absent**, and any answer, counterclaim, or amended pleading referenced.
- **Include any order, judgment, or award referenced but not produced.** An order changes the matter's shape and its absence means the row may be wrong.
- **Include any settlement agreement or release referenced but not produced.**
- Include expert reports, witness statements, and depositions referenced.
- Include insurance policies, claim notices, and coverage letters referenced.
- Include any litigation hold notice referenced.
- Include the contract, licence, or instrument the dispute arises under, where referenced and not produced.
- Include any related or consolidated matter's documents referenced.
- Include any appellate brief or notice of appeal referenced.
- Include any tolling agreement, standstill, or limitation waiver referenced.
- Exclude statutes, regulations, procedural rules, and case authorities cited.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where an order, judgment, or award is referenced and absent, add `; disposition not readable`.** These should be filtered first, because the status of the matter cannot be confirmed without them.
- **Where a settlement agreement is referenced and absent, add `; continuing obligations unknown`.**
- Where an insurance policy or coverage letter is referenced and absent, add `; coverage position unknown`.
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
| **Status verified against court record** | Yes (date) / No / Not required |
| **Exposure estimate** | Free text |
| **Outcome assessment** | Free text |
| **Coverage assessment** | Responds / Partial / Does not respond / Unassessed |
| **Disclosure schedule item** | Yes / No |
| **Special indemnity candidate** | Yes / No |
| **Escrow candidate** | Yes / No |
| **Continuing obligations post-closing** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: target's role, status, amount claimed,
class status, settlement terms, insurance position.

### Reconciliation work that never belongs in a column

- **Status verification.** Every material row with a `[status over 12 months old]`
  flag, checked against the live court or tribunal record. **A litigation schedule
  built from a stale data room is wrong**, and this is the cheapest correction
  available.
- **Exposure quantification.** All of it. Amounts claimed, class sizes,
  fee-shifting multipliers, and reserve figures exported and assessed by
  litigation counsel. **No column multiplies a per-claimant figure by a class
  size**, and none should.
- **Pattern detection.** Read across rows for recurring claim types, adverse party
  types, products, and contract forms. **A pattern indicates systemic conduct
  rather than isolated disputes**, and it is a different and larger finding. The
  answer is narrative and does not fit a grid — ask Assistant over the project.
- **Litigation against contracts.** Every `[standard form]` flag from
  `Related Contract, Asset, or Property`, matched to the Contracts tables. A claim
  under a standard customer form implies exposure across the whole customer base.
- **Insurance cross-check.** Every row's carrier and policy against the Insurance
  table. **Filter `Insurance Tendered` to `Not tendered` first** — untendered
  matters may still be notifiable, and late notice forfeits coverage. Then check
  every claims-made policy row for whether the tail was or can be bought.
- **Uninsured material exposure.** Rows where coverage is denied, disputed, or
  absent, against the risk allocation discussion. These are the special indemnity
  and escrow candidates.
- **Continuing settlement obligations.** Every `Settled, obligations continuing`
  row, extracted into the post-closing obligations register alongside the
  Contracts survival terms.
- **Chronology.** For any material matter, build the event timeline by hand from
  the dated documents. `Documents in Unit` is already in date order and is the
  starting point.
- **Threatened matters.** Filter `Matter Status on Record` to `Threatened only`
  and check each against the seller's disclosed litigation list. **A demand letter
  the seller has not disclosed as litigation is the most useful row in the table.**

---

## Test set

- [ ] Active commercial dispute with pleadings, orders, and correspondence
- [ ] Matter where the target is plaintiff
- [ ] Matter where the target is defendant with a counterclaim
- [ ] Matter where the target is a non-party but indemnifies a named defendant
- [ ] Matter where a director is named individually alongside the entity
- [ ] Matter on appeal by the target, with an unstayed judgment below
- [ ] Threatened dispute with a demand letter and no proceedings
- [ ] Putative class action, no certification ruling
- [ ] Class action with certification granted
- [ ] Class action with certification denied and an appeal pending
- [ ] Wage and hour collective action with stated opt-in numbers
- [ ] Shareholder derivative claim
- [ ] Matter with a partial dismissal removing the statutory claims
- [ ] Matter with summary judgment granted in part
- [ ] Matter with a spoliation sanction
- [ ] Matter with a default judgment and an order setting it aside
- [ ] Matter with a preliminary injunction in force against the target
- [ ] Matter seeking a product recall
- [ ] Matter claiming treble damages and attorneys' fees under a named statute
- [ ] Matter claiming an unspecified amount to be proven at trial
- [ ] Matter with an amount claimed reduced by amendment
- [ ] Settled matter with instalments still outstanding
- [ ] Settled matter with continuing licensing obligations
- [ ] Settled matter with a release limited to pleaded claims only
- [ ] Settled matter with a release extending to affiliates and successors
- [ ] Settled matter with confidentiality and no purchaser carve-out
- [ ] Matter with an unsigned settlement agreement
- [ ] Matter referenced as settled with the settlement agreement not produced
- [ ] Matter dismissed without prejudice
- [ ] Matter dismissed with prejudice
- [ ] Matter stayed pending arbitration
- [ ] Matter whose most recent document is three years old, no disposition
- [ ] Matter tendered with defence under reservation of rights
- [ ] Matter with coverage denied on late notice
- [ ] Matter never tendered where a policy is referenced
- [ ] Matter where excess layers have not been notified
- [ ] Matter with a stated reserve and a probability characterisation
- [ ] Matter arising under a standard customer form
- [ ] Matter with a litigation hold issued eight months after the demand letter
- [ ] Matter with a preservation demand received and no hold evidenced
- [ ] Matter with a response deadline that passed with no action evidenced
- [ ] Matter with a trial date within twelve months of the as-of date
- [ ] Regulatory enforcement action in a court, to confirm it belongs here
- [ ] Regulator information request only, to confirm it belongs in the Regulatory table
- [ ] Unit mistakenly containing two disputes

Then test the dependencies: change `Settlement Terms` from a settlement to
`Not settled` and confirm `Release Scope` moves to `Not applicable`. Change
`Insurance Tendered` from `Tendered and accepted` to `No coverage identified` and
confirm `Carrier and Coverage Position` follows. Change `Matter Status on Record`
and confirm `Status As-Of Date` re-runs and recalculates its staleness flag.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
