# Prompt Inventory — Regulatory: Correspondence and Examinations

Table 17 of the POC. Companion to Regulatory — Licences.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Regulatory`
- Review unit: **one regulatory matter** — the initiating communication, the
  target's response, any follow-up correspondence, any report or findings, and any
  closing or resolution letter produced for it
- Grouping used: **yes**, typically 1–8 documents per unit
- Intended reviewers and downstream use: regulatory and corporate/M&A teams; feeds
  the compliance history for the change-of-control filing, the disclosure
  schedule, and the coverage register
- Inventory version: v1.0

### Why this is separate from Licences

A licence is a Filing, read for status and effectiveness. Regulator
correspondence is Correspondence, read for the chronology and the assertion made.
An examination report is Analysis, read for scope and limitation. They cannot
share a schema, and the original single Regulatory table mixed all three.

### Why it matters more than it looks

Two reasons a buyer cares about this table beyond the underlying breaches:

1. **Compliance history is an input to the change-of-control approval.** A
   regulator deciding whether to approve a new controller looks at how the
   business has been supervised. An open enforcement matter can delay or condition
   an approval that would otherwise be routine, which puts this table on the
   critical path alongside Licences.
2. **An open matter is an inherited obligation with a deadline.** Remediation
   commitments, undertakings, and reporting obligations continue past closing, and
   they are frequently undocumented anywhere else.

### The boundary with Litigation

**Regulatory enforcement stays here until proceedings are commenced in a court or
tribunal.** An information request, an examination, a warning letter, a consent
order, and an administrative penalty are all rows here. A regulator suing in court
is a Litigation row. Where a matter crosses the line, it appears in both, and
`Escalation Status` is where the crossing is recorded.

## Assumptions to confirm before running

1. One row is one matter, not one letter. An examination generating a request, a
   report, a response, and a closing letter is one row.
2. **Routine periodic filings are not rows.** An annual return with no regulator
   response is a compliance activity, not a matter. Where a filing drew a query,
   the query and its resolution are a row.
3. Environmental enforcement is a separate table in the Environmental workstream.
4. Tax audits and revenue correspondence are separate tables in the Tax workstream.
5. Buy-side review; the entities in the Table Instructions list are the target
   group.
6. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

17 Harvey columns plus 8 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side regulatory diligence on the target group listed below. This table reviews correspondence with regulators, examinations, and enforcement matters short of court proceedings.

One row is one regulatory matter: the initiating communication, the target's response, any follow-up correspondence, any report or findings, and any closing or resolution letter produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the matter or the regulator.
- **Report the position as at the most recently dated document in the unit, and identify that document.** A regulatory matter moves and a cell without a date is not usable.
- **Distinguish what the regulator asserts from what the target accepts.** A finding in an examination report is the regulator's view; the target's response may dispute it. Report both and label each. Do not adopt either.
- **Do not assess the merits of any finding, the likelihood of enforcement, or the size of any exposure.** All three are legal judgements and all three are human columns.
- **Report privilege and confidentiality markings where present** and do not assess privilege. Regulator correspondence is frequently confidential by statute, and some of it may not be disclosable to a buyer at all.
- Report figures only as the documents state them. Do not calculate or total.
- Use entity and regulator names exactly as printed. **Do not report the names of individual employees; describe them by role.**
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
  Regulator
  Recipient Entity
  Related Licence or Registration
  Initiated Date

Stage 2 — Status
  Documents in Unit ──→ Resolution Status
                        Referenced but Not Produced
  Resolution Status ──→ Status As-Of Date

Stage 3 — Substance, routed on matter type
  Matter Type ──→ Subject Matter
                  Findings or Allegations
                  Scope and Limitations

Stage 4 — Consequences
  Findings or Allegations ──→ Target Response
  Required Actions ──→ Action Deadline
                       Remediation Evidenced
  Penalty or Sanction
  Continuing Obligations

Stage 5 — Escalation
  Escalation Status
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Resolution Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Matter Type | Classify | — | Subject Matter; Findings or Allegations; Scope and Limitations | v1.0 | draft |
| 3 | Regulator | Free Response | — | — | v1.0 | draft |
| 4 | Recipient Entity | Free Response | — | — | v1.0 | draft |
| 5 | Related Licence or Registration | Free Response | — | — | v1.0 | draft |
| 6 | Initiated Date | Date | — | — | v1.0 | draft |
| 7 | Resolution Status | Classify | @Documents in Unit | Status As-Of Date | v1.0 | draft |
| 8 | Status As-Of Date | Date | @Resolution Status | — | v1.0 | draft |
| 9 | Subject Matter | Free Response | @Matter Type | — | v1.0 | draft |
| 10 | Findings or Allegations | Free Response | @Matter Type | Target Response | v1.0 | draft |
| 11 | Scope and Limitations | Free Response | @Matter Type | — | v1.0 | draft |
| 12 | Target Response | Free Response | @Findings or Allegations | — | v1.0 | draft |
| 13 | Required Actions | Free Response | — | Action Deadline; Remediation Evidenced | v1.0 | draft |
| 14 | Action Deadline | Date | @Required Actions | — | v1.0 | draft |
| 15 | Remediation Evidenced | Classify | @Required Actions | — | v1.0 | draft |
| 16 | Penalty or Sanction | Free Response | — | — | v1.0 | draft |
| 17 | Continuing Obligations | Free Response | — | — | v1.0 | draft |
| 18 | Escalation Status | Classify | — | — | v1.0 | draft |
| 19 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

19 columns — two more than estimated. `Scope and Limitations` was added because an
examination report is an Analysis document and reading one without its scope is
the failure the taxonomy warns about; `Target Response` was separated from
`Findings or Allegations` so that a disputed finding is never reported as an
accepted one.

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

- Include the initiating communication, information and document requests, the target's responses and submissions, examination or inspection reports, findings letters, warning or caution letters, notices of violation, proposed and final orders, undertakings, penalty notices, remediation plans, progress reports, and any closing, no-further-action, or resolution letter.
- Include internal memoranda about the matter only where they are the only record of a response.
- Treat schedules and appendices attached to a document as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title or subject line. Where none is printed, describe it in five words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Initiating communication`, `Information request`, `Target response`, `Examination report`, `Findings letter`, `Warning letter`, `Notice of violation`, `Proposed order`, `Final order`, `Undertaking`, `Penalty notice`, `Remediation plan`, `Progress report`, `Closing letter`, or `Other`.
- **State who sent each document — the regulator or the target — since the alternation is the chronology.**
- **Where the most recent document is from the regulator and no target response follows, note that in the evidence field.** An unanswered regulator communication is a finding in itself.
- Where a document relates to a different matter, still list it and append ` [relates to [matter]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [from regulator | from target] — [Title] ([Function])`

Return no more than 15 lines and no more than 130 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Matter Type

- Native type: Classify
- Configured options, in UI order: `Information or document request`, `Routine examination or inspection`, `Targeted or for-cause examination`, `Warning or caution letter`, `Notice of violation or deficiency`, `Formal investigation`, `Enforcement action`, `Consent order or settlement`, `Undertaking given`, `Self-report by target`, `Approval or no-action request`, `Guidance or interpretive request`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Subject Matter`, `Findings or Allegations`, `Scope and Limitations`
- Purpose: what kind of matter this is, which routes the substantive columns and
  determines how seriously the row reads.

```markdown
## Task

Classify the nature of this regulatory matter. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits, since the order runs from most to least serious.

1. `Consent order or settlement`: the matter concluded, or is proposed to conclude, in an agreed order, settlement, or assurance of discontinuance. **These carry continuing obligations** and they are usually public.
2. `Enforcement action`: the regulator has commenced or concluded a formal action seeking a penalty, suspension, revocation, or other sanction, short of court proceedings.
3. `Formal investigation`: the regulator has opened a formal investigation or inquiry, whether or not an action has followed. Distinguished from an examination because the purpose is to determine whether to take action.
4. `Undertaking given`: the target has given a formal undertaking or commitment to the regulator, whether or not following an action.
5. `Notice of violation or deficiency`: the regulator has asserted a specific breach, deficiency, or matter requiring attention.
6. `Warning or caution letter`: the regulator has expressed concern or issued a warning without asserting a formal violation. **Not trivial** — a warning letter is frequently the step before an investigation, and a pattern of them matters more than any single one.
7. `Targeted or for-cause examination`: an examination prompted by a specific concern, complaint, or event. **Materially different from a routine cycle examination** and the distinction should never be lost.
8. `Routine examination or inspection`: a scheduled or cycle examination.
9. `Self-report by target`: the target notified the regulator of a breach or incident on its own initiative. **Report this as such** — self-reporting is generally viewed favourably and the characterisation matters to how the compliance history reads.
10. `Formal investigation` and the states above take precedence over `Information or document request` even where the file opens with a request.
11. `Approval or no-action request`: the target sought an approval, waiver, exemption, or no-action position.
12. `Guidance or interpretive request`: the target sought guidance on the application of a rule.
13. `Information or document request`: the regulator sought information with no stated concern.

**An information request may be the opening of something more serious.** Where the documents indicate a concern behind the request, classify on the concern.

## Fallback rules

- Use `Other` where the matter is regulatory but none of the options describes it.
- Use `Unable to determine` where the documents are too fragmentary to identify the nature of the matter.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Regulator

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which authority, which is the join key to the Licences table and the
  basis for reading the compliance history by regulator.

```markdown
## Task

State the authority conducting or initiating this matter.

## Rules

- Report the authority exactly as printed, including the specific division, bureau, enforcement unit, or examination team where stated.
- **Report any case officer's role rather than their name**, for example `enforcement counsel`, `examining officer`.
- Report any case, file, or matter reference the regulator has assigned, exactly as printed. **It is the key for any enquiry to the regulator and for the change-of-control filing disclosure.**
- Where more than one authority is involved — a joint examination, or a referral from one body to another — report each and label its role. **A referral to a criminal or prosecuting authority is a material escalation** and it should also appear in Escalation Status.
- Where the authority is a self-regulatory organisation or a delegate, report it and the ultimate authority.

## Fallback rules

- Return `Unable to determine` where the documents do not identify the authority.

## Output format

`[Authority as printed][ — [division or unit]][; reference: [as printed]]`, with any additional authority labelled.

Return no more than 45 words.
```

---

### 4. Recipient Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity is the subject, which determines whether the matter
  follows the business in a carve-out.

```markdown
## Task

State the target-group entity that is the subject of or party to this matter.

## Rules

- Use the review-subject list in the Table Instructions to determine which named entities are group entities.
- Report each name exactly as printed, including entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- Where more than one group entity is a subject, list each.
- **Where an individual — a director, officer, or approved person — is a subject of the matter alongside or instead of the entity, report the entity and note the individual's role in the evidence field.** Do not report the individual's name. A matter directed at an individual engages the indemnification, D&O, and employment analyses.
- Where the entity named is not on the review-subject list, report the name and append ` (not a listed entity)`.
- **Where the matter is addressed to a parent or affiliate but concerns the target's activities, report both and label each**, since it determines who carries the obligation.

## Fallback rules

- Return `Unable to determine` where the subject cannot be identified.

## Output format

`[Exact legal name]` per line, with any qualifier appended. Return no more than 40 words. Do not name individuals.
```

---

### 5. Related Licence or Registration

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which authorisation the matter attaches to, so the row joins the
  Licences table. **An open matter against a licence is an input to that licence's
  change-of-control approval.**

```markdown
## Task

Identify any licence, permit, registration, or authorisation this matter relates to.

## Rules

- Report the authorisation as the documents name it, with its number exactly as printed.
- **The number is the join key to the Regulatory — Licences table**, so report it without reformatting.
- Where the matter relates to more than one authorisation, list each.
- Where the matter relates to the target's activities generally rather than to a specific authorisation, say so.
- **Where the matter concerns activity conducted without an authorisation**, report that and append ` [unlicensed activity alleged]`. This is among the most serious findings available in the workstream and it may not appear in the Licences table at all, because there is no licence to be a row.
- Where the matter relates to an authorisation held by a different entity in the group, report it and name that entity.

## Fallback rules

- Return `Not applicable — general conduct matter` where the matter does not attach to a specific authorisation.
- Return `Unable to determine` where the authorisation cannot be identified.

## Output format

`[Authorisation as named] — [number as printed]` per line, with any bracketed flag appended.

Return no more than 40 words.
```

---

### 6. Initiated Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the matter began, which shows how long it has been running and
  whether it predates a change in management or a prior transaction.

```markdown
## Task

Identify the date this matter was initiated.

## Date-selection hierarchy

1. Use the date of the earliest communication from the regulator in the unit.
2. Where the matter is a self-report, use the date of the target's report.
3. Where the earliest document refers to an earlier communication not in the unit, use the date of that earlier communication as stated, and note in the evidence field that it is taken from a reference.

## Excluded dates

- The date of the conduct or period under examination. **Report that period in the evidence field**, since the gap between the conduct and the regulator's attention is informative
- The date of the target's response
- The date of any report or findings letter
- File name and metadata dates, and transmittal and scan dates

## Rules

- **Report the period under review or examination in the evidence field where the documents state it.** A 2024 examination covering 2019 to 2022 conduct tells a reviewer the exposure is historic, which bears on whether the seller or the buyer carries it.
- Compare the initiated date to the diligence as-of date. **Where the matter has been running more than eighteen months and Resolution Status is not closed, append ` [open over 18 months]`.** A long-running open matter usually means either a substantial issue or a stalled file, and both are worth a look.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended. Preserve partial precision as printed. Return `Not stated` where no initiation date can be selected.
```

---

### 7. Resolution Status

- Native type: Classify
- Configured options, in UI order: `Open, awaiting target response`, `Open, awaiting regulator response`, `Open, remediation in progress`, `Closed, no action taken`, `Closed, findings remediated`, `Closed with sanction`, `Concluded by consent order`, `Referred or escalated`, `Dormant`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Status As-Of Date`
- Purpose: where the matter stands on the documents.

**The `Open, awaiting target response` state is the one to filter first.** An
outstanding regulator request with no response in the file is either a live
deadline the business has missed or a document that was not produced, and both need
resolving before the change-of-control filing discloses the matter.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document and who sent it. Confirm the status against that document.

## Task

Classify the status of this matter as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Referred or escalated`: the documents record a referral to another authority, to a prosecuting body, or to court proceedings. **Also record this in Escalation Status.**
2. `Concluded by consent order`: the matter concluded in an agreed order, settlement, or assurance. **Continuing obligations almost always follow** and they are reported in Continuing Obligations.
3. `Closed with sanction`: the regulator imposed a penalty, censure, restriction, or other sanction and the matter is recorded as concluded.
4. `Closed, findings remediated`: the regulator confirmed closure following remediation, or issued a no-further-action letter after the target addressed findings.
5. `Closed, no action taken`: the regulator closed the matter without findings or action.
6. `Open, remediation in progress`: findings are accepted or unchallenged and remediation is underway, with no closure recorded.
7. `Open, awaiting regulator response`: the target's most recent submission or response is the latest document, with no regulator reply.
8. `Open, awaiting target response`: a regulator communication requiring a response is the latest document, with no target response in the unit. **Filter these first.**
9. `Dormant`: the most recent document is more than two years before the diligence as-of date and no closure is recorded. **Do not treat this as closed** — it may mean the file was not produced in full, and an unresolved regulatory matter does not lapse merely through inactivity.

**Closure must be evidenced by a document.** Do not infer closure from the passage of time, from a remediation plan, or from a target's internal note recording the matter as closed.

## Fallback rules

- Use `Unable to determine` where documents of the same date conflict, or where the most recent document is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Status As-Of Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Resolution Status`
- Downstream: none
- Purpose: the date the status speaks as of. **Regulatory files in data rooms are
  routinely incomplete**, and an open matter reported from a two-year-old document
  cannot be relied on.

```markdown
## Established result

- Resolution status: @Resolution Status

## Task

Identify the date of the most recently dated document in the review unit, which is the date as of which the status is reported.

## Rules

- Report the date of the most recent document, and state in the evidence field who sent it.
- **Prefer the most recent document bearing on the status** — a regulator communication, a target response, a report, an order, or a closing letter — over routine acknowledgements of a later date. Where a later routine document exists, report the substantive document's date and note the later one.
- Compare the reported date to the diligence as-of date in the Table Instructions and flag the gap:
  - more than six months: append ` [status over 6 months old]`
  - more than eighteen months: append ` [status over 18 months old]`
- **Where Resolution Status is any `Open` state and the flag is `[status over 18 months old]`, the row needs verification with the regulator or with the target's compliance function before it can be relied on.** That combination is the most common reason a compliance history is understated.

## Fallback rules

- Return `Not stated` where no document in the unit bears a date.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended.
```

---

### 9. Subject Matter

- Native type: Free Response
- Upstream: `@Matter Type`
- Downstream: none
- Purpose: what the matter is about, in enough detail for pattern recognition and
  for linking to another workstream.

```markdown
## Established result

- Matter Type: @Matter Type

## Task

Describe what this matter concerns, in two sentences or fewer.

## Rules

- Identify the rule, requirement, or area of regulation in issue, named as the documents name it.
- Identify the activity, product, service, process, or business line concerned, so the row can be linked to the commercial workstream.
- **Report the period the conduct or the review covers where stated.**
- **Describe the regulator's concern neutrally.** Use language such as `the regulator queried`, `the regulator asserted`, or `the notice alleges`. Do not describe alleged conduct as having occurred and do not adopt the regulator's characterisation as fact.
- **Do not name individual employees.** Describe them by role.
- Where the matter arose from a complaint, an incident, a whistleblower report, or a referral, say so, since the origin bears on how it is likely to develop.
- Do not summarise the findings; those have their own column.
- Do not assess the merits or the seriousness.

## Fallback rules

- Return `Unable to determine` where the documents do not identify what the matter concerns.

## Output format

Two sentences or fewer, no more than 55 words. Do not include quotations, section numbers, citation markers, or individual names.
```

---

### 10. Findings or Allegations

- Native type: Free Response
- Upstream: `@Matter Type`
- Downstream: `Target Response`
- Purpose: what the regulator actually said, kept strictly separate from what the
  target accepted.

```markdown
## Established result

- Matter Type: @Matter Type

## Task

Report the findings, deficiencies, or allegations the regulator has stated in this matter.

## Applicability

- Applies where Matter Type is `Routine examination or inspection`, `Targeted or for-cause examination`, `Warning or caution letter`, `Notice of violation or deficiency`, `Formal investigation`, `Enforcement action`, `Consent order or settlement`, or `Self-report by target`.
- Where Matter Type is `Information or document request`, `Approval or no-action request`, or `Guidance or interpretive request`, report any concern the regulator has expressed, and where none is expressed return `None stated`.

## Rules

- Report each finding in ten words or fewer, with the rule or requirement it relates to as the documents identify it.
- **Report the regulator's own severity characterisation exactly as printed** — material weakness, significant deficiency, matter requiring attention, minor, or a numbered or graded scale. **Do not translate between scales and do not assign a severity the regulator did not.**
- **Report findings as the regulator's assertions**, using `the regulator found` or `the notice alleges`. The target's position is a separate column and the two must never be merged.
- Report the stated number of findings by severity where the documents give counts.
- **Report any finding the regulator describes as repeat, recurring, or previously identified, and flag it.** A repeat finding is treated far more seriously by regulators than a first occurrence, and it is a strong signal about the compliance function.
- **Report any finding the regulator states affects customers, client money, or the public**, since those attract different treatment.
- Report no more than eight findings. Where more exist, report the eight most severe and append ` and [N] further findings`.
- Do not assess whether any finding is correct or whether it has been remediated.

## Fallback rules

- Return exactly `None stated` where the regulator has stated no finding or allegation.
- Return `Unable to determine` where the findings are illegible or their severity cannot be read.

## Output format

`Counts as stated: [severity: N]` where given, followed by one line per finding:

`[Severity as printed] — [finding] — [rule as identified][; repeat finding]`

Return no more than 8 lines and no more than 100 words.
```

---

### 11. Scope and Limitations

- Native type: Free Response
- Upstream: `@Matter Type`
- Downstream: none
- Purpose: what the examination actually covered.

**An examination report is an Analysis document**, and the taxonomy's rule applies:
it is read for scope and limitation as much as for conclusion. A clean report over
one business line says nothing about the others.

```markdown
## Established result

- Matter Type: @Matter Type

## Task

Report the scope of the regulator's review and any limitation the documents state.

## Applicability

- Applies where Matter Type is `Routine examination or inspection`, `Targeted or for-cause examination`, `Formal investigation`, or `Enforcement action`.
- For other matter types, report any stated scope of an information request, and otherwise return `Not applicable`.

## Include where expressly stated

- The period reviewed
- **The business lines, products, entities, or locations covered, and any expressly excluded**
- The rules, requirements, or regulatory areas examined
- The method: on-site, remote, desk-based, thematic, or sample-based
- **Any sampling approach, including the sample size and how it was selected**
- Any statement that the review was limited in scope, time, or resource
- Any statement that the regulator did not review a stated area
- Any statement that the absence of a finding is not assurance of compliance
- Any area the regulator identified for a future review

## Rules

- **Report the covered and excluded scope as prominently as each other.** A clean examination covering only one of five business lines is not a clean bill of health, and the exclusion is the finding.
- **Report the sampling basis where stated.** Findings from a sample of ten transactions imply a population, and the regulator usually says so.
- **Report any statement that a future review is intended**, since it is a scheduled event the buyer inherits.
- Report the scope as stated. Do not assess whether it was adequate.

## Fallback rules

- Return `Not stated` where the documents describe no scope.
- Return `Not applicable` where the matter type has no review scope.
- Return `Unable to determine` where the scope description is illegible or inconsistent.

## Output format

`Period: [as stated]; covered: [as stated]; excluded: [as stated or "none stated"]; method: [as stated]; sampling: [as stated or "Not addressed"]; future review: [as stated or "none"]`

Return no more than 80 words.
```

---

### 12. Target Response

- Native type: Free Response
- Upstream: `@Findings or Allegations`
- Downstream: none
- Purpose: what the target said back. **A disputed finding and an accepted finding
  are entirely different facts**, and merging them into a single findings column is
  the failure this separation prevents.

```markdown
## Established result

- Findings or allegations: @Findings or Allegations

## Task

If Findings or Allegations reported findings, report the target's response to them.

If it returned `None stated`, report any substantive response the target made to the regulator, and where none is in the unit return `No response in unit`.

If it returned `Unable to determine`, return exactly `Unable to determine — upstream findings unresolved`.

## Include where expressly stated

- Which findings the target accepted, in whole or in part
- **Which findings the target disputed, and on what basis in eight words or fewer**
- Any admission or express denial
- Any explanation of cause offered — systems, process, staffing, third party, or interpretation
- Any remediation the target proposed or reported as already completed
- Any request for an extension, a reconsideration, or a meeting
- Any statement that the target had already identified the issue before the regulator did
- Whether the response was made by the target, by counsel, or by a third-party consultant
- The date of the response

## Rules

- **Report acceptance and dispute separately, finding by finding where the documents allow it.** An accepted finding is an inherited obligation; a disputed one is a contingency, and the buyer prices them differently.
- **Report where the target states it had already identified the issue**, since a self-identified issue reads very differently in a compliance history.
- **Report where no response appears in the unit and one was required.** That is either a missed deadline or a production gap, and Resolution Status carries the flag.
- Report the response as made. **Do not assess whether it is likely to succeed** and do not adopt it.
- Do not name individuals.

## Fallback rules

- Return `No response in unit` where the documents contain no target response.
- Return `Not applicable` where the matter type required no response.

## Output format

`Accepted: [findings or "none"]; disputed: [findings and basis, or "none"]; cause offered: [brief or "none"]; self-identified: [yes | Not addressed]; responded by: [target | counsel | consultant]; dated [YYYY-MM-DD]`

Return no more than 85 words.
```

---

### 13. Required Actions

- Native type: Free Response
- Upstream: none
- Downstream: `Action Deadline`, `Remediation Evidenced`
- Purpose: what the business has to do. **These are inherited obligations with
  deadlines**, and they frequently appear nowhere else in the data room.

```markdown
## Task

Report the actions the regulator requires, or the target has committed to take, in this matter.

## Include where expressly stated

- Each required action, whether imposed by the regulator or offered by the target
- **Any requirement to change a system, process, policy, or control**
- Any requirement to appoint a monitor, independent consultant, skilled person, or auditor. **This is a substantial and continuing cost** and it is usually the most burdensome outcome short of a sanction
- Any requirement to remediate or compensate customers, and the population affected
- Any requirement to conduct a lookback review, and the period
- Any requirement to train staff or to make personnel or governance changes
- Any requirement to report progress, and on what frequency
- Any requirement to notify the regulator on completion
- Any restriction on business activity pending completion
- Any requirement to file amended returns or corrected disclosures

## Rules

- **Report any customer remediation or redress requirement prominently, with the affected population as stated.** A redress exercise is a quantifiable liability and it is often the largest financial consequence of a regulatory matter.
- **Report any monitor or skilled-person appointment prominently**, including who bears the cost.
- **Report any restriction on business activity**, since it constrains operations immediately.
- Report each action in eight words or fewer, and identify whether it was imposed or volunteered.
- Report figures and populations as stated. **Do not estimate a remediation cost or the size of an affected population.**

## Fallback rules

- Return exactly `None required` where the documents impose and record no required action.
- Return `Unable to determine` where required actions conflict or are illegible.

## Output format

One line per action:

`[Action] — [imposed | volunteered] — [reporting frequency or "none"]`

Return no more than 8 lines and no more than 95 words.
```

---

### 14. Action Deadline

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Required Actions`
- Downstream: none
- Purpose: the next deadline. **A deadline in the deal period is a task with an
  owner; a passed deadline with no evidence of completion is a live breach.**

```markdown
## Established result

- Required actions: @Required Actions

## Task

If Required Actions reported one or more actions, identify the earliest deadline for any of them.

If it returned `None required`, return exactly `Not applicable`.

If it returned `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the earliest deadline the documents state, with what it is for in five words or fewer.
- Include deadlines for remediation, for progress reports, for notification of completion, for a lookback review, and for a response to any outstanding request.
- Report only dates the documents state. **Do not calculate a deadline from a period, a rule, or the date of a communication.**
- Where several deadlines are stated, report the earliest after the diligence as-of date and note the count of later ones in the evidence field.
- **Where a stated deadline falls before the diligence as-of date and Remediation Evidenced does not show completion, report that date and append ` [deadline passed, completion not evidenced]`.** This is the single most actionable flag in the table: an unmet regulatory deadline is a fresh breach on top of the original finding.
- Where an extension was granted, report the extended date and append ` (extended from [date])`.

## Fallback rules

- Return `Not stated` where actions are required and the documents state no deadline. **Report in the evidence field any period stated, such as within 90 days**, without converting it to a date.

## Output format

`YYYY-MM-DD — [what it is for]`, with any bracketed flag or qualifier appended, or one of the exact fallback values above.
```

---

### 15. Remediation Evidenced

- Native type: Classify
- Configured options, in UI order: `Completion confirmed by regulator`, `Completion asserted by target, not confirmed`, `In progress per documents`, `Plan submitted, no progress evidenced`, `No evidence of remediation`, `Not applicable`, `Unable to determine`
- Upstream: `@Required Actions`
- Downstream: none
- Purpose: whether the required actions were actually done, and on whose word.

**Confirmation by the regulator and assertion by the target are different
evidence.** The first closes a matter; the second is a claim the buyer may be
inheriting untested, and the distinction is what this column exists to preserve.

```markdown
## Established result

- Required actions: @Required Actions

## Task

If Required Actions reported one or more actions, classify what the documents evidence about their completion.

If it returned `None required`, return `Not applicable`.

If it returned `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Completion confirmed by regulator`: a regulator communication in the unit confirms that the required actions have been completed satisfactorily, or closes the matter on that basis. **The only state that fully discharges the obligation.**
2. `Completion asserted by target, not confirmed`: the target has reported completion and no regulator confirmation appears. **The obligation may still be live** and the regulator may yet disagree, which is why this is not merged with the state above.
3. `In progress per documents`: progress reports or correspondence show work underway and not complete.
4. `Plan submitted, no progress evidenced`: a remediation plan was submitted and nothing evidences work against it.
5. `No evidence of remediation`: actions were required and the documents show nothing done.

**Where completion is partial** — some actions confirmed, others outstanding — classify on the **least** complete state and report the split in the evidence field. The row should overstate an open obligation rather than hide one.

**Do not infer completion from the passage of time, from the absence of further regulator contact, or from a target's internal note.**

## Fallback rules

- Use `Unable to determine` where the documents conflict about completion or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Penalty or Sanction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the matter cost, and whether it is public. **A published sanction
  is a reputational and disclosure fact independent of the money.**

```markdown
## Task

Report any penalty, fine, or sanction imposed, proposed, or agreed in this matter.

## Include where expressly stated

- Any monetary penalty, fine, or civil money penalty, with the amount and whether it is proposed, agreed, or final
- Any disgorgement, restitution, or customer redress amount, distinguished from a penalty
- Any censure, reprimand, or public statement
- **Whether the sanction is or will be published**, and where
- Any suspension, restriction, or condition imposed on an authorisation. **Also report this in the Licences table's Open Findings column**
- Any revocation or refusal to renew
- Any prohibition, disqualification, or condition imposed on an individual, described by role
- Any costs the target must pay
- Any reduction applied for cooperation, early settlement, or self-reporting, and the discount stated
- Any statement that no penalty was imposed

## Rules

- **Report whether a penalty is proposed, agreed, or final.** A proposed penalty is a negotiation position and a final one is a debt, and treating them alike overstates or understates the exposure.
- **Report publication prominently.** A published enforcement notice affects the change-of-control filing, customer relationships, and the disclosure schedule, and it cannot be undone.
- **Report any redress or restitution amount separately from any penalty**, since redress is usually the larger figure and it scales with the affected population.
- **Report any cooperation or self-report discount**, since it evidences how the target conducted itself.
- Report amounts as stated. **Do not total penalty and redress, and do not calculate an aggregate exposure.**
- Report any individual sanction by role only.

## Fallback rules

- Return exactly `None imposed` where the documents record no penalty or sanction.
- Return `Unable to determine` where amounts or sanctions conflict or are illegible.

## Output format

`Penalty: [amount, currency, [proposed | agreed | final]]; redress: [amount or "none"]; censure: [as stated or "none"]; published: [yes, [where] | no | Not addressed]; authorisation effect: [as stated or "none"]; individual sanction: [role and sanction, or "none"]`

Return no more than 85 words.
```

---

### 17. Continuing Obligations
 
- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what survives the matter's closure. **The obligations a consent order
  or undertaking leaves behind follow the business to the buyer**, and they are the
  reason a closed matter is not always a finished one.

```markdown
## Task

Report any obligation arising from this matter that continues after its resolution.

## Include where expressly stated

- Any undertaking given to the regulator, and its duration
- **Any continuing reporting or attestation obligation, and its frequency and end date**
- Any monitor, skilled person, or independent consultant engagement continuing, and who bears the cost
- Any requirement to maintain a changed system, control, policy, or governance arrangement
- Any restriction on business activity, product, or growth continuing after closure
- Any prohibition or condition applying to an individual, described by role
- Any commitment to a future review, audit, or examination
- **Any obligation to notify the regulator of a change of control, ownership, or management arising from this matter specifically**, as distinct from the licence's own requirement
- Any provision stating that the obligations bind successors
- Any provision under which the matter can be reopened, and on what trigger

## Rules

- **Report the duration of each obligation, and where none is stated say so.** An undertaking with no end date is permanent until the regulator releases it.
- **Report any successor-binding provision prominently.** It is what makes the obligation the buyer's problem rather than the seller's.
- **Report any reopening trigger**, since a matter that can be revived on a further breach is a contingent exposure rather than a closed one.
- **Report any monitor engagement with its cost bearer**, since a continuing monitorship is a material operating cost and an intrusion on management.
- Report the obligations as stated. **Do not assess their burden or estimate their cost.**

## Fallback rules

- Return exactly `None` where the matter leaves no continuing obligation.
- Return `Not applicable` where the matter is not resolved, so continuing obligations cannot yet arise. **Note that required actions in an open matter are reported in Required Actions**, not here.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

One line per obligation:

`[Obligation] — [duration or "no end date stated"] — [cost bearer where stated]`, then a final line: `Binds successors: [yes | Not addressed]; reopening trigger: [brief or "none"]`

Return no more than 8 lines and no more than 95 words.
```

---

### 18. Escalation Status

- Native type: Classify
- Configured options, in UI order: `No escalation`, `Referred to enforcement division`, `Referred to another regulator`, `Referred to prosecuting or criminal authority`, `Court or tribunal proceedings commenced`, `Escalation threatened, not effected`, `De-escalated or downgraded`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the matter has moved, or may move, beyond routine supervision.

**Also the boundary marker with the Litigation table.** Where proceedings have
been commenced, the matter is a Litigation row as well as this one, and this column
records the crossing.

```markdown
## Task

Classify whether this matter has been escalated beyond routine supervision. Choose exactly one configured option.

## Scope

- Consider referrals within the regulator, referrals to other authorities, and the commencement of proceedings.
- Consider any statement by the regulator that escalation is contemplated.
- Exclude the ordinary progression from an information request to an examination finding.

## Classification rules

Apply the first rule that fits.

1. `Referred to prosecuting or criminal authority`: the documents record a referral to a prosecutor, criminal investigation authority, or fraud agency. **The most serious state available.** Report in the evidence field whether individuals are within the referral, described by role.
2. `Court or tribunal proceedings commenced`: the regulator has commenced proceedings in a court or tribunal. **This matter is also a Litigation row**, and the reviewer should confirm it appears there.
3. `Referred to another regulator`: the matter has been referred or reported to a different authority, whether in the same jurisdiction or another. Note in the evidence field which authority, since it creates a second supervisory relationship.
4. `Referred to enforcement division`: the matter has moved from supervision or examination to a formal enforcement function within the same regulator. **A significant step** and usually explicit in the correspondence.
5. `Escalation threatened, not effected`: the regulator has stated that it may refer, escalate, or take formal action if a condition is not met. **Report the condition and any deadline in the evidence field** — this is a contingent escalation the buyer can often still prevent.
6. `De-escalated or downgraded`: the documents record a matter being returned to supervision, a finding downgraded, or an enforcement referral closed without action.
7. `No escalation`: the matter has remained within routine supervision or examination.

## Fallback rules

- Use `Unable to determine` where references to escalation are too incomplete to classify.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this matter file refers to that is not present.
  **Regulatory files are among the most incompletely produced in any data room.**

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this matter that the documents in this unit refer to and that is not present.

## Scope

- **Include any examination report, findings letter, or order referenced but not produced.**
- **Include any target response or submission referenced but not produced.**
- **Include any closing, no-further-action, or resolution letter referenced but not produced.** Without it, closure is unevidenced regardless of what anyone believes
- Include information requests and the target's document productions referenced.
- Include remediation plans, progress reports, and completion notifications referenced.
- Include any monitor, skilled person, or consultant report referenced.
- Include any consent order, undertaking, or settlement document referenced.
- Include any earlier examination or matter the documents refer to, particularly where a finding is described as a repeat.
- Include any internal investigation report or legal advice referenced, **noting that these may be privileged**; report the reference and do not assess privilege.
- Include any customer redress or lookback report referenced.
- Include any published notice or press release referenced.
- Exclude statutes, regulations, and rulebooks, **except where a specific rule or guidance provision is identified as the basis of a finding**, in which case list it.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a closing or resolution letter is referenced and absent, add `; closure unevidenced`.** Filter these first — a matter believed closed with no closing letter is the most common way a compliance history is understated.
- **Where an examination report or findings letter is absent, add `; findings unreadable`.**
- **Where an earlier matter is referenced in connection with a repeat finding, add `; prior matter, repeat finding`.** That earlier matter should be its own row and may not have been produced at all.
- Where a monitor or consultant report is absent, add `; independent assessment missing`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon in this table.

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
| **Status verified with regulator or compliance** | Yes (date) / No / Not required |
| **Exposure assessment** | Free text |
| **Affects change of control approval** | Yes / No / Unassessed |
| **Disclosure schedule item** | Yes / No |
| **Special indemnity candidate** | Yes / No |
| **Continuing obligations post-closing** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** Regulatory matters are few and each one can affect an
approval that gates closing.

### Reconciliation work that never belongs in a column

- **Compliance history for the filing.** Every row collated by regulator and by
  authorisation, into the disclosure the change-of-control application will
  require. **An undisclosed matter discovered by the regulator is far worse than a
  disclosed one**, and this is the table that prevents it.
- **Open matters against the Licences table.** Every row whose
  `Resolution Status` is an `Open` state, matched to the affected licence.
  **An open matter can delay or condition an approval that would otherwise be
  routine**, which puts it on the closing critical path.
- **Status verification.** Every row with a `[status over 18 months old]` flag,
  checked with the target's compliance function and, where appropriate, against
  the regulator's public register. Most regulators publish enforcement outcomes.
- **Closure verification.** Every row with a `; closure unevidenced` flag from
  Referenced but Not Produced. **A matter believed closed without a closing letter
  is not closed.**
- **Missed deadlines.** Every
  `[deadline passed, completion not evidenced]` flag. Each is a fresh breach on
  top of the original finding and each needs immediate attention.
- **Repeat findings.** Every `[repeat finding]` flag and every
  `; prior matter, repeat finding` reference. **Repeat findings are treated far
  more seriously by regulators** and the earlier matter may not have been produced
  at all.
- **Pattern detection.** Read across rows for recurring subject matter, recurring
  business lines, and escalating severity. A pattern indicates a systemic control
  weakness rather than isolated issues, which is a larger and different finding.
  Ask Assistant over the project; the answer is narrative.
- **Continuing obligations register.** Every `Continuing Obligations` entry,
  collated with the Litigation settlement obligations and the Contracts survival
  terms into one post-closing obligations register with named owners.
- **Redress quantification.** Every customer remediation or redress requirement,
  sized against the affected population with the finance workstream. **Never a
  Harvey column.**
- **Unlicensed activity.** Every `[unlicensed activity alleged]` flag, escalated
  immediately. It is among the most serious findings the workstream can produce.

---

## Test set

- [ ] Routine cycle examination with findings, response, and a closing letter
- [ ] Targeted examination prompted by a complaint
- [ ] Examination report covering one of five business lines
- [ ] Examination report with sample-based findings and a stated sample size
- [ ] Examination with a repeat finding identified as previously raised
- [ ] Examination report with no limitations section
- [ ] Information request with no stated concern
- [ ] Information request where the documents show an underlying concern
- [ ] Warning letter with no formal violation asserted
- [ ] Notice of violation with findings partly accepted and partly disputed
- [ ] Formal investigation opened, no action yet
- [ ] Enforcement action with a proposed penalty
- [ ] Enforcement action with a final published penalty
- [ ] Consent order with continuing reporting obligations
- [ ] Consent order requiring an independent monitor at the target's cost
- [ ] Undertaking given with no stated end date
- [ ] Matter requiring customer redress with a stated affected population
- [ ] Matter with a lookback review requirement
- [ ] Self-report by the target of a breach
- [ ] Matter where the target states it had already identified the issue
- [ ] Matter with a cooperation discount applied to the penalty
- [ ] Matter with a remediation deadline that passed, completion not evidenced
- [ ] Matter with completion asserted by the target and not confirmed
- [ ] Matter with completion confirmed by the regulator
- [ ] Matter with a remediation plan submitted and no progress evidenced
- [ ] Matter referred to the regulator's enforcement division
- [ ] Matter referred to another regulator
- [ ] Matter referred to a prosecuting authority
- [ ] Matter where the regulator threatened escalation if a condition was not met
- [ ] Matter where an enforcement referral was closed without action
- [ ] Matter where court proceedings were commenced, to confirm it also belongs in Litigation
- [ ] Matter alleging activity conducted without an authorisation
- [ ] Matter directed at an individual approved person as well as the entity
- [ ] Matter open with the latest document being a regulator request, no response
- [ ] Matter whose latest document is three years old with no closure recorded
- [ ] Matter referenced as closed with the closing letter not produced
- [ ] Matter referencing an earlier examination not produced
- [ ] Matter file marked privileged and confidential
- [ ] Approval request with a no-action response
- [ ] Unit mistakenly containing two matters

Then test the dependencies: change `Required Actions` from stated actions to
`None required` and confirm `Action Deadline` and `Remediation Evidenced` both
move to `Not applicable`. Change `Findings or Allegations` to `None stated` and
confirm `Target Response` re-runs to `No response in unit` or reports any
substantive response. Change `Matter Type` from `Routine examination or
inspection` to `Information or document request` and confirm
`Scope and Limitations` re-runs against the request rules.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
