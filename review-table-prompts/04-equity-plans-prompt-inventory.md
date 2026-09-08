# Prompt Inventory — Equity Plans

Platform-ready Harvey Review Table. Companion to the Capitalization table, and the
table that makes its `Incorporated terms` answers resolvable.

Keep this file outside Harvey. Exports omit Table Instructions and Harvey does not
version prompts, so this is the authoritative history.

## Table

- Matter: `[Project name]`
- Platform: Harvey Review Tables (UI)
- Project: `[Matter] - Corporate` (same project as Corporate and Capitalization)
- Review unit: **one plan** — the plan document, every amendment and restatement,
  the board and owner approvals adopting it and each reserve increase, and the
  standard form award agreements issued under it
- Grouping used: **yes**, typically 3–8 documents per unit
- Row count: usually 3 to 6 per matter
- Intended reviewers and downstream use: corporate/M&A team; resolves the
  incorporated terms in the Capitalization table, and feeds the transaction
  payments schedule, the overhang calculation, and the coverage register
- Inventory version: v1.0
- Last full run: —
- Last evaluated: —

### Why this table exists

Five columns in the Capitalization table return `Incorporated terms` because grant
agreements routinely say vesting, acceleration, post-termination exercise, transfer
restrictions, and forfeiture are "as set forth in the Plan." Those answers are
correct and they are useless on their own. This table is where they resolve.

It is a small table read carefully once, not a large table filtered. Three to six
rows, each read end to end by a lawyer, because a single plan governs hundreds of
instruments and one wrong reading propagates across the whole option pool.

### Resolution map

Build this table immediately after Capitalization, and use this mapping to resolve
each incorporated term.

| Capitalization column returning `Incorporated terms` | Resolves to |
| --- | --- |
| Vesting Schedule | `Default Vesting` |
| Acceleration on Change of Control | `Default Acceleration on Change of Control` **and** `Corporate Transaction Treatment` |
| Post-Termination Exercise Period | `Default Post-Termination Exercise` |
| Repurchase or Forfeiture on Termination | `Default Repurchase or Forfeiture` |
| Transfer Restrictions | `Default Transfer Restrictions` |
| Expiration or Maturity | `Maximum Award Term` |
| Class or Series | `Award Types Permitted` |
| Price Terms | `Tax Qualification Provisions` (the plan's fair market value and minimum exercise price rules) |
| **Quantity and Unit** | **Nothing here.** A plan never states an individual award's quantity. If a Capitalization row returns `Incorporated terms` for quantity, the **grant notice is missing** — that is a coverage finding, not a resolution |

**Two cautions on using the map.** A plan default is not necessarily what applies
to a given award: a grant agreement may vary it, and which governs is a legal
question, so `Operative Version Confirmed` and the individual grant's own terms
stay with a human. And the plan resolves defaults only — it can never resolve a
holder-specific fact.

## Assumptions to confirm before running

1. Each unit contains one plan and its own amendments and approvals. A unit
   containing two different plans produces a merged reading of both, which is the
   worst failure available in this table.
2. Buy-side review; the adopting entities in the Table Instructions list are the
   review subjects.
3. Form award agreements are grouped **into** the plan's unit, not treated as
   Capitalization rows. A blank form is not an instrument.
4. Individual grants are rows in the Capitalization table, not here.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Pre-run verification

- [ ] Every Classify column's options configured in the UI, in the order listed in
      each record. **7 Classify columns.**
- [ ] Typed columns tested. Test `Plan Adoption Date` and `Plan Expiration Date`
      (Date) with `Not stated`. Record what the type accepts: ______
- [ ] Verbatim column behaviour confirmed. **Three Verbatim columns here, and one
      of them quotes a full change of control definition**, so test the length
      handling on the longest plan you have.
- [ ] Table Instructions pasted from this file, entity list and as-of date set.
- [ ] Dependency index re-derived from the prompts.
- [ ] Tested with a plan that has been amended twice to increase the reserve, to
      confirm `Reserve Increase History` reports each increase separately rather
      than a total.
- [ ] Tested with a plan whose stated expiration date has passed.
- [ ] Legal choices confirmed by the team: the `Corporate Transaction Treatment`
      option set, and the decision to report `Default Acceleration` and
      `Corporate Transaction Treatment` as two columns rather than one.

### Column count

31 Harvey columns plus 8 human columns. Column count is a smaller concern here
than in the other tables, since the row count is tiny — a wide grid over four rows
is readable. Do not split unless your tenant's cap forces it.

---

## Table Instructions

- Version: v1.0
- Last changed: —

About 2,600 characters. Two rules here are specific to this table: the
default-versus-individual rule, and the reserve arithmetic prohibition.

```markdown
## Matter

[Project name]. Buyer-side equity plan diligence on the target group listed below.

One row is one equity plan: the plan document, every amendment and restatement, the board and owner approvals adopting it and each reserve increase, and the standard form award agreements issued under it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Adopting entities

Use these names exactly as written when an entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Terminology

Columns refer to `units` generically. Read this as shares for a corporation, and as membership interests, units, or percentage interests for a limited liability company or partnership.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the plan or its participants.
- **Report the plan's default terms.** Do not state what applies to any individual award, and do not state whether an award agreement may or does vary a default. A grant agreement may depart from the plan, and which governs is a legal question for the reviewer.
- **Report figures only as the documents state them. Do not calculate anything.** Do not total reserve increases, do not compute units remaining available, do not compute overhang or dilution, and do not net forfeitures. Report each figure as stated with its date, and let the reviewer reconcile.
- Where two documents in the unit address the same term, report the term as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Where a term is stated to be governed by a document that is not in the current review unit, return `Incorporated terms`. Do not treat the plan as silent, and do not supply the other document's terms.
- Use entity and individual names exactly as printed; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Write currency amounts with the currency as printed.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

Lighter than the other tables. Most columns read the plan directly, and `Plan
Type` routes only where the qualifying evidence genuinely differs.

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Plan Name and Version
  Plan Type
  Adopting Entity
  Plan Expiration Date
  Evergreen Provision
  Share Recycling
  Eligible Participants
  Maximum Award Term
  Default Vesting
  Default Post-Termination Exercise
  Default Repurchase or Forfeiture
  Default Transfer Restrictions
  Default Acceleration on Change of Control
  Corporate Transaction Treatment
  Change of Control Definition
  Administrator Discretion
  Repricing Authority
  Amendment and Termination
  Non-US Sub-Plans

Stage 2 — Record status
  Documents in Unit ──→ Plan Adoption Date
                        Approval Evidence
                        Chain Completeness
                        Reserve Increase History
                        Referenced but Not Produced
  Approval Evidence ──→ Approval Detail

Stage 3 — Routed on plan type
  Plan Type ──→ Units Reserved as Stated
                Award Types Permitted
                Tax Qualification Provisions

Stage 4 — Quotation
  Default Acceleration on Change of Control ──→ Acceleration Language
  Corporate Transaction Treatment           ──→ Corporate Transaction Language
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Documents in Unit | Free Response | — | Plan Adoption Date; Approval Evidence; Chain Completeness; Reserve Increase History; Referenced but Not Produced | v1.0 | draft |
| 2 | Plan Name and Version | Free Response | — | — | v1.0 | draft |
| 3 | Plan Type | Classify | — | Units Reserved as Stated; Award Types Permitted; Tax Qualification Provisions | v1.0 | draft |
| 4 | Adopting Entity | Free Response | — | — | v1.0 | draft |
| 5 | Plan Adoption Date | Date | @Documents in Unit | — | v1.0 | draft |
| 6 | Plan Expiration Date | Date | — | — | v1.0 | draft |
| 7 | Approval Evidence | Classify | @Documents in Unit | Approval Detail | v1.0 | draft |
| 8 | Approval Detail | Free Response | @Approval Evidence | — | v1.0 | draft |
| 9 | Chain Completeness | Classify | @Documents in Unit | — | v1.0 | draft |
| 10 | Units Reserved as Stated | Free Response | @Plan Type | — | v1.0 | draft |
| 11 | Reserve Increase History | Free Response | @Documents in Unit | — | v1.0 | draft |
| 12 | Evergreen Provision | Classify | — | — | v1.0 | draft |
| 13 | Share Recycling | Free Response | — | — | v1.0 | draft |
| 14 | Award Types Permitted | Free Response | @Plan Type | — | v1.0 | draft |
| 15 | Eligible Participants | Free Response | — | — | v1.0 | draft |
| 16 | Maximum Award Term | Free Response | — | — | v1.0 | draft |
| 17 | Default Vesting | Free Response | — | — | v1.0 | draft |
| 18 | Default Post-Termination Exercise | Free Response | — | — | v1.0 | draft |
| 19 | Default Repurchase or Forfeiture | Free Response | — | — | v1.0 | draft |
| 20 | Default Transfer Restrictions | Free Response | — | — | v1.0 | draft |
| 21 | Default Acceleration on Change of Control | Classify | — | Acceleration Language | v1.0 | draft |
| 22 | Acceleration Language | Verbatim | @Default Acceleration on Change of Control | — | v1.0 | draft |
| 23 | Corporate Transaction Treatment | Classify | — | Corporate Transaction Language | v1.0 | draft |
| 24 | Corporate Transaction Language | Verbatim | @Corporate Transaction Treatment | — | v1.0 | draft |
| 25 | Change of Control Definition | Verbatim | — | — | v1.0 | draft |
| 26 | Administrator Discretion | Free Response | — | — | v1.0 | draft |
| 27 | Repricing Authority | Classify | — | — | v1.0 | draft |
| 28 | Tax Qualification Provisions | Free Response | @Plan Type | — | v1.0 | draft |
| 29 | Amendment and Termination | Free Response | — | — | v1.0 | draft |
| 30 | Non-US Sub-Plans | Free Response | — | — | v1.0 | draft |
| 31 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Plan Adoption Date`, `Approval Evidence`, `Chain Completeness`, `Reserve Increase History`, `Referenced but Not Produced`
- Purpose: inventory the plan family, so a reviewer can see the amendment sequence
  and whether each approval was produced.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the plan document, every amendment and amended and restated version, board consents and resolutions adopting the plan or approving an amendment, owner consents or minutes approving the plan or a reserve increase, and standard form award agreements.
- Treat exhibits and schedules physically attached to a document as part of that document.
- Do not include documents that are only referenced but not present. Those belong to the Referenced but Not Produced column.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Plan`, `Plan amendment`, `Plan restatement`, `Board approval`, `Owner approval`, `Form award agreement`, `Sub-plan`, or `Other`.
- For a form award agreement, state the award type it is for in three words or fewer, for example `option form`, `RSU form`.
- **Where a document relates to a different plan than the subject of this row, still list it and append ` [relates to [plan name]]`.** A unit containing two plans produces a merged reading of both, and this is how that surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 15 lines and no more than 120 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Plan Name and Version

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the plan's exact name and current version, which is the join key for
  every Capitalization row that names a plan.

```markdown
## Task

State the exact name of the plan and identify the version this review unit represents.

## Rules

- Report the plan name exactly as printed on the operative plan document, including the year in the title where present, for example `2019 Equity Incentive Plan`.
- Where the operative document is an amended and restated version, report its full title as printed, for example `Amended and Restated 2019 Equity Incentive Plan`, and give its date.
- Where the plan has been amended without restatement, report the base plan name and append ` (as amended through [YYYY-MM-DD])`, using the date of the latest amendment in the unit.
- Report the entity name as part of the title only where the document prints it that way.
- Do not normalize the name, expand abbreviations, or correct the year. Grant agreements reference the plan by name, and a normalized name will not match.

## Fallback rules

- Return `Unable to determine` where no document in the unit states the plan's name, or the name is illegible.

## Output format

`[Exact plan name]`, with any qualifier appended as described above. Return no more than 30 words.
```

---

### 3. Plan Type

- Native type: Classify
- Configured options, in UI order: `Omnibus equity incentive plan`, `Stock option plan`, `Restricted stock unit plan`, `Employee stock purchase plan`, `Stock appreciation right or phantom plan`, `Profits interest plan`, `Non-US sub-plan`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Units Reserved as Stated`, `Award Types Permitted`, `Tax Qualification Provisions`
- Purpose: route the reserve, award type, and tax columns, since the qualifying
  evidence differs between an omnibus plan and a cash-settled phantom plan.

```markdown
## Task

Classify the plan that is the subject of this review unit. Choose exactly one configured option.

## Classification rules

Classify on the awards the plan authorizes, not on its title.

- `Omnibus equity incentive plan`: authorizes more than one award type, typically options together with restricted stock, restricted stock units, or other awards. This is the most common form and the default where the plan permits several award types.
- `Stock option plan`: authorizes only options, whether incentive, non-qualified, or both.
- `Restricted stock unit plan`: authorizes only restricted stock units or similar settlement-based awards.
- `Employee stock purchase plan`: participants purchase units through payroll deduction over an offering period, usually at a discount.
- `Stock appreciation right or phantom plan`: awards are measured by unit value and settled in cash or notionally, conferring no unit ownership.
- `Profits interest plan`: authorizes interests in future profits and appreciation of a partnership or limited liability company.
- `Non-US sub-plan`: a schedule, addendum, or sub-plan operating under a parent plan for participants in a particular jurisdiction. Classify here even where it is titled as a plan in its own right.

A plan authorizing options and nothing else is a `Stock option plan` even where it is titled an equity incentive plan.

## Fallback rules

- Use `Other` where the plan authorizes awards none of the options describes.
- Use `Unable to determine` where the award provisions are incorporated from a document not in the unit, or are illegible or internally inconsistent.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Adopting Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity adopted the plan, since awards over a subsidiary's
  units are a different problem from awards over the parent's.

```markdown
## Task

State the entity that adopted the plan and whose units the plan covers.

## Rules

- Report the name exactly as printed, including the entity suffix.
- Where the printed name differs from the entity list in the Table Instructions, report the printed name and append ` (variant of [listed name])`.
- Where the plan states that units of a different entity are subject to awards — for example a parent's units awarded to subsidiary employees — report the adopting entity and append ` (units of [entity name])`.
- Where the plan was assumed by another entity in a prior transaction recorded in the unit, report the current sponsor and append ` (assumed from [prior entity], [YYYY-MM-DD])`.
- Where the plan names participating subsidiaries or affiliates, do not list them here. Report them in Eligible Participants.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the adopting entity.

## Output format

`[Exact legal name]`, with any qualifier appended as described above. Return no more than 30 words.
```

---

### 5. Plan Adoption Date

- Native type: Date — **confirm the type accepts `Not stated` before use**
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: when the plan took effect, which starts the plan term and determines
  which awards were granted under which version.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the original plan document and distinguish it from later amendments and restatements. Confirm the date against the documents in the current unit.

## Task

Identify the date the plan was originally adopted.

## Date-selection hierarchy

1. Use the adoption or effective date the original plan document states for itself.
2. If none is stated, use the date of the board consent or resolution adopting the plan.
3. If neither is available, use the date of owner approval of the plan.

## Excluded dates

- The date of an amendment or an amended and restated version
- The date of a reserve increase or its approval
- The date of a form award agreement
- The date of the first grant made under the plan
- File name and metadata dates, and notarization, transmittal, and scan dates

## Rules

- **Report the original adoption date, not the date of a restatement.** Where the only plan document in the unit is an amended and restated version, use an original adoption date it recites; where it recites none, use the restatement's own effective date and nothing else. The distinction matters because the plan term and the tax qualification window both run from original adoption.
- Where the plan states an effective date conditional on owner approval, report the stated effective date. Whether the condition was satisfied is reported in Approval Evidence.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 6. Plan Expiration Date

- Native type: Date — **confirm the type accepts `Not stated` and `Not addressed` before use**
- Upstream: none
- Downstream: none
- Purpose: the date after which no further awards may be granted. **A grant made
  after the plan expired is a defect**, and an expired plan means the buyer cannot
  use it for retention awards after closing.

```markdown
## Task

Identify the date after which no further awards may be granted under the plan.

## Rules

- Report the expiration, termination, or sunset date the plan states for the granting of awards.
- Where the plan states a term rather than a date — commonly ten years from adoption or from owner approval — report the resulting date only if the plan itself states it. Otherwise return `Not stated` and let the reviewer derive it. Do not calculate a date from a term.
- Do not report the maximum term of an individual award, which is a separate column and is a different concept: awards already granted usually survive the plan's expiration.
- Do not report a termination date arising from the plan being terminated early by the board, unless a document in the unit records that termination, in which case report it and append ` (terminated early, [YYYY-MM-DD])`.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where it falls before that date, append ` [expired on record]`.

## Fallback rules

- Return `Not addressed` where the plan sets no limit on the period during which awards may be granted.
- Return `Not stated` where the plan states a term but no date, and the date cannot be reported without calculating.
- Return `Unable to determine` where dates in the unit conflict, or are illegible.

## Output format

`YYYY-MM-DD`, with any qualifier appended, or one of the exact fallback values above.
```

---

### 7. Approval Evidence

- Native type: Classify
- Configured options, in UI order: `Board and owner approval in unit`, `Board approval only in unit`, `Owner approval only in unit`, `Approval referenced, not produced`, `No approval evidenced`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Approval Detail`
- Purpose: whether the plan was properly authorized. **Owner approval is what
  makes incentive stock option treatment available**, so its absence converts a
  pool of purported ISOs into non-qualified options — a real tax finding.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify any approval documents. Confirm the approval and its signature evidence against those documents.

## Task

Classify the approval evidence for the plan in this review unit. Choose exactly one configured option.

## Scope

- Consider approvals of the plan's adoption. Approvals of reserve increases are reported in Reserve Increase History.
- Consider only approvals relating to the plan that is the subject of this row.
- **Do not treat an unsigned consent as an approval.** A consent with no signature marker evidences nothing; classify as if it were absent and describe it in Approval Detail.

## Classification rules

Apply the first rule that fits.

1. `No approval evidenced`: nothing in the unit refers to or contains a board or owner approval of the plan.
2. `Approval referenced, not produced`: the plan or another document recites that it was approved, giving an approval date or a reference, and no signed approval document is present.
3. `Owner approval only in unit`: a signed owner consent, resolution, or minute approving the plan is present, and no signed board approval is.
4. `Board approval only in unit`: a signed board consent or resolution adopting the plan is present, and no signed owner approval is.
5. `Board and owner approval in unit`: both are present and signed.

## Fallback rules

- Use `Unable to determine` where an approval document is present but illegible, or where documents in the unit conflict about whether the plan was approved.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Approval Detail

- Native type: Free Response
- Upstream: `@Approval Evidence`
- Downstream: none
- Purpose: the particulars of each approval, so a reviewer can test whether the
  approval matches the plan as adopted and whether it was timely.

```markdown
## Established result

- Approval evidence: @Approval Evidence

## Task

If Approval Evidence is `Board and owner approval in unit`, `Board approval only in unit`, or `Owner approval only in unit`, report the particulars of each approval present.

If Approval Evidence is `Approval referenced, not produced`, report what the reference states: the approving body, the date recited, and the document referenced, and begin the answer with `Referenced only —`.

If Approval Evidence is `No approval evidenced`, return exactly `Not applicable`.

If Approval Evidence is `Unable to determine`, return exactly `Unable to determine — upstream approval evidence is unresolved`.

## Rules

- Use the established result for routing, but confirm each particular against the documents in the current unit.
- For each approval, give the approving body, the document title, its date, whether it is signed, and the plan version it approves as named in it.
- Where the approval names a plan version different from the operative plan document in the unit, append ` [approves a different version]`.
- Where an unsigned approval document is present, report it with `unsigned` and do not describe the plan as approved.
- Where owner approval postdates the plan's stated effective date by more than twelve months, append ` [owner approval more than 12 months after adoption]`. That timing bears on incentive stock option qualification.
- Do not state whether the approval was validly given, whether it satisfied the plan or the charter, or whether ratification is needed. Those are human columns.

## Output format

One line per approval:

`[Approving body] — [document title], [YYYY-MM-DD], [signed | unsigned] — approves [plan version as named]` followed by any bracketed flags.

Return no more than 60 words. Do not include quotations, section numbers, or citation markers.
```

---

### 9. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Base plan absent`, `Sequence gap`, `Form award agreement absent`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: flag rows where the plan record is incomplete, so a reviewer knows
  before relying on any default that the row may not show current terms. **This
  table's defaults resolve incorporated terms across the whole option pool**, so
  an incomplete chain here contaminates the Capitalization table too.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether the plan record in this review unit appears complete. Choose exactly one configured option.

## Scope

- Consider only documents constituting or amending the plan that is the subject of this row, and the form award agreements issued under it.
- Exclude individual grant agreements, which are Capitalization rows.
- Exclude referenced third-party documents, statutes, and regulations.

## Classification rules

Apply the first rule that fits.

1. `Base plan absent`: the unit contains amendments, approvals, or form agreements but the plan document itself is not present.
2. `Amendment referenced but absent`: a document in the unit refers to an amendment or restatement of the plan that is not present. A restatement's recital of amendment history is the most common source of this evidence.
3. `Sequence gap`: amendments are numbered and a number in the sequence is missing.
4. `Form award agreement absent`: the plan and every amendment are present, and no form award agreement is, for an award type the plan authorizes. Without the form, the terms individual grants incorporate cannot be fully read.
5. `Complete on its face`: the plan, every referenced amendment, and at least one form award agreement are present.

`Complete on its face` states only that nothing in these documents reveals a gap.

## Fallback rules

- Use `Unable to determine` where a reference to a further document is too vague to tell whether it amends this plan, or where amendment references are illegible.
- Do not use `Unable to determine` for a single unamended plan with a form agreement. That is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Units Reserved as Stated

- Native type: Free Response
- Upstream: `@Plan Type`
- Downstream: none
- Purpose: the current stated reserve, reported as stated so the reviewer can
  reconcile it against outstanding awards in Excel.

```markdown
## Established result

- Plan Type: @Plan Type

## Task

Report the number of units reserved for issuance under the plan, as currently stated.

## Rules by plan type

- `Omnibus equity incentive plan`, `Stock option plan`, `Restricted stock unit plan`, `Employee stock purchase plan`: the aggregate units reserved, and any sub-limit by award type or by class.
- `Stock appreciation right or phantom plan`: the notional units or the cash pool reserved, as stated. Where the plan is cash-settled and states no unit reserve, say so under the fallback rules.
- `Profits interest plan`: the units or percentage interest reserved as stated.
- `Non-US sub-plan`: the sub-plan's own allocation where stated, and where it draws on the parent plan's reserve, say so.

## Rules

- Report the figure stated in the most recently dated document in the unit that states a reserve, with the class of units, and identify that document.
- **Do not calculate.** Do not add the original reserve to later increases, do not subtract awards granted or outstanding, do not compute units remaining available, and do not compute overhang or a percentage of outstanding units. Each increase is reported separately in Reserve Increase History.
- Report any incentive stock option sub-limit separately, since it is usually a fixed number that does not grow with the pool.
- Report a reserve expressed as a percentage of outstanding units as printed, without converting it.

## Fallback rules

- Return `Not stated` where no reserve figure appears.
- Return `Not applicable` where the plan is cash-settled and reserves no units.
- Return `Incorporated terms` where the reserve is stated to be set by a document not present in the unit.
- Return `Unable to determine` where figures in documents of the same date conflict.

## Output format

`[Figure] [class] reserved as stated in [document title], [YYYY-MM-DD][; ISO sub-limit [figure]][; sub-limits: [brief]]`

Return no more than 50 words. Do not include totals or availability figures you derived.
```

---

### 11. Reserve Increase History

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: every increase, separately, with its approval. **A reserve increase
  without owner approval is a validity problem for every award granted out of that
  increase**, and it is a common finding.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify amendments and approvals relating to the reserve. Confirm each increase against those documents.

## Task

List every increase to the plan's reserve that the documents in this unit record, with the approval evidenced for each.

## Rules

- Report each increase separately, in date order, with the amount of the increase as stated, the resulting reserve where stated, the document effecting it, and the approvals present for it.
- **Do not total the increases and do not compute a cumulative reserve.** Report each figure as the document states it.
- For each increase, state whether board approval, owner approval, both, or neither is present and signed in the unit.
- **Where an increase is recorded with no owner approval present, append ` [no owner approval in unit]`.** Where the increase relates to a plan permitting incentive stock options, that flag also bears on tax qualification.
- Where an increase was effected automatically under an evergreen provision rather than by amendment, report it as stated and add `(evergreen)`.
- Where an amendment reduces the reserve, report it as a negative change with the amount as stated.
- Do not state whether any increase was validly approved or effective.

## Fallback rules

- Return exactly `None recorded` where the documents record no increase.

Note: `None recorded` is a positive finding, not a fallback state. For a plan with an evergreen provision, it may mean the automatic increases were never documented, which is itself worth the reviewer's attention.

## Output format

One line per increase, earliest first:

`[YYYY-MM-DD] — [+figure] — per [document title] — approvals: [board | owner | both | none]` followed by any bracketed flags.

Return no more than 10 lines and no more than 110 words. Do not include cumulative totals.
```

---

### 12. Evergreen Provision

- Native type: Classify
- Configured options, in UI order: `Present, percentage of outstanding units`, `Present, fixed number`, `Present, lesser of formula`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the reserve increases automatically each year. **The buyer
  inherits this**, and an evergreen provision quietly enlarges the pool between
  signing and closing and every year afterwards.

```markdown
## Task

Classify whether the plan provides for the reserve to increase automatically, without a further amendment. Choose exactly one configured option.

## Scope

- Include any provision increasing the reserve automatically on a recurring date, however described — evergreen, automatic increase, or annual replenishment.
- **Exclude share recycling**, meaning provisions returning forfeited, cancelled, withheld, or unexercised units to the pool. That is a separate column and a different mechanism: recycling replenishes, it does not enlarge.
- Exclude increases requiring a board or owner amendment, which are reported in Reserve Increase History.

## Classification rules

- `Present, percentage of outstanding units`: the increase is a stated percentage of units outstanding on the increase date.
- `Present, fixed number`: the increase is a stated number of units.
- `Present, lesser of formula`: the increase is the lesser or lower of a percentage, a fixed number, or an amount determined by the board. This is the most common drafting and it caps the exposure, so it is worth distinguishing.

Where the provision permits the board to reduce or eliminate the annual increase, still classify on the stated formula and report the board's discretion in Administrator Discretion.

## Fallback rules

- Use `Not addressed` where the plan provides for no automatic increase.
- Use `Unable to determine` where the provision is illegible or incomplete, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 13. Share Recycling

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether units from forfeited, cancelled, or withheld awards return to
  the pool, which determines whether the reserve figure means what it appears to.

```markdown
## Task

Report the plan's provisions on units that become available again after an award ends or is settled.

## Include where expressly stated

- Units subject to awards that are forfeited, cancelled, expire unexercised, or are repurchased
- Units withheld to satisfy an exercise price
- Units withheld to satisfy tax withholding
- Units not issued on the net settlement or net exercise of an award
- Any provision expressly stating that such units do **not** return to the reserve

## Rules

- State for each category whether the units return to the reserve or do not.
- Where the treatment differs by award type — commonly, option units recycle but withheld tax units do not — report each.
- Where the plan states that recycled units are not available for incentive stock option grants, report that.
- **Do not calculate.** Do not estimate how many units have recycled.
- Do not state whether the stated reserve reflects recycling to date.

## Fallback rules

- Return `Not addressed` where the plan says nothing about units becoming available again.
- Return `Incorporated terms` where the treatment is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Forfeited or expired: [returns | does not return]; exercise price withholding: [treatment]; tax withholding: [treatment]; net settlement: [treatment]; ISO limitation: [brief or "none stated"]`

Return no more than 60 words. Use `Not addressed` for any category the plan does not state.
```

---

### 14. Award Types Permitted

- Native type: Free Response
- Upstream: `@Plan Type`
- Downstream: none
- Purpose: what the plan authorizes, and over which class. **An award of a type the
  plan does not permit is invalid**, so this is what individual grants are tested
  against.

```markdown
## Established result

- Plan Type: @Plan Type

## Task

Report the award types the plan authorizes and the class of units they are granted over.

## Rules

- List each award type the plan expressly authorizes, using the plan's own terms, for example `incentive stock options`, `non-qualified stock options`, `restricted stock`, `restricted stock units`, `stock appreciation rights`, `performance awards`, `profits interests`.
- **Report incentive and non-qualified options separately** where the plan authorizes both, because they carry different eligibility and tax rules and individual grants must be tested against the right one.
- State the class or series of units awards are granted over, exactly as designated.
- Report any award type the plan expressly prohibits.
- Report any limit on a particular award type, such as a cap on full-value awards or a fungible share ratio, as stated.
- Where the plan permits cash settlement of any award type, say which.
- Do not state whether any outstanding award falls within the permitted types.

## Fallback rules

- Return `Not addressed` where the plan authorizes awards without identifying types.
- Return `Incorporated terms` where the permitted types are stated to be set out in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Class: [designation]; types: [list]; limits: [brief or "none stated"]; cash settlement: [types or "none stated"]`

Return no more than 60 words. Do not include quotations, section numbers, or citation markers.
```

---

### 15. Eligible Participants

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who may receive awards. **Incentive stock options may only be granted to
  employees**, so a grant of purported ISOs to a contractor or a director is a
  defect, and this column is what surfaces the population to test.

```markdown
## Task

Report who is eligible to receive awards under the plan.

## Rules

- List the eligible categories as the plan states them, for example `employees`, `directors`, `consultants`, `advisors`, `officers`.
- **State any category restricted to a particular award type**, above all any provision limiting incentive stock options to employees. This is the element the eligibility review turns on.
- Report which entities' service providers are eligible: the adopting entity only, its subsidiaries, its affiliates, or a defined group. Name the defined term as printed.
- Report any requirement that a participating subsidiary be designated by the board, and whether the unit contains such a designation.
- Report any eligibility exclusion the plan states, and any minimum service or hours requirement.
- Report any non-US eligibility carve-out or condition.
- Do not state whether any holder was eligible, and do not identify any individual.

## Fallback rules

- Return `Not addressed` where the plan states no eligibility provision.
- Return `Incorporated terms` where eligibility is stated to be determined under a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Eligible: [categories]; ISO limited to: [category or "Not addressed"]; entities: [as stated]; conditions: [brief or "none stated"]`

Return no more than 60 words. Do not include individual names, section numbers, or citation markers.
```

---

### 16. Maximum Award Term

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the longest term an award may run, which resolves `Expiration or
  Maturity` for every grant that incorporates it.

```markdown
## Task

Report the maximum term the plan permits for an award.

## Rules

- Report the maximum term as stated, for example `10 years from the grant date`.
- **Report separately any shorter maximum for incentive stock options granted to a holder owning more than a stated percentage of the units**, commonly five years for a ten percent owner. That shorter term is a qualification requirement and it is frequently overlooked.
- Report the term as stated. Do not calculate an expiration date for any award.
- Where the maximum differs by award type, report each.
- Do not report the plan's own expiration date, which is a separate column and a different concept.
- Do not report the post-termination exercise period, which is a separate column.

## Fallback rules

- Return `Not addressed` where the plan sets no maximum term.
- Return `Not applicable` where the plan authorizes only awards that have no term, such as fully vested restricted stock.
- Return `Incorporated terms` where the maximum is stated to be set out in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`General: [term]; ISO: [term or "same"]; ten percent owner ISO: [term or "Not addressed"]; by award type: [brief or "uniform"]`

Return no more than 45 words.
```

---

### 17. Default Vesting

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **resolves `Vesting Schedule`** for every Capitalization row returning
  `Incorporated terms`.

```markdown
## Task

Report the vesting terms that apply under the plan where an award agreement or grant notice does not specify a schedule.

## Scope

- Report the plan's default schedule, and the schedule in any form award agreement in the unit.
- Where the plan sets no default and leaves vesting entirely to each grant notice, say so under the fallback rules. That is a real and common answer, and it tells the reviewer the schedule must come from the individual grant.
- Report the plan's default. **Do not state what applies to any individual award.**

## Include where expressly stated

- The total vesting period, the cliff, and the instalment frequency
- Any minimum vesting requirement the plan imposes on all awards
- Whether vesting is measured from the grant date or another date
- The treatment of vesting during an approved leave of absence, and on a change in status from employee to consultant
- Any performance-vesting framework the plan provides

## Rules

- Report the plan default and the form agreement schedule separately, and say where they differ. The form agreement is what most grants actually adopt.
- **Do not calculate.** Do not convert a schedule into unit counts or apply it to any date.
- Where an amendment changes the default, report the terms in the most recently dated document that addresses them.

## Fallback rules

- Return `Not addressed — schedule set by each grant notice` where the plan provides no default schedule. This is the expected answer for many omnibus plans.
- Return `Incorporated terms` where the default is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Plan default: [schedule or "Not addressed"]; form agreement: [schedule or "no form in unit"]; minimum vesting: [as stated or "none"]; leave treatment: [brief or "Not addressed"]`

Return no more than 75 words. Do not include calculated figures, section numbers, or citation markers.
```

---

### 18. Default Post-Termination Exercise

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **resolves `Post-Termination Exercise Period`**. Determines whether
  departing holders' options quietly expired or are still live and part of the
  overhang the buyer inherits.

```markdown
## Task

Report the period within which an award may be exercised or settled after a holder's service ends, as the plan and any form award agreement provide.

## Rules

- Report the general period, and then any different period stated for termination without cause, resignation, termination for cause, death, disability, and retirement.
- Report whether the plan provides that an award terminates immediately on termination for cause.
- **Report any provision that the period cannot extend beyond the award's maximum term**, since that is what determines the true outside date.
- Report any provision tolling or extending the period where exercise would violate securities law or a blackout, which can materially lengthen the window.
- Report the plan default and the form agreement period separately, and say where they differ.
- Report periods as stated. Do not calculate any date.
- Report the plan's default. **Do not state what applies to any individual award.**
- Where the plan or form provides a period longer than three months for an incentive stock option, report it as stated. Whether the award retains ISO status is a legal question for the reviewer.

## Fallback rules

- Return `Not addressed — period set by each award agreement` where the plan provides no default.
- Return `Not applicable` where the plan authorizes no award requiring exercise or settlement after service ends.
- Return `Incorporated terms` where the period is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`General: [period]; cause: [period or "immediate termination"]; death or disability: [period]; capped by award term: [yes | Not addressed]; form agreement: [period or "same"]`

Return no more than 70 words. Do not include calculated dates, section numbers, or citation markers.
```

---

### 19. Default Repurchase or Forfeiture

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **resolves `Repurchase or Forfeiture on Termination`**. Determines
  whether a departing holder's units come back to the company or go to the buyer's
  payment list.

```markdown
## Task

Report the plan's provisions for forfeiting awards or repurchasing units when a holder's service ends or another stated event occurs.

## Rules

- State what is forfeited on termination of service: unvested awards, all awards, or nothing.
- State any right to repurchase units already acquired on exercise or settlement, who holds it, the price basis, and the period within which it must be exercised.
- **Distinguish repurchase at original cost from repurchase at fair market value**, since the difference decides whether a departing holder receives value.
- Report any different treatment for termination for cause, and the plan's definition of cause in ten words or fewer.
- Report any clawback or recoupment provision, including any triggered by restatement, misconduct, or breach of a restrictive covenant.
- Report the plan default and the form agreement terms separately, and say where they differ.
- Report the plan's default. **Do not state what applies to any individual award.**
- Do not state whether any right survives or is triggered by this transaction.

## Fallback rules

- Return `Not addressed` where the plan provides for no forfeiture or repurchase.
- Return `Incorporated terms` where the terms are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Forfeiture on termination: [what]; repurchase right: [holder, price basis, window, or "Not addressed"]; cause variation: [brief]; clawback: [brief or "Not addressed"]`

Return no more than 75 words. Do not include quotations, section numbers, or citation markers.
```

---

### 20. Default Transfer Restrictions

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **resolves `Transfer Restrictions`**. Sets the mechanics for delivering
  awards and underlying units at closing.

```markdown
## Task

Report the plan's restrictions on transferring awards and the units acquired under them.

## Include where expressly stated

- Whether awards are transferable, and any exception for transfer by will or intestacy, to a family member, or to a trust
- Any requirement for administrator consent to a transfer
- Rights of first refusal or first offer over units acquired under the plan, and who holds them
- Any market stand-off or lock-up obligation
- Any requirement that a holder become a party to a stockholders, voting, or co-sale agreement as a condition of the award or of exercise
- Any drag-along or voting obligation the plan imposes on holders
- Any legend or transfer restriction the plan requires on issued units

## Rules

- Report awards and underlying units separately. They are commonly treated differently: awards non-transferable, units subject to a refusal right.
- **Report any accession requirement prominently**, because it means the holder is bound by an agreement that may not be in this unit at all — name the agreement as the plan names it.
- Report the plan default and the form agreement terms separately, and say where they differ.
- Report the plan's default. **Do not state what applies to any individual award.**
- Do not state whether any restriction applies to this transaction or whether a waiver has been obtained.

## Fallback rules

- Return `Not addressed` where the plan imposes no transfer restriction.
- Return `Incorporated terms` where the restrictions are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Awards: [restriction]; units: [restriction]; accession required to: [agreement name or "none"]; drag or voting obligation: [brief or "Not addressed"]`

Return no more than 70 words. Do not include quotations, section numbers, or citation markers.
```

---

### 21. Default Acceleration on Change of Control

- Native type: Classify
- Configured options, in UI order: `Single trigger`, `Double trigger`, `Partial acceleration`, `Discretionary acceleration`, `Acceleration only if not assumed`, `No acceleration`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `Acceleration Language`
- Purpose: **resolves `Acceleration on Change of Control`** for every grant that
  incorporates it. **This is the most consequential cell in the table**, because it
  sets the default across the entire option pool and therefore the size of the
  transaction payments schedule.

```markdown
## Task

Classify how the plan provides that vesting is affected by a change of control. Choose exactly one configured option.

## Scope

- Report the plan's default and the treatment in any form award agreement in the unit. Where they differ, classify on the plan and report the difference in the Language column.
- Report the plan's default. **Do not state what applies to any individual award.**

## Classification rules

Apply the first rule that fits.

1. `Acceleration only if not assumed`: awards accelerate only where the acquirer does not assume, continue, or substitute them. This is very common and it is a distinct answer, because the outcome depends on the buyer's own election rather than on the deal happening.
2. `Discretionary acceleration`: acceleration depends on a decision of the board or the plan administrator, with no automatic entitlement.
3. `Single trigger`: vesting accelerates on the change of control itself, with no further condition.
4. `Double trigger`: vesting accelerates only where the change of control is followed by a qualifying termination of service.
5. `Partial acceleration`: a stated proportion, number, or period of vesting accelerates rather than the whole award. Use this whether the trigger is single or double, and state which in the Language column.
6. `No acceleration`: the plan addresses a change of control and provides expressly that vesting does not accelerate.

Where the plan provides both a default of `Acceleration only if not assumed` **and** administrator discretion to accelerate in any event, classify as `Acceleration only if not assumed` and report the discretion in Administrator Discretion.

Classify on the operative mechanics, not on whether the plan uses the words single or double trigger.

## Fallback rules

- Use `Not addressed` where the plan says nothing about vesting on a change of control.
- Use `Incorporated terms` where the treatment is stated to be governed by a document not present in the unit.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 22. Acceleration Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Default Acceleration on Change of Control`
- Downstream: none
- Purpose: the exact text. This language governs the whole pool, so a partner reads
  it word by word before any acceleration number enters the price model.

```markdown
## Established result

- Default acceleration on change of control: @Default Acceleration on Change of Control

## Task

If Default Acceleration on Change of Control is `Single trigger`, `Double trigger`, `Partial acceleration`, `Discretionary acceleration`, `Acceleration only if not assumed`, or `No acceleration`, quote the acceleration provision exactly as written.

If it is `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever acceleration language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the trigger, the proportion accelerating, and any qualifying-termination condition, together with the definitions of `Cause` and `Good Reason` the provision relies on where those appear in the unit. **The good reason definition is what makes a double trigger operative.**
- Do not quote the change of control definition here. It has its own column.
- Where a form award agreement in the unit states different acceleration terms from the plan, quote both and label each with its source.
- Where the combined text exceeds 250 words, quote the operative provision in full and the parts of each definition stating the qualifying conditions, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction would accelerate any award.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 23. Corporate Transaction Treatment

- Native type: Classify
- Configured options, in UI order: `Administrator may choose among alternatives`, `Assumption or substitution required`, `Cash-out permitted`, `Termination if not exercised`, `Awards continue unchanged`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `Corporate Transaction Language`
- Purpose: **what the acquirer may do with outstanding awards.** This is the column
  that determines the buyer's options at closing: whether awards can be cashed
  out, must be assumed, or can be terminated. It is a separate question from
  acceleration and the two are routinely conflated.

```markdown
## Task

Classify what the plan permits or requires to happen to outstanding awards on a merger, sale, or other corporate transaction. Choose exactly one configured option.

## Scope

- This column is about the **treatment** of awards — assumption, substitution, cash-out, or termination. **Acceleration of vesting is a separate column.** A plan commonly provides both, and they answer different questions: acceleration decides what vests, treatment decides what the buyer can do with it.
- Include provisions on adjustment of awards for a recapitalization, stock split, or similar event only where they bear on a change of control.
- Report the plan's default. **Do not state what applies to any individual award.**

## Classification rules

Apply the first rule that fits.

1. `Administrator may choose among alternatives`: the plan gives the administrator a menu — assume, substitute, cash out, terminate, or accelerate — to be selected at the time. This is the most common and the most flexible for a buyer.
2. `Assumption or substitution required`: the plan requires the acquirer to assume or substitute awards, with no cash-out or termination alternative.
3. `Cash-out permitted`: the plan permits awards to be cancelled for a cash payment, without a general menu of alternatives.
4. `Termination if not exercised`: the plan permits awards to be terminated on the transaction, subject to notice and an opportunity to exercise.
5. `Awards continue unchanged`: the plan provides that awards continue on their existing terms with no alternative treatment.

Where the plan permits cash-out, report whether the payment is measured by the spread over the exercise price or by the full transaction value; put that detail in the Language column.

## Fallback rules

- Use `Not addressed` where the plan says nothing about the treatment of awards on a corporate transaction. That is a finding, because the buyer then has no plan-based mechanism to deal with the pool.
- Use `Incorporated terms` where the treatment is stated to be governed by a document not present in the unit.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. Corporate Transaction Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Corporate Transaction Treatment`
- Downstream: none
- Purpose: the exact text, which is what the buyer's option treatment mechanics are
  drafted against.

```markdown
## Established result

- Corporate transaction treatment: @Corporate Transaction Treatment

## Task

If Corporate Transaction Treatment is `Administrator may choose among alternatives`, `Assumption or substitution required`, `Cash-out permitted`, `Termination if not exercised`, or `Awards continue unchanged`, quote the corporate transaction provision exactly as written.

If it is `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever corporate transaction language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote each alternative treatment the provision permits, any notice period and exercise window required before termination, and the basis on which a cash-out payment is measured.
- Quote any provision requiring that substituted awards preserve the intrinsic value or the vesting schedule of the original.
- Do not quote the acceleration provision or the change of control definition; both have their own columns.
- Where the provision exceeds 250 words, quote the lead-in and each permitted alternative, replacing subordinate procedural text with `[...]` between sentences.
- Do not add analysis, and do not indicate which treatment this transaction would use.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 25. Change of Control Definition

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: none
- Downstream: none
- Purpose: the definition both the acceleration and the treatment provisions turn
  on. **Whether this transaction is a change of control at all is decided here**,
  and the definition often differs from the one in the charter or the employment
  agreements.

```markdown
## Task

Quote the plan's definition of the term the acceleration and corporate transaction provisions use to describe a change of ownership or control.

## Scope

- Quote the defined term whatever it is called: `Change of Control`, `Change in Control`, `Corporate Transaction`, `Sale Event`, `Liquidity Event`, or similar.
- Where the plan defines more than one such term and uses different ones in the acceleration and treatment provisions, quote each and label which provision uses it. That mismatch is itself a finding.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the definition, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the full definition including every limb: share acquisition and its percentage threshold, merger or consolidation, sale of all or substantially all assets, board composition change, and liquidation or dissolution.
- Quote any express exclusion, such as a financing round, an internal reorganisation, or a transaction in which existing holders retain control. **Exclusions decide whether a deal falls inside the definition** and they are the most consequential part.
- Where the definition depends on a further defined term such as `Person`, `Affiliate`, or `Incumbent Board`, quote that term's definition too where it appears in the unit.
- Where the definition exceeds 300 words, quote each limb's operative language and every exclusion, replacing intervening procedural text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction falls within the definition.

## Fallback rules

- Return exactly `Not addressed` where the plan uses no such defined term.
- Return `Incorporated terms` where the definition is stated to sit in a document not present in the unit.

## Output format

The quoted text, followed by the source tag. Where more than one term is defined, label each with the provision that uses it. Return no more than 350 words.
```

---

### 26. Administrator Discretion

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the board or administrator can do **unilaterally**. This is often
  the buyer's most useful lever: broad discretion means the pool can be dealt with
  at closing without holder consent, and narrow discretion means it cannot.

```markdown
## Task

Report the powers the plan gives the administrator to act on awards without the consent of holders.

## Include where expressly stated

- Power to accelerate vesting, in whole or in part, and whether it is available at any time or only on a stated event
- Power to amend an outstanding award, and whether holder consent is required where the amendment is adverse
- Power to cancel, cash out, or substitute awards
- Power to extend or shorten an exercise period
- Power to permit or prohibit transfer of an award
- Power to reduce or waive an annual evergreen increase
- Power to delegate authority to a committee or to an officer, and any limit on that delegation
- Any statement that the administrator's determinations are final and binding
- Who the administrator is: the board, a named committee, or a delegate

## Rules

- For each power, state whether holder consent is required and whether the power is subject to any condition.
- **Where the plan states that no amendment may adversely affect an outstanding award without the holder's consent, report it prominently.** That single provision determines whether the pool can be restructured at closing unilaterally.
- Report who the administrator is and whether the unit evidences the committee's appointment.
- Report the plan's terms. Do not state whether any power would be validly exercised or is available on this transaction.

## Fallback rules

- Return `Not addressed` where the plan confers no such powers.
- Return `Incorporated terms` where the powers are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Administrator: [who]; acceleration: [power and conditions]; amendment of awards: [power; holder consent required or not]; cash-out or cancellation: [power]; delegation: [brief or "Not addressed"]`

Return no more than 90 words. Do not include quotations, section numbers, or citation markers.
```

---

### 27. Repricing Authority

- Native type: Classify
- Configured options, in UI order: `Permitted without owner approval`, `Requires owner approval`, `Expressly prohibited`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether underwater options can be repriced or exchanged. Relevant
  wherever the transaction price sits below outstanding strike prices, and it is a
  standard governance point.

```markdown
## Task

Classify whether the plan permits the exercise price of an outstanding award to be reduced, or the award to be cancelled and replaced with a lower-priced or different award. Choose exactly one configured option.

## Scope

- Include repricing, exchange programmes, cancel-and-regrant, and cash buyouts of underwater awards.
- **Exclude adjustments for a stock split, reverse split, stock dividend, recapitalization, or similar structural event**, which are mechanical and are not repricing.
- Exclude substitution of awards in a corporate transaction, which is reported in Corporate Transaction Treatment.

## Classification rules

- `Permitted without owner approval`: the plan expressly permits repricing, or gives the administrator amendment power broad enough to cover it without an owner vote.
- `Requires owner approval`: the plan permits repricing only with owner approval.
- `Expressly prohibited`: the plan states that awards may not be repriced or exchanged.

Where the plan is silent on repricing but gives the administrator a general power to amend outstanding awards subject to holder consent only, classify as `Not addressed` rather than as permitted. The general amendment power is reported in Administrator Discretion, and whether it reaches repricing is a legal question.

## Fallback rules

- Use `Not addressed` where the plan neither permits nor prohibits repricing.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 28. Tax Qualification Provisions

- Native type: Free Response
- Upstream: `@Plan Type`
- Downstream: none
- Purpose: the plan-level tax provisions that determine whether awards carry the
  treatment the company and its holders assume they do. **Resolves `Price Terms`**
  where a grant incorporates the plan's fair market value rules.

```markdown
## Established result

- Plan Type: @Plan Type

## Task

Report the plan's provisions addressing the tax qualification and compliance of awards.

## Include where expressly stated

- Any provision that options are intended to qualify as incentive stock options, and the conditions the plan imposes for that
- **The minimum exercise price rule**, commonly not less than fair market value on the grant date, and any higher percentage for a ten percent owner
- **How fair market value is determined** — by independent appraisal, by board determination, or by a stated method. This is what resolves the price rules a grant incorporates
- The annual limit on the value of incentive stock options that may first become exercisable, and how the plan treats awards exceeding it
- Any provision addressing Section 409A compliance for awards other than options
- Any withholding provision, and whether withholding may be satisfied by withholding units
- For a `Profits interest plan`, any safe-harbour, hurdle, or capital-account provision addressing the interest's tax character
- For an `Employee stock purchase plan`, any provision that the plan is intended to qualify under the applicable statute, and the offering and purchase limits
- Any provision disclaiming responsibility for a holder's tax treatment

## Rules

- Report each element as stated, using the plan's own language for the standard applied.
- Do not state whether any award in fact qualifies, whether the fair market value determination was adequate, or whether an exposure exists. Those are legal conclusions.
- Do not calculate any limit or any holder's position.

## Fallback rules

- Return `Not addressed` for any element the plan does not state; do not omit it silently.
- Return `Not applicable` where the plan authorizes only awards to which none of these provisions could apply.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`ISO intended: [yes | Not addressed]; minimum exercise price: [rule]; FMV determined by: [method]; ISO annual limit: [as stated or "Not addressed"]; 409A: [brief or "Not addressed"]; withholding: [brief]`

Return no more than 90 words. Do not include quotations, section numbers, or citation markers.
```

---

### 29. Amendment and Termination

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who can change or end the plan, and whose consent is needed. Determines
  whether the plan can be amended or terminated at closing and by whom.

```markdown
## Task

Report how the plan may be amended and how it may be terminated.

## Rules

- State who may amend the plan, and the vote or action required.
- **State which amendments require owner approval.** Reserve increases, an extension of the plan term, a change to eligibility, and any change requiring approval under an applicable listing or tax rule are the usual categories, and they are the ones that matter.
- State whether an amendment may adversely affect an outstanding award without the holder's consent.
- State who may terminate the plan and on what notice.
- **State the effect of termination on outstanding awards** — whether they continue on their terms or are cancelled. This decides whether terminating the plan at closing disposes of the pool or leaves it in place.
- State any provision that the plan terminates automatically on a stated event.
- Report the plan's terms. Do not state whether an amendment or termination would be validly effected.

## Fallback rules

- Return `Not addressed` for either element where the plan states no mechanics.
- Return `Incorporated terms` where the mechanics are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Amendment: [who — action]; owner approval required for: [categories]; adverse amendment: [holder consent required or not]; termination: [who — notice]; effect on outstanding awards: [as stated]`

Return no more than 80 words. Do not include quotations, section numbers, or citation markers.
```

---

### 30. Non-US Sub-Plans

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any jurisdiction-specific schedule or sub-plan, which routes to local
  counsel rather than being analysed by US-law analogue.

```markdown
## Task

Report any sub-plan, schedule, addendum, or country-specific appendix operating under this plan for participants outside the United States.

## Rules

- List each jurisdiction covered, and name the sub-plan or appendix as the documents name it.
- State whether the sub-plan document is present in the review unit.
- Report any statement that the sub-plan is intended to qualify for a particular tax or regulatory treatment in that jurisdiction, using the document's own words.
- Report any provision reserving to the administrator the power to adopt further sub-plans without amending the plan.
- Report any provision addressing exchange control, data protection, securities filings, or employment-law consequences in a named jurisdiction.
- **Do not analyse the sub-plan's effect under non-US law, and do not map it to a US-law analogue.** Report what it says and which jurisdiction it addresses, so the row can be routed to local counsel.

## Fallback rules

- Return exactly `None identified` where the plan provides for no non-US sub-plan or appendix.
- Return `Incorporated terms` where sub-plans are referred to but their terms are stated to sit in documents not present in the unit, and name each as referenced.

## Output format

One line per jurisdiction:

`[Jurisdiction] — [sub-plan name as referenced] — [in unit | not produced] — [stated intended treatment or "none stated"]`

Return no more than 10 lines and no more than 90 words.
```

---

### 31. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document the plan family refers to that is not in the unit.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document the documents in this unit refer to and that is not present in the unit.

## Scope

- Include plan amendments and restatements referenced but absent.
- Include board and owner approvals of the plan and of any reserve increase, referenced but not produced.
- Include form award agreements for award types the plan authorizes, where no form is present.
- Include non-US sub-plans and country appendices referenced but absent.
- Include stockholders, voting, or co-sale agreements holders are required to accede to.
- Include committee charters or delegation resolutions referenced as appointing the administrator.
- Include any Form S-8, Form D, or Rule 701 disclosure referenced but absent.
- Exclude statutes, regulations, and published standards.
- Exclude individual grant agreements, which are Capitalization rows.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Committee Charter`, report it as printed and add `(no date stated)`.
- **Where an approval is referenced as authorizing the plan or a reserve increase, add `; authorizes [plan adoption | reserve increase]`**, because a reserve increase with no producible owner approval is a validity problem for every award granted from it.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; authorizes [what]]`

Return no more than 12 lines and no more than 110 words.
```

---

## Human-review fields

Separate table columns, never populated by Harvey.

| Column | Values |
| --- | --- |
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Operative version confirmed** | Yes / No, superseded / Chain incomplete |
| **Plan validly adopted** | Yes / Owner approval defect / Unresolved |
| **Reserve validly increased** | Yes / Approval defect / Not applicable / Unresolved |
| **ISO qualification** | Intact / At risk / Not applicable / Unassessed |
| **Transaction treatment available** | Cash out / Assume / Substitute / Terminate / Constrained / Unresolved |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Given the row count, **every cell in this table should be reviewed**, not sampled.
Three to six rows govern the entire equity pool.

### Reconciliation work that never belongs in a column

- Units reserved against awards outstanding in the Capitalization table, to
  compute units available and the overhang. **Awards granted in excess of the
  reserve is a validity problem** and it happens.
- Grants dated after the plan's expiration date, from the Capitalization grant
  dates against `Plan Expiration Date`.
- Grants of incentive stock options to holders whose `Holder Type` in the
  Capitalization table is not `Current employee`, tested against
  `Eligible Participants`.
- Awards whose term exceeds `Maximum Award Term`.
- Total acceleration cost, combining this table's default with the Capitalization
  rows that returned `Incorporated terms`, and feeding the 280G analysis.
- Whether each reserve increase in `Reserve Increase History` has a corresponding
  owner approval, and whether awards granted after it exceed the pre-increase
  reserve.

---

## Test set

Small row count, so build the test set from real plans rather than synthetic ones
where possible.

- [ ] Omnibus plan with options and RSUs, complete with board and owner approval
- [ ] Option-only plan titled as an equity incentive plan
- [ ] Amended and restated plan reciting an original adoption date years earlier
- [ ] Plan amended twice to increase the reserve, one increase with no owner approval
- [ ] Plan with an evergreen provision expressed as the lesser of a percentage and a fixed number
- [ ] Plan with share recycling for forfeitures but not for tax withholding
- [ ] Plan whose stated expiration date has passed
- [ ] Plan with owner approval more than twelve months after adoption
- [ ] Plan with an unsigned adopting board consent
- [ ] Plan where adoption is referenced but no approval document is produced
- [ ] Plan providing acceleration only if awards are not assumed
- [ ] Plan providing single-trigger acceleration
- [ ] Plan with double-trigger acceleration and a good reason definition
- [ ] Plan with an administrator menu of corporate transaction alternatives
- [ ] Plan requiring assumption or substitution with no cash-out alternative
- [ ] Plan silent on corporate transaction treatment
- [ ] Plan defining both `Change in Control` and `Corporate Transaction`, used in different provisions
- [ ] Plan with a change of control definition excluding a financing round
- [ ] Plan expressly prohibiting repricing
- [ ] Plan with no form award agreement in the unit
- [ ] Plan with a UK or French sub-plan referenced but not produced
- [ ] Profits interest plan with a hurdle provision
- [ ] Phantom or SAR plan, cash-settled, reserving no units
- [ ] Unit mistakenly containing two different plans

Then test the dependencies: change `Default Acceleration on Change of Control`
from `Single trigger` to `Not addressed` and confirm `Acceleration Language` moves
to `Not addressed`; do the same for `Corporate Transaction Treatment` and its
Language column. Confirm a locked Verbatim cell does not silently retain the old
quotation.

Finally, test the resolution map end to end: take one Capitalization row that
returned `Incorporated terms` for vesting and acceleration, and confirm that this
table's `Default Vesting` and `Default Acceleration on Change of Control` actually
answer it. If they do not, the gap is in this table's scope, not in the
Capitalization prompt.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
| --- | --- | --- | --- | --- | --- | --- |
| | | v1.0 | Initial draft | — | — | — |
