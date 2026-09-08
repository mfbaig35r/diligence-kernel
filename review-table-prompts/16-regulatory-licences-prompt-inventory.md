# Prompt Inventory — Regulatory: Licences

Table 16 of the POC. **This workstream sets the deal calendar more often than any
other.**

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Regulatory`
- Review unit: **one licence, permit, or registration** — the instrument itself,
  any renewal, amendment, or endorsement, any conditions schedule, and any
  transfer or change-of-control approval produced for it
- Grouping used: **yes**, typically 1–5 documents per unit
- Intended reviewers and downstream use: regulatory and corporate/M&A teams;
  feeds the closing conditions and regulatory calendar, the consent schedule, and
  the coverage register
- Inventory version: v1.0

### Why this table sets the timetable

A prior-approval requirement with a ninety-day statutory review period is a
closing condition, and it fixes the earliest possible closing date regardless of
how quickly everything else moves. Nothing else in diligence has that property.

**The whole workstream turns on one number: the ownership or control threshold.**
The original schema asked whether transfer requires consent but never asked for
the percentage, which is the only input the threshold analysis actually needs.
`Ownership or Control Threshold` and its Verbatim pair are why this table exists.

### The three questions

1. **Does the deal cross a threshold?** The percentage, whether indirect control
   counts, and what filing follows.
2. **How long does that take?** The statutory review period, which drives the
   closing calendar.
3. **Does the licence survive?** Transferability, and whether a qualifying
   individual or a financial requirement has to be re-established.

## Assumptions to confirm before running

1. One row is one licence in one jurisdiction held by one entity. The same licence
   type held by three entities in three states is nine rows, because thresholds,
   review periods, and status differ.
2. **Regulator correspondence and enforcement is a separate table.** A licence and
   an examination report are different roles and cannot share a schema.
3. Environmental permits are a separate table, in the Environmental workstream.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

24 Harvey columns plus 9 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side regulatory diligence on the target group listed below. This table reviews licences, permits, and registrations.

One row is one licence, permit, or registration: the instrument itself, any renewal, amendment, or endorsement, any conditions schedule, and any transfer or change-of-control approval produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the licence or the regulator.
- **Report what the documents state. Do not supply a requirement from the governing statute or regulations, even where it is well known.** A threshold, a review period, or a fitness test that is not in the documents is `Not addressed` here, and the reviewer establishes it from the law.
- **A licence document states the position as at its own date.** Nothing in a data room updates it. Report the status the documents show and identify the document.
- **Do not determine whether this transaction crosses any threshold, whether a filing is required, or how long an approval will take.** Those depend on the deal structure and the ownership chain, and all three are human columns.
- Report numbers, percentages, and dates exactly as printed. Do not calculate.
- Use entity names exactly as printed; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Licence Type
  Holder Entity
  Regulator
  Jurisdiction
  Licence Number

Stage 2 — Validity
  Documents in Unit ──→ Status
                        Referenced but Not Produced
  Issue Date, Expiry Date
  Expiry Date ──→ Renewal Requirements
  Holder Entity ──→ Holder Matches Target Entity

Stage 3 — Substance
  Scope of Permitted Activity
  Conditions and Undertakings
  Financial Requirements
  Qualifying Individual Requirement
  Ongoing Reporting Obligations

Stage 4 — The transaction block
  Ownership or Control Threshold ──→ Threshold Language
                                     Indirect Control Captured
  Filing Type Required ──→ Statutory Review Period
  Transferability
  Fitness and Probity Requirements
  Prior Change of Control Approvals

Stage 5 — Enforcement history
  Open Findings or Enforcement
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Licence Type | Free Response | — | — | v1.0 | draft |
| 3 | Holder Entity | Free Response | — | Holder Matches Target Entity | v1.0 | draft |
| 4 | Holder Matches Target Entity | Classify | @Holder Entity | — | v1.0 | draft |
| 5 | Regulator | Free Response | — | — | v1.0 | draft |
| 6 | Jurisdiction | Free Response | — | — | v1.0 | draft |
| 7 | Licence Number | Free Response | — | — | v1.0 | draft |
| 8 | Issue Date | Date | — | — | v1.0 | draft |
| 9 | Expiry Date | Date | — | Renewal Requirements | v1.0 | draft |
| 10 | Renewal Requirements | Free Response | @Expiry Date | — | v1.0 | draft |
| 11 | Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 12 | Scope of Permitted Activity | Free Response | — | — | v1.0 | draft |
| 13 | Conditions and Undertakings | Free Response | — | — | v1.0 | draft |
| 14 | Financial Requirements | Free Response | — | — | v1.0 | draft |
| 15 | Qualifying Individual Requirement | Free Response | — | — | v1.0 | draft |
| 16 | Ongoing Reporting Obligations | Free Response | — | — | v1.0 | draft |
| 17 | Ownership or Control Threshold | Free Response | — | Threshold Language; Indirect Control Captured | v1.0 | draft |
| 18 | Threshold Language | Verbatim | @Ownership or Control Threshold | — | v1.0 | draft |
| 19 | Indirect Control Captured | Classify | @Ownership or Control Threshold | — | v1.0 | draft |
| 20 | Filing Type Required | Classify | — | Statutory Review Period | v1.0 | draft |
| 21 | Statutory Review Period | Free Response | @Filing Type Required | — | v1.0 | draft |
| 22 | Transferability | Classify | — | — | v1.0 | draft |
| 23 | Fitness and Probity Requirements | Free Response | — | — | v1.0 | draft |
| 24 | Prior Change of Control Approvals | Free Response | — | — | v1.0 | draft |
| 25 | Open Findings or Enforcement | Free Response | — | — | v1.0 | draft |
| 26 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

26 columns — two more than estimated. `Holder Matches Target Entity` follows the
pattern used in IP and Real Estate, and `Prior Change of Control Approvals` earned
its place because a prior approval file is the best available evidence of what the
regulator will actually require this time.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Status`, `Referenced but Not Produced`
- Purpose: inventory the licence file.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the licence, permit, or registration certificate, the original application, any renewal certificate or confirmation, any amendment, endorsement, or variation, any conditions schedule, any approval of a prior transfer or change of control, and any regulator confirmation of status.
- Treat schedules and conditions annexed to a certificate as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where none is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated or issue date.
- State the function as one of `Licence certificate`, `Application`, `Renewal`, `Amendment or variation`, `Conditions schedule`, `Transfer or CoC approval`, `Status confirmation`, or `Other`.
- **Where a document relates to a different licence, entity, or jurisdiction than the subject of this row, still list it and append ` [relates to [licence, entity, or jurisdiction]]`.** A unit covering three states produces a merged row, and this is how that surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 10 lines and no more than 90 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Licence Type

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the authorisation is, named as the regulator names it.

Free Response rather than Classify because licence nomenclature is
jurisdiction-specific and unbounded: a controlled vocabulary would either be
enormous or force everything into `Other`.

```markdown
## Task

State the type of licence, permit, registration, or authorisation this review unit documents.

## Rules

- **Report the type exactly as the regulator names it**, for example `Money Transmitter License`, `Class 3 Waste Carrier Registration`, `Part 135 Air Carrier Certificate`, `Consumer Credit Licence`. Do not translate it into a generic category, and do not normalize across jurisdictions — the name is how it is searched and renewed.
- Where the authorisation carries a class, category, endorsement, or schedule designation, report it, since the class usually determines the permitted activity.
- Where the instrument is a registration or notification rather than a licence, report it as named and note the distinction, since registrations frequently carry lighter change-of-control requirements than licences.
- Where the instrument is an exemption or a no-action position rather than an authorisation, report it as such.
- Report any endorsement or additional authorisation added by a later document in the unit.

## Fallback rules

- Return `Unable to determine` where the documents do not identify what the authorisation is.

## Output format

`[Type as named][; class or category: [as stated]]`. Return no more than 30 words.
```

---

### 3. Holder Entity

- Native type: Free Response
- Upstream: none
- Downstream: `Holder Matches Target Entity`
- Purpose: which entity holds the authorisation, exactly as recorded.

```markdown
## Task

State the entity or person that holds this authorisation, as recorded.

## Rules

- Report the name **exactly as printed on the licence or in the register extract**, including entity suffix, punctuation, and any misspelling or outdated form. Do not correct, normalize, expand, or update it. **An error in the licence register is a finding** and correcting it here hides it.
- Where a later document in the unit records a change of holder or a name change, report the current holder and append ` (changed from [prior name], [YYYY-MM-DD])`.
- **Where the holder is a branch, division, or trading name rather than a legal entity, report it as printed and add `(not a legal entity as recorded)`.**
- Where the authorisation is held by an individual on behalf of the business, report the individual as printed and add `(individual holder)`. **A licence held personally does not transfer with the business** and it is a distinct problem.
- Where more than one holder is recorded, list each.
- Report any trading or doing-business-as name recorded alongside the legal name.

## Fallback rules

- Return `Not stated` where the documents do not name a holder.
- Return `Unable to determine` where the name is illegible.

## Output format

`[Name exactly as printed]`, with any qualifier appended. Return no more than 35 words.
```

---

### 4. Holder Matches Target Entity

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Held under a former name`, `Held by an individual`, `Held by a third party`, `Held by a branch or trading name`, `No holder recorded`, `Unable to determine`
- Upstream: `@Holder Entity`
- Downstream: none
- Purpose: whether the authorisation sits inside the acquired group. Same pattern
  as the IP and Real Estate ownership tests.

```markdown
## Established result

- Holder entity: @Holder Entity

Use this result and the target group list in the Table Instructions. Confirm the name against the documents.

## Task

Classify the relationship between the recorded holder and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No holder recorded`: Holder Entity returned `Not stated`.
2. `Held by an individual`: the recorded holder is a natural person. **A personally held licence does not pass with a share sale of the employer**, and where that individual is not staying, the authorisation may have to be reapplied for entirely.
3. `Held by a branch or trading name`: the recorded holder is a branch, division, or trading name rather than a legal entity. Report in the evidence field which legal entity the documents indicate it belongs to.
4. `Held under a former name`: the recorded name matches a prior name of a target entity as disclosed in the documents in this unit. **The register should be updated**, and a stale name can delay a change-of-control filing.
5. `Held by a third party`: the recorded holder is an entity that is not a target entity and is not a former name of one. **This may mean the business operates under someone else's authorisation**, which is a serious finding.
6. `Matches with name variance`: the recorded name is the same entity as one on the target group list but differs in form.
7. `Matches a target entity exactly`: the name is character-for-character a name on the target group list.

**Do not resolve a variance by assuming.** Where the name is similar but could be a different entity, use `Held by a third party` and note the similarity in the evidence field.

Where a target entity's former name is not disclosed in this unit, use `Held by a third party`; the Corporate table's `Prior Names` column resolves it.

## Fallback rules

- Use `Unable to determine` where the name is illegible or Holder Entity returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Regulator

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who issued it and who must be applied to. **The counterparty for the
  filing**, and the join key to the Regulatory Correspondence table.

```markdown
## Task

State the authority that issued this authorisation.

## Rules

- Report the authority exactly as printed, including the specific department, division, bureau, or office where stated. **The division matters** — filings and approvals are handled by named units and the correspondence goes to them.
- Report any named contact office, licensing unit, or case officer identified in the documents.
- Where the authorisation is issued by one body and supervised by another, report both and label each.
- Where the authorisation is issued under a delegated or self-regulatory arrangement, report the delegate and the ultimate authority.
- Where the documents identify a filing address, portal, or system for applications, report it in the evidence field, since it is the practical route for the change-of-control filing.

## Fallback rules

- Return `Unable to determine` where the documents do not identify the issuing authority.

## Output format

`[Authority as printed][ — [division or office]]`, with any supervisory authority labelled. Return no more than 40 words.
```

---

### 6. Jurisdiction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the authorisation operates, which is not always the same as the
  regulator's seat.

```markdown
## Task

State the jurisdiction in which this authorisation permits activity.

## Rules

- **Report the jurisdiction of operation, which may differ from the regulator's seat.** A federal authorisation permits activity nationally; a state licence permits it in one state; a passported authorisation may permit activity in several jurisdictions from one licence, and the passporting is the point.
- Where the authorisation is stated to permit activity in jurisdictions beyond the issuing one, list them, and where more than eight are listed report the first eight and append ` and [N] further jurisdictions`.
- Where the authorisation is limited to a named territory, county, district, or site, report the limitation.
- **Where the authorisation is limited to named premises or locations, report them**, since it links the row to the Real Estate tables and a site move can require a new authorisation.
- Report the level — federal or national, state or provincial, local or municipal — since it determines whose approval a change of control needs.

## Fallback rules

- Return `Not stated` where the documents do not identify the jurisdiction of operation.

## Output format

`[Jurisdiction][; level: [as stated]][; premises: [as stated]]`. Return no more than 45 words.
```

---

### 7. Licence Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the register identifier, which is the key for verifying status
  independently and for the change-of-control filing.

```markdown
## Task

State the licence, permit, or registration number.

## Rules

- **Report the number exactly as printed, including any prefix, suffix, slashes, spaces, and check characters. Do not reformat.** Register searches and filings fail on reformatted numbers, and this cell is what a verification search is run from.
- Where the authorisation carries more than one identifier — a licence number and a firm reference number, or a state number and a national registry number such as an NMLS identifier — report each and label it.
- Where the holder has a separate registration number distinct from the licence number, report both.
- Where a renewal issued a new number, report the current number and append ` (previously [number])`.

## Fallback rules

- Return `Not stated` where no number appears in the documents.
- Return `Unable to determine` where numbers conflict or are illegible.

## Output format

`[Label] [number]` per identifier, separated by semicolons. Return no more than 30 words.
```

---

### 8. Issue Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the authorisation was first granted, which bears on renewal cycles
  and on how long the business has held it.

```markdown
## Task

Identify the date this authorisation was first issued.

## Date-selection hierarchy

1. Use an original issue or grant date the documents state for the authorisation.
2. If none, use the issue date printed on the earliest certificate in the unit.
3. If neither, use the effective date of the earliest authorisation document in the unit.

## Excluded dates

- The date of a renewal, where an original issue date is stated. **Report the most recent renewal date in the evidence field**, since renewal history is useful, but the issue date is the original
- The date of the application
- The date of an amendment or endorsement
- The date of a register extract or status confirmation
- File name and metadata dates, and printing and scan dates

## Rules

- **Report the original issue date, not the current certificate's date.** Where only the current certificate is present and it shows a recent issue date with no original, report that date and note in the evidence field that no original is available.
- Where a certificate shows both an original issue date and a current effective date, report the original and note the current in the evidence field.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no issue date can be selected.
```

---

### 9. Expiry Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: none
- Downstream: `Renewal Requirements`
- Purpose: when the authorisation lapses. **A licence expiring during the deal
  period is a task with a regulator's timetable attached.**

```markdown
## Task

Identify the date this authorisation expires.

## Rules

- Report the expiry, valid-until, or renewal-due date stated on the most recent certificate or renewal in the unit.
- **Where the authorisation is stated to continue in force indefinitely subject to conditions or annual fees, return `Not applicable — continuous`** and report any annual fee or return obligation in Renewal Requirements. Many authorisations do not expire but do lapse for non-payment or non-filing, and that is a different mechanism.
- Where the documents state a term rather than a date, report the resulting date only if a document states it. Do not calculate.
- Compare the reported date to the diligence as-of date. Flag it:
  - already passed: append ` [expired on record]`
  - within three months: append ` [expires within 3 months]`
  - within twelve months: append ` [expires within 12 months]`
- **Where `[expired on record]` applies and no renewal appears in the unit, this is a live compliance finding** — operating on a lapsed authorisation is usually an offence, not merely an irregularity.

## Fallback rules

- Return `Not stated` where the authorisation is of a kind that expires and no date appears.
- Return `Unable to determine` where dates conflict.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or `Not applicable — continuous`.
```

---

### 10. Renewal Requirements

- Native type: Free Response
- Upstream: `@Expiry Date`
- Downstream: none
- Purpose: what has to be done to keep the authorisation, and how far ahead.
  **A renewal falling due in the deal period may have to be filed by the seller
  and may itself disclose the transaction.**

```markdown
## Established result

- Expiry date: @Expiry Date

## Task

Report what is required to renew or maintain this authorisation.

## Include where expressly stated

- The renewal filing deadline, and how far before expiry it falls
- **The renewal lead time, meaning how long the regulator takes to process a renewal.** Where a renewal takes longer than the remaining term, operating continuity depends on a pending-application provision
- Any requirement to file audited accounts, returns, or reports with the renewal
- Any renewal fee
- Any continuing education, testing, or competence requirement
- Any requirement to confirm or update ownership, control, or officer information on renewal. **This is where a renewal can itself disclose or trigger a change-of-control review**
- Any annual fee, annual return, or periodic confirmation required to prevent lapse where the authorisation does not expire
- Any grace period after expiry, and whether activity may continue during it
- Any provision permitting continued operation while a renewal application is pending

## Rules

- **Report the pending-application provision where present.** It is the difference between a late renewal being an administrative matter and being an interruption of the business.
- **Report any ownership or control confirmation required on renewal**, since it interacts directly with the transaction and may need sequencing.
- Report deadlines and periods as stated. Do not calculate a filing date.

## Fallback rules

- Return `Not addressed` where the documents state no renewal or maintenance requirement.
- Return `Not applicable` where the authorisation is one-off and requires no maintenance.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Deadline: [as stated]; lead time: [as stated or "Not addressed"]; filings required: [brief]; fee: [as stated]; ownership confirmation: [required | Not addressed]; operation while pending: [permitted | Not addressed]; grace period: [as stated or "none"]`

Return no more than 80 words.
```

---

### 11. Status

- Native type: Classify
- Configured options, in UI order: `Active`, `Active with conditions`, `Pending or in application`, `Suspended`, `Restricted or limited`, `Revoked or cancelled`, `Expired`, `Surrendered or withdrawn`, `Under review`, `Not stated`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the authorisation is live, as at the most recent document.

**Scope discipline.** A certificate speaks as of its own date. Report the status
the documents show, give the date in the evidence field, and let the reviewer
verify against the public register — most licence registers are searchable and
verification is quick.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document bearing on status. Confirm the status against it.

## Task

Classify the status of this authorisation as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Revoked or cancelled`: the documents record revocation, cancellation, or refusal to renew by the regulator.
2. `Surrendered or withdrawn`: the holder gave up the authorisation or withdrew an application.
3. `Suspended`: the documents record suspension, whether temporary or pending an investigation.
4. `Expired`: the stated expiry has passed and no renewal appears in the unit.
5. `Restricted or limited`: the authorisation remains in force with a restriction imposed by the regulator on its scope, volume, or activities — as distinct from conditions attached at grant.
6. `Under review`: the documents record a pending review, investigation, examination, or enforcement process affecting the authorisation.
7. `Pending or in application`: the documents show an application filed and not yet determined. **Report whether activity is permitted while pending in the evidence field**, since that determines whether the business is currently operating lawfully.
8. `Active with conditions`: in force subject to conditions attached at grant or on renewal.
9. `Active`: in force with no conditions or adverse status recorded.

**Distinguish `Active with conditions` from `Restricted or limited`.** Conditions attached at grant are the ordinary terms of the authorisation; a restriction imposed later is a regulatory action and it belongs with the enforcement history.

Give the date of the document the status comes from in the evidence field, and where that document is more than twelve months older than the diligence as-of date, note the gap.

## Fallback rules

- Use `Not stated` where the documents evidence the authorisation without stating a status.
- Use `Unable to determine` where statuses conflict or the relevant text is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Scope of Permitted Activity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the authorisation permits. **The gap between what is permitted and
  what the business actually does is the highest-value finding this workstream
  generates.**

```markdown
## Task

Report the activities this authorisation permits.

## Include where expressly stated

- The permitted activities, as the authorisation describes them
- Any class, category, or schedule of activities, with its designation
- Any activity expressly excluded or not covered
- Any volume, value, capacity, or transaction limit
- Any limitation to named premises, sites, vehicles, or equipment
- Any limitation to named products, services, or customer types
- Any limitation on channel — in person, remote, online, or through agents
- Any requirement to conduct the activity through named individuals
- Any territorial limitation within the jurisdiction

## Rules

- **Report the scope as printed, using the authorisation's own categories.** Do not translate a regulatory category into a plain-language description; the category is what the regulator enforces against.
- **Report every limit — volume, value, capacity, premises, or product.** A licence permitting the right activity subject to a volume cap the business has outgrown is a live compliance problem and the cap is the finding.
- Report any activity expressly excluded, since exclusions define the boundary more reliably than inclusions.
- **Do not assess whether the target's actual operations fall within the permitted scope.** That comparison requires the operational facts and it is human work against the commercial workstream.

## Fallback rules

- Return `Not stated` where the documents do not describe the permitted activity.
- Return `Incorporated terms` where the scope is stated to be set out in a schedule or rules not present in the unit.
- Return `Unable to determine` where descriptions conflict or are illegible.

## Output format

`Permitted: [as printed]; class: [as stated]; limits: [volume, value, premises, product, as stated]; excluded: [as stated or "none stated"]`

Return no more than 85 words.
```

---

### 13. Conditions and Undertakings

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the obligations attached to holding the authorisation, which the buyer
  inherits and must continue to satisfy.

```markdown
## Task

Report the conditions, restrictions, and undertakings attached to this authorisation.

## Include where expressly stated

- Conditions attached at grant or on renewal
- Any undertaking the holder has given to the regulator
- Any restriction imposed by the regulator after grant, with its date
- Any requirement to maintain systems, controls, policies, or procedures
- Any requirement to hold insurance, a bond, or other security
- Any requirement to segregate or safeguard client money or assets
- Any requirement to maintain a physical presence, registered office, or local representative
- Any requirement to notify the regulator of stated events, and the notification period
- **Any condition that is stated to lapse, be reviewed, or fall away on a stated date or event**
- Any condition imposed following an enforcement action, with the action identified

## Rules

- Report each condition in eight words or fewer, with its source document and date.
- **Distinguish conditions attached at grant from conditions imposed following enforcement**, and label each. A condition imposed after an investigation tells a reviewer there was an investigation, and it belongs alongside the enforcement history.
- **Report any obligation to notify the regulator of a change of control or of officers here as well as in the transaction columns**, since it is a condition of the authorisation and breaching it is a regulatory matter independent of the approval requirement.
- Report no more than ten conditions. Where more exist, report the ten with the greatest operational effect and append ` and [N] further conditions`.
- Do not assess compliance.

## Fallback rules

- Return exactly `None attached` where the authorisation is unconditional.
- Return `Incorporated terms` where conditions are stated to be set out in a schedule or rules not present in the unit. **This is common and it is a coverage gap**, because the conditions cannot be read.
- Return `Unable to determine` where conditions conflict or are illegible.

## Output format

One line per condition:

`[Condition] — [at grant | imposed [YYYY-MM-DD]] — [source document]`

Return no more than 10 lines and no more than 100 words.
```

---

### 14. Financial Requirements

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: capital, bonding, and net worth requirements. **A change of control can
  reset these**, and a new bond or a fresh capital injection is a cost and a
  timetable item the buyer may not expect.

```markdown
## Task

Report any financial requirement attached to this authorisation.

## Include where expressly stated

- Minimum capital, net worth, or tangible net worth requirement, with the amount
- Any surety bond, guarantee, letter of credit, or deposit requirement, with the amount and the surety or issuer
- **The bond's expiry or renewal date, and any evergreen or continuous provision**
- Any requirement to maintain permissible or eligible investments
- Any liquidity or reserve requirement
- Any professional indemnity or other insurance requirement, with the limits
- Any requirement to file audited financial statements, and on what frequency
- **Any requirement to notify the regulator of a deterioration in financial position, or of a failure to meet a threshold**
- Any parent or affiliate guarantee, keep-well, or capital maintenance undertaking given to the regulator
- Any requirement triggered or reset by a change of control or a change in ownership

## Rules

- **Report any parent guarantee or capital maintenance undertaking given to the regulator prominently.** Where the guarantor is the seller or an entity outside the acquired group, it must be replaced at closing, and the regulator's agreement to the replacement is itself an approval.
- **Report any bond and its expiry.** A surety bond usually cannot be assumed and a new bond takes underwriting time.
- Report amounts and dates as stated. **Do not calculate whether a requirement is met**, and do not compare to any financial data.

## Fallback rules

- Return exactly `None stated` where the documents state no financial requirement.
- Return `Incorporated terms` where requirements are stated to be set out in rules not present in the unit.
- Return `Unable to determine` where requirements conflict or are illegible.

## Output format

`Capital or net worth: [as stated]; bond: [amount, surety, expiry, or "none"]; insurance: [as stated or "none"]; reporting: [frequency]; guarantee to regulator: [as stated or "none"]; reset on change of control: [as stated or "Not addressed"]`

Return no more than 85 words.
```

---

### 15. Qualifying Individual Requirement

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether the authorisation depends on a named person. **If that person
  leaves at closing, the licence is at risk** — and a departure is exactly what a
  transaction tends to produce.

```markdown
## Task

Report any requirement that this authorisation depend on a named or qualified individual.

## Include where expressly stated

- Any named responsible person, qualifying individual, nominated officer, designated manager, or approved person
- The role each holds, and any qualification, licence, examination, or experience requirement attached
- **Any requirement that the individual be approved, registered, or notified to the regulator, and any process for replacing them**
- **Any period within which a replacement must be appointed if the individual ceases to act, and any consequence of failing to do so**
- Any requirement for a minimum number of qualified individuals
- Any residence, presence, or local-employment requirement
- Any requirement for a compliance officer, money laundering reporting officer, or equivalent
- Any requirement that the individual not be an employee of another regulated business

## Rules

- **Report the individual's role rather than their name where possible**, so the requirement can be matched to the Employment table without carrying personal data into this row. Where the documents name an approved individual and the name is needed to identify the requirement, report it.
- **Report the replacement window and the consequence of a vacancy prominently.** A licence that lapses or must cease operating if the qualifying individual leaves is a retention priority, and the row should be flagged to the Employment table's key-person analysis.
- **Report whether a replacement requires prior regulator approval or only notification.** Prior approval means a vacancy cannot be filled immediately.
- Report the requirements as stated. Do not assess whether they are currently satisfied.

## Fallback rules

- Return exactly `None stated` where the authorisation does not depend on a named or qualified individual.
- Return `Incorporated terms` where the requirement is stated to be set out in rules not present in the unit.
- Return `Unable to determine` where requirements conflict or are illegible.

## Output format

`Roles required: [as stated]; qualifications: [as stated]; regulator approval: [prior approval | notification | Not addressed]; replacement window: [as stated or "Not addressed"]; consequence of vacancy: [as stated or "Not addressed"]`

Return no more than 80 words. Prefer roles over individual names.
```

---

### 16. Ongoing Reporting Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the recurring filings the buyer inherits, and the notification
  obligations the transaction itself may trigger.

```markdown
## Task

Report the periodic and event-driven reporting obligations attached to this authorisation.

## Include where expressly stated

- Periodic returns, reports, or statements, with their frequency and due dates
- Audited or unaudited financial filings
- Any requirement to report transaction volumes, complaints, incidents, or breaches
- **Event-driven notification obligations, and the period for each**: change of control, change of ownership above a threshold, change of officers or qualifying individuals, change of registered office or premises, change of name, insolvency events, material litigation, regulatory action by another authority, and data or security incidents
- Any requirement to notify a material change in the business or its activities
- Any record-retention obligation, with the period
- Any requirement to permit inspection or to provide information on demand

## Rules

- **Report the event-driven notification obligations separately from the periodic ones, and report the notification period for each.** These are what the transaction triggers, and a change-of-control notification with a five-business-day period after completion is a task that has to be diarised before signing.
- **Report any obligation to notify a change of officers**, since post-closing board changes commonly trigger it and it is routinely overlooked.
- Report periods and frequencies as stated. Do not calculate due dates.
- Do not assess whether past filings were made; that is the Open Findings column and the human review.

## Fallback rules

- Return exactly `None stated` where the documents state no reporting obligation.
- Return `Incorporated terms` where obligations are stated to be set out in rules not present in the unit. **Common, and the rules should be obtained** — the notification periods are in them.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

`Periodic: [obligation and frequency]` per line, then `Event-driven: [event — period]` per line.

Return no more than 10 lines and no more than 100 words.
```

---

### 17. Ownership or Control Threshold

- Native type: Free Response
- Upstream: none
- Downstream: `Threshold Language`, `Indirect Control Captured`
- Purpose: **the entire point of the workstream.**

The percentage of ownership or voting power that triggers a filing is the only
input the threshold analysis needs, and the original schema never asked for it.
Aggregated across rows and compared against the buyer's resulting direct and
indirect ownership, this column produces the regulatory filing list — and that
list produces the closing calendar.

```markdown
## Task

Report any threshold of ownership, voting power, or control stated in the documents as triggering a notification, approval, or other requirement.

## Include where expressly stated

- **The percentage of shares, voting power, or equity interest at which a requirement is triggered**, and what the percentage is of
- Any second or subsequent threshold — for example a first notification at 10 percent and approval at 25 percent
- Any threshold expressed in terms other than a percentage: the ability to appoint a majority of the board, the ability to exercise significant influence, or the ability to direct management and policies
- Any aggregation rule requiring holdings of connected persons, affiliates, or persons acting in concert to be added together
- Any threshold applying to a decrease in holding as well as an increase
- Any de minimis or exemption from the threshold
- Any different threshold for a passive or institutional holder

## Rules

- **Report the percentage exactly as printed, and report what it applies to** — shares, voting securities, voting power, equity interests, or capital. The base matters as much as the number.
- **Report every threshold, not only the lowest.** A licence with notification at 10 percent and prior approval at 25 percent produces two different obligations with two different timetables.
- **Report any aggregation rule.** Aggregation is what turns a set of individually sub-threshold holdings into a triggering acquisition, and it is the most commonly missed element.
- Report qualitative control tests as printed. A control test with no percentage is still a threshold and it is usually the harder one to advise on.
- **Do not supply a threshold from the governing statute or regulations.** Where the documents state none, return `Not addressed`; the reviewer establishes it from the law. Reporting a remembered statutory figure as though the documents stated it is the worst failure available in this column.
- **Do not state whether this transaction crosses any threshold.** That requires the ownership chain and the deal structure.

## Fallback rules

- Return `Not addressed` where the documents state no threshold. **This is common — a certificate rarely recites the statutory framework — and it is a routing instruction, not a conclusion.** The human column carries the analysis.
- Return `Incorporated terms` where the threshold is stated to be set out in rules or a statute not present in the unit, and name the source as referenced.
- Return `Unable to determine` where thresholds conflict or are illegible.

## Output format

One line per threshold:

`[Percentage or test] of [base] — triggers [notification | prior approval | other, as stated]`, then a final line: `Aggregation: [as stated or "Not addressed"]`

Return no more than 6 lines and no more than 80 words. Do not include any figure not stated in the documents.
```

---

### 18. Threshold Language

- Native type: Verbatim
- Upstream: `@Ownership or Control Threshold`
- Downstream: none
- Purpose: the exact text. **A threshold analysis is argued on the wording of the
  control definition**, and a partner reads it before the filing strategy is set.

```markdown
## Established result

- Ownership or control threshold: @Ownership or Control Threshold

## Task

If Ownership or Control Threshold reported a threshold, quote the provision stating it exactly as written.

If it returned `Not addressed`, return exactly `Not addressed`.

If it returned `Incorporated terms`, return exactly `Not addressed`.

If it returned `Unable to determine`, quote whatever threshold language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the threshold together with the definition of control, controlling interest, or connected person that it relies on**, where the definition appears in the unit. The definition is where indirect ownership and aggregation are settled, and the threshold on its own is not enough to advise on.
- Quote any aggregation provision and any exemption or de minimis carve-out.
- Quote any provision stating whether the requirement is prior approval or subsequent notification, where it appears in the same provision.
- Where the combined text exceeds 250 words, quote the threshold, every limb of the control definition, and each carve-out, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction crosses the threshold.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 19. Indirect Control Captured

- Native type: Classify
- Configured options, in UI order: `Direct holdings only`, `Indirect and ultimate control captured`, `Ultimate beneficial owner test`, `Both direct and indirect, separate thresholds`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Ownership or Control Threshold`
- Downstream: none
- Purpose: whether a change at parent level reaches this authorisation. **Decides
  whether a holdco-level transaction engages the licence at all.**

```markdown
## Established result

- Ownership or control threshold: @Ownership or Control Threshold

## Task

If Ownership or Control Threshold reported a threshold, classify whether it reaches indirect or upstream ownership.

If it returned `Not addressed` or `Incorporated terms`, return `Not addressed`.

If it returned `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

- `Indirect and ultimate control captured`: the provision reaches ownership or control held through intermediate entities, using language such as direct or indirect, whether directly or through one or more intermediaries, ultimate parent, or person controlling the holder.
- `Ultimate beneficial owner test`: the provision looks through the entire ownership chain to natural persons, and requires their identification. **This is the most demanding form** — it requires disclosure of the buyer's own ultimate owners, which for a fund structure can be a substantial and slow exercise.
- `Both direct and indirect, separate thresholds`: different thresholds apply to direct and indirect holdings.
- `Direct holdings only`: the provision reaches only a transfer of the holder's own shares or interests, with no reference to ownership above it. **A holdco-level transaction may fall outside it entirely**, which is the most useful negative finding this column produces.

Report in the evidence field whether the provision requires identification of the ultimate parent, the ultimate beneficial owners, or both, and whether any look-through threshold applies to intermediate entities.

## Fallback rules

- Use `Unable to determine` where the provision is illegible, or where it cannot be told which level it reaches.

## Output format

Return only the exact configured option and no explanation.
```

---

### 20. Filing Type Required

- Native type: Classify
- Configured options, in UI order: `Prior approval required`, `Prior notification with waiting period`, `Post-closing notification`, `New application required`, `No filing on change of control`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Statutory Review Period`
- Purpose: what has to be filed and when relative to closing. **The distinction
  between prior approval and post-closing notification is the difference between a
  closing condition and a diary entry.**

```markdown
## Task

Classify what filing the documents state is required on a change of ownership or control of the holder. Choose exactly one configured option.

## Scope

- Consider requirements stated in the authorisation, its conditions, or any transfer approval in the unit.
- Consider requirements applying on a change of control of the holder, of its parent, or of its ultimate owner.
- Exclude periodic filings and unrelated event notifications, which are reported in Ongoing Reporting Obligations.

## Classification rules

Apply the first rule that fits.

1. `New application required`: the authorisation cannot be transferred or continued and a fresh application is required. **The most severe outcome**, because the business may have to operate under a temporary permission or not at all in the interim.
2. `Prior approval required`: the regulator's affirmative approval must be obtained before completion. **This is a closing condition** and it sets the earliest closing date.
3. `Prior notification with waiting period`: notification must be filed before completion and a period must elapse, after which the transaction may proceed absent objection. Functionally a closing condition, but with a defined end date rather than an open-ended review.
4. `Post-closing notification`: notification is required after completion, within a stated period. **Not a closing condition**, but a hard post-closing deadline whose breach is a regulatory matter.
5. `No filing on change of control`: the documents state expressly that no filing is required.

**Where the requirement differs by threshold** — notification at one level and approval at a higher one — classify on the more onerous requirement and report both in the evidence field.

**Do not supply a filing requirement from the governing statute.** Where the documents state none, use `Not addressed`.

## Fallback rules

- Use `Not addressed` where the documents do not address filings on a change of control. **Common, and it means the reviewer must establish the position from the law** rather than that no filing is required.
- Use `Unable to determine` where requirements conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 21. Statutory Review Period

- Native type: Free Response
- Upstream: `@Filing Type Required`
- Downstream: none
- Purpose: how long the filing takes. **This is the number that sets the deal
  calendar**, and any period longer than the intended timetable converts the
  approval into the critical path.

```markdown
## Established result

- Filing type required: @Filing Type Required

## Task

If Filing Type Required is `Prior approval required`, `Prior notification with waiting period`, `Post-closing notification`, or `New application required`, report the periods and mechanics the documents state.

If it is `No filing on change of control`, return exactly `Not applicable`.

If it is `Not addressed` or `Unable to determine`, return exactly `Not addressed`.

## Include where expressly stated

- **The period within which the regulator must determine the application, or the waiting period that must elapse**
- Any period within which the filing must be made, whether before or after completion
- Any provision for the period to be extended, suspended, or restarted — commonly on a request for further information. **A clock that restarts on any information request is effectively open-ended**, and that is the finding
- Any deemed approval or deemed non-objection if the regulator does not respond
- Any fee payable
- Any requirement for a public notice, consultation, or comment period
- Any requirement for the buyer to provide information, financial statements, or details of its own ultimate owners
- Any interim or temporary permission available pending determination

## Rules

- **Report the period as stated and do not supply a statutory period from memory.** A wrong review period produces a wrong closing date, and that is the most consequential error this table can make.
- **Report any extension or restart provision prominently.** The stated period is the floor, not the expected duration.
- **Report any interim permission available**, since it can decouple the approval from the closing timetable entirely.
- Report the information the buyer must provide, since buyer-side preparation is often the longest lead item and it cannot start until it is known.
- Do not estimate an actual timetable and do not state when approval would be obtained.

## Fallback rules

- Return `Not addressed` where a filing is required and the documents state no period. **The reviewer establishes it from the law and from the regulator's published service standards.**
- Return `Unable to determine` where periods conflict or are illegible.

## Output format

`Determination period: [as stated]; filing deadline: [as stated]; extension or restart: [as stated or "Not addressed"]; deemed outcome: [as stated or "none"]; fee: [as stated]; buyer information required: [brief]; interim permission: [as stated or "Not addressed"]`

Return no more than 85 words. Do not include any period not stated in the documents.
```

---

### 22. Transferability

- Native type: Classify
- Configured options, in UI order: `Transfers with the entity, no filing`, `Transfers with approval`, `Not transferable, new application required`, `Transferable to a named class of transferee`, `Personal to the holder`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the authorisation survives the transaction at all.

**In a share purchase the entity keeps its own licence** and the question is
whether a filing is triggered. In an asset purchase, or where the licence is
personal to an individual, the authorisation may not move at all — and that can
determine the deal structure rather than merely add a condition to it.

```markdown
## Task

Classify whether and how this authorisation can move with the business. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Personal to the holder`: the authorisation is held by or granted personally to an individual and is not capable of transfer. **Where that individual is not remaining with the business, the authorisation is effectively lost.**
2. `Not transferable, new application required`: the authorisation cannot be assigned or transferred, and a transferee must apply afresh. **Decisive in an asset deal or a carve-out.**
3. `Transferable to a named class of transferee`: transfer is permitted only to a transferee meeting stated criteria — an existing licensee, a person of a stated type, or one satisfying a fitness test.
4. `Transfers with approval`: the authorisation may be assigned or transferred with the regulator's approval.
5. `Transfers with the entity, no filing`: the authorisation is held by the entity and continues unaffected by a change in that entity's ownership, with no filing required. **This is the best case in a share purchase.**

**Distinguish transferability from the change-of-control filing requirement.** An authorisation can be perfectly non-transferable and yet be entirely unaffected by a share purchase, because the holder does not change. Classify what the documents say about transfer, and let the Filing Type Required column carry the change-of-control position.

Report in the evidence field whether the documents distinguish a share transfer from an asset transfer, and whether any transfer approval in the unit shows how the regulator handled it previously.

## Fallback rules

- Use `Not addressed` where the documents do not address transfer.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 23. Fitness and Probity Requirements

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the regulator will require of the **buyer** and its people. Often
  the longest-lead item in the whole transaction, because it depends on
  information the buyer has to gather about itself.

```markdown
## Task

Report any fitness, suitability, probity, or good-character requirement the documents state.

## Include where expressly stated

- Any requirement that the holder, its controllers, its directors, or its officers be fit and proper, suitable, or of good character
- **Any requirement applying to a new controller or acquirer on a change of control**
- Any specific disqualification: conviction, bankruptcy, disqualification as a director, prior regulatory action, or dishonesty offence
- Any requirement to disclose criminal records, regulatory history, litigation, or financial difficulty
- Any requirement for fingerprinting, background checks, or criminal record certificates
- Any requirement to identify and provide information on ultimate beneficial owners
- Any competence, experience, or qualification requirement for controllers or officers
- Any requirement for individuals to be separately approved or registered
- Any requirement for a business plan, financial projections, or a statement of the acquirer's intentions

## Rules

- **Report the requirements applying to a new controller or acquirer prominently and separately from those applying to the existing holder.** These are what the buyer must satisfy, and gathering the material — background checks on the buyer's officers, ultimate beneficial ownership through a fund structure, criminal record certificates in multiple jurisdictions — is routinely the longest lead item in the deal.
- Report any requirement for individual approval separately, since each individual is a separate application with its own timetable.
- Report the requirements as stated. **Do not assess whether any person would satisfy them.**

## Fallback rules

- Return exactly `None stated` where the documents state no fitness requirement.
- Return `Incorporated terms` where the requirements are stated to be set out in rules not present in the unit. **Common, and the rules should be obtained early**, since buyer-side preparation depends on knowing them.
- Return `Unable to determine` where requirements conflict or are illegible.

## Output format

`Applies to: [holder | controllers | officers | acquirer]; test: [as stated]; disqualifications: [brief]; disclosures required: [brief]; background checks: [as stated or "Not addressed"]; UBO identification: [required | Not addressed]; individual approvals: [as stated or "none"]`

Return no more than 90 words.
```

---

### 24. Prior Change of Control Approvals

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **how this regulator has actually handled a change of control before.**

A prior approval file is the most useful document in the unit. It shows the real
process, the real timetable, the information the regulator asked for, and any
conditions it imposed — none of which can be reliably predicted from the rules.

```markdown
## Task

Report any prior transfer, change of control, or new-controller approval in this review unit.

## Include where expressly stated

- The date of the application and the date of the approval, **and the elapsed period between them**
- The transaction the approval related to, in six words or fewer
- The approving authority and any case officer or reference
- **Any condition the regulator imposed as part of the approval**
- Any information or undertaking the regulator required from the incoming controller
- Any interim or temporary permission granted pending determination
- Any requirement for individual approvals alongside the entity approval, and how long those took
- Any refusal, withdrawal, or resubmission in the history
- Any post-approval reporting or review the regulator required

## Rules

- **Report the actual elapsed period from application to approval.** It is better evidence of the timetable than any stated statutory period, and it is the figure to plan against.
- **Report every condition the regulator imposed**, since it is the best available indication of what it will require this time, and conditions imposed on a prior controller frequently continue to bind.
- Report any information request the file shows, since it tells the buyer what to prepare.
- Report what the documents state. **Do not predict what the regulator will do on this transaction**, and do not assume the prior process will repeat.

## Fallback rules

- Return exactly `None in unit` where no prior approval appears.

Note: this is a positive finding, not a fallback state. **Where the target has changed hands before and no approval file was produced, that is a coverage gap worth pursuing** — the file is usually the single most useful document for planning the filing.

- Return `Unable to determine` where approval documents are illegible.

## Output format

One line per approval:

`[Transaction] — applied [YYYY-MM-DD], approved [YYYY-MM-DD] ([elapsed period]) — conditions: [brief or "none"]`

Return no more than 4 lines and no more than 75 words.
```

---

### 25. Open Findings or Enforcement

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any adverse regulatory history attaching to this authorisation.
  **A poor compliance record makes a change-of-control approval slower and more
  conditional**, independent of the underlying breach.

```markdown
## Task

Report any regulatory finding, enforcement action, or open matter affecting this authorisation that the documents in this unit disclose.

## Include where expressly stated

- Any examination, inspection, or audit finding, with its date and severity as characterised
- Any breach, deficiency, or matter requiring attention identified by the regulator
- Any warning, censure, reprimand, or public statement
- Any fine, penalty, or monetary sanction, with the amount
- Any consent order, settlement, or undertaking with the regulator
- Any suspension, restriction, or condition imposed following an action
- Any remediation required, with its deadline, and whether the documents evidence completion
- Any matter recorded as open, ongoing, or under review
- Any self-reported breach

## Rules

- **Report whether each matter is open or closed on the documents, and the date of the most recent document bearing on it.** An open finding is a live obligation the buyer inherits and it may have to be disclosed in the change-of-control filing.
- **Report any remediation deadline and compare it to the diligence as-of date.** Where a deadline has passed with no evidence of completion, append ` [remediation deadline passed]`.
- Report the regulator's own characterisation of severity using its words, and do not translate it into another scale.
- **Report any self-reported breach separately**, since self-reporting is usually viewed favourably and the distinction matters to how the history reads.
- Cross-reference: enforcement correspondence itself belongs in the Regulatory — Correspondence table, and the reviewer joins them on the regulator and the licence number.
- Do not assess severity, likelihood of further action, or the effect on a pending approval.

## Fallback rules

- Return exactly `None disclosed` where the documents disclose no adverse finding.

Note: this reflects these documents only. **Most regulators publish enforcement histories** and the reviewer should check the public record rather than rely on this cell.

- Return `Unable to determine` where records conflict or are illegible.

## Output format

One line per matter:

`[Matter] — [YYYY-MM-DD] — [severity as characterised] — [open | closed] — remediation: [deadline or "none"]`, with any bracketed flag appended.

Return no more than 8 lines and no more than 95 words.
```

---

### 26. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this licence file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this authorisation that the documents in this unit refer to and that is not present.

## Scope

- **Include any conditions schedule, rulebook, handbook, or set of rules the authorisation is stated to be subject to.** These contain the thresholds, notification periods, and fitness requirements, and their absence is why several columns return `Incorporated terms`
- Include the original application and any supporting material referenced.
- Include renewal certificates and confirmations referenced but absent.
- Include amendments, variations, and endorsements referenced but absent.
- **Include any prior transfer or change-of-control approval referenced but absent.**
- Include examination reports, inspection findings, and enforcement documents referenced but absent.
- Include surety bonds, insurance certificates, and financial filings referenced as required.
- Include individual approval or registration documents for any qualifying individual referenced.
- Include any related authorisation the documents state is held alongside this one.
- Exclude statutes and regulations, **except where a specific rulebook, guidance note, or handbook chapter is identified as containing the conditions or thresholds** — those should be obtained and should be listed.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a rulebook, conditions schedule, or set of rules is referenced and absent, add `; thresholds and conditions unreadable`.** Filter these first: they are what the transaction analysis depends on.
- **Where a prior change-of-control approval is referenced and absent, add `; prior CoC precedent`.**
- Where a qualifying individual's approval document is absent, add `; individual approval unproven`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; flag]`

Return no more than 12 lines and no more than 120 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Status verified against register** | Yes (date) / No / Not available |
| **Threshold crossed by this deal** | Yes / No / Requires local counsel / Unassessed |
| **Filing required** | Prior approval / Prior notification / Post-closing / None / Unassessed |
| **Closing condition** | Yes / No / Unresolved |
| **Estimated timetable** | Free text |
| **Qualifying individual retention critical** | Yes / No / Unassessed |
| **Scope adequate for operations** | Yes / Gap identified / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: holder, status, expiry, threshold, filing
type, review period.

### Reconciliation work that never belongs in a column

- **The threshold analysis.** For each row, compare the buyer's resulting direct
  and indirect ownership against the threshold. **This is a multi-hop question
  through the ownership chain and it is human work** — Harvey supplies the
  threshold, a lawyer supplies the chain and the conclusion.
- **The regulatory calendar.** Every row where a prior approval or notification is
  required, sequenced with its review period against the deal timetable.
  **The longest period sets the earliest closing date**, and identifying it is the
  single most valuable output of this table.
- **Licences against operations.** Match rows against the site list, the business
  activities, and the jurisdictions of operation. **An activity requiring a licence
  in a jurisdiction where none is produced is the highest-value finding this
  workstream generates**, and it is invisible from any single row.
- **Status verification.** Every material row against the public register. Most
  licence registers are searchable and a certificate in a data room proves nothing
  about today.
- **Expiry and renewal calendar.** Every `[expires within 3 months]` and
  `[expired on record]` flag, with a named owner and a decision on whether the
  seller or the buyer files.
- **Qualifying individual retention.** Every row with a qualifying individual
  requirement, matched to the Employment table. **Where the individual is not
  staying and a replacement needs prior approval, this becomes a closing item.**
- **Financial requirement reset.** Every row with a bond, capital requirement, or
  guarantee to the regulator, against the financing plan. Guarantees from entities
  outside the acquired group must be replaced.
- **Fitness preparation.** Every row with acquirer fitness requirements, collated
  into a single buyer-side information request. **This is the longest lead item and
  it can start before signing.**
- **Enforcement history.** Public enforcement records for each regulator and
  holder, since the data room will not contain everything.

---

## Test set

- [ ] Active state licence with conditions and a stated expiry
- [ ] Federal authorisation with no expiry, subject to annual fees
- [ ] Licence expired before the as-of date with no renewal produced
- [ ] Licence expiring within three months of the as-of date
- [ ] Licence with a pending renewal and a continued-operation provision
- [ ] Licence held under a target entity's former name
- [ ] Licence held by an individual personally
- [ ] Licence held by a trading name rather than a legal entity
- [ ] Licence held by an entity not on the target group list
- [ ] Licence with a 10 percent notification and a 25 percent approval threshold
- [ ] Licence with a qualitative control test and no percentage
- [ ] Licence with an aggregation rule for persons acting in concert
- [ ] Licence whose threshold reaches indirect and ultimate ownership
- [ ] Licence whose threshold reaches direct holdings only
- [ ] Licence requiring identification of ultimate beneficial owners
- [ ] Licence certificate stating no threshold at all
- [ ] Licence requiring prior approval with a 90-day determination period
- [ ] Licence with a review period that restarts on any information request
- [ ] Licence with deemed non-objection after a waiting period
- [ ] Licence requiring post-closing notification within five business days
- [ ] Licence stating that no filing is required on a change of control
- [ ] Licence not transferable, requiring a new application
- [ ] Licence with a prior change-of-control approval showing a seven-month elapsed period
- [ ] Licence with a prior approval that imposed continuing conditions
- [ ] Licence with a named qualifying individual and a 30-day replacement window
- [ ] Licence requiring prior approval to replace the qualifying individual
- [ ] Licence with a minimum net worth requirement
- [ ] Licence with a surety bond expiring within the deal period
- [ ] Licence with a parent guarantee given to the regulator by the seller
- [ ] Licence with a volume cap on permitted activity
- [ ] Licence limited to named premises
- [ ] Licence with conditions stated to be in a rulebook not produced
- [ ] Licence with an open examination finding and a passed remediation deadline
- [ ] Licence suspended by the regulator
- [ ] Licence restricted following an enforcement action
- [ ] Licence under review with an investigation pending
- [ ] Passported authorisation covering several jurisdictions
- [ ] Registration rather than a licence, with lighter requirements
- [ ] Unit covering the same licence type in three states

Then test the dependencies: change `Ownership or Control Threshold` from a stated
percentage to `Not addressed` and confirm `Threshold Language` returns
`Not addressed` and `Indirect Control Captured` follows. Change
`Filing Type Required` from `Prior approval required` to
`No filing on change of control` and confirm `Statutory Review Period` moves to
`Not applicable`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
