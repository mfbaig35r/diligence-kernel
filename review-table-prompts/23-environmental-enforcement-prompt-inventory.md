# Prompt Inventory — Environmental: Enforcement

Table 23 of the POC, completing batch 7 and the Environmental workstream.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Environmental`
- Review unit: **one enforcement matter** — the initiating notice or
  communication, the target's response, any inspection report, any order,
  agreement, or penalty notice, remediation submissions, and any closing letter
  produced for it
- Grouping used: **yes**, typically 1–8 documents per unit
- Intended reviewers and downstream use: environmental and corporate/M&A teams;
  feeds the special indemnity and escrow analysis, the permit transfer analysis,
  the disclosure schedule, and the coverage register
- Inventory version: v1.0

### Three reasons this table matters beyond the breaches themselves

1. **An open matter can block or condition a permit transfer.** Several regimes
   require outstanding enforcement to be resolved before a permit is transferred or
   renewed. That converts a compliance matter into a **closing condition**, and it
   is why this table is read alongside Environmental — Permits rather than after
   it.
2. **Environmental obligations bind the land and the operator.** A consent order,
   a cleanup order, or a recorded land use restriction survives the transaction
   regardless of who signed it, and in a share purchase the entity carries it. The
   `Continuing Obligations` column is where that is captured.
3. **Environmental enforcement can be criminal.** Knowing violations, false
   reporting, and unpermitted discharges attract personal and corporate criminal
   exposure in many regimes. `Escalation Status` carries a referral state for that
   reason, and a criminal referral is a different order of finding from a civil
   penalty.

### The boundaries with three other tables

- **Regulatory — Correspondence** takes non-environmental regulator matters. Only
  environmental enforcement is a row here.
- **Litigation** takes the matter once proceedings are commenced in a court, and
  also takes citizen suits and third-party toxic tort claims. Where a matter
  crosses, it appears in both and `Escalation Status` records the crossing.
- **Environmental — Assessments** holds the technical findings. Where an
  enforcement matter concerns contamination, the delineation and cost sit in the
  assessment row for that site, not here.

## Assumptions to confirm before running

1. One row is one matter, not one letter. An inspection generating a report, a
   notice, a response, a remediation plan, and a closing letter is one row.
2. **Routine self-reported exceedances are rows only where the regulator
   responded.** A monitoring return recording an exceedance with no regulator
   action is a compliance record, and the Permits table's monitoring obligations
   cover it. Where the regulator responded, the response and the matter are a row.
3. Third-party and citizen claims are Litigation rows, not rows here, even where
   they concern environmental harm.
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

[Project name]. Buyer-side environmental diligence on the target group listed below. This table reviews environmental enforcement matters, inspections, and regulator correspondence short of court proceedings.

One row is one enforcement matter: the initiating notice or communication, the target's response, any inspection report, any order, agreement, or penalty notice, remediation submissions, and any closing letter produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the matter or the site.
- **Report the position as at the most recently dated document in the unit, and identify that document.** An enforcement matter moves, and a cell without a date is not usable.
- **Distinguish what the regulator alleges from what the target accepts.** An allegation in a notice of violation is the regulator's assertion; the response may dispute it. Report both and label each. Do not adopt either.
- **Do not assess the merits of any allegation, the likelihood of further action, the size of any exposure, or whether a defence is available.** All four are legal judgements and all four are human columns.
- **Report privilege and confidentiality markings where present and do not assess privilege.** Environmental audit and self-disclosure material attracts protection in some regimes, and internal investigation reports are frequently privileged.
- Report figures, quantities, and concentrations only as the documents state them. Do not calculate, total, or convert units.
- Use entity, facility, and authority names exactly as printed. **Do not report the names of individual employees; describe them by role.**
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Matter Type
  Authority
  Recipient Entity
  Facility or Site
  Related Permit
  Initiated Date

Stage 2 — Status
  Documents in Unit ──→ Resolution Status
                        Referenced but Not Produced
  Resolution Status ──→ Status As-Of Date

Stage 3 — Substance, routed on matter type
  Matter Type ──→ Alleged Violation
                  Media Affected
  Alleged Violation ──→ Target Response

Stage 4 — Consequences
  Penalty or Sanction
  Required Corrective Action ──→ Action Deadline
                                 Remediation Evidenced
  Continuing Obligations

Stage 5 — Escalation and recovery
  Escalation Status
  Insurance and Recovery Referenced
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Resolution Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Matter Type | Classify | — | Alleged Violation; Media Affected | v1.0 | draft |
| 3 | Authority | Free Response | — | — | v1.0 | draft |
| 4 | Recipient Entity | Free Response | — | — | v1.0 | draft |
| 5 | Facility or Site | Free Response | — | — | v1.0 | draft |
| 6 | Related Permit | Free Response | — | — | v1.0 | draft |
| 7 | Initiated Date | Date | — | — | v1.0 | draft |
| 8 | Resolution Status | Classify | @Documents in Unit | Status As-Of Date | v1.0 | draft |
| 9 | Status As-Of Date | Date | @Resolution Status | — | v1.0 | draft |
| 10 | Alleged Violation | Free Response | @Matter Type | Target Response | v1.0 | draft |
| 11 | Media Affected | Classify | @Matter Type | — | v1.0 | draft |
| 12 | Target Response | Free Response | @Alleged Violation | — | v1.0 | draft |
| 13 | Penalty or Sanction | Free Response | — | — | v1.0 | draft |
| 14 | Required Corrective Action | Free Response | — | Action Deadline; Remediation Evidenced | v1.0 | draft |
| 15 | Action Deadline | Date | @Required Corrective Action | — | v1.0 | draft |
| 16 | Remediation Evidenced | Classify | @Required Corrective Action | — | v1.0 | draft |
| 17 | Continuing Obligations | Free Response | — | — | v1.0 | draft |
| 18 | Escalation Status | Classify | — | — | v1.0 | draft |
| 19 | Insurance and Recovery Referenced | Free Response | — | — | v1.0 | draft |
| 20 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

20 columns. `Insurance and Recovery Referenced` earned its place: environmental
matters frequently have a recovery route against a prior owner, an insurer, or a
contractor, and that route is an asset the buyer may acquire.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Resolution Status`, `Referenced but Not Produced`
- Purpose: inventory the matter file in date order, which is the chronology the
  row is read against.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the initiating notice or communication, inspection and site visit reports, information requests, the target's responses and submissions, notices of violation or deficiency, warning letters, proposed and final orders, consent orders and agreements, penalty notices, remediation plans and workplans, progress and completion reports, and any closing, no-further-action, or resolution letter.
- Include self-disclosure or self-reporting submissions where the matter arose that way.
- Treat schedules and appendices attached to a document as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title or subject line. Where none is printed, describe it in five words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Initiating notice`, `Inspection report`, `Information request`, `Target response`, `Notice of violation`, `Warning letter`, `Proposed order`, `Consent order or agreement`, `Final order`, `Penalty notice`, `Remediation plan`, `Progress report`, `Completion report`, `Closing letter`, `Self-disclosure`, or `Other`.
- **State who sent each document — the regulator or the target — since the alternation is the chronology.**
- **Where the most recent document is from the regulator and no target response follows, note that in the evidence field.** An unanswered regulator communication is a finding in itself.
- Where a document relates to a different matter or site, still list it and append ` [relates to [matter or site]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [from regulator | from target] — [Title] ([Function])`

Return no more than 15 lines and no more than 130 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Matter Type

- Native type: Classify
- Configured options, in UI order: `Routine inspection`, `Complaint-driven inspection`, `Information request`, `Notice of violation`, `Warning or advisory letter`, `Administrative order`, `Cleanup or remediation order`, `Consent order or agreement`, `Penalty or civil action`, `Formal investigation`, `Self-disclosure by target`, `Spill or incident report`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Alleged Violation`, `Media Affected`
- Purpose: what kind of matter this is, which determines both how seriously the row
  reads and what obligations follow.

```markdown
## Task

Classify the nature of this environmental matter. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits, since the order runs from most to least serious.

1. `Cleanup or remediation order`: an order requiring investigation or remediation of contamination. **The most consequential type**, because the obligation runs with the site, the cost is usually the largest in the workstream, and the order commonly binds successors expressly.
2. `Penalty or civil action`: a formal proceeding seeking a monetary penalty or injunctive relief, short of court proceedings.
3. `Consent order or agreement`: the matter concluded, or is proposed to conclude, in an agreed order, consent decree, or assurance. **These carry continuing obligations and they are usually public and usually binding on successors.**
4. `Administrative order`: an order requiring compliance, ceasing an activity, or taking stated steps, without a penalty element.
5. `Formal investigation`: the regulator has opened a formal investigation or inquiry, whether or not action has followed.
6. `Notice of violation`: the regulator asserts a specific breach of a permit, a regulation, or a statute.
7. `Warning or advisory letter`: the regulator expresses concern or issues a warning without asserting a formal violation. **Not trivial** — it is frequently the step before a notice, and a pattern matters more than any single letter.
8. `Complaint-driven inspection`: an inspection prompted by a complaint, a report, or an incident. **Materially different from a routine cycle inspection**, and the distinction should never be lost.
9. `Routine inspection`: a scheduled or cycle inspection.
10. `Spill or incident report`: a report of a release, spill, or incident, whether made by the target or by a third party. **Report in the evidence field whether the target self-reported**, since mandatory release reporting is a strict obligation and a failure to report is usually treated more seriously than the release.
11. `Self-disclosure by target`: a voluntary disclosure of a violation under an audit or self-disclosure policy. **Report as such** — self-disclosure commonly attracts penalty mitigation and the characterisation matters to how the history reads.
12. `Information request`: the regulator sought information with no stated concern.

**An information request or a routine inspection may be the opening of something more serious.** Where the documents indicate a specific concern behind it, classify on the concern.

## Fallback rules

- Use `Other` where the matter is environmental but none of the options describes it.
- Use `Unable to determine` where the documents are too fragmentary to identify the nature of the matter.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Authority

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which regulator, which is the join key to the Permits table and the
  basis for reading the compliance history by authority.

```markdown
## Task

State the authority conducting or initiating this matter.

## Rules

- Report the authority exactly as printed, including the region, district, programme office, or enforcement unit where stated.
- **Report the level — federal or national, state or provincial, regional, or local — since environmental enforcement is commonly concurrent**, and a matter can be pursued by more than one body over the same conduct.
- **Report every authority involved and label its role.** A referral from a state agency to a federal one, or the involvement of a local air district alongside a state agency, is a material escalation and it means more than one relationship to manage.
- **Report any referral to a prosecuting, criminal investigation, or attorney general's office prominently**, and also record it in Escalation Status.
- Report any case, file, docket, or enforcement reference the authority assigns, exactly as printed. **It is the key for any enquiry and for the disclosure a permit transfer application will require.**
- Report any case officer's role rather than their name.

## Fallback rules

- Return `Unable to determine` where the documents do not identify the authority.

## Output format

`[Authority as printed][ — [unit or region]]; level: [as stated][; reference: [as printed]]`, with any additional authority labelled.

Return no more than 50 words.
```

---

### 4. Recipient Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which entity or person the matter is directed at. **Determines who
  carries the obligation and whether it follows the business.**

```markdown
## Task

State the target-group entity or person that is the subject of or party to this matter.

## Rules

- Use the review-subject list in the Table Instructions to determine which named entities are group entities.
- Report each name exactly as printed, including entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- **Report the capacity in which the recipient is named — owner, operator, generator, transporter, or arranger** — since environmental liability attaches by role, and a target named as an arranger for off-site disposal carries a very different exposure from one named as the site operator.
- **Where an individual — a director, officer, environmental manager, or responsible person — is a subject of the matter alongside or instead of the entity, report the entity and note the individual's role in the evidence field.** Do not report the individual's name. **A matter directed at an individual signals potential personal or criminal exposure** and it engages the indemnification, D&O, and employment analyses.
- Where the entity named is not on the review-subject list, report the name and append ` (not a listed entity)`.
- **Where the matter is addressed to a prior owner or operator of the site, report that and label it.** A matter naming a predecessor is relevant because the obligation may still attach to the land, and because the predecessor may be a recovery route.

## Fallback rules

- Return `Unable to determine` where the subject cannot be identified.

## Output format

`[Exact legal name] — [capacity as stated]` per recipient, with any qualifier appended. Return no more than 45 words. Do not name individuals.
```

---

### 5. Facility or Site

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the matter arises. **The join key to the Permits, Assessments,
  and Real Estate tables.**

```markdown
## Task

State the facility, site, or location this matter concerns.

## Rules

- Report the facility name and street address exactly as printed. **Do not standardize or correct**, since it is the join key to three other tables.
- Report the regulator's facility identifier where given.
- **Report the specific unit, process, outfall, stack, tank, or area concerned where the documents identify one**, since a matter about one emission point is not a matter about the whole site.
- **Where the matter concerns an off-site location — a disposal facility, a receiving water, a neighbouring property, or a transport route — report it and label it as off-site.** Off-site liability for waste sent to a third-party facility is a distinct and frequently overlooked exposure, and the target may be named alongside dozens of others.
- Where the matter concerns multiple sites, list each.
- **Where the matter concerns a site the target no longer owns or operates, report that where stated.** Liability for past ownership or operation survives disposal in many regimes.
- Where the matter is corporate-wide rather than site-specific, say so.

## Fallback rules

- Return `Not stated` where the documents do not identify a location.
- Return `Unable to determine` where the location is illegible.

## Output format

`[Facility name], [address as printed][; regulator ID: [as stated]][; unit: [as stated]]` per location, with any label appended.

Return no more than 55 words.
```

---

### 6. Related Permit

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which permit the matter attaches to. **An open matter against a permit
  is an input to that permit's transfer or renewal**, and this is the join.

```markdown
## Task

Identify any environmental permit, authorisation, or registration this matter relates to.

## Rules

- Report the permit as the documents name it, with its number exactly as printed. **The number is the join key to the Environmental — Permits table**, so do not reformat it.
- Report the specific permit condition or limit alleged to have been breached, as identified.
- Where the matter relates to more than one permit, list each.
- **Where the matter alleges activity conducted without a required permit, report that and append ` [unpermitted activity alleged]`.** This is among the most serious findings in the workstream, it frequently carries criminal exposure, and **it will not appear in the Permits table at all because there is no permit to be a row.**
- **Where the matter concerns a statutory or regulatory obligation that arises independently of any permit** — a release reporting duty, a waste transfer duty, a general duty of care — report that and say so.
- Where the matter relates to a permit held by a different group entity, report it and name that entity.

## Fallback rules

- Return `Not applicable — no permit involved` where the matter does not attach to a permit and none was required.
- Return `Unable to determine` where the permit cannot be identified.

## Output format

`[Permit as named] — [number as printed][; condition breached: [as identified]]` per permit, with any bracketed flag appended.

Return no more than 45 words.
```

---

### 7. Initiated Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the matter began, which shows how long it has been running and
  whether it predates a prior transaction or a change in management.

```markdown
## Task

Identify the date this matter was initiated.

## Date-selection hierarchy

1. Use the date of the earliest communication from the regulator in the unit.
2. Where the matter is a self-disclosure or a spill report, use the date of the target's report.
3. Where the earliest document refers to an earlier communication not in the unit, use the date of that earlier communication as stated, and note that it is taken from a reference.

## Excluded dates

- The date of the conduct, release, or period under investigation. **Report that period in the evidence field**, since the gap between the conduct and the regulator's attention is informative and bears on limitation
- The date of the target's response
- The date of an inspection report issued after the inspection
- File name and metadata dates, and transmittal and scan dates

## Rules

- **Report the date of the conduct or the release in the evidence field where stated, and report the inspection date separately from the report date.** A 2024 notice about a 2019 release tells a reviewer the exposure is historic, which bears on whether the seller or the buyer carries it and on any limitation argument.
- Compare the initiated date to the diligence as-of date. **Where the matter has been running more than eighteen months and Resolution Status is not closed, append ` [open over 18 months]`.**
- **Note in the evidence field whether the matter predates a prior acquisition of the target or the site**, where the documents allow that to be seen. An inherited matter is frequently subject to an earlier indemnity that may still be enforceable, and that is an asset.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended. Preserve partial precision as printed. Return `Not stated` where no initiation date can be selected.
```

---

### 8. Resolution Status

- Native type: Classify
- Configured options, in UI order: `Open, awaiting target response`, `Open, awaiting regulator response`, `Open, remediation in progress`, `Open, under negotiation`, `Closed, no action taken`, `Closed, findings remediated`, `Closed with penalty`, `Concluded by consent order`, `Referred or escalated`, `Dormant`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Status As-Of Date`
- Purpose: where the matter stands on the documents.

**Closure must be evidenced by a document.** Environmental matters do not lapse
through inactivity, and a matter believed closed with no closing letter is the most
common way an environmental compliance history is understated.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document and who sent it. Confirm the status against that document.

## Task

Classify the status of this matter as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Referred or escalated`: the documents record a referral to another authority, to a prosecuting body, or to court proceedings. **Also record this in Escalation Status.**
2. `Concluded by consent order`: the matter concluded in an agreed order, consent decree, or assurance. **Continuing obligations almost always follow.**
3. `Closed with penalty`: a penalty or sanction was imposed and the matter is recorded as concluded.
4. `Closed, findings remediated`: the regulator confirmed closure following remediation, or issued a no-further-action or completion letter.
5. `Closed, no action taken`: the regulator closed the matter without findings or action.
6. `Open, under negotiation`: the parties are negotiating a resolution, a penalty, or the terms of an order, with nothing concluded.
7. `Open, remediation in progress`: findings are accepted or unchallenged and remediation or corrective action is underway.
8. `Open, awaiting regulator response`: the target's most recent submission is the latest document, with no regulator reply.
9. `Open, awaiting target response`: a regulator communication requiring a response is the latest document, with no target response in the unit. **Filter these first** — it is either a missed deadline or a production gap, and both need resolving before any permit transfer application discloses the matter.
10. `Dormant`: the most recent document is more than two years before the diligence as-of date and no closure is recorded. **Do not treat this as closed.** Environmental matters do not expire through inactivity, and the file may simply be incomplete.

**Closure must be evidenced.** Do not infer closure from the passage of time, from the completion of remediation, from a remediation plan, or from a target's internal note recording the matter as closed. **Only a regulator document closes a matter.**

## Fallback rules

- Use `Unable to determine` where documents of the same date conflict, or where the most recent document is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Status As-Of Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Resolution Status`
- Downstream: none
- Purpose: the date the status speaks as of. **Environmental files in data rooms
  are routinely incomplete**, and an open matter reported from an old document
  cannot be relied on.

```markdown
## Established result

- Resolution status: @Resolution Status

## Task

Identify the date of the most recently dated document in the review unit, which is the date as of which the status is reported.

## Rules

- Report the date of the most recent document, and state in the evidence field who sent it.
- **Prefer the most recent document bearing on the status** — a regulator communication, a target response, an order, a completion report, or a closing letter — over routine acknowledgements of a later date. Where a later routine document exists, report the substantive document's date and note the later one.
- Compare the reported date to the diligence as-of date and flag the gap:
  - more than six months: append ` [status over 6 months old]`
  - more than eighteen months: append ` [status over 18 months old]`
- **Where Resolution Status is any `Open` state and the flag is `[status over 18 months old]`, the row needs verification with the regulator, the target's environmental function, or the public enforcement register before it can be relied on.** Most environmental regulators publish enforcement and compliance histories, so verification is usually available.

## Fallback rules

- Return `Not stated` where no document in the unit bears a date.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended.
```

---

### 10. Alleged Violation

- Native type: Free Response
- Upstream: `@Matter Type`
- Downstream: `Target Response`
- Purpose: what the regulator says went wrong, kept strictly separate from what the
  target accepted.

```markdown
## Established result

- Matter Type: @Matter Type

## Task

Report the violations, deficiencies, or findings the regulator has stated in this matter.

## Applicability

- Applies where Matter Type is any of `Routine inspection`, `Complaint-driven inspection`, `Notice of violation`, `Warning or advisory letter`, `Administrative order`, `Cleanup or remediation order`, `Consent order or agreement`, `Penalty or civil action`, `Formal investigation`, `Self-disclosure by target`, or `Spill or incident report`.
- Where Matter Type is `Information request`, report any concern the regulator has expressed, and where none is expressed return `None stated`.

## Rules

- Report each alleged violation in twelve words or fewer, **with the permit condition, regulation, or statutory provision it is said to breach, as the documents identify it.**
- **Report the period over which each violation is said to have occurred.** A single exceedance and a three-year pattern are very different exposures, and penalties in most regimes are assessed per day of violation.
- **Report any quantity, concentration, or exceedance figure exactly as stated, with its units and the limit it is compared to.** Do not convert units and do not calculate an exceedance factor.
- **Report the regulator's own severity characterisation exactly as printed** — significant non-compliance, high priority violation, minor, or a graded scale. Do not translate between scales.
- **Report any allegation described as knowing, wilful, repeat, or continuing, and flag it.** Those characterisations drive penalty severity and, in several regimes, criminal exposure.
- **Report any allegation of false, incomplete, or unsubmitted reporting separately and prominently.** Reporting violations are frequently treated more seriously than the underlying substantive breach, because they undermine the whole monitoring regime.
- Report findings as the regulator's assertions, using `the regulator alleges` or `the notice states`. **The target's position is a separate column.**
- Report no more than eight violations. Where more exist, report the eight most severe and append ` and [N] further alleged violations`.

## Fallback rules

- Return exactly `None stated` where the regulator has stated no violation or finding.
- Return `Unable to determine` where the allegations are illegible or their severity cannot be read.

## Output format

One line per allegation:

`[Severity as printed] — [allegation] — [provision breached] — [period] — [figures as stated][; knowing or repeat]`

Return no more than 8 lines and no more than 110 words.
```

---

### 11. Media Affected

- Native type: Classify
- Configured options, in UI order: `Air`, `Surface water`, `Groundwater`, `Soil or land`, `Waste handling`, `Storage tanks`, `Multiple media`, `Reporting or records only`, `Other`, `Not applicable`, `Unable to determine`
- Upstream: `@Matter Type`
- Downstream: none
- Purpose: which environmental medium is involved. **Determines the remediation
  profile and the likely cost order**, and it is the axis on which a pattern across
  rows becomes visible.

```markdown
## Established result

- Matter Type: @Matter Type

## Task

Classify the environmental medium or media this matter concerns. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Multiple media`: the matter concerns two or more media. **Report each in the evidence field.** A release affecting soil and groundwater together is materially more expensive to address than either alone.
2. `Groundwater`: contamination of, or discharge to, groundwater. **The most expensive medium to remediate and the slowest**, since groundwater remediation commonly runs for decades and migrates off site.
3. `Soil or land`: soil or land contamination.
4. `Storage tanks`: matters concerning underground or aboveground storage tanks, including their installation, testing, integrity, or closure. **Kept separate because tank regimes have their own requirements and their own financial assurance**, and a tank matter frequently develops into a soil and groundwater matter.
5. `Waste handling`: generation, storage, labelling, manifesting, transport, or disposal of waste, including off-site disposal liability.
6. `Surface water`: discharge to or contamination of surface water, including stormwater.
7. `Air`: emissions to air, including monitoring, control equipment, and permit limits.
8. `Reporting or records only`: the matter concerns reporting, record-keeping, or notification obligations with no substantive release or emission alleged. **Do not treat this as trivial** — reporting violations attract significant penalties and are frequently the entry point to a wider investigation.

## Fallback rules

- Use `Other` where the matter concerns an environmental medium or subject none of the options describes, such as noise, odour, or protected habitat.
- Use `Not applicable` where the matter is an information request with no medium identified.
- Use `Unable to determine` where the medium cannot be identified.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Target Response

- Native type: Free Response
- Upstream: `@Alleged Violation`
- Downstream: none
- Purpose: what the target said back. **A disputed allegation and an accepted one
  are entirely different facts.**

```markdown
## Established result

- Alleged violation: @Alleged Violation

## Task

If Alleged Violation reported allegations, report the target's response to them.

If it returned `None stated`, report any substantive response the target made, and where none is in the unit return `No response in unit`.

If it returned `Unable to determine`, return exactly `Unable to determine — upstream allegations unresolved`.

## Include where expressly stated

- Which allegations the target accepted, in whole or in part
- **Which allegations the target disputed, and on what basis in ten words or fewer** — factual dispute, monitoring or laboratory error, permit interpretation, upset or bypass defence, or third-party cause
- Any admission or express denial
- Any explanation of cause offered — equipment failure, human error, contractor act, extreme weather, or a third party
- **Any statement that the target had already identified and was addressing the issue before the regulator raised it**
- Any remediation or corrective action the target proposed or reported as already completed
- Any request for an extension, a reconsideration, a hearing, or a meeting
- Any mitigation offered — cooperation, self-reporting, prompt correction, or an environmental audit
- Whether the response was made by the target, by counsel, or by a consultant
- The date of the response

## Rules

- **Report acceptance and dispute separately, allegation by allegation where the documents allow it.** An accepted violation is an inherited obligation; a disputed one is a contingency.
- **Report any upset, bypass, or emergency defence asserted**, since these are recognised in several regimes and their availability is a legal question the reviewer must pursue.
- **Report where the target attributes cause to a contractor or third party**, since it points at a recovery route reported in Insurance and Recovery Referenced.
- **Report where no response appears and one was required.** That is either a missed deadline or a production gap.
- Report the response as made. **Do not assess whether it is likely to succeed** and do not adopt it.
- Do not name individuals.

## Output format

`Accepted: [allegations or "none"]; disputed: [allegations and basis, or "none"]; cause offered: [brief or "none"]; self-identified: [yes | Not addressed]; mitigation asserted: [brief or "none"]; responded by: [target | counsel | consultant]; dated [YYYY-MM-DD]`

Return no more than 95 words.
```

---

### 13. Penalty or Sanction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the matter cost, and whether it is public.

```markdown
## Task

Report any penalty, fine, or sanction imposed, proposed, or agreed in this matter.

## Include where expressly stated

- Any monetary penalty, with the amount and whether it is proposed, agreed, or final
- **Any per-day or per-violation basis on which the penalty was calculated, and the number of days or violations counted.** Environmental penalties are commonly assessed per day, which is how a modest daily figure becomes a large total
- Any economic benefit or gravity component the documents identify
- Any supplemental or beneficial environmental project agreed in lieu of part of a penalty, with its cost and scope
- Any reduction applied for cooperation, self-disclosure, prompt correction, or an inability to pay, with the discount stated
- Any restitution, natural resource damage, or third-party compensation component
- **Whether the penalty or the matter is or will be published**, and where
- Any suspension, restriction, or condition imposed on a permit. **Also report this in the Permits table's status and conditions columns**
- Any revocation or refusal to renew a permit
- Any prohibition, disqualification, or sanction imposed on an individual, described by role
- Any costs the target must pay
- Any statement that no penalty was imposed

## Rules

- **Report whether a penalty is proposed, agreed, or final.** A proposed penalty is a negotiation position; environmental penalties are very frequently negotiated down substantially, and treating a proposed figure as a liability overstates it.
- **Report any supplemental environmental project separately, with its cost.** These are common, they substitute for penalty, and the committed spend is a real obligation that continues past closing.
- **Report publication prominently.** Environmental enforcement is published as a matter of course in many regimes, and a published notice affects permit transfers, customer relationships, and the disclosure schedule permanently.
- Report amounts as stated. **Do not total penalty, restitution, and project costs, and do not calculate a per-day total.**
- Report any individual sanction by role only.

## Fallback rules

- Return exactly `None imposed` where the documents record no penalty or sanction.
- Return `Unable to determine` where amounts or sanctions conflict or are illegible.

## Output format

`Penalty: [amount, currency, [proposed | agreed | final]]; basis: [per day or per violation, as stated]; supplemental project: [cost and scope, or "none"]; reduction: [as stated or "none"]; published: [yes, [where] | no | Not addressed]; permit effect: [as stated or "none"]; individual sanction: [role and sanction, or "none"]`

Return no more than 95 words.
```

---

### 14. Required Corrective Action

- Native type: Free Response
- Upstream: none
- Downstream: `Action Deadline`, `Remediation Evidenced`
- Purpose: what the business has to do. **Inherited obligations with deadlines**,
  and frequently the largest cost in the workstream.

```markdown
## Task

Report the corrective, remedial, or compliance actions the regulator requires, or the target has committed to take, in this matter.

## Include where expressly stated

- Each required action, whether imposed or offered
- **Any requirement to investigate, delineate, or characterise contamination**, and the media and area covered
- **Any requirement to remediate, and the remedial standard or target level to be achieved.** The standard is what determines the cost more than anything else, and a standard tied to a residential end use is far more onerous than one tied to industrial use
- Any requirement to install, upgrade, or replace equipment or abatement
- Any requirement to change a process, procedure, or management system
- Any requirement to conduct monitoring, and for how long
- **Any requirement to appoint an independent consultant, auditor, or supervising professional**, and who bears the cost
- Any requirement to submit a plan, workplan, or schedule for approval, and by when
- Any requirement to record a land use restriction or environmental covenant. **Also report this in Continuing Obligations**
- Any restriction on operating, discharging, or accepting waste pending completion
- Any requirement to notify or compensate third parties or neighbours
- Any requirement to remove or close a tank or a unit

## Rules

- **Report the remedial standard or target level where stated**, since it is the single largest determinant of cost.
- **Report any requirement for regulator approval of a plan before work begins**, since it inserts a determination period into the timetable and the buyer inherits both.
- **Report any restriction on operating pending completion prominently**, since it constrains the business immediately rather than eventually.
- **Report any monitoring duration**, since long-term monitoring frequently exceeds the remediation cost in total.
- Report each action in ten words or fewer, and identify whether it was imposed or volunteered.
- Report figures and standards as stated. **Do not estimate a cost, a volume, or a duration.**

## Fallback rules

- Return exactly `None required` where the documents impose and record no required action.
- Return `Unable to determine` where required actions conflict or are illegible.

## Output format

One line per action:

`[Action] — [imposed | volunteered] — [standard or target, where stated] — [approval required: yes | no]`

Return no more than 10 lines and no more than 105 words.
```

---

### 15. Action Deadline

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Required Corrective Action`
- Downstream: none
- Purpose: the next deadline. **A passed deadline with no evidence of completion is
  a fresh breach on top of the original one.**

```markdown
## Established result

- Required corrective action: @Required Corrective Action

## Task

If Required Corrective Action reported one or more actions, identify the earliest deadline for any of them.

If it returned `None required`, return exactly `Not applicable`.

If it returned `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the earliest deadline the documents state, with what it is for in five words or fewer.
- Include deadlines for submitting a plan, commencing work, completing remediation, achieving a standard, submitting progress or completion reports, and responding to any outstanding request.
- Report only dates the documents state. **Do not calculate a deadline from a period, an order date, or a rule.**
- Where several deadlines are stated, report the earliest after the diligence as-of date and note the count of later ones in the evidence field.
- **Where a stated deadline falls before the diligence as-of date and Remediation Evidenced does not show completion, report that date and append ` [deadline passed, completion not evidenced]`.** This is the most actionable flag in the table: **an unmet environmental deadline is an independent violation, it is commonly penalised per day, and it is exactly the kind of matter that must be resolved before a permit transfer.**
- Where an extension was granted, report the extended date and append ` (extended from [date])`.
- **Where the order sets a long-term schedule with milestones extending years out, report the next milestone and note the final completion date in the evidence field.**

## Fallback rules

- Return `Not stated` where actions are required and the documents state no deadline. **Report in the evidence field any period stated, such as within 60 days**, without converting it to a date.

## Output format

`YYYY-MM-DD — [what it is for]`, with any bracketed flag or qualifier appended, or one of the exact fallback values above.
```

---

### 16. Remediation Evidenced

- Native type: Classify
- Configured options, in UI order: `Completion confirmed by regulator`, `Completion asserted by target, not confirmed`, `In progress per documents`, `Plan approved, no progress evidenced`, `Plan submitted, not approved`, `No evidence of action`, `Not applicable`, `Unable to determine`
- Upstream: `@Required Corrective Action`
- Downstream: none
- Purpose: whether the work was done, and on whose word.

**Only a regulator's confirmation discharges an environmental obligation.** A
target's assertion of completion is a claim the buyer may be inheriting untested,
and the regulator can revisit it.

```markdown
## Established result

- Required corrective action: @Required Corrective Action

## Task

If Required Corrective Action reported one or more actions, classify what the documents evidence about their completion.

If it returned `None required`, return `Not applicable`.

If it returned `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Completion confirmed by regulator`: a regulator communication in the unit confirms the required actions are complete, or issues a no-further-action, closure, or completion determination. **Report the form of the determination and its date in the evidence field**, and note whether it is conditional or contains a reopener.
2. `Completion asserted by target, not confirmed`: the target has reported completion and no regulator confirmation appears. **The obligation may still be live**, and a regulator can reject a completion report years later.
3. `In progress per documents`: progress reports or correspondence show work underway and not complete.
4. `Plan approved, no progress evidenced`: a plan or workplan was approved by the regulator and nothing evidences work against it.
5. `Plan submitted, not approved`: a plan was submitted and no approval appears. **Work usually cannot lawfully begin until approval issues**, so this is a stalled matter rather than a progressing one.
6. `No evidence of action`: actions were required and the documents show nothing done.

**Where completion is partial** — some actions confirmed, others outstanding — classify on the **least** complete state and report the split in the evidence field.

**Do not infer completion from the passage of time, from the absence of further regulator contact, from a consultant's report, or from a target's internal note.**

## Fallback rules

- Use `Unable to determine` where the documents conflict about completion or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 17. Continuing Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what survives the matter's closure. **In environmental matters this is
  frequently the largest part of the exposure**, and it runs with the land or the
  entity regardless of who signed the order.

```markdown
## Task

Report any obligation arising from this matter that continues after its resolution.

## Include where expressly stated

- **Any long-term monitoring obligation, its media, its frequency, and its duration**
- **Any operation and maintenance obligation for an installed remedy** — a cap, a barrier, a pump-and-treat system, a vapour mitigation system — and its expected duration
- **Any recorded land use restriction, activity and use limitation, environmental covenant, or deed restriction, with its recording reference where stated.** These bind the land permanently and they must also appear in the Real Estate — Owned Property restrictive covenants column
- Any restriction on the site's use, redevelopment, or excavation
- Any continuing reporting, certification, or attestation obligation, and its frequency
- Any financial assurance required to be maintained for the continuing obligation, and its amount
- Any institutional control the target must maintain or enforce
- **Any reopener provision permitting the regulator to require further work**, and on what trigger — new information, a change of use, or a failure of the remedy
- **Any provision stating that the obligations bind successors and assigns**
- Any continuing obligation to indemnify or cooperate with the regulator or a third party
- Any obligation surviving the sale of the site

## Rules

- **Report the duration of each obligation, and where none is stated say so.** Environmental monitoring obligations with no end date are common, and a perpetual obligation is a permanent cost centre.
- **Report the reopener provision prominently.** A closure with a reopener is a conditional closure, and a change in the site's use — which a buyer may well plan — is a standard reopener trigger.
- **Report any successor-binding provision prominently.** It is what makes the obligation the buyer's problem, and environmental orders bind successors far more often than commercial agreements do.
- **Report any recorded restriction with its recording reference**, so it can be matched to the Real Estate row and the Assessments row for the same site.
- Report the obligations as stated. **Do not assess their burden, estimate their cost, or assess whether the remedy is likely to remain effective.**

## Fallback rules

- Return exactly `None` where the matter leaves no continuing obligation.
- Return `Not applicable` where the matter is not resolved, so continuing obligations cannot yet arise. **Required actions in an open matter are reported in Required Corrective Action**, not here.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

One line per obligation:

`[Obligation] — [duration or "no end date stated"] — [cost bearer where stated][; recorded at [reference]]`

then a final line: `Binds successors: [yes | Not addressed]; reopener: [trigger or "none"]; financial assurance: [as stated or "none"]`

Return no more than 10 lines and no more than 105 words.
```

---

### 18. Escalation Status

- Native type: Classify
- Configured options, in UI order: `No escalation`, `Referred to enforcement division`, `Referred to another regulator`, `Referred to prosecuting or criminal authority`, `Criminal charges brought`, `Court or tribunal proceedings commenced`, `Citizen or third-party action referenced`, `Escalation threatened, not effected`, `De-escalated or downgraded`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the matter has moved beyond administrative enforcement.

**Environmental enforcement can be criminal**, and personal liability for
directors, officers, and environmental managers is a real feature of several
regimes. A criminal referral is a different order of finding from a civil penalty
and it changes the disclosure, the indemnity, and sometimes the deal.

```markdown
## Task

Classify whether this matter has been escalated beyond administrative enforcement. Choose exactly one configured option.

## Scope

- Consider referrals within the regulator, referrals to other authorities, criminal referrals and charges, and the commencement of proceedings.
- Consider any statement by the regulator that escalation is contemplated.
- Consider any reference to a citizen suit, a third-party action, or a notice of intent to sue.
- Exclude the ordinary progression from an inspection to a notice of violation.

## Classification rules

Apply the first rule that fits.

1. `Criminal charges brought`: charges, an indictment, or a criminal information has been brought against the entity or an individual. **The most serious state available.** Report in the evidence field whether individuals are charged, described by role, and whether the entity is charged.
2. `Referred to prosecuting or criminal authority`: the documents record a referral for criminal investigation or prosecution, without charges yet brought.
3. `Court or tribunal proceedings commenced`: the regulator has commenced civil proceedings in a court or tribunal. **This matter is also a Litigation row.**
4. `Citizen or third-party action referenced`: the documents refer to a citizen suit, a notice of intent to sue, or a third-party claim arising from the same conduct. **A distinct and additional exposure** — citizen suits commonly proceed independently of the regulator's own position, and the claim belongs in the Litigation table.
5. `Referred to another regulator`: the matter has been referred or reported to a different authority. Note which, since it creates a second supervisory relationship.
6. `Referred to enforcement division`: the matter has moved from inspection or compliance assistance to a formal enforcement function within the same regulator.
7. `Escalation threatened, not effected`: the regulator has stated it may refer, escalate, or take formal action if a condition is not met. **Report the condition and any deadline in the evidence field** — this is a contingent escalation the buyer can often still prevent.
8. `De-escalated or downgraded`: the documents record a matter returned to compliance assistance, a finding downgraded, or an enforcement referral closed without action.
9. `No escalation`: the matter has remained within administrative enforcement.

## Fallback rules

- Use `Unable to determine` where references to escalation are too incomplete to classify.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Insurance and Recovery Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether anyone else might pay. **Environmental matters frequently have
  a recovery route** against a prior owner, a contractor, a waste facility, or an
  insurer — and a recovery right is an asset the buyer acquires with the entity.

```markdown
## Task

Report anything in the documents indicating that a party other than the target may bear or contribute to the cost of this matter.

## Include where expressly stated

- Any insurance notified, the carrier, the policy, and the coverage position stated
- **Any environmental or pollution legal liability policy referenced**, and whether the condition is stated to be known or pre-existing. **Known conditions are typically excluded**, which is why identified matters usually drive indemnity rather than insurance
- Any indemnity from a prior owner, prior operator, seller, or landlord referenced
- **Any indemnity given on a prior acquisition of the target or the site**, with its date, and any time or amount limit. **An inherited indemnity may still be enforceable and it is an asset**, and the transaction should preserve rather than lose it
- Any contribution or cost-recovery claim against a third party referenced — a contractor, a transporter, a disposal facility, a neighbouring owner, or a former tenant
- Any statement that the target has been named alongside other potentially responsible parties, and any allocation among them
- Any settlement, de minimis buyout, or contribution agreement referenced
- Any escrow, holdback, or reserve from a prior transaction referenced
- Any statutory cost-recovery or orphan-share funding referenced

## Rules

- **Report any indemnity from a prior transaction prominently, with its limits and expiry.** These are routinely forgotten, they are frequently the only real recovery route, and **an indemnity that expires shortly after closing changes the urgency of pursuing it.**
- **Report where the target is one of several named responsible parties**, with any stated allocation or share. Multi-party liability regimes commonly impose joint and several liability, so a small share is not a small exposure — but the contribution rights against the others are an asset.
- **Report the insurer's coverage position with its stated grounds**, and note that a known-conditions exclusion is the usual answer for an identified matter.
- Report amounts as stated. **Do not total recoveries, net them against the exposure, or assess the prospects of any claim.**

## Fallback rules

- Return exactly `None referenced` where the documents reference no insurance or recovery route.
- Return `Unable to determine` where references conflict or are illegible.

## Output format

`Insurance: [carrier, policy, position, or "none"]; prior-owner indemnity: [party, date, limits, or "none"]; third-party recovery: [party and basis, or "none"]; other responsible parties: [as stated or "none"]; prior escrow: [as stated or "none"]`

Return no more than 90 words.
```

---

### 20. Referenced but Not Produced

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

List every document relating to this matter that the documents in this unit refer to and that is not present.

## Scope

- **Include any inspection report, notice of violation, or order referenced but not produced.**
- **Include any closing, no-further-action, or completion letter referenced but not produced.** Without it closure is unevidenced.
- Include the target's responses and submissions referenced.
- Include remediation plans, workplans, and their approvals referenced.
- Include progress reports, completion reports, and verification sampling reports referenced.
- **Include any consent order, agreement, or undertaking referenced.**
- Include any consultant, monitor, or independent professional report referenced.
- Include any recorded land use restriction or environmental covenant referenced.
- **Include any earlier matter or inspection the documents refer to, particularly where a violation is described as a repeat.**
- Include any monitoring data, laboratory report, or exceedance record the allegations rest on.
- Include any insurance notice, coverage letter, or prior-owner indemnity referenced.
- Include any internal audit or investigation report referenced, **noting that these may be privileged**; report the reference and do not assess privilege.
- Include any permit or permit condition referenced as breached, where the permit is not in the Permits table's unit.
- Exclude general statutes and regulations.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a closing or completion letter is referenced and absent, add `; closure unevidenced`.** Filter these first — a matter believed closed without regulator confirmation is the most common way an environmental history is understated.
- **Where an order, consent order, or agreement is absent, add `; obligations unreadable`.** The continuing obligations and the successor-binding provisions cannot be assessed without it.
- **Where an inspection report or notice is absent, add `; allegations unreadable`.**
- **Where an earlier matter is referenced in connection with a repeat violation, add `; prior matter, repeat violation`.** That matter should be its own row and may not have been produced.
- Where monitoring data underlying an allegation is absent, add `; underlying data missing`.
- Where a recorded restriction is absent, add `; continuing obligation unreadable`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon in this table.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; flag]`

Return no more than 15 lines and no more than 135 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Status verified with regulator or register** | Yes (date) / No / Not required |
| **Exposure estimate** | Free text |
| **Affects permit transfer or renewal** | Yes / No / Unassessed |
| **Criminal exposure** | None / Entity / Individual / Both / Unassessed |
| **Recovery route available** | None / Prior-owner indemnity / Insurance / Third party / Unassessed |
| **Disclosure schedule item** | Yes / No |
| **Special indemnity or escrow candidate** | Yes / No / Unassessed |
| **Continuing obligations post-closing** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** Environmental enforcement rows are few and each can affect a
permit transfer that gates closing, carry criminal exposure, or leave an obligation
running for decades.

### Reconciliation work that never belongs in a column

- **Open matters against permit transfers.** Every row whose `Resolution Status` is
  an `Open` state, matched to the affected permit in the Environmental — Permits
  table. **Several regimes require outstanding enforcement to be resolved before a
  permit is transferred or renewed**, which puts these rows on the closing critical
  path rather than the risk list.
- **Closure verification.** Every row with a `; closure unevidenced` flag, and
  every `Completion asserted by target, not confirmed` row. **Only a regulator
  document closes an environmental matter**, and a regulator can reject a
  completion report years later.
- **Missed deadlines.** Every
  `[deadline passed, completion not evidenced]` flag. Each is an independent
  violation, commonly penalised per day, and each needs immediate attention.
- **Status verification.** Every row with a `[status over 18 months old]` flag,
  checked against the regulator's public enforcement and compliance register.
  **Most environmental regulators publish these** and the data room will not
  contain everything.
- **Repeat violations.** Every `[repeat violation]` flag and every
  `; prior matter, repeat violation` reference. **Repeat violations drive penalty
  severity and, in several regimes, criminal exposure**, and the earlier matter may
  never have been produced.
- **Pattern detection.** Read across rows by `Media Affected`, by site, and by
  subject matter. **A pattern indicates a systemic control failure rather than
  isolated incidents**, which is a larger and different finding, and it also
  predicts how the regulator will treat the next one. Ask Assistant over the
  project; the answer is narrative.
- **Continuing obligations register.** Every `Continuing Obligations` entry,
  consolidated with the controlled conditions from the Assessments table, the
  permit conditions from the Permits table, and the recorded restrictions from Real
  Estate. **One register, with named owners, durations, and cost bearers** — these
  are the obligations most likely to be lost at closing and most expensive to
  rediscover.
- **Recovery routes.** Every prior-owner indemnity, contribution claim, and insurance
  notification, with its limits and expiry. **Preserve them in the transaction
  documents rather than losing them**, and check whether any expires shortly after
  closing.
- **Cost quantification.** Every open remediation obligation, scoped and costed by
  a consultant against the stated remedial standard, with the long-term monitoring
  duration included. **Never a Harvey column**, and the monitoring tail frequently
  exceeds the remediation itself.
- **Criminal exposure.** Every referral or charge, with counsel, including the
  position of individuals and the availability of indemnification and D&O cover.

---

## Test set

- [ ] Routine inspection with minor findings and a closing letter
- [ ] Complaint-driven inspection with a notice of violation following
- [ ] Notice of violation for a permit limit exceedance over three years
- [ ] Notice of violation for a single exceedance
- [ ] Notice of violation for unpermitted activity
- [ ] Notice of violation for failure to report an exceedance
- [ ] Notice of violation characterised as significant non-compliance
- [ ] Notice of violation described as a repeat violation
- [ ] Warning letter with no formal violation asserted
- [ ] Administrative order requiring equipment upgrade
- [ ] Cleanup order requiring soil and groundwater remediation to a residential standard
- [ ] Cleanup order with a remedial standard tied to industrial use
- [ ] Consent order with a supplemental environmental project
- [ ] Consent order with thirty-year monitoring and a successor-binding clause
- [ ] Consent order with a reopener triggered by a change of site use
- [ ] Penalty notice with a proposed per-day penalty
- [ ] Penalty notice with a final penalty reduced for cooperation
- [ ] Matter with a self-disclosure and penalty mitigation
- [ ] Spill report self-reported within the statutory period
- [ ] Spill report where a third party reported the release
- [ ] Matter with an upset or bypass defence asserted
- [ ] Matter where the target attributes cause to a contractor
- [ ] Matter with allegations partly accepted and partly disputed
- [ ] Matter with a remediation plan submitted and not approved
- [ ] Matter with a plan approved and no progress evidenced
- [ ] Matter with completion asserted by the target and not confirmed
- [ ] Matter with a regulator no-further-action letter
- [ ] Matter with a conditional closure containing a reopener
- [ ] Matter with a remediation deadline passed and no completion evidenced
- [ ] Matter with a recorded activity and use limitation
- [ ] Matter requiring an independent supervising consultant at the target's cost
- [ ] Matter referred to the regulator's enforcement division
- [ ] Matter referred to another regulator
- [ ] Matter referred to a prosecuting authority
- [ ] Matter with criminal charges against the entity and an individual
- [ ] Matter with a citizen suit notice of intent referenced
- [ ] Matter where escalation was threatened if a deadline was missed
- [ ] Matter naming the target among several potentially responsible parties
- [ ] Matter with a prior-owner indemnity referenced from an earlier acquisition
- [ ] Matter notified to an environmental liability insurer and declined on known conditions
- [ ] Matter concerning off-site disposal at a third-party facility
- [ ] Matter concerning a site the target no longer owns
- [ ] Matter naming an environmental manager individually
- [ ] Matter open with the latest document a regulator request and no response
- [ ] Matter whose latest document is three years old with no closure
- [ ] Matter referenced as closed with the closing letter not produced
- [ ] Matter referencing an earlier inspection not produced
- [ ] Matter file marked privileged as an environmental audit
- [ ] Unit mistakenly containing two matters

Then test the dependencies: change `Required Corrective Action` from stated
actions to `None required` and confirm `Action Deadline` and
`Remediation Evidenced` both move to `Not applicable`. Change
`Alleged Violation` to `None stated` and confirm `Target Response` re-runs.
Change `Matter Type` from `Notice of violation` to `Information request` and
confirm `Alleged Violation` and `Media Affected` re-run against the request rules.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
