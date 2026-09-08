# Prompt Inventory — Employment: Individual Agreements

Table 8 of the POC. The largest table in the set, and the one that feeds the
transaction payments schedule.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Employment`
- Review unit: **one individual** — their offer letter, employment or consulting
  agreement, every amendment, any restrictive covenant or invention assignment
  agreement, any retention or change-in-control agreement, and any separation
  agreement
- Grouping used: **yes**, typically 1–6 documents per unit
- Intended reviewers and downstream use: employment and corporate/M&A teams;
  feeds the transaction payments schedule, the 280G analysis, the retention plan,
  the IP chain-of-title coverage check, and the coverage register
- Inventory version: v1.0

### Why the individual is the row

An executive's terms are rarely in one document. There is an offer letter, an
employment agreement, an amendment two years later raising salary, a
change-in-control agreement signed separately, and sometimes a separation
agreement. One row per document produces five rows that each look like the whole
picture. One row per individual, with the set grouped, produces the answer to the
question the deal team asks: what does this person cost, and what do they owe us.

**The limit matters.** Grouping lets Harvey read the set together. It does not
decide which document governs where they conflict, and a later amendment on
compensation does not necessarily displace an earlier agreement on covenants.
`Operative Version Confirmed` stays human.

### The three questions this table answers

1. **What does this person cost at closing?** Severance, change-in-control
   payments, retention bonuses, equity acceleration, and the 280G treatment.
2. **What do they owe the business after closing?** Non-compete, non-solicit,
   confidentiality, and above all whether the IP assignment is a present
   assignment or a promise.
3. **Can we keep them?** Notice periods, fixed-term expiry, immigration
   dependency, and what a departure triggers.

Everything else is context.

## Assumptions to confirm before running

1. Units are assembled per individual at upload. A unit mixing two people's
   agreements produces a merged row, and `Individual` is the only guard.
2. The employee census is **not** a row set here. It is a single record reconciled
   against this table's export in Excel.
3. Policies and handbooks are a separate table. A handbook is not an individual
   agreement, and mixing them breaks the schema.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

38 Harvey columns plus 9 human columns. **The largest table in the set.** If your
tenant's cap is lower, split into **Employment Terms** (columns 1–16) and
**Employment Payments and Covenants** (columns 17–38) over the same project,
joined on the individual's name in the export.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side employment diligence on the target group listed below.

One row is one individual: their offer letter, employment or consulting agreement, every amendment, any restrictive covenant or invention assignment agreement, any retention or change-in-control agreement, and any separation agreement. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Employing entities

Use these names exactly as written when an entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the individual or the employer.
- The subject of every answer is the individual who is the subject of the current row. Exclude other individuals named in the documents as signatories, managers, referees, or comparators.
- Where two documents in the unit address the same term, report the term as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Report figures only as the documents state them. Do not calculate, annualize, total, convert currency, or apply a multiplier to any figure.
- Use entity and individual names exactly as printed in the documents; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Write currency amounts with the currency as printed, for example `USD 250,000`.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Individual
  Employing Entity
  Role or Title
  Classification
  Jurisdiction of Employment
  Governing Law

Stage 2 — Record status
  Documents in Unit ──→ Execution Status
                        Chain Completeness
                        Employment Status on Record
                        Referenced but Not Produced

Stage 3 — Term and pay
  Employment Basis ──→ Fixed Term Expiry
                       Notice Periods
  Start Date, Base Compensation, Variable Compensation, Equity Referenced

Stage 4 — Payments on exit and on the deal
  Cause Definition, Good Reason Definition          (no upstream)
  Severance Entitlement ──→ Severance Language
  CoC Payment or Benefit ──→ CoC Benefit Detail
                             CoC Language
  Equity Acceleration Referenced, Retention or Transaction Bonus,
  280G Provisions                                    (no upstream)

Stage 5 — Covenants and IP
  Non-Compete   ──→ Non-Compete Language
  IP Assignment ──→ IP Assignment Language
  Non-Solicit Employees, Non-Solicit Customers,
  Confidentiality Survival                           (no upstream)

Stage 6 — Other terms
  Arbitration and Class Waiver, Immigration Dependency,
  Union or Works Council Coverage                    (no upstream)
```

`Classification` is referenced by no substantive column. It routes the reviewer,
not the extraction: a consultant's agreement is read the same way as an employee's,
but the misclassification analysis and the ISO eligibility check depend on the
cell. Referencing it in thirty prompts would add inputs no rule consumes.

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Execution Status; Chain Completeness; Employment Status on Record; Referenced but Not Produced | v1.0 | draft |
| 2 | Individual | Free Response | — | — | v1.0 | draft |
| 3 | Employing Entity | Free Response | — | — | v1.0 | draft |
| 4 | Role or Title | Free Response | — | — | v1.0 | draft |
| 5 | Classification | Classify | — | — | v1.0 | draft |
| 6 | Jurisdiction of Employment | Free Response | — | — | v1.0 | draft |
| 7 | Execution Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 8 | Chain Completeness | Classify | @Documents in Unit | — | v1.0 | draft |
| 9 | Employment Status on Record | Classify | @Documents in Unit | — | v1.0 | draft |
| 10 | Start Date | Date | — | — | v1.0 | draft |
| 11 | Employment Basis | Classify | — | Fixed Term Expiry; Notice Periods | v1.0 | draft |
| 12 | Fixed Term Expiry | Date | @Employment Basis | — | v1.0 | draft |
| 13 | Notice Periods | Free Response | @Employment Basis | — | v1.0 | draft |
| 14 | Base Compensation | Free Response | — | — | v1.0 | draft |
| 15 | Variable Compensation | Free Response | — | — | v1.0 | draft |
| 16 | Equity Referenced | Free Response | — | — | v1.0 | draft |
| 17 | Cause Definition | Free Response | — | — | v1.0 | draft |
| 18 | Good Reason Definition | Free Response | — | — | v1.0 | draft |
| 19 | Severance Entitlement | Free Response | — | Severance Language | v1.0 | draft |
| 20 | Severance Language | Verbatim | @Severance Entitlement | — | v1.0 | draft |
| 21 | CoC Payment or Benefit | Classify | — | CoC Benefit Detail; CoC Language | v1.0 | draft |
| 22 | CoC Benefit Detail | Free Response | @CoC Payment or Benefit | — | v1.0 | draft |
| 23 | CoC Language | Verbatim | @CoC Payment or Benefit | — | v1.0 | draft |
| 24 | Equity Acceleration Referenced | Classify | — | — | v1.0 | draft |
| 25 | Retention or Transaction Bonus | Free Response | — | — | v1.0 | draft |
| 26 | 280G Provisions | Classify | — | — | v1.0 | draft |
| 27 | Non-Compete | Free Response | — | Non-Compete Language | v1.0 | draft |
| 28 | Non-Compete Language | Verbatim | @Non-Compete | — | v1.0 | draft |
| 29 | Non-Solicit Employees | Free Response | — | — | v1.0 | draft |
| 30 | Non-Solicit Customers | Free Response | — | — | v1.0 | draft |
| 31 | IP Assignment | Classify | — | IP Assignment Language | v1.0 | draft |
| 32 | IP Assignment Language | Verbatim | @IP Assignment | — | v1.0 | draft |
| 33 | Confidentiality Survival | Free Response | — | — | v1.0 | draft |
| 34 | Arbitration and Class Waiver | Classify | — | — | v1.0 | draft |
| 35 | Immigration Dependency | Classify | — | — | v1.0 | draft |
| 36 | Union or Works Council Coverage | Classify | — | — | v1.0 | draft |
| 37 | Governing Law | Free Response | — | — | v1.0 | draft |
| 38 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Execution Status`, `Chain Completeness`, `Employment Status on Record`, `Referenced but Not Produced`
- Purpose: inventory the individual's document set, so a reviewer can see the
  sequence and whether the picture is complete.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the offer letter, employment or consulting agreement, every amendment or letter varying terms, restrictive covenant and invention assignment agreements, retention and change-in-control agreements, promotion and salary letters, and any separation or settlement agreement.
- Treat exhibits and schedules physically attached to a document as part of that document.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Offer letter`, `Employment agreement`, `Consulting agreement`, `Amendment`, `Salary or promotion letter`, `Restrictive covenant agreement`, `Invention assignment`, `Retention agreement`, `Change in control agreement`, `Separation agreement`, or `Other`.
- **Where a document relates to a different individual than the subject of this row, still list it and append ` [relates to [name]]`.** A unit mixing two people produces a merged row, and this is how that surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 12 lines and no more than 100 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Individual

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the individual's name, which is the join key for the census
  reconciliation and the cap table cross-check.

```markdown
## Task

State the name of the individual who is the subject of this review unit.

## Rules

- Report the name exactly as printed in the documents, in the form the documents use.
- Where the documents use different forms of the name — a full legal name in the agreement and a short form in a letter — report the fullest form and append ` (also [other form])`.
- Where more than one individual is a subject of documents in the unit, report each on its own line and append ` [multiple individuals in unit]` to the first line. **The unit needs splitting**, and no other column will show it.
- Do not report the individual's title, address, employee number, or any national identifier.
- Do not report signatories acting for the employer, witnesses, or individuals named as managers, referees, or comparators.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the individual, or the name is illegible.

## Output format

`[Name as printed]`, with any qualifier appended. Return no more than 25 words.
```

---

### 3. Employing Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity employs the individual. **Critical in a multi-entity
  group and decisive in a carve-out**, where employees of an entity not being
  acquired have to be transferred or left behind.

```markdown
## Task

State the entity that employs or engages the individual.

## Rules

- Take the employer from the parties clause, the letterhead, and the signature block, in that order of preference where they differ.
- Use the entity list in the Table Instructions to determine whether it is a group entity.
- Report the name exactly as printed, including the entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- **Where the employer changed during the individual's service** — by an amendment, a transfer letter, or a novation in the unit — report the current employer and append ` (transferred from [prior entity], [YYYY-MM-DD])`. A transfer between group entities affects continuity of service and is easy to miss.
- Where the employing entity is not on the Table Instructions list, report the name and append ` (not a listed entity)`. This surfaces an employer missing from the group structure.
- Where a second entity is named as a co-employer or as providing services alongside, report both.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the employer.

## Output format

`[Exact legal name]`, with any qualifier appended. Return no more than 30 words.
```

---

### 4. Role or Title

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the role, which drives key-person identification and the 280G
  disqualified-individual analysis.

```markdown
## Task

State the individual's role or title, and any reporting line the documents state.

## Rules

- Report the title exactly as printed in the most recently dated document in the unit that states one.
- Where an earlier document states a different title, append ` (previously [title], [YYYY-MM-DD])`. A promotion history is relevant to retention and to whether earlier terms still apply.
- Report any stated reporting line in four words or fewer, for example `reports to CEO`.
- **Report any statement that the individual is an officer or director of an entity**, since that determines whether they are a disqualified individual for the 280G analysis and whether they appear in the corporate table's officer list.
- Report any stated location or requirement to work at a particular site, in four words or fewer, since a relocation right or a fixed work location bears on integration.
- Do not report duties in detail, and do not summarize the job description.

## Fallback rules

- Return `Not stated` where no document in the unit states a title.

## Output format

`[Title][; reports to [role]][; officer or director of [entity]][; location: [brief]]`, with any promotion qualifier appended.

Return no more than 40 words.
```

---

### 5. Classification

- Native type: Classify
- Configured options, in UI order: `Employee`, `Independent contractor`, `Consultant`, `Officer and employee`, `Director, non-employee`, `Secondee`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: how the documents characterise the relationship. Feeds the
  misclassification review and the ISO eligibility check.

**Report the characterisation, not the reality.** Whether a person described as a
contractor is in substance an employee is a legal question that turns on how the
role actually operates, and it belongs to a human column.

```markdown
## Task

Classify how the documents characterise the individual's relationship with the employing entity. Choose exactly one configured option.

## Classification rules

- `Employee`: the documents describe employment, use employer and employee as the party terms, or provide employee benefits and payroll withholding.
- `Independent contractor`: the documents describe an independent contractor relationship, commonly with an express statement that the individual is not an employee, no benefits, and responsibility for their own taxes.
- `Consultant`: the documents describe consulting or advisory services, whether or not through a personal service company.
- `Officer and employee`: the individual is both an employee and a stated officer of an entity. **Use this in preference to `Employee`** where both apply, because it is the population the 280G and D&O analyses need.
- `Director, non-employee`: the individual serves on a governing body without an employment relationship.
- `Secondee`: the individual is employed by one entity and seconded to another, whether inside or outside the group.

Classify on the characterisation in the operative documents, not on the job title and not on whether the arrangement looks like employment in substance.

Where the relationship changed — a contractor later made an employee, or the reverse — classify on the current relationship in the most recently dated document, and note the change in the evidence field. **A conversion from contractor to employee is a flag for the misclassification review**, because it often signals the earlier characterisation was wrong.

Where the individual contracts through a personal service company, classify on the stated relationship and note the company in the evidence field.

## Fallback rules

- Use `Unable to determine` where the documents do not characterise the relationship, or where they conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 6. Jurisdiction of Employment

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the individual works, which governs covenant enforceability,
  statutory entitlements, and whether the row needs local counsel.

```markdown
## Task

State the jurisdiction in which the individual is employed or engaged.

## Rules

- Report the jurisdiction the documents identify as the place of work or employment: a state, a province, or a country.
- Where the documents state a work location but no jurisdiction, report the jurisdiction the location falls in only where the documents make it explicit; otherwise report the location as printed.
- Where the individual works remotely with no fixed location, report `remote` and any stated jurisdiction of registration or payroll.
- **Do not report the governing law of the agreement as the jurisdiction of employment.** They differ often, and the difference is exactly what matters: a non-compete governed by Delaware law is tested against the law of the state where the employee actually works. Governing law has its own column.
- Where the documents state a jurisdiction outside the United States, report it and append ` (non-US)` so the row can be routed to local counsel.

## Fallback rules

- Return `Not stated` where the documents identify no place of work or employment.

## Output format

`[Jurisdiction]`, with any qualifier appended. Return no more than 20 words.
```

---

### 7. Execution Status

- Native type: Classify
- Configured options, in UI order: `All documents executed`, `Principal agreement executed, later document unsigned`, `Principal agreement unsigned`, `Partially executed`, `Form or template`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: what the documents prove about their own completion. **An unsigned
  restrictive covenant agreement binds nobody**, and unsigned covenant paperwork
  is one of the most common findings in employment diligence.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks in the current unit.

## Task

Classify the visible execution status of the documents in this review unit. Choose exactly one configured option.

## Scope

- The principal agreement is the employment, consulting, or contractor agreement, or where none is present, the offer letter.
- Evaluate signature blocks, electronic-signature markers, and conformed signatures visible in the documents in this unit.
- Exclude witness and notary blocks from the party count.
- Where a document provides for the individual to acknowledge by countersignature, treat the individual's block as a party block.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the documents are unpopulated forms, with bracketed placeholders, a blank name, or blank compensation fields.
2. `Principal agreement unsigned`: the principal agreement provides signature blocks and none bears a signature marker.
3. `Partially executed`: any document in the unit has at least one signed and at least one unsigned party block. **The employer-signed, employee-unsigned pattern is the one to watch**, since it commonly affects covenant and invention assignment paperwork.
4. `Principal agreement executed, later document unsigned`: the principal agreement is fully signed and at least one amendment, covenant agreement, or side letter in the unit is unsigned.
5. `All documents executed`: every document in the unit bears a signature marker in every party block it provides.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, an initialled page without a signature, or a stated start date is not a signature marker.

## Fallback rules

- Use `Unable to determine` where signature evidence exists but cannot be read, where a signature page is referenced but missing, or where documents in the unit conflict.
- Do not treat a payroll record, a census entry, or a later document reciting the agreement as evidence that it was signed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Principal agreement absent`, `Covenant agreement referenced but absent`, `Invention assignment referenced but absent`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: flag rows where the individual's paperwork is incomplete, so a reviewer
  knows before reading any term that the row may not show current terms.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether this individual's document set appears complete. Choose exactly one configured option.

## Scope

- Consider documents governing this individual's engagement.
- Exclude policies, handbooks, and equity plans referenced generally; those are separate row sets and their absence is not a gap in this unit.
- Exclude documents relating to other individuals.

## Classification rules

Apply the first rule that fits.

1. `Principal agreement absent`: the unit contains amendments, letters, or covenant agreements but no employment, consulting, or contractor agreement and no offer letter setting the terms.
2. `Invention assignment referenced but absent`: a document states the individual has signed or must sign an invention or IP assignment agreement, and it is not present. **This is the highest-value gap this column finds**, because it feeds directly into the IP chain-of-title coverage check.
3. `Covenant agreement referenced but absent`: a document refers to a separate restrictive covenant, non-compete, or confidentiality agreement that is not present.
4. `Amendment referenced but absent`: a document refers to an amendment, variation, or side letter that is not present. A compensation figure reciting a prior increase is common evidence of this.
5. `Complete on its face`: the principal agreement is present and no document refers to a further agreement or amendment that is absent.

`Complete on its face` states only that nothing in these documents reveals a gap.

## Fallback rules

- Use `Unable to determine` where a reference to a further document is too vague to tell whether it governs this individual, or where references are illegible.
- Do not use `Unable to determine` for a single unamended agreement. That is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Employment Status on Record

- Native type: Classify
- Configured options, in UI order: `Active on record`, `Notice given`, `Terminated`, `Fixed term ended, no extension in unit`, `Never commenced`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the documents show the individual as still engaged. **The
  census says who is employed; this column says what the paperwork shows**, and
  the mismatch is a finding in both directions.

**Scope discipline.** This reports what the documents show as at the diligence
as-of date. It does not state whether the individual is currently employed;
employment is not in the documents. A reviewer reads this cell against the census.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory for routing. Confirm the classification against the documents in the current unit.

## Task

Classify what the documents in this unit show about the individual's engagement status as at the diligence as-of date in the Table Instructions. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Terminated`: the unit contains a separation agreement, settlement agreement, termination letter, resignation acceptance, or mutual release ending the engagement.
2. `Notice given`: the unit contains a notice of termination or resignation with a termination date falling on or after the diligence as-of date.
3. `Never commenced`: the unit contains an offer or agreement together with evidence that it was withdrawn, rejected, or that employment never began.
4. `Fixed term ended, no extension in unit`: the engagement is for a fixed term whose stated expiry falls before the diligence as-of date, and the unit contains no extension, renewal, or replacement agreement. **A fixed-term employee still working past expiry is a finding** in most jurisdictions, and it is invisible in a plain expiry column.
5. `Active on record`: none of the above applies.

Where a separation agreement is present but unsigned, classify as `Notice given` if it states a termination date, and otherwise `Active on record`. **An unsigned separation agreement has not terminated anything**, and the distinction matters because the severance may not be payable.

## Fallback rules

- Use `Unable to determine` where documents in the unit conflict about whether the engagement ended, or where a termination document is illegible.
- Do not use `Unable to determine` merely because a fixed term has expired. That is a finding, not an uncertainty.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Start Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: the commencement of service, which drives statutory entitlements,
  notice periods, and severance calculated by reference to length of service.

```markdown
## Task

Identify the date the individual's service commenced.

## Date-selection hierarchy

1. Use a continuous service date or original hire date the documents state, where they distinguish it from the date of the current agreement.
2. If none, use the start or commencement date the principal agreement or offer letter states.
3. If neither, use the effective date of the earliest agreement in the unit.

## Excluded dates

- The date of the current agreement, where an earlier start or continuous service date is stated
- The date of an amendment, promotion letter, or salary letter
- The date of a covenant or invention assignment agreement signed later
- The date of a transfer between group entities, where continuous service is preserved
- File name and metadata dates, and notarization, transmittal, and scan dates

## Rules

- **Where the documents state a continuous service date preserving service across a transfer or a rehire, report that date and not the date of the current employment.** Length of service drives statutory notice and redundancy entitlements in most jurisdictions, and the earlier date is the one that costs money.
- Report the date even where it equals the date of the agreement.
- Where the documents state a start date conditional on a contingency such as a background check or visa, report the stated date and note the condition in the evidence field.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no start date can be selected under the hierarchy.
```

---

### 11. Employment Basis

- Native type: Classify
- Configured options, in UI order: `At will`, `Fixed term`, `Indefinite with notice`, `Rolling term`, `Task or project based`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Fixed Term Expiry`, `Notice Periods`
- Purpose: how the engagement can end, which determines the cost and the timetable
  of removing or losing the individual.

```markdown
## Task

Classify the basis on which the individual is engaged. Choose exactly one configured option.

## Classification rules

- `At will`: the documents state that employment is at will and may be ended by either party at any time, with or without cause or notice.
- `Indefinite with notice`: the engagement has no fixed end date and either party may end it on stated notice. **This is the standard position outside the United States**, and it is materially different from at will because notice must be given or paid.
- `Fixed term`: the engagement runs to a stated end date or for a stated period.
- `Rolling term`: the engagement runs for a stated period and renews automatically unless notice is given.
- `Task or project based`: the engagement runs until completion of stated work, common for contractors and consultants.

Where the documents state that employment is at will **and** provide a notice period, classify as `Indefinite with notice` and note the at-will recital in the evidence field. A notice obligation is inconsistent with pure at-will employment and the tension is worth a reviewer's attention.

Where a fixed term has expired and the documents show no extension, still classify as `Fixed term`. The status is reported in Employment Status on Record.

## Fallback rules

- Use `Not addressed` where the documents state no basis and no notice provision.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Fixed Term Expiry

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Employment Basis`
- Downstream: none
- Purpose: when a fixed or rolling engagement ends, which is a retention date the
  deal team has to diary.

```markdown
## Established result

- Employment basis: @Employment Basis

## Task

If Employment Basis is `Fixed term` or `Rolling term`, identify the end date of the term currently running.

If Employment Basis is `Task or project based`, return `Not applicable — ends on completion of work`.

If Employment Basis is `At will`, `Indefinite with notice`, or `Not addressed`, return exactly `Not applicable`.

If Employment Basis is `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Use the established result for routing, but confirm the date against the documents in the current unit.
- Where a document in the unit extends or renews the term and states a new end date, use that date.
- Where the documents state a start date and a term length but no end date, report the end date those two produce **only if a document states it**. Do not calculate a date from a term.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where it falls before that date, append ` [expired on record]`.
- Do not report the notice period as an end date.

## Fallback rules

- Return `Not stated` where the engagement is fixed or rolling but no end date is stated and none can be reported without calculating.
- Return `Unable to determine` where dates in the unit conflict.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 13. Notice Periods

- Native type: Free Response
- Upstream: `@Employment Basis`
- Downstream: none
- Purpose: how long it takes to remove the individual, and how much warning the
  business gets if they leave. Both are integration facts.

```markdown
## Established result

- Employment basis: @Employment Basis

## Task

Report the notice each party must give to end the engagement.

## Applicability

- Applies where Employment Basis is `Indefinite with notice`, `Fixed term`, `Rolling term`, or `Task or project based`.
- Where Employment Basis is `At will`, report any notice provision the documents contain, and where they contain none return `Not applicable — at will`.
- Where Employment Basis is `Not addressed`, return exactly `Not addressed`.
- Where Employment Basis is `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the employer's notice and the individual's notice separately. **They differ often, and a long employee notice is a retention asset while a long employer notice is a cost.**
- Report any provision for pay in lieu of notice, and whether it is at the employer's election.
- Report any escalation of notice with length of service, as stated.
- Report any garden leave or paid-suspension provision permitting the employer to exclude the individual during notice, since it is what makes a long notice period usable.
- Report any immediate-termination right for cause separately, and where the documents define cause, note that the definition is in its own column.
- Report periods as stated. Do not calculate any date.
- Where a later document in the unit changes the periods, report those in the most recently dated document that addresses them.

## Fallback rules

- Return `Not addressed` for either element where the documents state no notice for it.
- Return `Incorporated terms` where notice is stated to be governed by a policy or handbook not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Employer: [period]; individual: [period]; pay in lieu: [as stated or "Not addressed"]; garden leave: [yes | Not addressed]; immediate for cause: [yes | Not addressed]`

Return no more than 60 words.
```

---

### 14. Base Compensation

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the fixed pay, reported as stated so it can be reconciled against the
  census. **Deltas between agreement and census usually mean an unproduced
  amendment or an undocumented raise**, which is the finding.

```markdown
## Task

Report the individual's base salary, fee, or rate as currently stated.

## Rules

- Report the figure stated in the most recently dated document in the unit that states one, with the currency, the period, and the document and date it comes from.
- **Where an earlier document states a different figure, append ` (previously [figure], [YYYY-MM-DD])`.** The progression is what tells a reviewer whether the current figure is likely current.
- **Do not calculate.** Do not annualize an hourly, daily, or monthly rate; do not convert currency; do not apply a stated increase to a prior figure; do not total base and variable pay.
- Where the individual is paid a rate rather than a salary, report the rate and the unit as printed, for example `USD 1,200 per day`.
- Where compensation is stated as a range or a band, report it as printed.
- Where the documents provide for a review of salary without setting a figure, note that in the evidence field rather than the cell.

## Fallback rules

- Return `Not stated` where no document in the unit states a base figure.
- Return `Incorporated terms` where the figure is stated to be set out in a schedule, offer letter, or payroll record not present in the unit. **This is common for executives whose figure sits in a separate compensation letter**, and it tells the reviewer what to request.
- Return `Unable to determine` where figures stated in documents of the same date conflict.

## Output format

`[Figure] [currency] per [period] — per [document title], [YYYY-MM-DD]`, with any prior-figure qualifier appended.

Return no more than 45 words. Do not include annualized or converted figures you derived.
```

---

### 15. Variable Compensation

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: bonus, commission, and incentive terms, and above all whether they are
  discretionary or contractual. **A contractual bonus is an accrued liability; a
  discretionary one is not.**

```markdown
## Task

Report the individual's variable compensation entitlements.

## Include where expressly stated

- The type: annual bonus, commission, incentive plan participation, profit share, or signing bonus
- The target or maximum, as a percentage of base or as an amount
- **Whether it is discretionary or contractual**, and any language reserving discretion
- The performance measures or targets, in six words or fewer
- The payment timing, and any requirement to be in employment at the payment date
- Any pro-rating on a leaver, or any forfeiture on termination
- Any clawback or repayment provision
- Any guaranteed or minimum bonus, including for a first year
- Any signing bonus with a repayment obligation if the individual leaves within a stated period

## Rules

- **Report the discretionary or contractual character explicitly.** It determines whether the amount is a liability the buyer inherits, and it is the single most consequential element here.
- Report the treatment of a leaver, since a good-leaver pro-rating obligation becomes payable on a departure at closing.
- Report any repayment obligation on a signing bonus, which is an asset rather than a liability.
- Report figures and formulas as stated. Do not calculate any amount, and do not estimate an accrual.

## Fallback rules

- Return exactly `None` where the documents provide for no variable compensation.
- Return `Incorporated terms — set out in [document name as referenced]` where the terms sit in a bonus plan, commission plan, or schedule not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`[Type]: [target or maximum]; [discretionary | contractual]; measures: [brief]; leaver treatment: [as stated or "Not addressed"]; clawback: [brief or "none stated"]`

Return no more than 75 words.
```

---

### 16. Equity Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any equity award the documents mention. **Matched against the
  Capitalization table, equity on the cap table with no grant agreement — or an
  agreement promising equity never granted — is a gap in both directions.**

```markdown
## Task

Report any equity, option, or equity-linked award the documents in this unit reference.

## Scope

- Include options, restricted stock, restricted stock units, warrants, phantom awards, profits interests, and any promise of a future grant.
- Include an award referenced as already granted, and an award the documents oblige the employer to grant.
- Exclude cash bonuses measured by company performance, which belong to Variable Compensation.
- Exclude general statements that the individual is eligible to participate in a plan, with no award referenced.

## Rules

- Report each award with the type, the quantity or percentage as stated, the strike or purchase price where stated, and the grant date where stated.
- **Where the documents promise a grant without evidencing one, report it and append ` (grant not evidenced in unit)`.** A contractual promise of equity that was never granted is a liability, and it appears nowhere in the Capitalization table.
- Report any vesting terms the documents state, in eight words or fewer. Where they refer to a plan, say so; the plan governs and it is reviewed in the Equity Plans table.
- Report any acceleration reference here only in outline; the detail is in the Equity Acceleration Referenced column.
- Do not calculate a value, and do not compute vested amounts.

## Fallback rules

- Return exactly `None referenced` where the documents reference no equity award.
- Return `Unable to determine` where references in the unit conflict, or are illegible.

## Output format

One line per award:

`[Type] — [quantity or percentage] — [price or "not stated"] — granted [YYYY-MM-DD or "not evidenced in unit"]`

Return no more than 5 lines and no more than 70 words.
```

---

### 17. Cause Definition

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what permits summary dismissal without severance. **The breadth of the
  cause definition determines what a termination at closing costs.**

```markdown
## Task

Report the definition of cause, or of gross misconduct, that permits termination without notice or severance.

## Rules

- Report the grounds the definition lists, consolidating substantially similar grounds. Report no more than eight, and where more exist, report the eight broadest and append ` and [N] further grounds`.
- **Report whether any ground requires materiality, wilfulness, or intent**, and whether any requires demonstrable harm to the employer. A cause definition limited to wilful, material misconduct is far narrower than one reaching any breach of policy, and the narrowness is what makes severance payable.
- Report any cure period the definition allows, and any requirement for a board determination or a hearing before cause can be invoked.
- Report where the definition includes conviction of an offence, and whether it requires conviction or permits charge or indictment.
- Report where the definition is expressly non-exhaustive.
- Do not assess whether any ground would be enforceable, and do not state whether cause exists.

## Fallback rules

- Return `Not addressed` where the documents permit termination for cause without defining it. **This is itself a finding**: an undefined cause standard is likely to be construed narrowly and the severance is more likely payable.
- Return `Not applicable` where the documents provide no termination-for-cause right at all.
- Return `Incorporated terms — defined in [document name as referenced]` where the definition sits in a plan, policy, or agreement not present in the unit.
- Return `Unable to determine` where definitions in the unit conflict, or are illegible.

## Output format

`Grounds: [list]; materiality or wilfulness required: [yes | no | varies by ground]; cure period: [as stated or "none"]; board determination required: [yes | Not addressed]`

Return no more than 80 words. Do not include quotations, section numbers, or citation markers.
```

---

### 18. Good Reason Definition

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what permits the individual to resign and still collect severance.

**This is what makes a double trigger operative.** A change-in-control agreement
with double-trigger severance and no good reason definition rarely pays out,
because the buyer simply does not dismiss the individual. With a good reason
definition covering a diminution of duties or a relocation, an integration that
changes the role can trigger it. The definition, not the trigger structure, is
where the money is.

```markdown
## Task

Report the definition of good reason, or of constructive termination, that permits the individual to resign with the consequences of a dismissal.

## Rules

- Report the triggers the definition lists. The usual set is a material diminution of duties, authority, or title; a material reduction in compensation; a relocation beyond a stated distance; a change in reporting line; a material breach of the agreement by the employer; and a failure of a successor to assume the agreement.
- **Report the relocation distance and the reporting-line trigger specifically where present.** Both are routinely triggered by ordinary post-closing integration, and they are the ones that convert an integration decision into a severance payment.
- **Report the successor-assumption trigger where present.** It fires on the transaction itself in an asset deal or a carve-out.
- Report the procedural conditions: any notice the individual must give, any cure period for the employer, and any deadline by which the individual must resign after the trigger. **An expired resignation window extinguishes the entitlement**, and these conditions are frequently the whole answer.
- Report whether any trigger requires the change to be material.
- Do not assess whether any trigger would be met by this transaction, and do not state whether good reason exists.

## Fallback rules

- Return `Not addressed` where the documents provide severance on resignation in stated circumstances without defining good reason.
- Return `Not applicable` where the documents provide no entitlement on resignation at all. **Note that this makes any double-trigger severance in this row largely theoretical**, and the reviewer should see that.
- Return `Incorporated terms — defined in [document name as referenced]` where the definition sits in a plan or agreement not present in the unit.
- Return `Unable to determine` where definitions in the unit conflict, or are illegible.

## Output format

`Triggers: [list]; relocation: [distance or "Not addressed"]; successor assumption: [yes | Not addressed]; individual notice: [period]; employer cure: [period]; resignation deadline: [period or "none stated"]`

Return no more than 85 words.
```

---

### 19. Severance Entitlement

- Native type: Free Response
- Upstream: none
- Downstream: `Severance Language`
- Purpose: what a termination costs. **Aggregated across rows, this column is a
  purchase-price line item**, and it was absent from the original schema entirely.

```markdown
## Task

Report the severance the individual is entitled to on termination, and on what triggers.

## Include where expressly stated

- The cash amount or formula: a multiple of salary, a period of salary continuation, a number of weeks or months per year of service, or a fixed sum
- Whether bonus is included, and on what basis — target, actual, or pro-rated
- Continued benefits or insurance coverage, and for how long
- Outplacement, legal fees, or other stated payments
- **The triggers that give rise to the entitlement**: dismissal without cause, resignation for good reason, redundancy, non-renewal of a fixed term, death, or disability
- Whether the entitlement is enhanced on or after a change of control, and by how much
- Any conditions on payment: a signed release, compliance with covenants, or a return of property
- Any offset against statutory entitlements or against notice pay
- The payment timing: lump sum or instalments

## Rules

- **Report the entitlement separately for each trigger where the amounts differ**, since the closing analysis depends on which trigger applies.
- Report formulas as printed. **Do not calculate any amount**, even where the salary figure is in the unit. Aggregation happens in Excel.
- Report the release condition prominently. An entitlement conditional on a signed release is a negotiating position rather than a fixed liability.
- Report any statutory-offset provision, since it determines whether the contractual figure is additional to or inclusive of statutory pay.
- Where a later document in the unit changes the entitlement, report the entitlement in the most recently dated document that addresses it.

## Fallback rules

- Return exactly `None` where the documents provide no severance entitlement beyond notice.
- Return `Incorporated terms — set out in [document name as referenced]` where severance sits in a severance plan, policy, or change-in-control plan not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per trigger:

`[Trigger] — [cash formula]; bonus: [treatment]; benefits: [period]; conditions: [brief]`

Return no more than 5 lines and no more than 100 words. Do not include any amount you calculated.
```

---

### 20. Severance Language

- Native type: Verbatim
- Upstream: `@Severance Entitlement`
- Downstream: none
- Purpose: the exact text, because a severance figure entering the price model gets
  read word by word first.

```markdown
## Established result

- Severance entitlement: @Severance Entitlement

## Task

If Severance Entitlement reported an entitlement, quote the severance provision exactly as written.

If it returned `None`, return exactly `Not addressed`.

If it returned `Incorporated terms`, return exactly `Not addressed`.

If it returned `Unable to determine`, quote whatever severance language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative entitlement, the triggers, and the conditions on payment.
- Do not quote the cause or good reason definitions here; both have their own columns.
- Where a change-of-control enhancement is stated in the same provision, quote it and label it.
- Where the provision exceeds 250 words, quote the entitlement and each trigger and condition in full, replacing subordinate procedural text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction would trigger payment.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 21. CoC Payment or Benefit

- Native type: Classify
- Configured options, in UI order: `Single trigger`, `Double trigger`, `Enhanced severance on CoC`, `Retention payment on CoC`, `Notice or consultation only`, `No CoC provision`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `CoC Benefit Detail`, `CoC Language`
- Purpose: what the transaction itself triggers for this individual. **Aggregated,
  this column is the transaction payments schedule.**

```markdown
## Task

Classify what a change of control of the employing entity or its parent triggers for this individual. Choose exactly one configured option.

## Scope

- Consider provisions triggered by a change of control, change in control, sale of the business, or similar defined transaction.
- Include cash payments, enhanced severance, retention payments, and benefit continuation.
- **Exclude equity acceleration**, which has its own column. Where a provision does both, classify on the cash or severance element here and report the acceleration there.
- Exclude a general severance entitlement not tied to a change of control.

## Classification rules

Apply the first rule that fits.

1. `Single trigger`: a payment or benefit becomes due on the change of control itself, with no further condition. **The most expensive structure for a buyer**, because the money leaves whether or not the individual stays.
2. `Double trigger`: a payment becomes due only where the change of control is followed by a qualifying termination or a resignation for good reason.
3. `Enhanced severance on CoC`: the individual's existing severance entitlement increases on or after a change of control, without a separate standalone payment.
4. `Retention payment on CoC`: a payment conditional on the individual **remaining** for a stated period after the transaction. Economically the opposite of a single trigger and it should never be filtered together with one.
5. `Notice or consultation only`: the documents require the individual to be notified or consulted, with no payment attached.
6. `No CoC provision`: the documents address a change of control and expressly provide that nothing is triggered.

Classify on the operative mechanics, not on whether the documents use the words single or double trigger.

## Fallback rules

- Use `Not addressed` where the documents say nothing about a change of control.
- Use `Incorporated terms` where the treatment is stated to be governed by a change-in-control plan or policy not present in the unit.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 22. CoC Benefit Detail

- Native type: Free Response
- Upstream: `@CoC Payment or Benefit`
- Downstream: none
- Purpose: the amount and the conditions, which is what the payments schedule needs.

```markdown
## Established result

- CoC payment or benefit: @CoC Payment or Benefit

## Task

If CoC Payment or Benefit is `Single trigger`, `Double trigger`, `Enhanced severance on CoC`, or `Retention payment on CoC`, report the amount and the conditions.

If it is `Notice or consultation only`, report the notice or consultation requirement and the period.

If it is `No CoC provision` or `Not addressed`, return exactly `Not applicable`.

If it is `Incorporated terms`, return `Incorporated terms — set out in [document name as referenced]`.

If it is `Unable to determine`, return exactly `Unable to determine — upstream classification is unresolved`.

## Rules

- Use the established result for routing, but confirm every element against the documents in the current unit.
- Report the amount or formula as stated, with the currency. **Do not calculate.**
- Report the definition of the triggering transaction in six words or fewer, and note whether it captures a sale of assets, a sale of the parent, or only a sale of the employing entity. **A definition limited to the employing entity does not fire on a parent-level deal**, and that is the whole question in a holdco transaction.
- For a double trigger, report the protection window after the change of control within which a termination must occur, and any pre-closing window.
- For a retention payment, report the service period required and any pro-rating on an earlier departure.
- Report the payment timing and any release or covenant-compliance condition.
- Do not state whether this transaction would trigger the payment.

## Output format

`Amount: [figure or formula]; transaction definition: [brief]; window: [period or "Not addressed"]; conditions: [brief]; timing: [as stated]`

Return no more than 80 words. Do not include any amount you calculated.
```

---

### 23. CoC Language

- Native type: Verbatim
- Upstream: `@CoC Payment or Benefit`
- Downstream: none
- Purpose: the exact text, including the transaction definition, which determines
  whether the deal as structured fires the clause at all.

```markdown
## Established result

- CoC payment or benefit: @CoC Payment or Benefit

## Task

If CoC Payment or Benefit is any value other than `No CoC provision`, `Not addressed`, or `Incorporated terms`, quote the change of control provision exactly as written.

If it is `No CoC provision`, `Not addressed`, or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever change of control language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the definition of the triggering transaction in full, including every limb and every exclusion**, where the definition appears in the unit. Whether this deal is a change of control for this individual is decided there, and an exclusion for an internal reorganisation or a transaction in which existing holders retain control can take the deal outside it entirely.
- Quote the operative entitlement and the protection window.
- Do not quote the cause or good reason definitions; both have their own columns.
- Where the combined text exceeds 250 words, quote the operative provision in full and every limb and exclusion of the transaction definition, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction falls within the definition.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 24. Equity Acceleration Referenced

- Native type: Classify
- Configured options, in UI order: `Single trigger acceleration`, `Double trigger acceleration`, `Partial acceleration`, `Acceleration referenced, terms in plan`, `No acceleration`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether this individual's agreement provides equity acceleration
  independently of the plan. **An agreement-level acceleration overrides the plan
  default** and is invisible in the Equity Plans table.

```markdown
## Task

Classify what the documents in this unit state about acceleration of the individual's equity awards on a change of control. Choose exactly one configured option.

## Scope

- Consider acceleration provisions in the employment, retention, change-in-control, or separation documents in this unit.
- Exclude the equity plan's own default terms, which are reviewed in the Equity Plans table. This column reports what **this individual's agreement** adds or changes.

## Classification rules

- `Single trigger acceleration`: the agreement provides that awards vest on the change of control itself.
- `Double trigger acceleration`: the agreement provides that awards vest on a qualifying termination following the change of control.
- `Partial acceleration`: a stated proportion accelerates, or vesting accelerates by a stated period such as twelve months.
- `Acceleration referenced, terms in plan`: the agreement refers to acceleration but states that the terms are governed by the plan or award agreement. **The plan governs, and this cell tells the reviewer to read it** rather than treating the agreement as silent.
- `No acceleration`: the agreement addresses acceleration and expressly provides for none, or expressly disapplies a plan default.
- `Not applicable`: the Equity Referenced column found no equity award and the documents reference none.

Where the agreement provides acceleration terms **more generous than** the plan default, classify on the agreement's terms. An individually negotiated single trigger sitting over a plan default of acceleration-if-not-assumed is a material finding and it will not appear anywhere else.

## Fallback rules

- Use `Not addressed` where the individual holds or is promised equity and the documents say nothing about acceleration.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 25. Retention or Transaction Bonus

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: payments tied to the transaction itself. These are usually funded by the
  seller but they shape retention, and they are frequently agreed late and
  documented separately.

```markdown
## Task

Report any bonus or payment the documents state is payable in connection with a transaction, a sale process, or continued service through a transaction.

## Scope

- Include transaction bonuses, sale bonuses, deal bonuses, retention bonuses, and stay-put payments.
- Include payments conditional on assisting with a sale process or on completion.
- Include any bonus payable out of the sale proceeds or from a seller-funded pool.
- Exclude ordinary annual bonuses, which belong to Variable Compensation.
- Exclude severance and change-of-control severance, which have their own columns.

## Include where expressly stated

- The amount or formula, with the currency
- The trigger: signing, completion, or continued service to a stated date
- Any service period required after completion, and the treatment of an earlier departure
- **Who bears the cost**, where the documents state it — the target, the seller, or a seller-funded pool
- The payment timing
- Any clawback or repayment obligation

## Rules

- **Report who bears the cost where stated.** A target-funded transaction bonus is a purchase-price adjustment; a seller-funded one is not, and the two are treated completely differently.
- Report the amount as stated. Do not calculate.
- Report any condition requiring the individual to remain after completion, since it is a retention term as well as a payment.

## Fallback rules

- Return exactly `None` where the documents provide no such payment.
- Return `Incorporated terms` where the terms sit in a bonus pool document or side letter not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Amount: [figure or formula]; trigger: [as stated]; service required: [period or "none"]; borne by: [as stated or "Not addressed"]; clawback: [brief or "none stated"]`

Return no more than 70 words.
```

---

### 26. 280G Provisions

- Native type: Classify
- Configured options, in UI order: `Cutback to safe harbour`, `Best-net cutback`, `Gross-up`, `Excise tax borne by individual`, `Shareholder approval contemplated`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: how the documents handle excise tax on transaction-related payments.
  **A gross-up is a direct and often large cost to the buyer**, and cutback
  language materially changes what is actually paid.

```markdown
## Task

Classify how the documents address excise tax on payments contingent on a change of control. Choose exactly one configured option.

## Scope

- Consider provisions addressing golden parachute excise tax, Section 280G, Section 4999, or equivalent language about excess parachute payments.
- Exclude ordinary tax withholding and gross-up provisions for relocation, benefits, or other non-transaction payments.
- Where the individual is employed outside the United States and no such provision could apply, return `Not applicable`.

## Classification rules

- `Gross-up`: the employer or the company pays the individual an additional amount to cover the excise tax. **The most expensive outcome for a buyer** and the one to filter for first.
- `Cutback to safe harbour`: payments are reduced to the maximum that avoids the excise tax entirely.
- `Best-net cutback`: payments are reduced only where the reduction leaves the individual better off after tax. This is the modern standard and it is a different calculation from a flat cutback.
- `Excise tax borne by individual`: the documents state expressly that the individual bears any excise tax, with no cutback and no gross-up.
- `Shareholder approval contemplated`: the documents refer to a shareholder vote to cleanse the payments. Relevant only for a private company, and it is a closing-process item that needs sequencing.
- `Not addressed`: the documents provide change-of-control payments and say nothing about excise tax. **This is a finding**, because the exposure exists whether or not the documents mention it.

Where the documents contain both a cutback and a shareholder-approval mechanism, classify on the cutback and note the approval mechanism in the evidence field.

## Fallback rules

- Use `Not applicable` where the documents provide no payment contingent on a change of control, so no excise tax could arise.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 27. Non-Compete

- Native type: Free Response
- Upstream: none
- Downstream: `Non-Compete Language`
- Purpose: what the individual cannot do after leaving, which is the protection the
  buyer is acquiring.

```markdown
## Task

Report any obligation restricting the individual from competing with the business after their engagement ends.

## Scope

- Include non-compete, non-competition, and restraint of trade obligations.
- Include obligations not to be employed by, engaged by, or hold an interest in a competing business.
- **Exclude non-solicitation of employees and of customers**, which have their own columns. Conflating them understates the protection and overstates the restraint.
- Exclude confidentiality obligations.
- Exclude garden leave, which is reported in Notice Periods.

## Include where expressly stated

- The restricted activity, in eight words or fewer, and any definition of a competing business
- The geographic scope
- The duration, and the date it runs from
- Any exception permitting a passive shareholding, and the permitted percentage
- Any provision for the restriction to be reduced or severed if held unenforceable
- **Any payment or consideration for the restriction**, including any obligation to pay during the restricted period
- Whether the restriction applies on any termination or only in stated circumstances

## Rules

- Report the scope limbs separately. A restriction on one activity in one state for six months is a different fact from a general one.
- **Report any obligation to pay during the restricted period.** In several jurisdictions a paid restriction is the only enforceable kind, and the payment is a cost the buyer inherits.
- Report whether the restriction falls away on a dismissal without cause, which is common and materially reduces its value.
- Do not assess enforceability. It varies by jurisdiction and is a human column.

## Fallback rules

- Return exactly `None` where the documents impose no non-compete.
- Return `Incorporated terms — set out in [document name as referenced]` where the restriction sits in a separate covenant agreement not present in the unit. **This pairs with the Chain Completeness flag** and the agreement is reported in Referenced but Not Produced.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Activity: [brief]; territory: [as stated]; duration: [period] from [date basis]; shareholding exception: [percentage or "none"]; payment during restriction: [as stated or "none"]; applies on: [any termination | stated circumstances]`

Return no more than 80 words.
```

---

### 28. Non-Compete Language

- Native type: Verbatim
- Upstream: `@Non-Compete`
- Downstream: none
- Purpose: the exact text. Non-competes are litigated on their wording, and the
  definition of a competing business is usually the operative limb.

```markdown
## Established result

- Non-compete: @Non-Compete

## Task

If Non-Compete reported a restriction, quote the non-compete provision exactly as written.

If it returned `None` or `Incorporated terms`, return exactly `Not addressed`.

If it returned `Unable to determine`, quote whatever non-compete language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative restriction together with the definition of the competing business, the restricted territory, and the restricted period, including any defined terms the provision relies on where those definitions appear in the unit. **The definition of the competing business is the limb that decides the scope**, and quoting the restriction without it is close to useless.
- Quote any severance, blue-pencil, or reduction provision, since it determines what survives if the restriction is too wide.
- Quote any exception or carve-out.
- Where the combined text exceeds 250 words, quote the operative restriction and every scope limb and carve-out, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether the restriction is enforceable.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 29. Non-Solicit Employees

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether the individual can take colleagues with them. Often the
  protection that matters most in a people business, and often more enforceable
  than a non-compete.

```markdown
## Task

Report any obligation restricting the individual from soliciting, recruiting, or employing the employer's personnel after their engagement ends.

## Scope

- Include non-solicitation and non-poaching of employees, workers, and contractors.
- Include obligations not to employ or engage, which are wider than obligations not to solicit.
- Exclude non-solicitation of customers, which is a separate column.
- Exclude non-compete obligations.

## Include where expressly stated

- The duration, and the date it runs from
- **The covered population**: all personnel, senior personnel, those the individual worked with, or those employed at a stated date. This is the limb that determines the restriction's real breadth
- **Whether it prohibits soliciting only, or also employing.** A no-employ obligation catches an approach the individual did not initiate and is materially wider
- Any exception for a general advertisement or a recruitment agency approach
- Any exception for someone who has already left the employer, and any period attached

## Rules

- Report the covered population as stated. A restriction limited to employees the individual personally managed is a much narrower fact than one covering everyone.
- **Report the solicit-versus-employ distinction explicitly.** It is the difference between a restriction that is usually enforceable and one that frequently is not.
- Do not assess enforceability.

## Fallback rules

- Return exactly `None` where the documents impose no such restriction.
- Return `Incorporated terms — set out in [document name as referenced]` where it sits in a covenant agreement not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Duration: [period] from [date basis]; population: [as stated]; prohibits: [solicit only | solicit and employ]; general advertisement exception: [yes | Not addressed]; departed-employee exception: [brief or "none"]`

Return no more than 70 words.
```

---

### 30. Non-Solicit Customers

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether the individual can take customers with them. The protection that
  most directly defends the revenue the buyer is paying for.

```markdown
## Task

Report any obligation restricting the individual from soliciting or dealing with the employer's customers, clients, suppliers, or prospects after their engagement ends.

## Scope

- Include non-solicitation and non-dealing obligations covering customers, clients, suppliers, distributors, and prospective customers.
- Exclude non-solicitation of employees, which is a separate column.
- Exclude non-compete obligations.

## Include where expressly stated

- The duration, and the date it runs from
- **The covered population**: all customers, those the individual dealt with, those the individual dealt with in a stated look-back period, or a named list
- **Whether it prohibits soliciting only, or also dealing with.** A non-dealing obligation catches a customer who approaches the individual unprompted and is materially wider
- Whether prospective customers or pipeline are covered, and how they are defined
- Whether suppliers are covered as well as customers
- Any exception for business unrelated to the employer's activities

## Rules

- Report the covered population and the look-back period as stated. A restriction covering customers the individual dealt with in the last twelve months is the standard formulation; one covering all customers ever is not.
- **Report the solicit-versus-deal distinction explicitly**, for the same reason as in the employee column.
- Report whether prospects are covered, since prospect restrictions are frequently the most contested part.
- Do not assess enforceability.

## Fallback rules

- Return exactly `None` where the documents impose no such restriction.
- Return `Incorporated terms — set out in [document name as referenced]` where it sits in a covenant agreement not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Duration: [period] from [date basis]; population: [as stated]; look-back: [period or "none"]; prohibits: [solicit only | solicit and deal]; prospects covered: [yes | Not addressed]; suppliers covered: [yes | Not addressed]`

Return no more than 75 words.
```

---

### 31. IP Assignment

- Native type: Classify
- Configured options, in UI order: `Present assignment`, `Agreement to assign in future`, `Assignment with statutory carve-out`, `Employer-owned by operation of law only`, `No assignment`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `IP Assignment Language`
- Purpose: whether the business actually owns what this person created.

**This is the most consequential column in the table for a technology target.** An
agreement to assign in the future transfers nothing — it is a defect requiring
remediation before closing, not an assignment. Filtered across every technical
employee and contractor, this column is the IP chain-of-title coverage check.

```markdown
## Task

Classify how the documents deal with intellectual property the individual creates. Choose exactly one configured option.

## Scope

- Consider assignment, vesting, and ownership provisions covering inventions, works, developments, and other intellectual property created by the individual.
- Include provisions in the employment or consulting agreement, and in any separate invention assignment agreement in the unit.
- Exclude confidentiality and trade secret obligations, which do not transfer ownership.
- Exclude licences of the individual's pre-existing IP to the employer, which are noted in the evidence field rather than classified here.

## Classification rules

Apply the first rule that fits.

1. `Agreement to assign in future`: the operative words are that the individual **agrees to assign, will assign, or shall assign**. This is a promise, not a transfer. **It is a defect**, it requires a confirmatory assignment, and it is the single most common IP finding in a private-company diligence.
2. `Employer-owned by operation of law only`: the documents assert that IP vests in or belongs to the employer by law, or as a work made for hire, without any words of present assignment. Whether that assertion holds depends on the jurisdiction and the category of work, so it is not equivalent to an assignment.
3. `Assignment with statutory carve-out`: a present assignment subject to a statutory exclusion for inventions made outside employment or without employer resources. Common and generally sound, but the carve-out defines what was not assigned.
4. `Present assignment`: the operative words assign presently — **assigns, hereby assigns, does hereby assign** — with no material qualification.
5. `No assignment`: the documents address IP and expressly leave ownership with the individual.

Classify on the operative verb tense and mood, not on the clause heading. A clause titled Assignment of Inventions that says the individual agrees to assign is `Agreement to assign in future`.

Where the documents contain both a present assignment and a further-assurances covenant, classify as `Present assignment`. A further-assurances obligation supports an assignment; it does not weaken it.

## Fallback rules

- Use `Not addressed` where the documents say nothing about IP the individual creates. **For a technical role this is a serious gap** and the reviewer will treat it as one.
- Use `Incorporated terms` where assignment is stated to sit in a separate agreement not present in the unit.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 32. IP Assignment Language

- Native type: Verbatim
- Upstream: `@IP Assignment`
- Downstream: none
- Purpose: the exact granting words. The difference between an assignment and a
  promise is a single verb, and a reviewer has to see it.

```markdown
## Established result

- IP assignment: @IP Assignment

## Task

If IP Assignment is `Present assignment`, `Agreement to assign in future`, `Assignment with statutory carve-out`, `Employer-owned by operation of law only`, or `No assignment`, quote the intellectual property provision exactly as written.

If it is `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever IP language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the operative granting words in full.** The verb is the finding, and it must appear in the quotation.
- Quote the definition of the assigned subject matter, any statutory carve-out, any disclosure obligation, any further-assurances covenant, any power of attorney, and any waiver of moral rights, where each appears in the unit.
- **Quote any power of attorney specifically**, since it determines whether the employer can perfect the assignment without the individual's cooperation — which matters most for former employees.
- Quote any schedule of excluded prior inventions, or note in the evidence field that one is referenced and empty or absent.
- Where the combined text exceeds 250 words, quote the granting words and each carve-out and covenant, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not state whether the assignment is effective.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 33. Confidentiality Survival

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how long confidentiality binds after departure, which is the residual
  protection when covenants have expired or are unenforceable.

```markdown
## Task

Report the confidentiality obligations binding the individual and how long they last after the engagement ends.

## Include where expressly stated

- The duration after termination: a stated period, or perpetual
- Whether trade secrets are subject to a longer or unlimited period than other confidential information
- The definition of confidential information in six words or fewer, and whether it extends to information about customers, employees, or third parties
- Any obligation to return or delete materials on termination
- Any permitted disclosure carve-outs: legal compulsion, whistleblowing, or regulatory report
- Any obligation not to retain copies

## Rules

- **Report the whistleblowing or protected-disclosure carve-out where present, and note its absence where the documents contain none.** In several jurisdictions a confidentiality clause without one is at risk, and its absence is a live compliance point rather than a drafting preference.
- Report the return-of-materials obligation, since it is the practical mechanism for protecting information at a departure.
- Report the period as stated. Do not calculate a date.

## Fallback rules

- Return `Not addressed` where the documents impose no confidentiality obligation.
- Return `Incorporated terms — set out in [document name as referenced]` where the obligation sits in a separate agreement or a policy not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Duration: [period or "perpetual"]; trade secrets: [separate treatment or "same"]; scope: [brief]; return of materials: [yes | Not addressed]; protected disclosure carve-out: [yes | Not addressed]`

Return no more than 65 words.
```

---

### 34. Arbitration and Class Waiver

- Native type: Classify
- Configured options, in UI order: `Arbitration with class waiver`, `Arbitration, no class waiver`, `Class waiver only`, `Courts, no arbitration`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: how employment disputes are resolved, which bears on aggregate exposure
  across the workforce.

```markdown
## Task

Classify how disputes between the individual and the employer are to be resolved. Choose exactly one configured option.

## Scope

- Consider provisions requiring arbitration, waiving class or collective proceedings, or waiving jury trial.
- Exclude the governing law provision, which has its own column.
- Exclude any grievance or internal complaint procedure that does not determine the forum.
- Exclude a carve-out permitting injunctive relief in court for covenant breaches; note it in the evidence field.

## Classification rules

- `Arbitration with class waiver`: disputes go to arbitration and the individual waives participation in class, collective, or representative proceedings. **Aggregated across the workforce, this materially reduces exposure**, which is why it is worth a column.
- `Arbitration, no class waiver`: arbitration is required with no class waiver.
- `Class waiver only`: a class or collective waiver with no arbitration requirement.
- `Courts, no arbitration`: the documents specify courts, or expressly exclude arbitration.

Report in the evidence field whether the arbitration provision names rules and a seat, whether costs are borne by the employer, and whether a jury trial waiver is included.

## Fallback rules

- Use `Not addressed` where the documents specify no forum.
- Use `Incorporated terms` where the provision is stated to sit in a policy, handbook, or separate agreement not present in the unit. **This is common** — arbitration provisions frequently sit in handbooks — and it points the reviewer at the Policies table.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 35. Immigration Dependency

- Native type: Classify
- Configured options, in UI order: `Employer-sponsored visa referenced`, `Work authorisation condition referenced`, `Permanent residence sponsorship referenced`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the individual's right to work depends on this employer. **A key
  person on an employer-sponsored visa is an integration risk**, because a change
  of employing entity can require a new petition and the person cannot simply be
  moved.

```markdown
## Task

Classify what the documents state about the individual's immigration status or work authorisation. Choose exactly one configured option.

## Scope

- Consider statements about visa sponsorship, work permits, work authorisation conditions, and permanent residence applications.
- Include a condition making employment contingent on obtaining or maintaining authorisation.
- Exclude general representations that the individual is legally entitled to work, with no sponsorship or condition attached.

## Classification rules

- `Employer-sponsored visa referenced`: the documents state that the individual holds or will hold a visa sponsored by the employer, or name a visa category tied to the employer.
- `Work authorisation condition referenced`: employment is conditional on the individual obtaining or maintaining work authorisation, without an employer-sponsored visa being named.
- `Permanent residence sponsorship referenced`: the employer has agreed to sponsor or support a permanent residence application.

Report in the evidence field any visa category named, any expiry date stated, and any obligation on the employer to bear application costs or to support a transfer.

**Do not assess immigration status, eligibility, or the effect of the transaction on any visa.** Report only what the documents state. The consequences of a change of employer are jurisdiction-specific and belong to specialist counsel.

## Fallback rules

- Use `Not addressed` where the documents say nothing about visas or work authorisation.
- Use `Unable to determine` where statements in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 36. Union or Works Council Coverage

- Native type: Classify
- Configured options, in UI order: `Collective agreement applies`, `Works council or employee representative body referenced`, `Both`, `Expressly not covered`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether collective consultation obligations attach to this individual.
  **Consultation obligations are timetable items**, and in several jurisdictions
  they must be completed before a transaction can proceed.

```markdown
## Task

Classify what the documents state about collective representation covering this individual. Choose exactly one configured option.

## Scope

- Consider references to a collective bargaining agreement, union recognition, works council, employee representative body, or staff committee.
- Include a statement that the individual's terms are set or supplemented by a collective agreement.
- Exclude general references to consultation with employees on operational matters.

## Classification rules

- `Collective agreement applies`: the documents state that a collective bargaining or similar agreement applies to the individual's terms, or that terms are incorporated from one.
- `Works council or employee representative body referenced`: the documents refer to a works council, representative body, or committee with a role in the individual's terms or in changes to them.
- `Both`: both apply.
- `Expressly not covered`: the documents state that no collective agreement applies.

Report in the evidence field the name of any agreement or body, and whether the documents identify a consultation obligation on a transfer or a change of control.

**Where a collective agreement is referenced, it is a document that should be produced.** The Referenced but Not Produced column reports it, and it belongs in the coverage register.

## Fallback rules

- Use `Not addressed` where the documents say nothing about collective representation.
- Use `Unable to determine` where references in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 37. Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the law governing the agreement, which is not the same as the
  jurisdiction of employment and is what covenant enforceability is argued under.

```markdown
## Task

Identify the governing law of the individual's agreement.

## Rules

- Report the jurisdiction chosen to govern, as stated.
- Report the jurisdiction only. Do not report the forum, venue, or arbitral seat.
- Where different documents in the unit choose different law, report the choice in the most recently dated document that addresses it and append ` (differs from [prior jurisdiction] in earlier documents)`.
- **Where the governing law differs from the jurisdiction of employment, append ` [differs from place of work]`.** The mismatch is the point: a covenant governed by one state's law will usually still be tested against the law of the state where the individual actually works, and this flag surfaces the population where that argument arises.
- Where a separate covenant or invention assignment agreement chooses different law from the employment agreement, report both and label each.

## Fallback rules

- Return `Not addressed` where no document in the unit contains a choice of law.
- Return `Unable to determine` where choices in the unit conflict irreconcilably.

## Output format

`[Jurisdiction]`, with any qualifier or flag appended. Return no more than 30 words.
```

---

### 38. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this individual's papers refer to that is not in the
  unit. Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this individual's engagement that the documents in this unit refer to and that is not present.

## Scope

- Include amendments, variations, salary letters, and side letters referenced but absent.
- Include separate restrictive covenant, confidentiality, and invention assignment agreements referenced but absent.
- Include retention, change-in-control, and severance plans or agreements referenced but absent.
- Include equity award agreements and grant notices referenced but absent.
- Include bonus and commission plans referenced as setting the individual's variable pay.
- Include handbooks, policies, and collective agreements the documents state apply to or bind the individual.
- Include any schedule of excluded prior inventions referenced but not attached.
- Exclude statutes, regulations, and published standards.
- Exclude documents relating to other individuals.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Company's Employee Handbook`, report it as printed and add `(no date stated)`.
- **Where an invention assignment or restrictive covenant agreement is referenced but absent, add `; covenant or IP gap`.** These two are the highest-value gaps this column finds, and the flag lets them be filtered across the whole workforce.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; covenant or IP gap]`

Return no more than 12 lines and no more than 110 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Operative version confirmed** | Yes / No, superseded / Chain incomplete |
| **Key person** | Yes / No |
| **Retention risk** | High / Medium / Low |
| **Covenant enforceable** | Likely / Doubtful / Jurisdiction-dependent / Unassessed |
| **Classification correct in substance** | Yes / Misclassification risk / Unassessed |
| **Transaction payment triggered** | Yes (amount) / No / Unclear |
| **280G disqualified individual** | Yes / No / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: individual, employing entity,
compensation, severance, change-of-control payment, IP assignment, covenants.

### Reconciliation work that never belongs in a column

- **Census reconciliation, both directions.** Every person on the census should
  have an agreement, and every agreement should match a person on the census.
  Mismatches either way are findings.
- **Compensation reconciliation.** Agreement figures against census figures.
  Deltas usually mean an unproduced amendment or an undocumented raise.
- **Equity cross-check.** Individuals here against holders in the Capitalization
  table. Equity on the cap table with no grant agreement, and an agreement
  promising equity never granted, are gaps in opposite directions.
- **IP assignment coverage.** Filter `IP Assignment` to
  `Agreement to assign in future`, `Employer-owned by operation of law only`,
  `Not addressed`, and `Incorporated terms`, then match against the IP chain of
  title. Anyone who contributed to critical IP without a present assignment is a
  remediation item before closing.
- **Transaction payment total.** Sum severance, change-of-control payments,
  retention bonuses, and acceleration across rows, in Excel, and feed the purchase
  price mechanics.
- **280G analysis.** Filter to officers, directors, and highly compensated
  individuals, and model with tax advisers. **Never a Harvey column.**
- **Contractor misclassification.** Filter `Classification` to
  `Independent contractor` and `Consultant`, then have a lawyer assess against how
  each role actually operates.
- **Covenant coverage.** Filter to key persons with no non-compete or a
  `Doubtful` enforceability assessment.

---

## Test set

- [ ] Executive with offer letter, employment agreement, one amendment, and a separate CoC agreement
- [ ] Employee with an offer letter only
- [ ] Employee whose agreement is unsigned by the individual
- [ ] Employee with a signed agreement and an unsigned invention assignment
- [ ] Unit containing documents for two different individuals
- [ ] Employee transferred between group entities with continuous service preserved
- [ ] Employee with a continuous service date earlier than the current agreement
- [ ] Contractor later converted to employee
- [ ] Consultant engaged through a personal service company
- [ ] Non-employee director
- [ ] Secondee employed by one entity and working for another
- [ ] At-will US employee
- [ ] Indefinite non-US employee with a three-month notice period
- [ ] At-will recital combined with a stated notice period
- [ ] Fixed-term employee whose term expired before the as-of date
- [ ] Employee with a signed separation agreement
- [ ] Employee with an unsigned separation agreement
- [ ] Executive with single-trigger CoC severance
- [ ] Executive with double-trigger severance and a good reason definition
- [ ] Executive with double-trigger severance and **no** good reason definition
- [ ] Executive with a good reason definition covering relocation and reporting-line change
- [ ] Executive with a CoC definition limited to the employing entity, not the parent
- [ ] Executive with a 280G gross-up
- [ ] Executive with a best-net cutback
- [ ] Executive with CoC payments and no 280G provision
- [ ] Employee with a retention bonus payable on staying twelve months post-closing
- [ ] Employee with a seller-funded transaction bonus
- [ ] Agreement with a present IP assignment
- [ ] Agreement with an agreement to assign in future
- [ ] Agreement asserting work-made-for-hire with no assignment words
- [ ] Agreement with a statutory invention carve-out
- [ ] Technical employee with no IP provision at all
- [ ] Agreement with an invention assignment referenced but not produced
- [ ] Employee with a non-compete payable during the restricted period
- [ ] Employee with a non-solicit covering solicit and employ
- [ ] Employee with a customer non-dealing obligation covering prospects
- [ ] Employee with covenants in a separate agreement not produced
- [ ] Employee with arbitration and class waiver in a handbook, not the agreement
- [ ] Employee on an employer-sponsored visa
- [ ] Employee covered by a collective agreement not produced
- [ ] Agreement governed by Delaware law with the individual working in California

Then test the dependencies: change `Employment Basis` from `Fixed term` to
`At will` and confirm `Fixed Term Expiry` moves to `Not applicable` and
`Notice Periods` re-runs. Change `CoC Payment or Benefit` from `Single trigger` to
`Not addressed` and confirm both dependent columns follow, and that a locked
Verbatim cell does not retain the old quotation.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
