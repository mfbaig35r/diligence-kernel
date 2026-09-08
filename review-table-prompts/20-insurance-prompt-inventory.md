# Prompt Inventory — Insurance

Table 20 of the POC, completing batch 6.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Finance`
- Review unit: **one policy** — the policy or binder, every endorsement, any
  certificate of insurance, the loss run for that policy, and any claim or
  coverage correspondence produced for it
- Grouping used: **yes**, typically 1–6 documents per unit
- Intended reviewers and downstream use: insurance, litigation, and corporate/M&A
  teams; feeds the run-off and tail analysis, the risk allocation discussion, the
  contractual insurance compliance check, and the coverage register
- Inventory version: v1.0

### The question this table asks

Not what is covered today. **What survives closing.**

`Coverage Trigger` is the column the table turns on, and it was absent from the
original schema. An occurrence policy responds to events during the policy period
whenever the claim is made, so its protection travels with the business almost
automatically. A claims-made policy responds only to claims **made** during the
period, so when it is cancelled or non-renewed at closing, everything not yet
claimed becomes uninsured unless a tail is bought. On D&O, professional, and cyber
lines — which are almost always claims-made — this is the whole insurance
question in an M&A deal.

`Extended Reporting Period` is its companion: whether the tail can be bought, for
how long, and at what cost.

## Assumptions to confirm before running

1. One row is one policy for one period. The same coverage line renewed three
   times is three rows, because limits, retentions, insurers, and exclusions all
   change on renewal. **For a claims-made line this is essential** — the
   retroactive date and the reporting position differ by period.
2. **Expired policies are rows.** For occurrence lines, a policy from six years
   ago may still respond to a claim made today, and for claims-made lines the
   retroactive date history is what establishes continuity of cover.
3. Employee benefit and health plans are not rows here. They belong to the
   Benefits and Pensions workstream, pending that scope decision.
4. Representation and warranty insurance for this transaction is a Deal Documents
   matter, not a row here. Note any existing R&W policy from a prior transaction
   as a row.
5. Buy-side review; the entities in the Table Instructions list are the target
   group.
6. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

27 Harvey columns plus 9 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side insurance diligence on the target group listed below.

One row is one policy for one period: the policy or binder, every endorsement, any certificate of insurance, the loss run for that policy, and any claim or coverage correspondence produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the policy or the insurer.
- **An endorsement changes the policy. Where an endorsement in the unit modifies a term, report the term as endorsed and identify the endorsement.** A policy read without its endorsements is routinely wrong on limits, insureds, and exclusions.
- **A certificate of insurance is evidence that a policy was issued. It is not the policy and its summary is not binding.** Where a certificate is the only document, report from it and say so.
- **Do not assess whether coverage responds to any claim, whether an exclusion applies, or whether a denial is well founded.** All three are coverage opinions and all three are human columns.
- Report figures only as the documents state them. Do not calculate, total, aggregate limits across policies or layers, or convert currency.
- Use entity and insurer names exactly as printed; do not shorten, expand, or correct them.
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
  Coverage Line
  Insurer
  Broker
  Policy Number
  Policy Period

Stage 2 — Evidence and insureds
  Documents in Unit ──→ Evidence Basis
                        Endorsement History
                        Referenced but Not Produced
  Named Insured ──→ Group Coverage Test

Stage 3 — The trigger block
  Coverage Trigger ──→ Retroactive Date
                       Prior Acts Coverage
                       Extended Reporting Period

Stage 4 — Limits and cost
  Per Occurrence Limit, Aggregate Limit, Sublimits,
  Retention or Deductible, Defence Costs Treatment,
  Premium and Audit

Stage 5 — Scope
  Coverage Line ──→ Material Exclusions
  Territory and Jurisdiction Scope
  Excess and Umbrella Layers

Stage 6 — Transaction and claims
  Change of Control Provision ──→ CoC Language
  Cancellation Provisions
  Open Claims Referenced
  Loss History Referenced
  Contractual Insurance Requirements
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Evidence Basis; Endorsement History; Referenced but Not Produced | v1.0 | draft |
| 2 | Coverage Line | Classify | — | Material Exclusions | v1.0 | draft |
| 3 | Insurer | Free Response | — | — | v1.0 | draft |
| 4 | Broker | Free Response | — | — | v1.0 | draft |
| 5 | Policy Number | Free Response | — | — | v1.0 | draft |
| 6 | Policy Period | Free Response | — | — | v1.0 | draft |
| 7 | Evidence Basis | Classify | @Documents in Unit | — | v1.0 | draft |
| 8 | Endorsement History | Free Response | @Documents in Unit | — | v1.0 | draft |
| 9 | Named Insured | Free Response | — | Group Coverage Test | v1.0 | draft |
| 10 | Group Coverage Test | Classify | @Named Insured | — | v1.0 | draft |
| 11 | Additional Insureds | Free Response | — | — | v1.0 | draft |
| 12 | Coverage Trigger | Classify | — | Retroactive Date; Prior Acts Coverage; Extended Reporting Period | v1.0 | draft |
| 13 | Retroactive Date | Date | @Coverage Trigger | — | v1.0 | draft |
| 14 | Prior Acts Coverage | Classify | @Coverage Trigger | — | v1.0 | draft |
| 15 | Extended Reporting Period | Free Response | @Coverage Trigger | — | v1.0 | draft |
| 16 | Per Occurrence Limit | Free Response | — | — | v1.0 | draft |
| 17 | Aggregate Limit | Free Response | — | — | v1.0 | draft |
| 18 | Sublimits | Free Response | — | — | v1.0 | draft |
| 19 | Retention or Deductible | Free Response | — | — | v1.0 | draft |
| 20 | Defence Costs Treatment | Classify | — | — | v1.0 | draft |
| 21 | Material Exclusions | Free Response | @Coverage Line | — | v1.0 | draft |
| 22 | Territory and Jurisdiction Scope | Free Response | — | — | v1.0 | draft |
| 23 | Excess and Umbrella Layers | Free Response | — | — | v1.0 | draft |
| 24 | Change of Control Provision | Classify | — | CoC Language | v1.0 | draft |
| 25 | CoC Language | Verbatim | @Change of Control Provision | — | v1.0 | draft |
| 26 | Cancellation Provisions | Free Response | — | — | v1.0 | draft |
| 27 | Premium and Audit | Free Response | — | — | v1.0 | draft |
| 28 | Open Claims Referenced | Free Response | — | — | v1.0 | draft |
| 29 | Loss History Referenced | Free Response | — | — | v1.0 | draft |
| 30 | Contractual Insurance Requirements | Free Response | — | — | v1.0 | draft |
| 31 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

31 columns — more than the 26 estimated. `Evidence Basis`, `Endorsement History`,
`Territory and Jurisdiction Scope`, `Excess and Umbrella Layers`, and
`Contractual Insurance Requirements` all earned their place. The endorsement point
is the important one: a policy without its endorsements is frequently wrong on the
very terms this table extracts.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Evidence Basis`, `Endorsement History`, `Referenced but Not Produced`
- Purpose: inventory the policy file, and above all record whether the endorsements
  are present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the policy wording, the schedule or declarations page, the binder, every endorsement and rider, any certificate of insurance, the loss run, claim notices, coverage position letters, the proposal or application, and any renewal or non-renewal notice.
- Treat the schedule and the wording as parts of the policy where they are bound together.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title or form number. **Report endorsement form numbers exactly as printed**, since they identify standard wordings and a reviewer will recognise them.
- Give each document's own stated or effective date.
- State the function as one of `Policy wording`, `Schedule or declarations`, `Binder`, `Endorsement`, `Certificate of insurance`, `Loss run`, `Claim notice`, `Coverage letter`, `Application or proposal`, `Renewal notice`, `Non-renewal notice`, or `Other`.
- **Where the declarations page is present without the policy wording, or the wording without the declarations, state that.** Each answers different questions and neither is complete alone.
- Where a document relates to a different policy or period, still list it and append ` [relates to [policy or period]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title or form number] ([Function])`

Return no more than 15 lines and no more than 120 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Coverage Line

- Native type: Classify
- Configured options, in UI order: `General liability`, `Products liability`, `Property and business interruption`, `Business interruption only`, `Workers compensation and employers liability`, `Directors and officers`, `Professional indemnity or errors and omissions`, `Cyber and technology`, `Employment practices liability`, `Fiduciary liability`, `Crime and fidelity`, `Environmental or pollution legal liability`, `Commercial auto`, `Marine, cargo, or transit`, `Umbrella or excess`, `Representation and warranty`, `Credit or trade credit`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Material Exclusions`
- Purpose: what the policy covers, which routes the exclusions column and
  determines which cross-workstream check the row feeds.

```markdown
## Task

Classify the coverage line this policy provides. Choose exactly one configured option.

## Rules

- Classify on the coverage actually granted, not the policy's marketing title.
- **Where a policy provides several coverages in one wording — a package or combined policy — classify on the coverage with the largest limit and report the others in the evidence field.** Note that a package policy may need to be split into several rows if the reviewer wants to track each coverage's limits and exclusions separately; flag that in the evidence field.
- `Directors and officers`: classify here whether the policy is Side A only, Side ABC, or includes entity coverage, and state which in the evidence field. **Side A only protects individuals and does nothing for the company**, which is a material distinction.
- `Professional indemnity or errors and omissions`: coverage for claims arising from the provision of professional services or products, including technology E&O.
- `Cyber and technology`: first-party and third-party cyber coverage. Report in the evidence field whether it includes regulatory fines and penalties where insurable, business interruption, and ransomware, since cyber wordings vary more than any other line.
- `Umbrella or excess`: sits above underlying policies. **Report the underlying policies it sits over in Excess and Umbrella Layers**, since an excess policy is meaningless without knowing what it attaches to.
- `Representation and warranty`: a policy from a prior transaction. Note the transaction in the evidence field.

## Fallback rules

- Use `Other` where the coverage is insurance none of the options describes.
- Use `Unable to determine` where the coverage granted cannot be identified.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Insurer

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who carries the risk, and whether they are good for it.

```markdown
## Task

State the insurer or insurers providing this policy.

## Rules

- Report the risk-bearing insurer's name exactly as printed. **Distinguish the insurer from the managing agent, the coverholder, the MGA, or the broker** — where a policy is written by an agent on behalf of an insurer, the insurer bears the risk and is the name that matters.
- **Where the risk is subscribed by several insurers, report each with its stated participation percentage**, and where more than five participate report the lead and the count. A subscription market policy means a claim must be agreed with several carriers.
- Report any financial strength or credit rating stated in the documents.
- **Where the insurer is a captive, a group company, or a fronting arrangement, report that**, since a captive means the group is bearing its own risk and the coverage is not genuine risk transfer. Use the review-subject list to identify a group insurer.
- Report the insurer's domicile or the market where stated, since a non-admitted or offshore insurer raises different questions.
- **Do not assess the insurer's creditworthiness or the security of the coverage.**

## Fallback rules

- Return `Unable to determine` where the insurer cannot be identified.

## Output format

`[Insurer as printed][ ([participation]%)]` per insurer, then a final line where relevant: `Rating: [as stated]; captive or fronted: [as stated]; agent: [as stated]`

Return no more than 55 words.
```

---

### 4. Broker

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who placed the programme. **The broker is the practical counterparty
  for the tail quotation and the run-off**, and continuity of broker relationship
  matters at closing.

```markdown
## Task

State the broker or intermediary that placed this policy.

## Rules

- Report the broker's name exactly as printed, with any office or team where stated.
- **Report any statement that the broker acts for the insured rather than the insurer**, or the reverse.
- Report any producer, sub-broker, or wholesale broker in the chain where the documents identify one.
- Report any broker commission or fee disclosure where stated.
- **Report whether the broker is appointed by the target or by the seller's group.** A programme placed through the seller's broker under a group arrangement will usually not continue after closing, and the buyer needs its own placement — which is a real timetable item and a common surprise.
- Report any statement that the policy forms part of a wider group or master programme.

## Fallback rules

- Return `Not stated` where the documents identify no broker.

## Output format

`[Broker as printed][ — [office or team]]; acts for: [as stated or "Not addressed"]; group programme: [yes | Not addressed]`

Return no more than 45 words.
```

---

### 5. Policy Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the reference for any enquiry, notification, or tail quotation, and the
  join key to the Litigation table's coverage columns.

```markdown
## Task

State the policy number and any related reference.

## Rules

- **Report the number exactly as printed, including prefixes, suffixes, slashes, and spaces. Do not reformat.** It is the reference for every notification and it is the join key to the Litigation table's `Carrier and Coverage Position` column.
- Where the policy carries separate numbers for separate sections, coverages, or layers, report each and label it.
- Where a renewal issued a new number, report the current number and append ` (previously [number])`.
- Where a binder number differs from the policy number, report both.
- Where the documents give a claim reference or a certificate number, report it in the evidence field rather than here.

## Fallback rules

- Return `Not stated` where no policy number appears.
- Return `Unable to determine` where numbers conflict or are illegible.

## Output format

`[Label] [number]` per reference, separated by semicolons, with any qualifier appended. Return no more than 30 words.
```

---

### 6. Policy Period

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: when the policy responds from and to. **For a claims-made line the
  period is the claim window, not the event window**, and the two are constantly
  confused.

```markdown
## Task

State the period of this policy.

## Rules

- Report the inception and expiry dates as printed, with any stated time of day where the policy gives one.
- **Report the period as endorsed where an endorsement extended, shortened, or reinstated it**, and identify the endorsement.
- Where the policy was cancelled mid-term, report the original expiry and the cancellation date, and append ` (cancelled [YYYY-MM-DD])`.
- Where a binder covers a period pending policy issue, report the binder period and say so.
- Compare the expiry to the diligence as-of date and flag it:
  - already passed: append ` [expired]`
  - within three months: append ` [expires within 3 months]`
  - within six months: append ` [expires within 6 months]`
- **An `[expired]` flag is not a finding by itself.** For an occurrence line an expired policy may still respond to events during its period, and for a claims-made line the expired period's exposure is exactly what the tail question is about. Both are why expired policies are rows.
- **Where the expiry falls within the expected deal period, note in the evidence field that renewal will fall to be negotiated around the transaction**, which affects both terms and the disclosure the insurer will require.

## Fallback rules

- Return `Not stated` where the documents state no period.
- Return `Unable to determine` where periods conflict or are illegible.

## Output format

`[YYYY-MM-DD] to [YYYY-MM-DD]`, with any bracketed flag or qualifier appended. Return no more than 35 words.
```

---

### 7. Evidence Basis

- Native type: Classify
- Configured options, in UI order: `Full policy with wording and schedule`, `Wording without schedule`, `Schedule or declarations only`, `Binder only`, `Certificate of insurance only`, `Broker summary or programme report only`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: how much weight the row carries. **A certificate of insurance is not a
  policy**, and an insurance schedule assembled from a broker's summary is not
  diligence on the wordings.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to classify what evidence is available. Confirm against the documents.

## Task

Classify the evidentiary basis for this row. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Broker summary or programme report only`: the only document is a broker's summary, programme schedule, or insurance report. **The weakest basis** — it is a third party's précis, it is not binding on the insurer, and no exclusion or condition can be read from it.
2. `Certificate of insurance only`: the only document is a certificate. **A certificate evidences that a policy exists and states limits; it is expressly not the policy and confers no rights.** Exclusions, conditions, retroactive dates, and change-of-control provisions cannot be read from one.
3. `Binder only`: the only document is a binder or cover note pending policy issue.
4. `Schedule or declarations only`: the schedule is present without the policy wording. **Limits, retentions, and insureds can be read; exclusions and conditions cannot.**
5. `Wording without schedule`: the wording is present without the schedule. **Exclusions and conditions can be read; limits, insureds, and the period cannot.**
6. `Full policy with wording and schedule`: both are present.

**Where the basis is anything other than `Full policy with wording and schedule`, several columns in this row will necessarily return `Not stated`, and that is a coverage gap rather than an extraction failure.** Note in the evidence field which questions cannot be answered on the available basis.

## Fallback rules

- Use `Unable to determine` where the documents cannot be characterised.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Endorsement History

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: every change made to the policy after issue. **A policy read without
  its endorsements is frequently wrong on limits, insureds, retroactive dates, and
  exclusions** — the very terms this table extracts.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the endorsements present. Confirm each against the endorsement itself.

## Task

List every endorsement, rider, or amendment to this policy in the review unit, and what each changed.

## Rules

- Report each endorsement in effective-date order with its form or endorsement number as printed, its effective date, and what it changed in eight words or fewer.
- **Report specifically any endorsement that changes: the named insured or adds an insured; a limit or sublimit; the retention; the retroactive date; the policy period; the territory; an exclusion, whether adding or removing one; or the change-of-control or assignment provision.** These are the endorsements that alter the answers elsewhere in the row.
- **Where an endorsement adds an exclusion, report it and flag it**, since a mid-term exclusion often follows a claim or a change in the insurer's appetite and it narrows the cover the schedule appears to give.
- **Where an endorsement is numbered in a sequence and a number is missing, note the gap.** Endorsements are usually numbered consecutively and a missing one means an unproduced change.
- Where the schedule lists endorsements that are not present in the unit, note that; the Referenced but Not Produced column carries it.
- Report the endorsements as they read. Do not assess their effect on any claim.

## Fallback rules

- Return exactly `None in unit` where no endorsement is present.

Note: **this is not the same as no endorsement existing.** Where the schedule lists endorsement form numbers, they exist and were not produced.

- Return `Unable to determine` where endorsements are illegible.

## Output format

One line per endorsement, earliest first:

`[Form or number] — [YYYY-MM-DD] — [what it changed]`, with any flag appended.

Return no more than 12 lines and no more than 100 words.
```

---

### 9. Named Insured

- Native type: Free Response
- Upstream: none
- Downstream: `Group Coverage Test`
- Purpose: who is actually insured, exactly as named.

```markdown
## Task

State the named insured or insureds under this policy.

## Rules

- Report each named insured exactly as printed, including entity suffix. **Do not correct or normalize**, since an entity insured under a wrong name may not be insured at all.
- Report the first named insured separately where the policy distinguishes it, since that party usually controls the policy, receives notices, and is responsible for the premium.
- **Report any endorsement adding or removing a named insured, with the endorsement and its effective date.** A subsidiary added mid-term is not covered for the earlier part of the period, which matters for occurrence lines and for claims-made retroactive analysis.
- **Report any automatic-acquisition or newly-acquired-subsidiary provision** extending cover to entities acquired during the period, with any threshold or notification condition. **This is what determines whether a recently acquired subsidiary is covered at all.**
- Report any definition of insured extending beyond named entities — to subsidiaries generally, to employees, to directors and officers, or to joint ventures — as stated.
- Where the policy is issued to a parent outside the acquired group with the target as a subsidiary insured, report both and label each.

## Fallback rules

- Return `Not stated` where the documents state no named insured. **Where Evidence Basis is `Wording without schedule` this is expected**, since the insureds are on the schedule.
- Return `Unable to determine` where names conflict or are illegible.

## Output format

`First named insured: [as printed]`, then `Also named: [as printed]` per additional insured, then `Insured definition extends to: [as stated or "Not addressed"]; automatic acquisition: [as stated or "Not addressed"]`

Return no more than 70 words.
```

---

### 10. Group Coverage Test

- Native type: Classify
- Configured options, in UI order: `All target entities named or covered`, `Some target entities not covered`, `Only one target entity covered`, `Policy held by seller group, target as subsidiary insured`, `Coverage depends on subsidiary definition`, `No target entity insured`, `Unable to determine`
- Upstream: `@Named Insured`
- Downstream: none
- Purpose: whether every entity being acquired is actually insured.

**A subsidiary not named is an uninsured subsidiary.** And where the policy is
held by the seller's parent with the target covered only as a subsidiary, the
target loses cover the moment it ceases to be a subsidiary — which is at closing.
That is the single most consequential structural point in insurance diligence and
this column exists to find it.

```markdown
## Established result

- Named insured: @Named Insured

Use this result and the target group list in the Table Instructions. Confirm against the documents.

## Task

Classify how this policy covers the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No target entity insured`: no entity on the review-subject list is a named insured and none falls within the insured definition.
2. `Policy held by seller group, target as subsidiary insured`: the first named insured is the seller, its parent, or an entity outside the acquired group, and the target is covered as a subsidiary or affiliate. **Cover almost always ceases at closing**, when the target stops being a subsidiary of the named insured. **This row requires a replacement policy or a run-off arrangement, and it is a closing item.**
3. `Coverage depends on subsidiary definition`: no target entity is named, but the insured definition extends to subsidiaries of a named insured and would on its face include target entities. **Whether it does is a policy-construction question**, and the reviewer must read the definition rather than assume.
4. `Only one target entity covered`: one entity on the list is insured and the group has more than one.
5. `Some target entities not covered`: more than one but not all are covered.
6. `All target entities named or covered`: every entity on the review-subject list is a named insured or expressly within the insured definition.

**Do not resolve a name variance by assuming.** Where an insured name is similar to a target entity but could be a different entity, treat that entity as not covered and note the similarity in the evidence field.

**List the uncovered entities in the evidence field** wherever any target entity is not covered, so the gap is actionable without opening the policy.

## Fallback rules

- Use `Unable to determine` where the insureds cannot be read, or where Named Insured returned `Not stated`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 11. Additional Insureds

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: third parties given rights under the policy, usually because a contract
  required it. **Cross-checks against the Contracts Commercial insurance column.**

```markdown
## Task

Report any additional insured, loss payee, or third party given rights under this policy.

## Include where expressly stated

- Each additional insured named, exactly as printed
- Any blanket additional insured endorsement extending cover to parties the insured is contractually required to name, and its conditions
- Any loss payee or mortgagee named
- Any waiver of subrogation in favour of a third party, and whether it is specific or blanket
- Any provision that cover for an additional insured is primary and non-contributory
- Any lender, landlord, customer, or vendor named
- Any severability or separation-of-insureds provision

## Rules

- **Report whether additional insureds are named specifically or covered by a blanket endorsement.** A blanket endorsement conditional on a written contract requiring it means the party is only covered if the contract actually says so — which is exactly what the Contracts Commercial `Insurance Required of Target` column establishes.
- **Report any primary and non-contributory wording**, since it is commonly required by contract and commonly absent, and its absence is a breach of the contract rather than of the policy.
- Report any waiver of subrogation, since it too is commonly a contractual requirement.
- Report the provisions as stated. **Do not assess whether any particular contractual requirement is satisfied**; that comparison happens against the Contracts export.

## Fallback rules

- Return exactly `None` where no additional insured or third-party interest is named or covered.
- Return `Not stated` where Evidence Basis does not permit the question to be answered.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Named: [as printed or "none"]; blanket endorsement: [as stated or "none"]; loss payee: [as printed or "none"]; waiver of subrogation: [specific | blanket | none]; primary and non-contributory: [yes | Not addressed]`

Return no more than 70 words.
```

---

### 12. Coverage Trigger

- Native type: Classify
- Configured options, in UI order: `Occurrence`, `Claims made`, `Claims made and reported`, `Losses discovered`, `Loss occurring during period`, `Not stated`, `Unable to determine`
- Upstream: none
- Downstream: `Retroactive Date`, `Prior Acts Coverage`, `Extended Reporting Period`
- Purpose: **the column this table turns on, and the one absent from the original
  schema.**

Whether coverage survives closing depends almost entirely on this cell. An
occurrence policy responds to events within the period regardless of when the
claim is made, so the protection travels with the business. A claims-made policy
responds only to claims made during the period, so on cancellation or non-renewal
everything not yet claimed becomes uninsured unless a tail is purchased. D&O,
professional indemnity, cyber, employment practices, and fiduciary lines are
almost always claims-made.

```markdown
## Task

Classify the trigger on which this policy responds. Choose exactly one configured option.

## Scope

- Read the insuring clause and any endorsement modifying it.
- Where different sections of a package policy have different triggers, classify on the section with the largest limit and report the others in the evidence field.

## Classification rules

- `Occurrence`: the policy responds to an occurrence, event, or injury taking place during the policy period, whenever the claim is made. **Typical of general liability, products liability, property, and auto.**
- `Claims made`: the policy responds to claims first made against the insured during the policy period, subject to any retroactive date, whenever the underlying act occurred. **Typical of D&O, professional indemnity, errors and omissions, cyber, employment practices, and fiduciary.**
- `Claims made and reported`: the policy responds only where the claim is both made against the insured **and** reported to the insurer during the period or a stated short extension. **Materially narrower than claims made** — a claim made in the last week of the period and reported after expiry may be uncovered entirely, and the distinction is easily missed.
- `Losses discovered`: the policy responds to losses discovered during the period, typical of crime and fidelity cover.
- `Loss occurring during period`: property and first-party wordings responding to loss or damage occurring in the period.

**Classify on the insuring clause, not on the line of business.** The typical trigger for a line is a strong prior but not a rule, and occurrence-form professional policies and claims-made general liability policies both exist.

## Fallback rules

- Use `Not stated` where the available documents do not disclose the trigger. **This is the expected answer where Evidence Basis is `Certificate of insurance only` or `Broker summary or programme report only`, and it is a serious gap** — the most important question about the policy cannot be answered from a certificate.
- Use `Unable to determine` where the insuring clause is illegible or internally inconsistent.

## Output format

Return only the exact configured option and no explanation.
```

---

### 13. Retroactive Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Coverage Trigger`
- Downstream: none
- Purpose: how far back a claims-made policy reaches. **Anything before the
  retroactive date is uninsured**, and a retroactive date later than the business's
  start means an uninsured historic tail.

```markdown
## Established result

- Coverage trigger: @Coverage Trigger

## Task

If Coverage Trigger is `Claims made` or `Claims made and reported`, identify the retroactive date, prior acts date, or continuity date stated.

If Coverage Trigger is `Occurrence`, `Losses discovered`, or `Loss occurring during period`, return exactly `Not applicable`.

If Coverage Trigger is `Not stated` or `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the retroactive date as stated, however labelled — retroactive date, prior acts date, continuity date, or inception of continuous cover.
- **Report the date as endorsed where an endorsement changed it**, and identify the endorsement. **A retroactive date advanced on renewal creates an uninsured gap** for acts between the old and new dates, and that is a finding.
- Where different sections or insureds have different retroactive dates, report each and label it.
- **Where the policy provides full prior acts cover with no retroactive date, return `Not applicable — full prior acts`** and confirm it in Prior Acts Coverage.
- **Where the retroactive date coincides with the current policy's inception, report it and append ` [no prior acts cover]`.** This is the worst common case: the policy covers only acts committed during its own period, so all historic exposure is uninsured.
- Compare the retroactive date to the earliest formation date the reviewer will have from the Corporate table. **Do not perform that comparison yourself**; simply report the date and note in the evidence field that continuity should be tested against the entity's history.

## Fallback rules

- Return `Not stated` where the trigger is claims made and no retroactive date appears. **Where Evidence Basis is a certificate or a broker summary this is expected and it is a gap.**

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 14. Prior Acts Coverage

- Native type: Classify
- Configured options, in UI order: `Full prior acts`, `Prior acts to retroactive date`, `No prior acts cover`, `Prior acts excluded by endorsement`, `Not applicable`, `Not stated`, `Unable to determine`
- Upstream: `@Coverage Trigger`
- Downstream: none
- Purpose: whether historic exposure is covered at all, stated as a controlled
  value so the population can be filtered.

```markdown
## Established result

- Coverage trigger: @Coverage Trigger

## Task

If Coverage Trigger is `Claims made` or `Claims made and reported`, classify the extent of cover for acts committed before the policy period.

If Coverage Trigger is `Occurrence`, `Losses discovered`, or `Loss occurring during period`, return `Not applicable`.

If Coverage Trigger is `Not stated` or `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

- `Full prior acts`: the policy covers claims arising from acts at any time before the period, with no retroactive date limitation.
- `Prior acts to retroactive date`: cover extends back to a stated retroactive date and no further.
- `No prior acts cover`: the retroactive date coincides with the policy inception, so only acts during the period are covered. **All historic exposure is uninsured under this policy**, and the reviewer must establish whether an earlier policy or a tail covers it.
- `Prior acts excluded by endorsement`: an endorsement expressly excludes prior acts, or excludes claims arising from specified prior circumstances. **Report the endorsement and what it excludes in the evidence field** — a specific prior-circumstances exclusion usually means the insurer knew about a problem and declined to cover it, which is a finding in its own right.

Report in the evidence field any prior and pending litigation exclusion date, and any known circumstances or prior knowledge exclusion, since these operate similarly and narrow historic cover in the same way.

## Fallback rules

- Use `Not stated` where the trigger is claims made and the available documents do not disclose the prior acts position.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 15. Extended Reporting Period

- Native type: Free Response
- Upstream: `@Coverage Trigger`
- Downstream: none
- Purpose: **whether the tail can be bought.**

For every claims-made policy this is the question that decides whether the
business's historic exposure is insured after closing. A run-off or extended
reporting period keeps the policy open for claims made after expiry in respect of
acts before it. Where one is available at a stated price for a stated period, the
answer is a purchase decision. Where none is available, the exposure is simply
uninsured, and that changes the risk allocation discussion.

```markdown
## Established result

- Coverage trigger: @Coverage Trigger

## Task

If Coverage Trigger is `Claims made` or `Claims made and reported`, report the extended reporting period, run-off, or tail cover available under this policy.

If Coverage Trigger is `Occurrence`, `Losses discovered`, or `Loss occurring during period`, return exactly `Not applicable`.

If Coverage Trigger is `Not stated` or `Unable to determine`, return exactly `Unable to determine`.

## Include where expressly stated

- **Any automatic extended reporting period granted without additional premium, and its length.** Usually short — 30 to 90 days — and it is not a tail
- **Any optional extended reporting period the insured may purchase, its available lengths, and the premium as a percentage of the annual premium**
- The period within which the option must be exercised after expiry or cancellation. **This is a hard deadline and missing it forfeits the option entirely**
- Whether the option is available on cancellation and non-renewal by either party, or only in stated circumstances
- **Whether a change of control triggers, permits, or forfeits the extended reporting period.** Many D&O policies convert automatically to run-off on a change of control, and some make the tail available only then
- Any run-off cover provision, and its length
- Whether the extended period provides a fresh limit or shares the expiring policy's limit. **Sharing the limit is the norm and it means the tail is not additional cover**
- Any restriction on the acts covered during the extended period

## Rules

- **Report the automatic and the optional periods separately.** The automatic period is a grace period, not a tail, and conflating them badly understates the exposure.
- **Report the exercise deadline prominently.** It runs from expiry or cancellation and it is commonly 30 or 60 days. A deal that closes without exercising it loses the option.
- **Report whether the tail shares or reinstates the limit.**
- Report the premium as a percentage or amount as stated. **Do not calculate the cost.**
- **Report any automatic conversion to run-off on a change of control**, since it may mean the tail is already provided for and no purchase is needed — or that the policy ceases to cover ongoing operations from closing.

## Fallback rules

- Return exactly `None available` where the policy provides no extended reporting period or run-off option. **This is the most serious answer this column can give** for a claims-made line.
- Return `Not stated` where the available documents do not disclose the position. **Expected where Evidence Basis is a certificate or summary, and a gap.**
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Automatic: [period or "none"]; optional: [periods available]; premium: [as stated]; exercise deadline: [period after expiry]; available on: [cancellation | non-renewal | change of control | as stated]; limit: [shared | reinstated | Not addressed]; run-off on CoC: [as stated or "Not addressed"]`

Return no more than 90 words.
```

---

### 16. Per Occurrence Limit

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the limit for a single claim or event.

```markdown
## Task

Report the per occurrence, per claim, or each-and-every-loss limit of this policy.

## Rules

- Report the limit as printed, with the currency, and state which basis the policy uses — per occurrence, per claim, per event, or each and every loss.
- **Report the limit as endorsed where an endorsement changed it**, and identify the endorsement.
- Where different sections or coverages have different limits, report each and label it.
- Where the policy states a combined single limit covering several heads of cover, report it as such.
- **Do not total limits across sections, layers, or policies, and do not convert currency.**
- **Where the policy has no per occurrence limit and operates on an aggregate only, say so** — common in D&O and professional lines, where a single large claim can exhaust the whole policy.

## Fallback rules

- Return `Not stated` where the documents state no per occurrence limit. **Where Evidence Basis is `Wording without schedule` this is expected**, since limits sit on the schedule.
- Return `Not applicable` where the policy operates on an aggregate basis only.
- Return `Unable to determine` where limits conflict or are illegible.

## Output format

`[Figure] [currency] per [basis]` per section, with any qualifier appended. Return no more than 45 words. Do not include totals you calculated.
```

---

### 17. Aggregate Limit

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the total available for the period, which is what a series of claims
  erodes.

```markdown
## Task

Report the aggregate limit of this policy.

## Rules

- Report the aggregate as printed, with the currency, and state the basis — annual aggregate, policy period aggregate, or aggregate per section.
- **Report the limit as endorsed where an endorsement changed it**, and identify the endorsement.
- **Report any erosion of the aggregate the documents disclose** — where a loss run, claim correspondence, or endorsement states that part of the aggregate has been used. **The stated aggregate is not the available limit** where claims have been paid, and this is where that shows.
- Report any reinstatement provision, and whether reinstatement is automatic or purchasable, with any premium.
- Report any separate aggregate for a particular coverage or peril.
- **Do not total aggregates across policies or layers, do not subtract paid claims from the aggregate, and do not calculate remaining availability.** That is arithmetic for the reviewer against the loss runs.

## Fallback rules

- Return `Not stated` where the documents state no aggregate.
- Return `Not applicable` where the policy states expressly that no aggregate applies.
- Return `Unable to determine` where limits conflict or are illegible.

## Output format

`[Figure] [currency] [basis]`; then `Erosion disclosed: [as stated or "none"]; reinstatement: [as stated or "none"]`

Return no more than 55 words. Do not include any figure you calculated.
```

---

### 18. Sublimits

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the inner limits that cap particular exposures. **A headline limit with
  a small sublimit on the relevant peril is a much weaker policy than it appears.**

```markdown
## Task

Report any sublimit, inner limit, or capped extension in this policy.

## Rules

- Report each sublimit with what it applies to and its amount as printed.
- **Report whether each sublimit sits within the aggregate or is additional to it.** A sublimit within the limit reduces what is available for everything else; one that is additional does not.
- Report common sublimits where present: for a cyber policy, ransomware, business interruption, regulatory fines, and forensic costs; for a property policy, flood, earthquake, business interruption indemnity period, and debris removal; for a D&O policy, investigation costs, Side A dedicated limits, and derivative demand costs; for a professional policy, mitigation costs and regulatory defence.
- **Report any indemnity period for business interruption cover**, since it caps the duration of recovery regardless of the amount.
- Report any per-claimant, per-location, or per-event sublimit.
- Report amounts as stated. **Do not total sublimits and do not compare them to the aggregate.**
- **Report any sublimit that appears disproportionately small relative to the headline limit only by reporting both figures.** Do not characterise it as inadequate; the assessment is the reviewer's.

## Fallback rules

- Return exactly `None stated` where the documents state no sublimit.
- Return `Not stated` where Evidence Basis does not permit the question to be answered.
- Return `Unable to determine` where sublimits conflict or are illegible.

## Output format

One line per sublimit:

`[Applies to] — [figure] [currency] — [within aggregate | additional]`

Return no more than 10 lines and no more than 90 words.
```

---

### 19. Retention or Deductible

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the business pays before the policy responds, which is a real
  liability and a cash-flow fact.

```markdown
## Task

Report the deductible, self-insured retention, or excess applying to this policy.

## Rules

- Report the amount as printed, with the currency, and state the basis — per occurrence, per claim, per event, or annual aggregate deductible.
- **Report the amount as endorsed where an endorsement changed it**, and identify the endorsement.
- Where different coverages or perils carry different retentions, report each and label it.
- **Report whether defence costs erode the retention or sit outside it**, since a retention that must be exhausted by defence spend before the insurer engages is materially more onerous.
- **Report any self-insured retention that the insured must actually pay rather than merely bear**, and any requirement that it be maintained in a funded account or supported by collateral. **A large SIR supported by a letter of credit is a financing item** and it should also appear in the Debt workstream.
- Report any aggregate stop-loss or corridor above which the retention ceases to apply.
- Report any waiting period for business interruption cover, in hours or days.
- Report amounts as stated. **Do not total retentions or estimate retained exposure.**

## Fallback rules

- Return `Not stated` where the documents state no retention.
- Return `Not applicable` where the documents state expressly that no deductible applies.
- Return `Unable to determine` where amounts conflict or are illegible.

## Output format

`[Figure] [currency] per [basis]` per coverage; then `Defence costs: [erode | outside]; collateral required: [as stated or "none"]; waiting period: [as stated or "none"]`

Return no more than 65 words.
```

---

### 20. Defence Costs Treatment
 
- Native type: Classify
- Configured options, in UI order: `Costs inclusive, erode the limit`, `Costs in addition to the limit`, `Costs in addition, capped`, `Costs shared or allocated`, `Not stated`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether defence spend eats the cover. **On a liability policy this can
  matter more than the limit itself**, because heavy defence costs on a
  costs-inclusive policy can exhaust the limit before any settlement is reached.

```markdown
## Task

Classify how defence, investigation, and legal costs are treated under this policy. Choose exactly one configured option.

## Scope

- Consider defence costs, legal costs, investigation costs, and claims expenses.
- Consider whether they fall within or outside the limit of indemnity.
- Where different sections treat costs differently, classify on the section with the largest limit and report the others in the evidence field.

## Classification rules

- `Costs inclusive, erode the limit`: defence costs are paid within the limit and reduce what remains for settlement or damages. **Standard on D&O, professional indemnity, cyber, and most claims-made lines**, and it means a limit is worth materially less than it appears where defence is expensive.
- `Costs in addition to the limit`: defence costs are paid outside the limit and do not reduce it. **Standard on general liability occurrence policies** and much more favourable.
- `Costs in addition, capped`: costs are outside the limit but subject to their own cap, which should be reported in Sublimits as well.
- `Costs shared or allocated`: costs are apportioned between insured and uninsured matters or between insured and uninsured parties, under an allocation provision. **Report the allocation basis in the evidence field**, since allocation disputes are a common source of coverage friction.

Report in the evidence field who controls the defence — the insurer, the insured, or the insured with the insurer's consent — and whether there is a duty to defend or only a duty to indemnify. **Control of defence determines who runs a dispute the buyer inherits**, and it is at least as consequential as the costs treatment.

## Fallback rules

- Use `Not stated` where the documents do not disclose the treatment. **Expected where Evidence Basis is a certificate or summary.**
- Use `Not applicable` for a first-party property or crime policy where no defence obligation arises.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 21. Material Exclusions

- Native type: Free Response
- Upstream: `@Coverage Line`
- Downstream: none
- Purpose: what the policy does not cover. **Routed on coverage line, because the
  exclusions that matter differ entirely between lines.**

```markdown
## Established result

- Coverage Line: @Coverage Line

## Task

Report the exclusions in this policy that are material to the target's business.

## Rules by coverage line

- `Directors and officers`: insured versus insured, prior acts and prior knowledge, conduct exclusions and their severability, bodily injury and property damage, ERISA or pension, professional services, major shareholder, and any specific-matter exclusion. **Report the insured versus insured exclusion and any carve-back for derivative actions and bankruptcy trustees**, since it determines whether claims by the company or a successor are covered at all.
- `Professional indemnity or errors and omissions`: specific services excluded, contractual liability, fee disputes, express warranties and guarantees, and any excluded jurisdiction.
- `Cyber and technology`: war and cyber-war, infrastructure failure, unencrypted device, failure to maintain minimum security standards, betterment, and any exclusion for regulatory fines. **Report any minimum-security-standards condition prominently, since it converts a control failure into an uninsured loss.**
- `General liability`, `Products liability`: pollution, professional services, employment practices, contractual liability, recall, and any excluded product or operation.
- `Property and business interruption`: flood, earthquake, named windstorm, cyber and non-physical damage, wear and tear, and any excluded location.
- `Employment practices liability`: wage and hour, mass or class actions, and any specific-matter exclusion.
- `Environmental or pollution legal liability`: known conditions, specified sites, and gradual pollution.
- For other lines, report the exclusions the documents identify as principal, and any specific-matter exclusion.

## Rules

- **Report any exclusion added by endorsement separately and flag it**, with the endorsement. **A specific-matter or specific-site exclusion added mid-term almost always means the insurer knew about a problem**, and it points the reviewer at something the rest of the diligence should have found.
- **Report any exclusion for a named claim, circumstance, product, site, or jurisdiction**, since these are the exclusions that actually bite rather than the standard printed set.
- Report the standard printed exclusions in outline only; report specific and endorsed exclusions in full.
- Report no more than ten exclusions. Where more exist, report the ten most material to this business and append ` and [N] further exclusions`.
- **Do not assess whether any exclusion would apply to any claim.** That is a coverage opinion.

## Fallback rules

- Return `Not stated` where Evidence Basis does not permit exclusions to be read. **Where Evidence Basis is `Certificate of insurance only`, `Schedule or declarations only`, or `Broker summary or programme report only`, this is the expected answer and it is a substantial gap** — exclusions are the single largest thing a certificate cannot tell you.
- Return `Unable to determine` where the exclusions section is illegible.

## Output format

One line per exclusion:

`[Exclusion] — [in wording | added by endorsement [number], [YYYY-MM-DD]]`

Return no more than 10 lines and no more than 100 words.
```

---

### 22. Territory and Jurisdiction Scope

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the policy responds. **A programme written for one territory does
  not cover operations elsewhere**, and a group that expanded without extending its
  cover has an uninsured footprint.

```markdown
## Task

Report the territorial and jurisdictional scope of this policy.

## Include where expressly stated

- **The territorial limits: where the insured activity or occurrence must take place for cover to attach**
- **The jurisdiction limits: where a claim may be brought or a judgment obtained for cover to respond.** These are separate concepts and both matter — a policy covering worldwide activity but only claims brought in one jurisdiction leaves a large gap
- Any excluded territory or jurisdiction, particularly any exclusion of a named country or of a sanctioned territory
- Any sanctions or trade control exclusion or clause
- Whether cover is written on a worldwide basis, worldwide excluding named jurisdictions, or limited to named territories
- Any requirement for local admitted policies in named countries, and whether this policy is a master or a local policy
- Any difference-in-conditions or difference-in-limits provision
- Any financial interest clause

## Rules

- **Report territory and jurisdiction separately**, since the distinction is the source of most territorial gaps.
- **Report any master and local policy structure**, since a non-admitted master policy may be unable to pay a loss locally in some countries regardless of what it says.
- **Report any sanctions clause**, since it can suspend cover entirely for a territory or a counterparty.
- Report the scope as stated. **Do not assess whether the target's operations fall within it**; that comparison is human work against the site list and the Corporate table's foreign qualifications.

## Fallback rules

- Return `Not stated` where the documents do not disclose the territorial scope.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Territory: [as stated]; jurisdiction: [as stated]; exclusions: [as stated or "none"]; sanctions clause: [yes | Not addressed]; structure: [master | local | standalone]; DIC or DIL: [as stated or "none"]`

Return no more than 75 words.
```

---

### 23. Excess and Umbrella Layers

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how this policy sits in a tower. **An excess policy is meaningless
  without knowing what it attaches to**, and a gap between layers is an uninsured
  band in the middle of a programme.

```markdown
## Task

Report how this policy relates to any underlying or excess layer.

## Include where expressly stated

- Whether this policy is primary, excess, or umbrella
- **For an excess or umbrella policy: the underlying policies it sits over, named with their insurers, policy numbers, and limits, and the attachment point**
- Whether the excess policy follows the form of the underlying policy, or has its own wording, and any difference in terms
- **Any requirement that the underlying limits be maintained, and any consequence of a failure to maintain them**
- Any drop-down provision applying where an underlying insurer fails or its limit is exhausted
- Any requirement that underlying limits be exhausted by actual payment rather than by settlement or agreement
- The total programme limit where stated
- Any co-insurance or self-insured layer within the tower

## Rules

- **Report the attachment point and the underlying limits as stated, and do not calculate the tower.** Where the attachment point of this policy exceeds the sum of the underlying limits, report both figures and note the discrepancy; **an uninsured gap between layers is a real and serious finding** and reporting the figures is what surfaces it.
- **Report any requirement that underlying limits be exhausted by actual payment**, since it means a settlement below the underlying limit does not trigger the excess layer at all.
- **Report any maintenance requirement**, since a lapsed underlying policy can leave the excess layer unable to respond.
- **Do not total the programme limit, and do not compute the gap.** Report the figures.

## Fallback rules

- Return exactly `Primary, no layers referenced` where this is a primary policy referencing no excess layer.
- Return `Not stated` where the documents do not disclose the structure.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Position: [primary | excess | umbrella]; attaches at: [figure or "n/a"]; underlying: [insurer, number, limit]` per layer; then `Follow form: [yes | no]; maintenance required: [yes | Not addressed]; exhaustion by payment: [yes | Not addressed]`

Return no more than 85 words. Do not include totals you calculated.
```

---

### 24. Change of Control Provision

- Native type: Classify
- Configured options, in UI order: `Policy terminates on change of control`, `Converts to run-off automatically`, `Insurer consent required`, `Notice required`, `Cover continues for prior acts only`, `Cover continues unaffected`, `Not addressed`, `Not stated`, `Unable to determine`
- Upstream: none
- Downstream: `CoC Language`
- Purpose: what the transaction does to the policy.

**On D&O and professional lines the automatic-run-off outcome is the norm and it is
frequently misread as continuity.** Converting to run-off means the policy stops
covering acts after closing while continuing to cover claims for acts before it —
so the buyer must place new cover for the going-forward business from day one, and
the run-off may need to be paid for.

```markdown
## Task

Classify what a change of control, merger, or sale of the insured does to this policy. Choose exactly one configured option.

## Scope

- Consider any provision addressing a change of control, change in ownership, merger, consolidation, sale of substantially all assets, or the insured ceasing to be a subsidiary of a named insured.
- Consider any transaction, assignment, or material change provision.
- Read any endorsement modifying it.

## Classification rules

Apply the first rule that fits.

1. `Policy terminates on change of control`: the policy ends on the transaction, with or without a return of premium. **The business is uninsured on that line from closing** unless replacement cover is bound.
2. `Converts to run-off automatically`: cover continues for acts, occurrences, or wrongful acts before the transaction and ceases for anything after it. **The norm on D&O and professional lines.** Report in the evidence field the run-off period and whether additional premium is payable.
3. `Cover continues for prior acts only`: substantively similar to run-off, where the documents describe it as a limitation rather than a conversion.
4. `Insurer consent required`: the transaction requires the insurer's consent for cover to continue. **A consent item on the closing checklist**, and the insurer will usually reprice.
5. `Notice required`: notification only, with cover continuing.
6. `Cover continues unaffected`: the policy states expressly that a change of control does not affect cover.

**Where the policy is held by the seller group with the target as a subsidiary insured, the Group Coverage Test column already flags that cover ceases at closing.** Classify this column on the policy's own change-of-control provision, and note the interaction in the evidence field.

## Fallback rules

- Use `Not addressed` where the policy wording contains no change-of-control provision. **For an occurrence policy this is often benign**, since the events during the period remain covered.
- Use `Not stated` where Evidence Basis does not permit the question to be answered. **Expected on a certificate and it is a material gap.**
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 25. CoC Language

- Native type: Verbatim
- Upstream: `@Change of Control Provision`
- Downstream: none
- Purpose: the exact text, which the run-off negotiation and the replacement
  placement are planned against.

```markdown
## Established result

- Change of control provision: @Change of Control Provision

## Task

If Change of Control Provision is any value other than `Not addressed`, `Not stated`, or `Unable to determine`, quote the change of control, transaction, or assignment provision exactly as written.

If it is `Not addressed`, `Not stated`, or `Unable to determine`, return exactly `Not addressed`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision — **which may be an endorsement rather than the wording** — and end the quotation with ` [Source: [document title or endorsement number], [YYYY-MM-DD]]`.
- **Quote the definition of the triggering transaction in full, including every limb and any percentage threshold**, where the definition appears in the unit.
- **Quote any run-off provision, its stated period, and any additional premium provision.**
- Quote any consent requirement and any provision on the insurer's right to reprice or impose terms.
- Quote any provision on the return of premium.
- Where the combined text exceeds 250 words, quote the operative provision, every limb of the definition, and the run-off terms, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction triggers the provision.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 26. Cancellation Provisions

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how the policy can be ended, and by whom. **Relevant to whether the
  buyer can replace cover cleanly at closing** and to whether the insurer can walk
  away.

```markdown
## Task

Report the cancellation and non-renewal provisions of this policy.

## Include where expressly stated

- The insured's right to cancel, and any notice period
- The insurer's right to cancel, the notice period, and the permitted grounds
- **Whether any premium is returned on cancellation, and on what basis** — pro rata or short rate. A short-rate return penalises early cancellation
- Any minimum earned premium or minimum retained premium
- **Any non-cancellable period**, which is common on D&O and professional lines
- Any automatic termination on non-payment, and any grace period
- Any requirement to give notice of non-renewal, and the period
- Any provision that cancellation does not affect claims already notified
- **Any consequence of cancellation for an extended reporting period option**, and whether cancellation preserves or forfeits it

## Rules

- **Report the premium return basis, since it is the cost of replacing cover early.** A short-rate cancellation on a policy with nine months to run is a real expense.
- **Report any effect of cancellation on the extended reporting period option prominently.** Where cancellation triggers the option, the exercise deadline starts running from cancellation and the buyer has a short window.
- **Report any minimum earned premium**, which means part of the premium is unrecoverable however early the policy ends.
- Report any non-cancellable period, since it may mean the policy cannot be ended at closing at all and must simply be allowed to run.

## Fallback rules

- Return `Not stated` where Evidence Basis does not permit the question to be answered.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Insured may cancel: [notice]; insurer may cancel: [notice and grounds]; premium return: [pro rata | short rate | none]; minimum earned: [as stated or "none"]; non-cancellable period: [as stated or "none"]; effect on ERP: [as stated or "Not addressed"]`

Return no more than 80 words.
```

---

### 27. Premium and Audit

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the cost, and whether more of it can arrive later. **An audit or
  adjustment premium is an unbooked liability**, and it can be substantial where
  the exposure base grew during the period.

```markdown
## Task

Report the premium for this policy and any adjustment mechanism.

## Include where expressly stated

- The premium as printed, with the currency, and the period it covers
- Any instalment schedule, and whether instalments remain outstanding
- **Whether the premium is a deposit or provisional premium subject to adjustment**
- **The exposure base for any adjustment** — payroll, turnover, headcount, vehicle count, or values at risk — and the rate
- Any audit right the insurer holds over the exposure base, and its timing
- Any minimum and deposit premium arrangement
- Any premium finance arrangement, and the financier
- Any taxes, levies, or broker fees stated separately
- Any experience-rating, retrospective-rating, or profit-share arrangement
- Any outstanding or disputed premium the documents disclose

## Rules

- **Report any adjustment or audit mechanism prominently.** Where a policy is written on a provisional premium against payroll or turnover, growth during the period produces an additional premium after expiry — **a liability the buyer inherits and one that appears in no schedule.** Workers compensation and general liability policies are the usual cases.
- **Report any premium finance arrangement**, since it is a debt obligation and it should also appear in the Debt workstream. Cancelling the policy usually accelerates it.
- Report any outstanding instalments, since unpaid premium can void cover.
- Report amounts as stated. **Do not calculate an adjustment, annualise, or convert currency.**

## Fallback rules

- Return `Not stated` where the documents state no premium.
- Return `Unable to determine` where figures conflict or are illegible.

## Output format

`Premium: [figure] [currency] for [period]; basis: [fixed | provisional subject to adjustment]; exposure base: [as stated or "n/a"]; audit right: [as stated or "none"]; instalments outstanding: [as stated or "none"]; premium finance: [as stated or "none"]`

Return no more than 80 words. Do not include figures you calculated.
```

---

### 28. Open Claims Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: claims against this policy, which erode the limit and link to the
  Litigation table.

```markdown
## Task

Report any claim, notification, or circumstance notified under this policy that the documents in this unit disclose.

## Include where expressly stated

- Each claim or notification, with its date, the claimant or matter as described, and the insurer's claim reference
- The amount claimed, the reserve set, and any amount paid, each as stated
- **The insurer's coverage position for each: accepted, accepted under reservation of rights, disputed, or denied, with the stated grounds**
- Any notification of circumstances that may give rise to a claim, as distinct from a claim
- Whether defence counsel has been appointed, and by whom
- Any claim closed, withdrawn, or settled, with the outcome as stated
- Any claim the insurer states falls below the retention

## Rules

- **Report any notification of circumstances separately from an actual claim.** On a claims-made policy a valid notification of circumstances during the period preserves cover for a claim arising later — **which can be the only thing standing between a historic problem and an uninsured loss**, and it is easily overlooked.
- **Report the insurer's coverage position with its stated grounds**, in ten words or fewer. A reservation of rights is not acceptance.
- **Report the claim reference and the matter description, since they are the join keys to the Litigation table** and to the loss run.
- Report amounts as stated. **Do not total claims, and do not subtract paid amounts from the aggregate limit.**
- Do not assess whether coverage responds to any claim.

## Fallback rules

- Return exactly `None referenced` where the documents disclose no claim or notification.
- Return `Unable to determine` where claim records conflict or are illegible.

## Output format

One line per claim:

`[YYYY-MM-DD] — [matter or claimant] — [reference] — claimed [figure]; reserve [figure]; paid [figure] — position: [as stated]`

Return no more than 8 lines and no more than 100 words.
```

---

### 29. Loss History Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the claims record, which predicts both future cost and the terms on
  which cover can be replaced.

```markdown
## Task

Report the loss history for this policy as the documents in this unit disclose it.

## Include where expressly stated

- Whether a loss run is present, its date, and the period it covers
- The number of claims in the period, and the number open and closed, as stated
- **Total incurred, total paid, and total outstanding reserves, each exactly as stated on the loss run**
- Any large or unusual individual loss identified
- Any claims frequency or severity trend the documents comment on
- Any loss ratio stated
- Any statement that the loss run is valued as at a stated date
- Any statement that no claims have been made

## Rules

- **Report the loss run's valuation date.** Reserves move, and a loss run six months old understates the position by an unknown amount.
- **Report the figures exactly as the loss run states them. Do not total across categories, do not add paid to outstanding, do not compute a loss ratio, and do not extrapolate a trend.** All of it is arithmetic against the loss run and it belongs in Excel.
- **Where a loss run is not present, say so under the fallback rules.** A loss run is a routine broker deliverable, so its absence is a coverage gap rather than evidence of a clean record — and **a clean loss history is a valuable fact that cannot be assumed from silence.**
- Report claim counts as stated. Do not count claims yourself from a list.

## Fallback rules

- Return exactly `No loss run in unit` where none is present.
- Return `Nil claims stated` where a document states that no claims have been made in the period.
- Return `Unable to determine` where loss figures conflict or are illegible.

## Output format

`Loss run dated [YYYY-MM-DD], covering [period]; claims: [count] ([open] open); incurred [figure]; paid [figure]; outstanding [figure]; notable: [brief or "none"]`

Return no more than 70 words. Do not include figures you calculated.
```

---

### 30. Contractual Insurance Requirements

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether this policy was placed to satisfy a contract, and whether it
  does. **The cross-check against the Contracts Commercial insurance column.**

```markdown
## Task

Report anything in this policy indicating it was placed to satisfy a contractual or statutory insurance requirement.

## Include where expressly stated

- Any certificate of insurance in the unit issued to a named third party, with that party's name and the date
- Any additional insured, loss payee, or waiver of subrogation endorsement naming a party the documents identify as a counterparty, landlord, lender, or customer
- Any endorsement stating that cover is primary and non-contributary in favour of a named party
- Any reference in the documents to a contract, lease, or agreement requiring this insurance
- Any statutory minimum the policy states it satisfies
- Any certificate holder list

## Rules

- **Report every third party named on a certificate, since each is a party whose contract required this cover.** The certificate is often the only evidence in the data room that a contractual insurance obligation exists at all, and it points the reviewer at the underlying agreement.
- **Report the limits stated on any certificate alongside the policy's actual limits where they differ**, and flag the difference. **A certificate overstating the cover is a real exposure**, and it happens.
- **Do not assess whether any contractual requirement is satisfied.** The comparison is against the Contracts Commercial `Insurance Required of Target` column and the Real Estate insurance provisions, and it happens in Excel.
- Report the requirements as evidenced. Do not infer a contractual requirement from the mere existence of the policy.

## Fallback rules

- Return exactly `None evidenced` where nothing indicates the policy was placed for a contractual requirement.
- Return `Unable to determine` where the documents are illegible.

## Output format

One line per third party:

`[Party as named] — [certificate | endorsement] dated [YYYY-MM-DD] — limits stated: [figure or "as policy"]`

Return no more than 8 lines and no more than 80 words.
```

---

### 31. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this policy file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this policy that the documents in this unit refer to and that is not present.

## Scope

- **Include the policy wording where only a schedule, certificate, or summary is present.**
- **Include the schedule or declarations page where only the wording is present.**
- **Include every endorsement listed on the schedule that is not present in the unit.** Endorsements are itemised on the schedule by form number, so a missing one is always identifiable.
- Include the loss run where referenced or absent.
- Include the application, proposal form, or submission referenced.
- Include any underlying or excess policy referenced in the tower.
- Include any local admitted policy referenced under a master programme.
- Include claim notices, coverage letters, and reservation of rights letters referenced.
- Include any prior year's policy referenced for continuity or retroactive date purposes.
- Include any premium finance agreement referenced.
- Include any certificate of insurance referenced as issued.
- Exclude statutes and regulations.

## Rules

- Name each document as the referencing document names it, and give its form number and date where stated.
- **Where an endorsement listed on the schedule is absent, add `; policy terms incomplete`.** Endorsements change limits, insureds, retroactive dates, and exclusions, so a missing one means the row may be wrong on any of them. Filter these first.
- **Where the policy wording is absent, add `; exclusions and conditions unreadable`.**
- **Where a prior year's policy is referenced and absent, add `; retroactive continuity unproven`.** For a claims-made line the chain of retroactive dates across years is what establishes whether historic cover is continuous.
- Where an underlying policy in a tower is absent, add `; attachment unverifiable`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon here — **schedules list their endorsements, and data rooms rarely contain all of them.**

## Output format

One line per missing document:

`[Name or form number as referenced] — [YYYY-MM-DD or "date not stated"][; flag]`

Return no more than 15 lines and no more than 130 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Full policy obtained** | Yes / Schedule only / Certificate only / Outstanding |
| **Coverage adequate for exposure** | Yes / Gap identified / Unassessed |
| **Tail or run-off required** | Yes (specify period) / No / Unassessed |
| **Tail quotation obtained** | Yes (amount) / Requested / Not required |
| **Replacement cover required at closing** | Yes / No / Unresolved |
| **Gap against contractual requirements** | None / Identified (specify) / Unassessed |
| **Group entities uninsured** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: named insured, coverage trigger,
retroactive date, extended reporting period, limits, change of control.

### Reconciliation work that never belongs in a column

- **The tail decision.** **Filter `Coverage Trigger` to `Claims made` and
  `Claims made and reported`** and work each row: the retroactive date, the
  extended reporting period availability and cost, the exercise deadline, and
  whether the change-of-control provision already converts the policy to run-off.
  **This is the single most valuable output of the table**, and the exercise
  deadlines mean it cannot wait until after closing.
- **The uninsured entity list.** Every `Group Coverage Test` row that is not
  `All target entities named or covered`, listing the uncovered entities. Every
  `Policy held by seller group, target as subsidiary insured` row needs replacement
  cover bound for closing.
- **Programme continuity.** For each claims-made line, lay the rows for successive
  years side by side and check that retroactive dates are continuous and that no
  year is missing. **A retroactive date advanced on a renewal creates an uninsured
  band**, and it is only visible across rows.
- **Tower integrity.** For each layered programme, check that each excess policy's
  attachment point equals the underlying limits. **Any gap is an uninsured band**,
  and any lapsed underlying policy may leave the excess unable to respond.
- **Litigation cross-check.** Every Litigation row's carrier and policy number
  against this table. **Filter Litigation's `Insurance Tendered` to `Not tendered`
  first** — untendered matters may still be notifiable and late notice forfeits
  cover. Then check whether any matter falls in a period whose policy is
  claims-made and expiring.
- **Contractual compliance.** The Contracts Commercial `Insurance Required of
  Target` column and the Real Estate insurance provisions against these rows.
  **Requirements the target does not meet are live contractual breaches**, and
  additional-insured and waiver-of-subrogation requirements are the ones most often
  agreed and never implemented.
- **Loss history analysis.** Loss runs exported and analysed for frequency,
  severity, and development. **All arithmetic, none of it a column**, and it drives
  both the reserve discussion and the terms on which cover can be replaced.
- **Audit premium exposure.** Every row with a provisional premium and an audit
  right, sized against actual payroll or turnover with the finance workstream.
- **Broker continuity.** Every row placed through the seller's broker or under a
  group programme, with a replacement placement planned. **This has a real lead
  time and it is a common closing scramble.**

---

## Test set

- [ ] General liability occurrence policy with full wording and schedule
- [ ] D&O claims-made policy with a retroactive date and an ERP option
- [ ] D&O policy converting automatically to run-off on a change of control
- [ ] D&O policy that is Side A only
- [ ] Professional indemnity policy on a claims-made-and-reported basis
- [ ] Claims-made policy whose retroactive date equals inception
- [ ] Claims-made policy with a retroactive date advanced by endorsement
- [ ] Claims-made policy with full prior acts cover
- [ ] Claims-made policy with a specific-matter prior circumstances exclusion
- [ ] Claims-made policy with no ERP available
- [ ] Claims-made policy with an ERP exercisable within 30 days of expiry
- [ ] Cyber policy with a ransomware sublimit and a minimum security standards condition
- [ ] Property policy with a flood sublimit and a BI indemnity period
- [ ] Workers compensation policy with a provisional premium on payroll
- [ ] Policy with an outstanding audit premium disclosed
- [ ] Policy financed through a premium finance agreement
- [ ] Policy where the first named insured is the seller's parent
- [ ] Policy naming three of five target entities
- [ ] Policy relying on a subsidiary definition with no target entity named
- [ ] Policy with an automatic newly-acquired-subsidiary provision
- [ ] Policy with a blanket additional insured endorsement
- [ ] Policy with a specific additional insured and a waiver of subrogation
- [ ] Certificate of insurance issued to a landlord
- [ ] Certificate stating limits higher than the policy schedule
- [ ] Row where the only document is a certificate of insurance
- [ ] Row where the only document is a broker programme summary
- [ ] Row where the schedule is present without the wording
- [ ] Row where the wording is present without the schedule
- [ ] Policy with endorsements 1 to 5 listed and 3 missing from the unit
- [ ] Policy with an exclusion added mid-term by endorsement
- [ ] Excess policy attaching above two underlying layers
- [ ] Excess policy whose attachment point exceeds the underlying limits
- [ ] Umbrella policy with a drop-down provision
- [ ] Policy with defence costs inside the limit
- [ ] Policy with defence costs in addition to the limit
- [ ] Policy with a large self-insured retention supported by a letter of credit
- [ ] Policy with an aggregate partly eroded by paid claims
- [ ] Policy terminating on change of control
- [ ] Policy requiring insurer consent to a change of control
- [ ] Policy with a non-cancellable period
- [ ] Policy with a short-rate cancellation premium return
- [ ] Policy with a notification of circumstances but no claim
- [ ] Policy with a claim denied on an exclusion
- [ ] Policy with a claim accepted under reservation of rights
- [ ] Policy with a loss run showing significant open reserves
- [ ] Policy with no loss run produced
- [ ] Policy with a nil claims statement
- [ ] Master policy with local admitted policies referenced but not produced
- [ ] Policy with a sanctions exclusion
- [ ] Expired policy from four years ago on an occurrence basis
- [ ] Policy expiring within the expected deal period
- [ ] R&W policy from a prior transaction

Then test the dependencies: change `Coverage Trigger` from `Claims made` to
`Occurrence` and confirm `Retroactive Date`, `Prior Acts Coverage`, and
`Extended Reporting Period` all move to `Not applicable`. Change `Named Insured`
from all target entities to a seller parent and confirm `Group Coverage Test`
moves to `Policy held by seller group, target as subsidiary insured`. Change
`Change of Control Provision` to `Not addressed` and confirm `CoC Language`
follows.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
