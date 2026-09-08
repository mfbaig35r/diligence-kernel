# Prompt Inventory — Employment: Policies

Table 9 of the POC. Small table, different question from the individual
agreements.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Employment`
- Review unit: **one policy** — the policy document, every version and amendment
  produced, and any acknowledgement form or jurisdiction-specific addendum issued
  under it
- Grouping used: **yes**, typically 1–4 documents per unit
- Row count: usually 5 to 20 per matter
- Intended reviewers and downstream use: employment team; feeds the unbooked
  liability analysis, the integration plan, and the coverage register
- Inventory version: v1.0

### The question this table asks

Not "what does the handbook say." The M&A questions are narrower and there are
three:

1. **Does this policy create enforceable entitlements?** A contractual policy is a
   promise to every covered employee at once. A policy expressly stated to be
   non-contractual, with a reservation of the right to amend, is not.
2. **Does it create an unbooked liability?** Accrued leave payable on
   termination, a severance formula, a bonus entitlement, or a sabbatical accrual
   are balance-sheet items that frequently sit only in a policy document.
3. **Can the buyer change it?** A policy the employer can amend unilaterally is an
   integration decision. One requiring consent or consultation is a project.

Everything else about a handbook is context.

### Why it is separate from Individual Agreements

A policy is one document binding hundreds of people. Mixing it into a row set
where one row is one individual produces a row that is neither. It is also the
resolution target for the individual table: several columns there return
`Incorporated terms — set out in the Employee Handbook`, and this is where those
resolve.

### Resolution map

| Individual Agreements column returning `Incorporated terms` | Resolves to |
|---|---|
| Notice Periods | `Entitlements Created` |
| Severance Entitlement | `Entitlements Created` |
| Variable Compensation | `Entitlements Created` |
| Confidentiality Survival | `Restrictive and IP Provisions` |
| Arbitration and Class Waiver | `Dispute Resolution Provisions` |
| Non-Compete, Non-Solicit | `Restrictive and IP Provisions` |
| IP Assignment | `Restrictive and IP Provisions` |

**Caution.** A policy term is displaced by an individual agreement where they
conflict, and which governs is a legal question. This table reports what the
policy says; it does not tell you what applies to any named person.

## Assumptions to confirm before running

1. Policies are one row each, not bundled. A handbook containing twenty policies
   is one row where the handbook is the operative document, and the individual
   policies are reported in `Entitlements Created`.
2. Benefit plan documents — pension, health, 401(k), deferred compensation — are
   **not** rows here. They belong to the Benefits and Pensions workstream, which
   is one of the three pending the scope decision.
3. Buy-side review; the entities in the Table Instructions list are the target
   group.
4. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

15 Harvey columns plus 6 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side employment diligence on the target group listed below. This table reviews employer policies, handbooks, and codes.

One row is one policy: the policy document, every version and amendment produced, and any acknowledgement form or jurisdiction-specific addendum issued under it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Adopting entities

Use these names exactly as written when an entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the employer or its workforce.
- **Report what the policy provides. Do not state what applies to any named individual.** An individual agreement may displace a policy term, and which governs is a legal question for the reviewer.
- Where two documents in the unit address the same term, report the term as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Report figures only as the documents state them. Do not calculate, total, annualize, or estimate any accrual or liability.
- Use entity names exactly as printed in the documents; do not shorten, expand, or correct them. Do not report the names of individual employees.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Policy Type
  Adopting Entity
  Population Covered

Stage 2 — Status
  Documents in Unit ──→ Effective Date
                        Version History
                        Referenced but Not Produced
  Policy Type       ──→ Contractual Status
  Contractual Status ──→ Acknowledgement Requirement

Stage 3 — Substance, routed on type
  Policy Type ──→ Entitlements Created
                  Accrued Liability Indicators
                  Restrictive and IP Provisions
                  Dispute Resolution Provisions

Stage 4 — Change control
  Contractual Status ──→ Amendment and Reservation of Rights
  Jurisdiction-Specific Addenda                     (no upstream)
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Effective Date; Version History; Referenced but Not Produced | v1.0 | draft |
| 2 | Policy Type | Classify | — | Contractual Status; Entitlements Created; Accrued Liability Indicators; Restrictive and IP Provisions; Dispute Resolution Provisions | v1.0 | draft |
| 3 | Adopting Entity | Free Response | — | — | v1.0 | draft |
| 4 | Population Covered | Free Response | — | — | v1.0 | draft |
| 5 | Effective Date | Date | @Documents in Unit | — | v1.0 | draft |
| 6 | Version History | Free Response | @Documents in Unit | — | v1.0 | draft |
| 7 | Contractual Status | Classify | @Policy Type | Acknowledgement Requirement; Amendment and Reservation of Rights | v1.0 | draft |
| 8 | Acknowledgement Requirement | Classify | @Contractual Status | — | v1.0 | draft |
| 9 | Amendment and Reservation of Rights | Free Response | @Contractual Status | — | v1.0 | draft |
| 10 | Entitlements Created | Free Response | @Policy Type | — | v1.0 | draft |
| 11 | Accrued Liability Indicators | Free Response | @Policy Type | — | v1.0 | draft |
| 12 | Restrictive and IP Provisions | Free Response | @Policy Type | — | v1.0 | draft |
| 13 | Dispute Resolution Provisions | Classify | @Policy Type | — | v1.0 | draft |
| 14 | Jurisdiction-Specific Addenda | Free Response | — | — | v1.0 | draft |
| 15 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Effective Date`, `Version History`, `Referenced but Not Produced`
- Purpose: inventory the policy family, so a reviewer can see the version sequence.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the policy document, every earlier or later version produced, every amendment or supplement, any acknowledgement or receipt form, and any jurisdiction-specific addendum or appendix.
- Treat appendices and forms physically attached to a version as part of that version.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date or version date.
- State the function as one of `Policy`, `Superseded version`, `Amendment`, `Acknowledgement form`, `Jurisdiction addendum`, or `Other`.
- **Where a document is a different policy than the subject of this row, still list it and append ` [different policy: [name]]`.** A unit mixing two policies produces a merged row.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 10 lines and no more than 80 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Policy Type

- Native type: Classify
- Configured options, in UI order: `Employee handbook`, `Code of conduct`, `Leave and time off`, `Compensation and bonus`, `Severance or redundancy`, `Remote and hybrid work`, `Expenses and travel`, `Disciplinary and grievance`, `Health and safety`, `Equal opportunity and anti-harassment`, `Whistleblowing`, `Data, IT, and acceptable use`, `Recruitment and background checks`, `Training and development`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: five columns
- Purpose: route the substantive columns, since a leave policy and a code of
  conduct create entirely different kinds of exposure.

```markdown
## Task

Classify the policy that is the subject of this review unit. Choose exactly one configured option.

## Classification rules

- `Employee handbook`: a consolidated document containing several policies. **Use this in preference to a component type** where the document covers multiple subjects, and the component policies are reported in Entitlements Created.
- `Code of conduct`: standards of business conduct, ethics, conflicts of interest, gifts, and anti-bribery obligations binding employees.
- `Leave and time off`: holiday, vacation, paid time off, sick leave, parental leave, sabbatical, and other absence entitlements.
- `Compensation and bonus`: salary review, bonus, commission, or incentive frameworks applying across a population rather than to an individual.
- `Severance or redundancy`: a framework setting severance or redundancy terms for a population. **The highest-value type in this table**, because it creates a liability applying to everyone covered.
- `Remote and hybrid work`: location, remote working, and hybrid attendance requirements. Relevant to integration where the buyer's expectations differ.
- `Disciplinary and grievance`: procedures for misconduct, performance management, and complaints.
- `Whistleblowing`: protected disclosure and reporting channels.
- `Data, IT, and acceptable use`: use of systems, monitoring, personal device, and information handling rules binding employees.

Classify on the operative subject, not the title. A document titled a code of conduct that principally sets leave entitlements is `Leave and time off`.

## Fallback rules

- Use `Other` where the policy addresses a subject none of the options describes.
- Use `Unable to determine` where the document is too fragmentary to identify its subject.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Adopting Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity issued the policy, which bears on whether it binds
  the whole group or one employer.

```markdown
## Task

State the entity that issued or adopted this policy.

## Rules

- Take the issuer from the document's letterhead, its title, its introduction, and any approval or authorisation statement.
- Use the entity list in the Table Instructions to determine whether it is a group entity.
- Report the name exactly as printed, including the entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- Where the policy is issued by a parent or group entity and stated to apply across the group, report the issuer and append ` (group-wide)`.
- Where the entity is not on the Table Instructions list, report the name and append ` (not a listed entity)`.
- Where the document names no entity and uses only a trading name or brand, report it as printed and add `(trading name only)`.

## Fallback rules

- Return `Not stated` where the document identifies no issuing entity at all. **This is common for handbooks and it matters**, because a policy that names no employer is harder to attribute and harder to amend.

## Output format

`[Exact name]`, with any qualifier appended. Return no more than 30 words.
```

---

### 4. Population Covered

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who the policy binds. **Determines the size of any liability it
  creates**, and a policy silent on its population is presumed to cover everyone.

```markdown
## Task

Report which employees, entities, and jurisdictions this policy applies to.

## Include where expressly stated

- The entities covered: the issuer only, named subsidiaries, or the whole group
- The jurisdictions or locations covered, and any excluded
- The employee categories covered: all employees, salaried only, a grade or band, a named function, or a stated seniority
- Whether contractors, consultants, agency workers, or temporary staff are covered
- Any express exclusion, such as employees covered by a collective agreement or employees in a named jurisdiction
- Any minimum service requirement before the policy applies

## Rules

- **Where the policy states no limit on its population, report `All employees — no limitation stated`.** That is the most consequential answer in this column, because it means any entitlement in the policy applies to the entire workforce.
- Report whether contractors are covered explicitly. A code of conduct extending to contractors reaches further than the employment population.
- Report the excluded categories, since exclusions define the boundary more reliably than inclusions.
- Do not estimate headcount, and do not name individuals.

## Fallback rules

- Return `Unable to determine` where the population cannot be identified from the document.

## Output format

`Entities: [as stated]; jurisdictions: [as stated]; categories: [as stated]; contractors: [covered | not covered | Not addressed]; exclusions: [brief or "none stated"]`

Return no more than 65 words.
```

---

### 5. Effective Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: when the current version took effect, which determines which version
  applied to any past event.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the operative version and distinguish it from superseded versions. Confirm the date against the documents.

## Task

Identify the date the operative version of this policy took effect.

## Date-selection hierarchy

1. Use an effective date the operative version states for itself.
2. If none, use a version, revision, or issue date printed on the operative version.
3. If neither, use an approval or adoption date the document states.

## Excluded dates

- The date of a superseded version
- The date of a scheduled future review
- The date of an acknowledgement form signed by an employee
- File name and metadata dates, and printing, download, and scan dates
- A copyright year printed in a footer

## Rules

- **Report the date of the operative version, not of the earliest version.** The version history column carries the sequence.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where the document states a scheduled review date that has passed, note that in the evidence field rather than in the cell.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy. **`Not stated` is a common and meaningful answer here** — an undated policy cannot be shown to have applied at any particular time.
```

---

### 6. Version History

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: the sequence of versions, which is what tells a reviewer whether a past
  entitlement differed from the current one.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the versions present. Confirm each version reference against the documents.

## Task

Report the version history of this policy as the documents disclose it.

## Rules

- List each version present in the unit, in date order, with its version number or label as printed.
- **List each version the documents reference but that is not present**, with its date where stated, and append ` (not in unit)`. A policy reciting that it replaces a 2019 version tells you a 2019 version exists.
- Where a version log or revision table appears in the document, report each entry it lists.
- Where the operative version states what it changed, report the change in six words or fewer.
- Where no version information appears anywhere, say so under the fallback rules.
- Do not calculate how long any version was in force.

## Fallback rules

- Return exactly `Single version, no history disclosed` where the unit contains one version and it references none.

Note: this is a positive finding, not a fallback state. It does not mean no earlier version exists; only the employer's records establish that.

## Output format

One line per version, earliest first:

`[Version or label] — [YYYY-MM-DD or "date not stated"] — [in unit | not in unit][; changed: [brief]]`

Return no more than 8 lines and no more than 80 words.
```

---

### 7. Contractual Status

- Native type: Classify
- Configured options, in UI order: `Expressly non-contractual`, `Expressly contractual`, `Mixed — some terms contractual`, `Not addressed`, `Unable to determine`
- Upstream: `@Policy Type`
- Downstream: `Acknowledgement Requirement`, `Amendment and Reservation of Rights`
- Purpose: whether the policy creates enforceable entitlements.

**This is the most consequential column in the table.** A contractual policy is a
promise made to every covered employee simultaneously. A policy expressly stated
to be non-contractual, with a clear reservation of the right to amend, is a
statement of practice the buyer can change. The difference decides whether every
entitlement in the `Entitlements Created` column is a liability or an aspiration.

```markdown
## Established result

- Policy Type: @Policy Type

## Task

Classify whether this policy states that its terms form part of employees' contracts of employment. Choose exactly one configured option.

## Scope

- Consider express statements about the policy's contractual effect, and any statement that it is for guidance only, does not form part of any contract, or is not intended to create legal obligations.
- Consider any statement that specified terms **are** contractual while others are not.
- Exclude a general statement that employees must comply with the policy. An obligation to comply does not make the policy contractual in the employee's favour.
- Exclude an acknowledgement form, which is reported in its own column.

## Classification rules

- `Expressly non-contractual`: the document states that it does not form part of any contract of employment, or is for guidance or information only.
- `Expressly contractual`: the document states that its terms form part of, or are incorporated into, employees' contracts.
- `Mixed — some terms contractual`: the document distinguishes contractual from non-contractual terms. **Report which terms are contractual in the evidence field**, since that set is the liability.
- `Not addressed`: the document says nothing about its contractual effect. **This is the answer to worry about**, not the reassuring one: a policy conferring a clear entitlement and saying nothing about contractual status may well be enforceable, and the silence is what makes it arguable.

Classify on the express statement, not on how the entitlements are worded. A policy conferring detailed entitlements while stating expressly that it is non-contractual is `Expressly non-contractual`, and the tension is for the reviewer.

## Fallback rules

- Use `Unable to determine` where statements in the unit conflict, or where the relevant text is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Acknowledgement Requirement

- Native type: Classify
- Configured options, in UI order: `Signed acknowledgement required, form in unit`, `Signed acknowledgement required, form not in unit`, `Electronic acceptance required`, `Deemed acceptance on continued employment`, `No acknowledgement required`, `Not addressed`, `Unable to determine`
- Upstream: `@Contractual Status`
- Downstream: none
- Purpose: how the policy is brought to employees' attention, which bears on
  whether restrictive or IP provisions inside it bind anyone.

**Why this matters more than it looks.** Where a handbook contains an arbitration
clause, a confidentiality obligation, or an IP assignment, the acknowledgement is
often the only thing making it binding. An acknowledgement requirement with no
signed forms produced is a coverage gap across the whole workforce.

```markdown
## Established result

- Contractual status: @Contractual Status

## Task

Classify how employees are required to acknowledge or accept this policy. Choose exactly one configured option.

## Scope

- Consider any requirement to sign, acknowledge, accept, or confirm receipt.
- Consider any statement that continued employment constitutes acceptance.
- Exclude a general obligation to comply with the policy.
- Exclude training or attestation requirements not directed at accepting the policy itself.

## Classification rules

- `Signed acknowledgement required, form in unit`: an acknowledgement or receipt form is present in the review unit. Note in the evidence field whether any produced form is completed or blank.
- `Signed acknowledgement required, form not in unit`: the policy requires a signed acknowledgement and no form is present. **A coverage finding** — the signed forms are what evidence that employees are bound, and they belong in the coverage register.
- `Electronic acceptance required`: acceptance is through a system, portal, or click-through.
- `Deemed acceptance on continued employment`: the policy states that continuing to work constitutes acceptance, with no positive act required.
- `No acknowledgement required`: the policy states expressly that no acknowledgement is needed.

Where the policy requires both a signed acknowledgement and electronic acceptance, classify on the signed requirement.

## Fallback rules

- Use `Not addressed` where the policy says nothing about acknowledgement or acceptance.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Amendment and Reservation of Rights

- Native type: Free Response
- Upstream: `@Contractual Status`
- Downstream: none
- Purpose: whether the buyer can change the policy after closing, and what it takes.

```markdown
## Established result

- Contractual status: @Contractual Status

## Task

Report how this policy may be amended, withdrawn, or replaced.

## Include where expressly stated

- Whether the employer reserves the right to amend, vary, or withdraw the policy at any time
- Whether amendment requires employee consent
- Whether amendment requires consultation with employees, a works council, a union, or a representative body
- Any notice period before an amendment takes effect
- Who within the employer may approve an amendment
- Any statement that no amendment is effective unless in writing
- Any statement that the policy prevails over, or yields to, an individual contract where they conflict

## Rules

- **Report the reservation of rights explicitly.** A clear unilateral reservation is what turns a policy from a liability into a management tool, and its absence is the finding.
- **Report any consultation requirement prominently.** A consultation obligation with a works council or union makes a post-closing change a project with a timetable, not a decision, and it should be flagged to the integration plan.
- Report any conflict provision, since it determines whether the policy or an individual agreement wins.
- Report the terms as stated. Do not assess whether a unilateral variation would be effective, which is jurisdiction-specific.

## Fallback rules

- Return `Not addressed` where the policy says nothing about amendment. **Note that a contractual policy with no reservation of the right to amend is the hardest combination to change**, and the reviewer should see the two cells together.
- Return `Incorporated terms` where amendment is stated to be governed by a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Reservation of rights: [as stated or "Not addressed"]; consent required: [yes | no | Not addressed]; consultation required: [with whom or "Not addressed"]; notice: [period or "none stated"]; conflict with individual contract: [as stated or "Not addressed"]`

Return no more than 70 words.
```

---

### 10. Entitlements Created

- Native type: Free Response
- Upstream: `@Policy Type`
- Downstream: none
- Purpose: what the policy actually promises. **This is the column the individual
  agreements table's `Incorporated terms` answers resolve to**, and the one the
  liability analysis is built from.

```markdown
## Established result

- Policy Type: @Policy Type

## Task

Report the substantive entitlements or benefits this policy confers on covered employees.

## Rules by policy type

- `Leave and time off`: the entitlement for each leave type, the accrual basis, any carry-over limit, whether leave is paid, any service-linked increase, and the treatment on termination.
- `Severance or redundancy`: the formula, the qualifying conditions, any service threshold, whether it is additional to statutory entitlement, and any enhanced terms on a change of control.
- `Compensation and bonus`: the bonus or commission framework, the target or maximum, whether it is discretionary or contractual, the payment timing, and the leaver treatment.
- `Employee handbook`: report the entitlement-conferring policies it contains, one line each, with the entitlement in eight words or fewer. **Do not summarize the whole handbook**; report only what it promises.
- `Remote and hybrid work`: any entitlement to work remotely, any minimum office attendance requirement, and any equipment or allowance entitlement.
- `Expenses and travel`: any allowance, per diem, or class-of-travel entitlement.
- `Health and safety`, `Code of conduct`, `Whistleblowing`, `Disciplinary and grievance`, `Equal opportunity and anti-harassment`, `Data, IT, and acceptable use`, `Recruitment and background checks`, `Training and development`: report only entitlements these confer, which is often none. Obligations imposed on employees are not entitlements. See the fallback rules.

## Rules

- **State for each entitlement whether the policy describes it as discretionary or as an entitlement.** That single distinction determines whether it is a liability.
- Report figures, periods, and formulas as printed. **Do not calculate any amount, accrual, or aggregate.**
- Report any entitlement expressed as exceeding a statutory minimum, since the excess is the contractual exposure.
- Report no more than eight entitlements. Where more exist, report the eight with the largest financial effect and append ` and [N] further entitlements`.
- Do not report the policy's obligations on employees, its procedures, or its statements of principle.

## Fallback rules

- Return exactly `None — obligations only` where the policy imposes obligations on employees without conferring any entitlement. **This is the correct and common answer for a code of conduct or an IT policy**, and it is not a gap.
- Return `Incorporated terms` where the entitlements are stated to be set out in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per entitlement:

`[Entitlement] — [amount, period, or formula] — [discretionary | entitlement]`

Return no more than 8 lines and no more than 100 words. Do not include any figure you calculated.
```

---

### 11. Accrued Liability Indicators

- Native type: Free Response
- Upstream: `@Policy Type`
- Downstream: none
- Purpose: the provisions that create balance-sheet liabilities. **These are
  frequently unbooked**, because they sit only in a policy document and nobody in
  the finance workstream has read it.

```markdown
## Established result

- Policy Type: @Policy Type

## Task

Report any provision under which an accrued but unused entitlement becomes payable, carries forward, or must be honoured.

## Include where expressly stated

- **Payment for accrued and unused leave on termination**, and whether it is capped
- Carry-over of unused leave into a later year, and any expiry or cap on carried leave
- Any unlimited or uncapped accrual
- Long service awards, sabbatical entitlements, and their accrual basis
- Bonus or commission earned but not yet paid at termination, and whether it is forfeited
- Accrued severance or redundancy entitlement linked to length of service
- Any deferred entitlement, retention payment, or loyalty payment
- Any obligation to make a payment on a change of control or a transfer of the business
- Any repayment obligation running the other way, such as recoverable training costs or a relocation clawback

## Rules

- **Report the termination treatment for every accruing entitlement.** An entitlement that lapses on termination is not a liability; one payable on termination is. The distinction is the whole purpose of this column.
- Report caps and carry-over limits as stated, since an uncapped carry-over is a materially larger exposure than a capped one.
- Report any repayment obligation owed by the employee, which is an asset rather than a liability.
- Report figures and formulas as stated. **Do not calculate or estimate any accrual, and do not attempt to size the liability.** That is arithmetic against payroll data and it happens in Excel.

## Fallback rules

- Return exactly `None identified` where the policy creates no accruing entitlement payable or carried forward.
- Return `Incorporated terms` where the terms are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per indicator:

`[Entitlement] — accrual: [basis]; cap: [as stated or "uncapped"]; on termination: [payable | forfeited | Not addressed]`

Return no more than 6 lines and no more than 85 words. Do not include any estimate of value.
```

---

### 12. Restrictive and IP Provisions

- Native type: Free Response
- Upstream: `@Policy Type`
- Downstream: none
- Purpose: restrictive covenants, confidentiality, and IP assignment hiding inside
  a policy. **Policies routinely carry provisions that belong in a contract**, and
  they will not be found anywhere else in the review.

```markdown
## Established result

- Policy Type: @Policy Type

## Task

Report any confidentiality, intellectual property, restrictive covenant, or monitoring provision this policy imposes on employees.

## Include where expressly stated

- Confidentiality obligations, and any duration after employment ends
- **Any assignment of intellectual property, and whether it assigns presently or states that the employee agrees to assign.** A present assignment in a handbook is unusual and worth knowing about; a promise to assign is a defect wherever it appears
- Any waiver of moral rights
- Non-compete, non-solicitation, or non-dealing obligations
- Any obligation to return or delete materials on termination
- Any monitoring of communications, systems, or devices, and any consent to it
- Any personal device or bring-your-own-device provision affecting ownership of data or work product
- Any obligation to disclose inventions, side activities, or outside interests
- Any conflict of interest or outside employment restriction

## Rules

- **Report the operative verb for any IP provision**, because the difference between assigns and agrees to assign decides whether anything transferred.
- Report the duration of any post-employment obligation, since a policy-based obligation surviving termination is often the only residual protection.
- Report any monitoring provision, which bears on the privacy workstream as well as employment.
- Report the terms as stated. Do not assess enforceability, which is jurisdiction-specific and doubtful for covenants imposed by policy rather than contract.

## Fallback rules

- Return exactly `None` where the policy contains no such provision. **This is the expected answer for most policy types.**
- Return `Incorporated terms` where the provisions are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per provision:

`[Provision] — [scope and duration as stated]` — and for any IP provision, quote the operative verb in the evidence field.

Return no more than 6 lines and no more than 80 words.
```

---

### 13. Dispute Resolution Provisions

- Native type: Classify
- Configured options, in UI order: `Arbitration with class waiver`, `Arbitration, no class waiver`, `Class waiver only`, `Internal procedure only`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Policy Type`
- Downstream: none
- Purpose: whether the policy is where the arbitration and class-waiver provisions
  live. **They frequently are**, and the individual agreements table returns
  `Incorporated terms` pointing here.

```markdown
## Established result

- Policy Type: @Policy Type

## Task

Classify how this policy provides for employment disputes to be resolved. Choose exactly one configured option.

## Scope

- Consider provisions requiring arbitration, waiving class or collective proceedings, or waiving jury trial.
- Consider internal grievance and complaint procedures.
- Exclude the policy's own amendment and interpretation provisions.

## Classification rules

- `Arbitration with class waiver`: the policy requires arbitration and waives class, collective, or representative proceedings. **Aggregated across the covered population, this materially reduces exposure**, which is why the column exists.
- `Arbitration, no class waiver`: arbitration required, no class waiver.
- `Class waiver only`: a class or collective waiver with no arbitration requirement.
- `Internal procedure only`: the policy sets out a grievance, complaint, or appeal procedure and says nothing about arbitration or class proceedings.

Report in the evidence field whether the provision states that it survives termination, whether it applies to claims arising before the policy's effective date, and whether an opt-out is offered. **An opt-out materially weakens the waiver** because it makes coverage a question of who opted out, and the records for that may not exist.

## Fallback rules

- Use `Not addressed` where the policy provides no dispute mechanism of any kind.
- Use `Not applicable` where the policy type could not carry one, such as an expenses or travel policy.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 14. Jurisdiction-Specific Addenda

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: country or state supplements, which route to local counsel rather than
  being analysed by US-law analogue.

```markdown
## Task

Report any jurisdiction-specific addendum, appendix, or supplement to this policy.

## Rules

- List each jurisdiction covered, naming the addendum as the documents name it.
- State whether the addendum is present in the review unit.
- Report what the addendum varies in six words or fewer, for example `notice periods`, `leave entitlement`, `covenant duration`.
- Report any statement that the addendum prevails over the main policy for that jurisdiction.
- Report any statement that the policy is subject to local law where it conflicts.
- **Do not analyse the addendum's effect under non-US law, and do not map it to a US-law analogue.** Report what it says and which jurisdiction it addresses, so the row can be routed to local counsel.
- Where the main policy is stated to apply in a jurisdiction with no addendum, and the policy type is one where local law commonly mandates different terms — leave, severance, or restrictive covenants — note that in the evidence field.

## Fallback rules

- Return exactly `None identified` where the policy has no jurisdiction-specific supplement.
- Return `Incorporated terms` where addenda are referenced but their terms are stated to sit in documents not present in the unit, and name each as referenced.

## Output format

One line per jurisdiction:

`[Jurisdiction] — [addendum name as referenced] — [in unit | not produced] — varies: [brief]`

Return no more than 10 lines and no more than 85 words.
```

---

### 15. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this policy refers to that is not in the unit.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document the documents in this unit refer to and that is not present.

## Scope

- Include other policies, procedures, and codes referenced as applying alongside or as forming part of this one.
- Include earlier or superseded versions referenced but absent.
- Include acknowledgement, receipt, and consent forms referenced but not produced.
- Include jurisdiction-specific addenda and sub-policies referenced but absent.
- Include benefit plan documents, summary plan descriptions, and insurance documents referenced as conferring entitlements.
- Include collective agreements referenced as applying to any covered population.
- Include forms, schedules, and appendices listed as attached but not present.
- Include any employee handbook this policy is stated to form part of.
- Exclude statutes, regulations, and published standards.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Company's Bonus Plan`, report it as printed and add `(no date stated)`.
- **Where a signed acknowledgement form is required and not produced, add `; acknowledgement evidence gap`.** Without the signed forms there is no evidence any employee is bound by provisions sitting only in this policy, and the flag lets that be filtered.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; acknowledgement evidence gap]`

Return no more than 12 lines and no more than 100 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Operative version confirmed** | Yes / No, superseded / History incomplete |
| **Creates enforceable entitlement** | Yes / No / Jurisdiction-dependent / Unassessed |
| **Unbooked liability** | None / Identified (specify) / Unassessed |
| **Amendable post-closing** | Unilaterally / Consultation required / Consent required / Unclear |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** A policy table has ten or twenty rows and each one binds the
whole workforce, so the sampling logic used on large tables does not apply.

### Reconciliation work that never belongs in a column

- **Accrued leave liability.** Take `Accrued Liability Indicators`, apply it to
  payroll and leave-balance data in Excel, and check the result against the
  accounts. **An accrued leave liability that appears in the policy and not in the
  accounts is a purchase-price adjustment.**
- **Severance policy against individual agreements.** Where a severance policy
  applies to a population, check whether it exceeds what individual agreements
  provide. The higher of the two usually governs and the policy is often the
  higher.
- **Resolution of `Incorporated terms`.** Take every Individual Agreements row
  returning `Incorporated terms` for notice, severance, bonus, covenants, IP, or
  arbitration, and confirm that a row in this table actually answers it. Where
  none does, the policy was not produced and it belongs in the coverage register.
- **Acknowledgement coverage.** For any policy carrying restrictive, IP, or
  arbitration provisions, check whether signed acknowledgements exist for the
  covered population. This is usually a sampling exercise against HR records.
- **Consultation obligations.** Filter `Amendment and Reservation of Rights` to
  rows requiring consultation, and sequence them into the integration timetable.

---

## Test set

- [ ] Employee handbook containing several policies, expressly non-contractual
- [ ] Employee handbook with no statement about contractual status
- [ ] Handbook expressly stating that specified terms are contractual
- [ ] Leave policy with accrued leave payable on termination
- [ ] Leave policy with unlimited carry-over
- [ ] Leave policy where accrued leave is forfeited on termination
- [ ] Severance policy with a formula exceeding statutory entitlement
- [ ] Severance policy with enhanced terms on a change of control
- [ ] Bonus policy expressly discretionary
- [ ] Bonus policy conferring a contractual entitlement with a leaver pro-rating
- [ ] Code of conduct imposing obligations and conferring nothing
- [ ] Handbook containing an arbitration clause with a class waiver
- [ ] Handbook containing an arbitration clause with an opt-out
- [ ] Handbook containing an IP assignment using "agrees to assign"
- [ ] Handbook containing a present IP assignment
- [ ] Policy containing a non-compete
- [ ] IT policy with a monitoring provision and employee consent
- [ ] Policy requiring signed acknowledgement, with a completed form in the unit
- [ ] Policy requiring signed acknowledgement, with no form produced
- [ ] Policy with deemed acceptance on continued employment
- [ ] Policy with a clear unilateral reservation of the right to amend
- [ ] Contractual policy with no reservation of rights
- [ ] Policy requiring works council consultation before amendment
- [ ] Policy with a UK and a German addendum, one produced and one not
- [ ] Undated policy with no version information
- [ ] Policy stating it supersedes a 2019 version not in the unit
- [ ] Superseded and current versions in the same unit
- [ ] Unit mistakenly containing two different policies
- [ ] Policy naming no issuing entity
- [ ] Policy expressly excluding employees covered by a collective agreement

Then test the dependencies: change `Policy Type` from `Leave and time off` to
`Code of conduct` and confirm the four routed columns re-run, with
`Entitlements Created` moving toward `None — obligations only`. Change
`Contractual Status` from `Expressly contractual` to `Expressly non-contractual`
and confirm `Acknowledgement Requirement` and
`Amendment and Reservation of Rights` re-run.

Finally, test the resolution map: take one Individual Agreements row returning
`Incorporated terms` for severance or arbitration, and confirm a row in this table
answers it. If none does, the gap is a missing policy, not a prompt defect.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
