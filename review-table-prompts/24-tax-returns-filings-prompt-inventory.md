# Prompt Inventory — Tax: Returns and Filings

Table 24 of the POC.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Tax`
- Review unit: **one return or filing** — the return as filed, its schedules and
  attachments, any amended return for the same period, any extension request, and
  any payment or refund record produced for it
- Grouping used: **yes**, typically 1–5 documents per unit
- Intended reviewers and downstream use: tax and corporate/M&A teams; feeds the
  tax indemnity and escrow analysis, the attribute preservation analysis, the
  disclosure schedule, and the coverage register
- Inventory version: v1.0

### What this table is and is not

**It is a legal extraction layer, not tax diligence.** Spec §3 originally put tax
out of scope on the ground that it does not run through Harvey and the schemas
would not fit. That was right about quantification and wrong about the documents:
returns and filings contain a set of facts a legal reviewer needs and can extract
reliably — periods filed, elections made, attributes claimed, limitation periods,
and jurisdictions registered in.

**Everything numerical stays with tax advisers.** No column computes a liability,
recalculates a position, tests a limitation, models an attribute, or assesses
whether a position is sustainable. The table produces the inventory the tax
advisers work from and the facts the SPA needs.

### The four questions a legal reviewer needs answered

1. **What has been filed, and what has not?** A period not filed is an open
   liability with no limitation period running against it.
2. **When does exposure close?** `Statute of Limitations` is what sets the tax
   indemnity tail in the SPA, and it is the single most useful column here for a
   corporate lawyer.
3. **What attributes are at risk?** Loss and credit carryforwards are commonly
   limited or lost on a change of ownership. **The buyer may be paying for
   attributes the transaction destroys.**
4. **Where is the target exposed but not registered?** The gap between where a
   business operates and where it files is the classic mid-market tax finding, and
   it has no limitation period running because no return was ever filed.

## Assumptions to confirm before running

1. One row is one return, for one entity, one tax type, one jurisdiction, one
   period. A consolidated federal return is one row for the filing entity; the
   members are reported in `Consolidated or Combined Group`.
2. **Tax agreements, audit correspondence, rulings, and assessments are the
   companion table.** A return is a Record; an audit is Correspondence; a tax
   sharing agreement is an Instrument.
3. Financial statements, tax provisions, and deferred tax computations are the
   finance workstream's, not rows here. Where a provision or reserve is disclosed
   in a return or its attachments, `Uncertain Positions and Reserves` captures it.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

20 Harvey columns plus 9 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side tax diligence on the target group listed below. This table reviews tax returns and filings.

One row is one return or filing: the return as filed, its schedules and attachments, any amended return for the same period, any extension request, and any payment or refund record produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the taxpayer or its affairs.
- **Report figures exactly as stated on the return, with the line, schedule, or form reference where the document provides one. Do not calculate anything.** Do not recompute a liability, total across schedules, net a loss against income, apply a rate, accrue interest or penalties, convert currency, or reconcile one figure to another. **A recomputed figure is indistinguishable from a filed one in an export, and a tax position is defined by what was actually filed.**
- **A return states the taxpayer's own position as filed. It is not an authority and it is not a determination.** Report positions as positions.
- **Do not assess whether any position is correct or sustainable, whether any attribute survives, whether any limitation period has expired, or whether any exposure exists.** All four require the law and the facts together and all four are for tax advisers.
- Do not report the names or identifying numbers of individual taxpayers, employees, or shareholders. Report entities and roles.
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
  Filing Type
  Taxpayer Entity
  Taxing Jurisdiction
  Tax Period

Stage 2 — Filing record
  Documents in Unit ──→ Filing Status
                        Amendments and Adjustments
                        Referenced but Not Produced
  Taxpayer Entity ──→ Taxpayer Match
  Filing Date

Stage 3 — Substance, routed on filing type
  Filing Type ──→ Return Position Summary
                  Loss and Credit Carryforwards
                  Transfer Pricing
                  Registration and Nexus Footprint

Stage 4 — Positions and structure
  Elections Made
  Consolidated or Combined Group
  Uncertain Positions and Reserves
  Related-Party Transactions Disclosed

Stage 5 — Exposure window and payment
  Filing Date ──→ Statute of Limitations
  Payment Status
  Preparer and Signatory
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Filing Status; Amendments and Adjustments; Referenced but Not Produced | v1.0 | draft |
| 2 | Filing Type | Classify | — | Return Position Summary; Loss and Credit Carryforwards; Transfer Pricing; Registration and Nexus Footprint | v1.0 | draft |
| 3 | Taxpayer Entity | Free Response | — | Taxpayer Match | v1.0 | draft |
| 4 | Taxpayer Match | Classify | @Taxpayer Entity | — | v1.0 | draft |
| 5 | Taxing Jurisdiction | Free Response | — | — | v1.0 | draft |
| 6 | Tax Period | Free Response | — | — | v1.0 | draft |
| 7 | Filing Date | Date | — | Statute of Limitations | v1.0 | draft |
| 8 | Filing Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 9 | Return Position Summary | Free Response | @Filing Type | — | v1.0 | draft |
| 10 | Loss and Credit Carryforwards | Free Response | @Filing Type | — | v1.0 | draft |
| 11 | Elections Made | Free Response | — | — | v1.0 | draft |
| 12 | Consolidated or Combined Group | Free Response | — | — | v1.0 | draft |
| 13 | Uncertain Positions and Reserves | Free Response | — | — | v1.0 | draft |
| 14 | Related-Party Transactions Disclosed | Free Response | — | — | v1.0 | draft |
| 15 | Transfer Pricing | Free Response | @Filing Type | — | v1.0 | draft |
| 16 | Statute of Limitations | Free Response | @Filing Date | — | v1.0 | draft |
| 17 | Registration and Nexus Footprint | Free Response | @Filing Type | — | v1.0 | draft |
| 18 | Amendments and Adjustments | Free Response | @Documents in Unit | — | v1.0 | draft |
| 19 | Payment Status | Free Response | — | — | v1.0 | draft |
| 20 | Preparer and Signatory | Free Response | — | — | v1.0 | draft |
| 21 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

21 columns. `Related-Party Transactions Disclosed` was separated from
`Transfer Pricing` during drafting: a related-party disclosure on a domestic
return is a related-party diligence fact, while transfer pricing is a
cross-border documentation question, and they have different reviewers.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Filing Status`, `Amendments and Adjustments`, `Referenced but Not Produced`
- Purpose: inventory the filing and its attachments, and record whether the
  schedules are present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the return as filed, its schedules, statements, and elections, any amended or superseding return for the same period, any extension request, any filing confirmation or acknowledgement, any payment record or refund notice, and any workpaper or reconciliation produced with it.
- Treat schedules and statements bound into the return as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed form number and title, exactly as printed. **Form numbers are how tax documents are identified and requested**, so report them precisely.
- Give each document's own stated or filed date.
- State the function as one of `Return as filed`, `Amended return`, `Schedule or statement`, `Election statement`, `Extension request`, `Filing confirmation`, `Payment record`, `Refund notice`, `Workpaper`, or `Other`.
- **Where the return is present without its schedules, state that.** The schedules carry the elections, the attribute detail, the related-party disclosures, and the group membership, and a return without them answers very few of this table's questions.
- **Where an amended return is present, note in the evidence field what it changed.**
- **Where the document is an unsigned or draft return, state that**, since a draft return is not a filing.
- Where a document relates to a different entity, period, or tax type, still list it and append ` [relates to [entity, period, or type]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Form number and title] ([Function])`

Return no more than 12 lines and no more than 110 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Filing Type

- Native type: Classify
- Configured options, in UI order: `Federal or national income`, `State or provincial income`, `Franchise or capital`, `Sales and use`, `Value added or goods and services`, `Payroll and employment`, `Property`, `Excise or industry-specific`, `Withholding`, `Information return`, `Non-resident or treaty`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Return Position Summary`, `Loss and Credit Carryforwards`, `Transfer Pricing`, `Registration and Nexus Footprint`
- Purpose: route the substantive columns, since an income return, a sales tax
  return, and a payroll return share almost no fields.

```markdown
## Task

Classify the type of tax this filing relates to. Choose exactly one configured option.

## Rules

- Classify on the tax the return reports, using the form's own identification.
- `Franchise or capital`: a tax on capital, net worth, or the privilege of doing business rather than on income. **Kept separate because it is commonly overlooked** and because it can be payable in a jurisdiction where there is no income tax liability at all.
- `Information return`: a return reporting information without assessing tax on the filer — partnership and pass-through information returns, benefit plan returns, foreign entity and account reporting, and payee information reporting. **Report in the evidence field what the return reports**, since the penalty exposure for unfiled or incorrect information returns can be substantial and independent of any tax liability.
- `Withholding`: returns reporting tax withheld on payments to third parties, including cross-border withholding.
- `Non-resident or treaty`: returns or claims made under a double tax treaty or a non-resident regime.
- `Sales and use` and `Value added or goods and services` are separate options because the regimes and the exposure profiles differ substantially.

**Report the exact form number in the evidence field**, since the form identifies the regime more precisely than any category.

Where one filing reports more than one tax, classify on the principal tax and note the others.

## Fallback rules

- Use `Other` where the filing reports a tax none of the options describes.
- Use `Unable to determine` where the documents are too fragmentary to identify the tax.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Taxpayer Entity

- Native type: Free Response
- Upstream: none
- Downstream: `Taxpayer Match`
- Purpose: which entity filed, exactly as named.

```markdown
## Task

State the taxpayer named on this filing.

## Rules

- Report the name exactly as printed on the return, including entity suffix and any trade name. **Do not correct or normalize it.**
- **Do not report the taxpayer identification number, employer identification number, social security number, or any equivalent identifier.** Note in the evidence field only whether an identifier is present, and never its value.
- Where the return is filed by one entity on behalf of a group, report the filing entity and note that it files for a group; the members are reported in `Consolidated or Combined Group`.
- **Where the return is filed by a disregarded entity, a branch, or a division, report it as printed and add `(disregarded or branch filing)`.** These filings frequently sit outside the entity list and are easy to miss.
- Where the taxpayer's name on the return differs from a name on the review-subject list, report the return's name.
- **Where the filing is a joint or individual return naming natural persons, report `Individual return` without names.** An individual return in a corporate data room is unusual and should be flagged rather than transcribed.

## Fallback rules

- Return `Not stated` where the return names no taxpayer.
- Return `Unable to determine` where the name is illegible.

## Output format

`[Name exactly as printed]`, with any qualifier appended. Return no more than 30 words. Do not include any identification number.
```

---

### 4. Taxpayer Match

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Filed under a former name`, `Disregarded entity or branch of a target entity`, `Filed by seller or an affiliate outside the group`, `Filed by a third party`, `Individual return`, `No taxpayer named`, `Unable to determine`
- Upstream: `@Taxpayer Entity`
- Downstream: none
- Purpose: whether the filing belongs to the acquired group.

**The `Filed by seller or an affiliate outside the group` state matters most.**
Where the target has been filing inside the seller's consolidated or combined
group, it leaves that group at closing — which triggers deconsolidation, may create
several liability for the group's prior taxes, and makes the tax sharing agreement
in the companion table the operative document.

```markdown
## Established result

- Taxpayer entity: @Taxpayer Entity

Use this result and the target group list in the Table Instructions. Confirm the name against the documents.

## Task

Classify the relationship between the named taxpayer and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No taxpayer named`: Taxpayer Entity returned `Not stated`.
2. `Individual return`: the filing is a personal or joint return of natural persons.
3. `Filed by seller or an affiliate outside the group`: the filing entity is the selling shareholder, its parent, or an affiliate outside the acquired group — including where a target entity is a member of that filer's consolidated or combined group. **The most consequential state**, and it points directly at deconsolidation and the tax sharing agreement.
4. `Disregarded entity or branch of a target entity`: the filer is a disregarded entity, branch, or division of a target entity.
5. `Filed under a former name`: the named taxpayer matches a prior name of a target entity as disclosed in the documents in this unit.
6. `Filed by a third party`: the named taxpayer is an entity that is neither a target entity, nor a former name of one, nor the seller's group.
7. `Matches with name variance`: the named taxpayer is the same entity as one on the target group list but differs in form.
8. `Matches a target entity exactly`: the name is character for character a name on the target group list.

**Do not resolve a variance by assuming.** Where the name is similar but could be a different entity, use `Filed by a third party` and note the similarity in the evidence field.

Where a target entity's former name is not disclosed in this unit, use `Filed by a third party`; the Corporate table's `Prior Names` column resolves it.

## Fallback rules

- Use `Unable to determine` where the name is illegible or Taxpayer Entity returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Taxing Jurisdiction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which authority, which is the join key to the companion table and the
  axis on which the filing footprint is assessed.

```markdown
## Task

State the taxing authority and jurisdiction this filing was made to.

## Rules

- Report the authority exactly as printed, and the jurisdiction it acts for.
- **Report the level — federal or national, state or provincial, county, or municipal.** Local filing obligations are the ones most commonly missed, and a business can be fully compliant federally while unregistered in a dozen municipalities.
- Where the return is a combined or unitary state filing covering several jurisdictions, report the filing jurisdiction and note the others.
- **Where the filing is made to a non-US authority, report the country and append ` [non-US]`**, so the row can be routed to local tax advisers.
- Report any authority-assigned account, registration, or file number **only as a note that one exists in the evidence field**, without reporting its value.
- Where the return covers a jurisdiction other than the one it is filed with, say so.

## Fallback rules

- Return `Not stated` where the authority cannot be identified.
- Return `Unable to determine` where the jurisdiction is illegible.

## Output format

`[Authority as printed] — [jurisdiction]; level: [as stated]`, with any flag appended. Return no more than 40 words.
```

---

### 6. Tax Period

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which period the filing covers. **The axis on which coverage gaps
  become visible**, and the input to the limitation analysis.

```markdown
## Task

State the tax period this filing covers.

## Rules

- Report the period exactly as stated, with its start and end dates where given, for example `fiscal year ended 2024-12-31`, `quarter ended 2024-03-31`, `calendar year 2023`.
- **Report whether the period is a full period or a short period, and where short, report why if the return states it** — a change of accounting period, an entity formed or dissolved mid-year, or an ownership change. **A short-period return is frequently evidence of a prior transaction or a restructuring**, and it is worth the reviewer's attention.
- Report the accounting year end where it differs from the calendar year.
- Where the return covers a period straddling a prior ownership change, say so.
- **Where the return is filed for a period after a stated deconsolidation or entry into a group, note that**, since it marks the boundary of the group filing history.
- Report periods as stated. **Do not calculate a period length or infer a period from a filing date.**

## Fallback rules

- Return `Not stated` where the return does not state its period.
- Return `Unable to determine` where periods conflict or are illegible.

## Output format

`[Period as stated][; short period: [reason or "reason not stated"]]`. Return no more than 35 words.
```

---

### 7. Filing Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: `Statute of Limitations`
- Purpose: when the return was filed. **The date from which almost every
  limitation period runs**, which is why it feeds the limitation column.

```markdown
## Task

Identify the date this return was filed.

## Date-selection hierarchy

1. Use a filing acknowledgement, electronic filing confirmation, or authority date stamp in the unit.
2. If none, use the date the return states it was signed.
3. If neither, use a postmark or transmittal date shown in the unit.

## Excluded dates

- The end of the tax period
- The statutory or extended due date. **Report those in the evidence field where the documents state them**, since the relationship between the due date and the filing date is what shows whether the return was late
- The date of an amended return, which is reported in Amendments and Adjustments
- The date of a payment
- File name and metadata dates, and printing and scan dates

## Rules

- **Report whether the return was filed on or before its stated due date, where the documents state the due date.** A late return can extend or restart the limitation period in several regimes and can attract its own penalty, and the comparison is only possible where both dates are reported.
- **Report any extension in the evidence field, with the extended due date.** An extension changes the due date, not the period.
- **Where no filing confirmation is present, note in the evidence field that the filing date rests on the signature date alone.** A signed return is not a filed return, and this distinction is the most common weakness in this column.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no filing date can be selected under the hierarchy.
```

---

### 8. Filing Status

- Native type: Classify
- Configured options, in UI order: `Filed, confirmation in unit`, `Filed, signature only`, `Filed late`, `Extended, filed within extension`, `Extended, not yet filed`, `Amended`, `Draft or unsigned`, `Not filed`, `Under audit`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the return was actually filed, and on what evidence.

**A draft return in a data room is not a filing.** Nor is a signed but
unacknowledged one, quite. The distinction matters because an unfiled period has
no limitation period running against it — the exposure stays open indefinitely.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the filing evidence available. Confirm against the documents.

## Task

Classify the filing status of this return. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Under audit`: the documents indicate the return or its period is under examination. **Also a row in the companion table**, and the audit suspends the practical finality of the return.
2. `Not filed`: the documents indicate the return was required and not filed, or a period is identified as unfiled.
3. `Draft or unsigned`: the return in the unit is marked draft, is unsigned, or shows no filing evidence and no signature. **This is not a filing** and it should never be recorded as one.
4. `Extended, not yet filed`: an extension request is present and no return for the period appears.
5. `Amended`: an amended return for the period is present. Report the original and amended positions in Amendments and Adjustments.
6. `Filed late`: filing evidence shows the return was filed after its stated due date, including any extended due date. **Report the delay in the evidence field.**
7. `Extended, filed within extension`: an extension was obtained and the return was filed within it.
8. `Filed, confirmation in unit`: an acknowledgement, electronic filing confirmation, or authority stamp evidences filing.
9. `Filed, signature only`: the return is signed and dated with no filing confirmation. **Filing rests on inference**, and where the period matters the confirmation should be obtained.

**Do not infer filing from a payment record, a subsequent return referring back to the period, or a tax provision in the accounts.** Those are consistent with filing but they do not evidence it.

## Fallback rules

- Use `Unable to determine` where filing evidence conflicts or is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Return Position Summary

- Native type: Free Response
- Upstream: `@Filing Type`
- Downstream: none
- Purpose: the headline figures as filed, reported so the tax advisers have an
  inventory to work from.

```markdown
## Established result

- Filing Type: @Filing Type

## Task

Report the principal figures this return states.

## Rules by filing type

- `Federal or national income`, `State or provincial income`: gross receipts or revenue, taxable income or loss, tax before credits, credits claimed, total tax, payments and withholding applied, and the balance due or refund claimed.
- `Franchise or capital`: the base on which the tax is computed and the tax due.
- `Sales and use`, `Value added or goods and services`: gross sales, taxable sales, exempt sales, tax collected, input credits or deductions claimed, and net tax due.
- `Payroll and employment`: total wages, taxable wages, tax withheld, employer contributions, and total deposits.
- `Property`: the assessed value and the tax due.
- `Withholding`, `Non-resident or treaty`: amounts paid, amounts withheld, and any treaty rate applied.
- `Information return`: state that no tax is assessed and report the principal amounts the return reports.
- `Excise or industry-specific`: the base, the rate as stated, and the tax due.

## Rules

- **Report each figure exactly as stated, with its line or schedule reference where the return provides one.** The reference is how a tax adviser finds it again.
- **Do not calculate anything.** Do not compute an effective rate, total across schedules, net a loss against income, apply a rate, reconcile the balance due, or convert currency. **Where a figure is not on the return, it is `Not stated`.**
- Report a loss as a loss, with the figure as printed, and do not convert it to a negative or a positive.
- Where the return reports figures for a group, report them as group figures and say so.
- **Do not assess whether any figure is correct or whether the return appears complete.**

## Fallback rules

- Return `Not stated` where the return's figures are absent, which is expected where the schedules were not produced.
- Return `Unable to determine` where figures conflict or are illegible.

## Output format

One line per figure:

`[Item] — [figure] [currency][ (line [reference])]`

Return no more than 10 lines and no more than 95 words. Do not include any figure you calculated.
```

---

### 10. Loss and Credit Carryforwards

- Native type: Free Response
- Upstream: `@Filing Type`
- Downstream: none
- Purpose: the attributes on the balance sheet of the tax return. **Loss and credit
  carryforwards are commonly limited or lost on a change of ownership**, so the
  buyer may be paying for attributes the transaction itself destroys — and it is
  frequently the largest single tax point in a deal.

```markdown
## Established result

- Filing Type: @Filing Type

## Task

Report the loss, credit, and other tax attributes carried forward that this return states.

## Applicability

- Applies where Filing Type is `Federal or national income`, `State or provincial income`, `Franchise or capital`, or `Non-resident or treaty`.
- For other filing types, report any carryforward the return states, and otherwise return `Not applicable`.

## Include where expressly stated

- **Net operating loss or trading loss carryforwards, with the amount and the year each arose**
- Capital loss carryforwards, with the amount and year
- **Credit carryforwards, identified by credit type, with the amount and year** — research, foreign tax, minimum tax, investment, or other
- Any expiry date or expiry year stated for a carryforward
- Any carryforward stated to be subject to a limitation, and the limitation as described
- **Any annual limitation amount stated as arising from a prior ownership change**, and the date of that change
- Any interest expense, charitable contribution, or other carryforward
- Any carryback claimed or available
- Any valuation allowance or unrecognised attribute referenced
- Any state or provincial attribute differing from the federal amount

## Rules

- **Report each attribute with the year it arose and its stated expiry.** The vintage matters: attributes expire, and an old loss may be worth nothing regardless of the transaction.
- **Report any existing limitation from a prior ownership change prominently, with its date.** Where the target has changed hands before, its attributes may already be limited, and **a second change of ownership can stack a further limitation on top.**
- **Report the attributes exactly as stated. Do not total them, do not compute a tax value at any rate, do not apply any limitation, and do not assess whether the attributes survive this transaction.** The attribute analysis is a tax adviser's exercise requiring the ownership history, the valuation, and the law, and none of it belongs in a grid.

## Fallback rules

- Return exactly `None stated` where the return states no carryforward.
- Return `Not applicable` where the filing type carries no attributes.
- Return `Unable to determine` where attributes conflict or are illegible.

## Output format

One line per attribute:

`[Attribute type] — [amount] [currency] — arose [year] — expires [year or "not stated"][; limitation: [as stated]]`

Return no more than 10 lines and no more than 100 words. Do not include totals or tax values you calculated.
```

---

### 11. Elections Made

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the elections that define the entity's tax character and treatment.
  **An election can determine the whole structure of the transaction**, and an
  invalid or terminated one is a live exposure.

```markdown
## Task

Report every tax election this return or its attachments states has been made.

## Include where expressly stated

- **Any entity classification election** — a check-the-box election, an election to be treated as a corporation or as a partnership, or an equivalent
- **Any pass-through election** — S corporation status, a qualified subchapter S subsidiary election, or an equivalent regime election. **Report the effective date**, and any statement about whether the entity has continuously qualified
- Any consolidated or combined filing election, and the group it relates to
- Any accounting method election — cash or accrual, inventory method, or a change of method
- Any depreciation, expensing, or capitalisation election
- Any basis adjustment or partnership basis election
- Any election relating to a prior acquisition, including an election to treat a stock purchase as an asset purchase
- Any installment sale, deferral, or spread election
- Any treaty election or claim
- Any state or provincial election differing from the federal position
- Any protective or contingent election
- Any statement that an election was revoked, terminated, or is under review

## Rules

- **Report each election with its effective date and the form or statement it was made on.** The election statement is the evidence, and a claimed election with no statement in the file is not evidenced.
- **Report any pass-through election prominently.** Where the target is a pass-through entity, the transaction's structure, the sellers' tax position, and often the price all turn on it — and **an inadvertently terminated election is a significant exposure**, because the entity would have been taxable as a corporation for every affected year.
- **Report any election relating to a prior acquisition**, since it establishes the entity's basis position and may affect this transaction's structure.
- Report the elections as stated. **Do not assess whether any election is valid, effective, or has been preserved**, and do not conclude that an election is available for this transaction.

## Fallback rules

- Return exactly `None stated` where the return and its attachments disclose no election.
- Return `Unable to determine` where elections conflict or are illegible.

## Output format

One line per election:

`[Election] — effective [YYYY-MM-DD or year] — per [form or statement]`

Return no more than 8 lines and no more than 90 words.
```

---

### 12. Consolidated or Combined Group

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who files with whom. **Where the target files inside the seller's group,
  it leaves that group at closing** — and in several regimes each member is
  severally liable for the whole group's tax for the years it was a member,
  regardless of any agreement between them.

```markdown
## Task

Report the consolidated, combined, or group filing arrangement this return discloses.

## Include where expressly stated

- Whether the return is filed on a consolidated, combined, unitary, or group basis
- **The common parent or filing entity, exactly as named**
- **Every member entity listed, exactly as named**, with any indication of when each joined or left the group
- Any member entity that is not on the review-subject list
- Any statement that a member joined or left the group during the period, with the date
- Any intercompany transaction eliminated or reported at group level
- Any statement of the allocation of group tax among members
- **Any statement about several or joint liability of members for group tax**
- Any separate-entity or stand-alone computation attached
- Any state or provincial group differing in composition from the federal group

## Rules

- **Report the common parent and note whether it is inside or outside the acquired group**, using the review-subject list. **This single fact determines whether the target is leaving a group at closing**, which is the question the whole column exists for.
- **List every member as named.** Where more than twelve are listed, report the count, name the parent and every target-group member, and append ` and [N] further members`. **A member entity that does not appear on the review-subject list is a finding in either direction** — an unknown affiliate, or an entity the buyer thought it was acquiring.
- **Report any several-liability statement prominently.** Group members commonly remain liable for the group's tax for their membership years even after leaving, **and a tax sharing agreement allocates that liability between the parties but does not remove it as against the authority.** The agreement itself is a row in the companion table.
- Report any allocation method as stated. **Do not compute any member's share.**
- Do not assess whether the group filing was properly made.

## Fallback rules

- Return exactly `Separate filing` where the return is filed on a stand-alone basis.
- Return `Unable to determine` where the group composition is illegible or inconsistent.

## Output format

`Basis: [consolidated | combined | unitary]; parent: [name] ([inside | outside] acquired group); members: [names]; several liability: [as stated or "Not addressed"]; allocation: [as stated or "Not addressed"]`

Return no more than 100 words.
```

---

### 13. Uncertain Positions and Reserves

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the positions the taxpayer itself flagged as uncertain. **The best
  available guide to where the real exposure is**, because it is the taxpayer's own
  assessment of its weakest ground.

```markdown
## Task

Report any uncertain tax position, reserve, disclosure, or aggressive position this return or its attachments discloses.

## Include where expressly stated

- Any uncertain tax position disclosed, and the issue it relates to
- Any reserve or provision for an uncertain position, with the amount
- **Any position disclosed on a disclosure statement, protective disclosure, or equivalent**, and the position disclosed
- Any reportable or listed transaction disclosure, and the transaction described
- Any position stated to be taken contrary to, or without clear support from, an authority
- Any position for which an opinion or advice was obtained, and from whom
- Any position stated to be subject to a penalty protection disclosure
- Any statement of a position's more-likely-than-not or equivalent assessment
- Any accounting method or timing position identified as uncertain
- Any position relating to a prior transaction, restructuring, or intercompany arrangement

## Rules

- **Report each position with the issue, the amount at stake where stated, and the disclosure it appears on.** The disclosure statement is the taxpayer telling the authority where to look, and it is equally where a buyer should look.
- **Report any reportable or listed transaction disclosure prominently.** These carry heavy penalty regimes, they attract examination, and the penalties can apply independently of whether the underlying position was right.
- **Report where an opinion was obtained**, since the opinion is a document that should be produced and it is a row in the companion table.
- **Report reserves as stated, with the basis of measurement where given. Do not total reserves, do not compute an exposure, and do not assess whether a position is sustainable.**
- **Note in the evidence field any privilege or work-product marking**, since positions material and tax advice frequently attract protection, and do not assess privilege.

## Fallback rules

- Return exactly `None disclosed` where the return and its attachments disclose no uncertain position or reserve.

Note: this reflects these documents only. **Uncertain positions are more often recorded in the tax provision workpapers and the audit response than on the return**, and those sit with the finance workstream and the companion table.

- Return `Unable to determine` where disclosures conflict or are illegible.

## Output format

One line per position:

`[Issue] — [amount at stake or reserve, or "not stated"] — per [disclosure or form]`

Return no more than 8 lines and no more than 90 words.
```

---

### 14. Related-Party Transactions Disclosed

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: transactions with affiliates, founders, and shareholders as disclosed
  for tax. **Frequently the only place a related-party arrangement is documented at
  all**, and the join to the related-party workstream.

```markdown
## Task

Report the related-party transactions and balances this return or its schedules disclose.

## Include where expressly stated

- Any loan to or from a shareholder, officer, director, member, or partner, with the balance
- Any loan to or from an affiliate or group company, with the balance
- Any compensation, management fee, or service charge paid to a related party
- Any rent, royalty, or licence fee paid to or received from a related party
- Any sale, purchase, or transfer of assets involving a related party
- Any distribution, dividend, or return of capital to owners
- Any guarantee given to or received from a related party
- Any debt forgiveness or capital contribution involving a related party
- Any transaction the return identifies as not at arm's length
- Any related party identified by relationship rather than by name

## Rules

- **Report the parties by relationship rather than by individual name** — `shareholder`, `officer`, `affiliate [entity name]` — and name entities but not natural persons.
- **Report shareholder and officer loan balances prominently, with the direction.** A loan **to** a shareholder is an asset the buyer may be acquiring and may need repaid or waived at closing; a loan **from** a shareholder is debt commonly repaid or capitalised at closing. The direction determines which, and it also engages the Debt workstream.
- **Report any transaction identified as not at arm's length**, since it invites both a tax adjustment and a related-party finding.
- **Report each related party and arrangement so it can be matched against the related-party workstream.** A related-party arrangement disclosed on a tax return and documented nowhere else is a common finding, and the tax return is often the only evidence it exists.
- Report balances and amounts as stated. **Do not total, net, or assess whether any transaction was at arm's length.**

## Fallback rules

- Return exactly `None disclosed` where the return discloses no related-party transaction.
- Return `Unable to determine` where disclosures conflict or are illegible.

## Output format

One line per transaction or balance:

`[Type] — [related party by relationship or entity name] — [amount] [currency] — [direction where relevant]`

Return no more than 10 lines and no more than 95 words. Do not name natural persons.
```

---

### 15. Transfer Pricing

- Native type: Free Response
- Upstream: `@Filing Type`
- Downstream: none
- Purpose: the cross-border intercompany pricing position, and whether it is
  documented. **Undocumented transfer pricing is a penalty exposure independent of
  whether the pricing was right.**

```markdown
## Established result

- Filing Type: @Filing Type

## Task

Report the transfer pricing position and documentation this return discloses.

## Applicability

- Applies where Filing Type is `Federal or national income`, `State or provincial income`, `Non-resident or treaty`, or `Information return` where the return reports cross-border or intercompany matters.
- For other filing types, report any transfer pricing disclosure the return makes, and otherwise return `Not applicable`.

## Include where expressly stated

- Whether the return discloses cross-border transactions with related parties, and their categories — goods, services, royalties, interest, management charges, or cost sharing
- The amounts of intercompany transactions by category, as stated
- **The transfer pricing method applied to each category**, as named
- **Any statement that contemporaneous transfer pricing documentation exists**, and its date
- Any advance pricing agreement referenced, with its parties and term
- Any cost sharing or cost contribution arrangement referenced
- Any intercompany loan and its stated interest rate
- Any statement of country-by-country or master file or local file reporting
- Any adjustment made to intercompany pricing on the return
- Any jurisdiction identified as a party to intercompany transactions
- **Any statement that documentation is not maintained, or is maintained only for certain categories**

## Rules

- **Report whether documentation is stated to exist, and report its absence where the return is silent.** In most regimes contemporaneous documentation is what protects against penalties, so **an undocumented position is a penalty exposure even where the pricing itself is defensible** — and the documentation is a document that should be produced.
- **Report any intercompany interest rate**, since it engages both the transfer pricing and the interest deductibility questions.
- Report the method and amounts as stated. **Do not assess whether the method is appropriate, whether the pricing is arm's length, or whether documentation is adequate.**
- **Report the jurisdictions involved**, since each is a separate tax authority with its own documentation rules and its own examination risk.

## Fallback rules

- Return exactly `No cross-border related-party transactions disclosed` where the return discloses none.
- Return `Not applicable` where the filing type raises no transfer pricing question.
- Return `Unable to determine` where disclosures conflict or are illegible.

## Output format

`Categories: [as stated with amounts]; method: [as named]; documentation: [exists, dated [date] | not stated | stated not maintained]; APA: [as stated or "none"]; jurisdictions: [as stated]`

Return no more than 90 words.
```

---

### 16. Statute of Limitations

- Native type: Free Response
- Upstream: `@Filing Date`
- Downstream: none
- Purpose: **when the exposure for this period closes.**

The single most useful column in this table for a corporate lawyer, because the
tax indemnity tail in the SPA is set by reference to it. A period whose limitation
period has run is closed; a period still open is a live exposure; and **an unfiled
period has no limitation period running at all** — the exposure stays open
indefinitely, which is why the unfiled cases matter more than the filed ones.

```markdown
## Established result

- Filing date: @Filing Date

## Task

Report what the documents state about the limitation, assessment, or examination period for this filing.

## Include where expressly stated

- Any statutory limitation or assessment period the documents state, and its length
- Any expiry date of the limitation period the documents state
- **Any waiver, extension, or consent extending the limitation period, with the extended date and the scope of the extension.** These are commonly signed during an examination, and **an extension in the file means the period a buyer assumed was closed is open**
- Any statement that the limitation period is suspended, tolled, or does not run
- Any statement that a longer period applies — commonly where income was substantially understated, where a return was not filed, or where fraud is alleged
- Any statement that no limitation period applies
- Any separate limitation period stated for a state, provincial, or local jurisdiction
- Any statement that the period is affected by a carryback or carryforward claim
- Any closing agreement or determination stated to close the period

## Rules

- **Report only what the documents state. Do not calculate a limitation expiry from the filing date and a statutory period, even where the period is standard and well known.** A calculated date looks identical to a stated one in an export, statutory periods vary by tax and jurisdiction and are subject to multiple extensions, **and the tax indemnity tail in the SPA may be drafted from this column.** Getting it wrong by inference is worse than leaving it blank.
- **Report any waiver or extension prominently, with its scope.** An extension may be limited to specified issues, and the distinction matters.
- **Where Filing Date is `Not stated` or Filing Status is `Not filed`, say so and note that no limitation period can be established.** For an unfiled period **the exposure is open indefinitely in most regimes**, and that is the most consequential answer this column gives.
- Report the periods and dates as stated. **Do not assess whether any period has expired or whether any exposure is closed.**

## Fallback rules

- Return `Not addressed` where the documents state nothing about the limitation period. **This is the common answer**, since returns rarely recite the limitation rules, and it is a routing instruction: the reviewer establishes it from the law and the filing date.
- Return `Not applicable` where Filing Status is `Not filed` or `Draft or unsigned`, and note in the evidence field that no period runs.
- Return `Unable to determine` where statements conflict or are illegible.

## Output format

`Period stated: [as stated or "Not addressed"]; expiry stated: [date or "not stated"]; waiver or extension: [date and scope, or "none"]; extended period asserted: [as stated or "none"]; closed by agreement: [as stated or "no"]`

Return no more than 80 words. Do not include any date you calculated.
```

---

### 17. Registration and Nexus Footprint

- Native type: Free Response
- Upstream: `@Filing Type`
- Downstream: none
- Purpose: where the target is registered and filing. **The gap between where a
  business operates and where it files is the classic mid-market tax finding**,
  and because no return was filed there is no limitation period running against
  it.

```markdown
## Established result

- Filing Type: @Filing Type

## Task

Report what this filing discloses about the taxpayer's registrations, filing footprint, and activity by jurisdiction.

## Include where expressly stated

- **Every jurisdiction in which the return reports income, sales, receipts, payroll, or property**, as apportionment or allocation schedules commonly list
- The apportionment factors reported by jurisdiction, as stated
- Any jurisdiction listed with activity but a nil or zero apportionment
- **Any jurisdiction in which the taxpayer states it is registered**, and any registration date
- Any statement that the taxpayer has no filing obligation in a stated jurisdiction
- For a sales and use or value added filing: the jurisdictions in which tax is collected, any exemption certificates relied on, and any statement of sales into jurisdictions where no tax was collected
- For a payroll filing: the jurisdictions in which employees are reported
- Any statement of physical presence, property, or employees in a jurisdiction
- Any voluntary disclosure or amnesty referenced for a jurisdiction

## Rules

- **List every jurisdiction the return identifies, whether or not tax was paid there.** The apportionment schedule of a multi-state income return is frequently the single best available map of where the business actually operates, and it is what the filing footprint is tested against.
- **Report any jurisdiction with reported activity and no corresponding registration or filing, where the documents show both.** That combination is the finding, and it has **no limitation period running against it** because no return was filed.
- **For a sales and use filing, report any indication of sales into jurisdictions where no tax was collected.** Economic nexus rules mean remote sales can create obligations without any physical presence, and this exposure is commonly unrecognised and grows with every period.
- Report factors and amounts as stated. **Do not calculate an apportionment percentage, do not total by jurisdiction, and do not assess whether nexus exists anywhere.**

## Fallback rules

- Return `Not stated` where the return discloses no jurisdictional information.
- Return `Not applicable` where the filing type is single-jurisdiction and discloses no footprint.
- Return `Unable to determine` where the disclosures are illegible or inconsistent.

## Output format

`Jurisdictions with reported activity: [list]; registered in: [as stated or "not stated"]; factors: [as stated]; activity without filing indicated: [as stated or "none"]`

Return no more than 90 words. Do not include percentages you calculated.
```

---

### 18. Amendments and Adjustments

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: how the filed position has changed. **An amended return is the taxpayer
  correcting itself**, and the reason it amended is usually the finding.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify original and amended filings. Confirm the details against the documents.

## Task

Report every amendment, adjustment, or revision to this period's filing that the documents disclose.

## Rules

- Report each amended return with its filing date, and **what it changed, in ten words or fewer**.
- **Report the original and amended figures for each item changed, exactly as stated on each return.** Do not compute the difference.
- **Report the stated reason for the amendment where the return gives one.** An amendment to claim a refund, to correct an error, to reflect a federal adjustment, or to report a carryback each read very differently.
- **Report any amendment made to conform to an adjustment by another authority**, since it means an examination concluded elsewhere and there should be a row for it in the companion table.
- Report any adjustment made by the authority rather than by the taxpayer, with its date and the amount as stated.
- Report any refund claimed or additional tax paid with the amendment, as stated.
- **Report any statement that an amendment restarted or extended the limitation period.**
- Where an amendment is referenced but not present, note it; the Referenced but Not Produced column carries it.
- Do not assess whether any amendment was correct or whether it invites examination.

## Fallback rules

- Return exactly `None` where no amendment or adjustment is disclosed.
- Return `Unable to determine` where amendments conflict or are illegible.

## Output format

One line per amendment:

`[YYYY-MM-DD] — [what changed] — original [figure], amended [figure] — reason: [as stated or "not stated"]`

Return no more than 6 lines and no more than 85 words. Do not include differences you calculated.
```

---

### 19. Payment Status

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether the tax was actually paid. **An unpaid liability is a debt and
  frequently a lien**, and a tax lien is a first-priority encumbrance in many
  regimes.

```markdown
## Task

Report what the documents state about payment of the tax for this period.

## Include where expressly stated

- The balance due or refund claimed on the return, as stated
- Any payment made, with its date and amount
- Any estimated payments or deposits applied, as stated
- Any refund received, applied to another period, or offset
- **Any unpaid balance, with the amount and the date as of which it is stated**
- Any interest or penalty assessed or stated as accruing
- **Any instalment agreement, payment plan, or deferral, with its terms**
- Any offer in compromise or settlement of a liability
- **Any tax lien filed or threatened, with its date**
- Any levy, garnishment, or collection action
- Any statement that a payment was late, and the delay
- Any credit or overpayment carried to another period

## Rules

- **Report any unpaid balance with its as-of date.** Interest and penalties accrue, so a balance figure without a date is not usable, and **do not accrue anything yourself.**
- **Report any tax lien prominently.** A tax lien is typically a first-priority encumbrance that outranks consensual security, **it must be released at closing, and it should also appear in the Debt — Lien Filings table.** Where it does not, one of the two tables has a gap.
- **Report any instalment agreement with its terms**, since it is an ongoing obligation the buyer inherits and a default on it can accelerate the whole liability.
- **Report any penalty separately from interest and from the tax**, since penalty exposure is frequently negotiable while tax is not.
- Report amounts and dates as stated. **Do not total tax, interest, and penalty, and do not calculate a payoff.**

## Fallback rules

- Return exactly `Fully paid per documents` where the documents evidence payment of the balance shown.
- Return `Not stated` where the documents do not address payment.
- Return `Unable to determine` where payment records conflict or are illegible.

## Output format

`Balance on return: [figure]; paid: [figure and date, or "no evidence"]; unpaid: [figure as at [date], or "none"]; interest and penalty: [as stated or "none"]; instalment agreement: [terms or "none"]; lien: [date or "none"]`

Return no more than 85 words. Do not include totals you calculated.
```

---

### 20. Preparer and Signatory

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who prepared and signed. **Bears on the reliability of the filing, on
  penalty protection, and on who holds the workpapers.**

```markdown
## Task

State who prepared and who signed this return.

## Rules

- Report the preparing firm's name exactly as printed, and whether the return was prepared internally or by an external adviser.
- **Report the signatory by role rather than by name** — officer, director, member, partner, or authorised representative. **Do not report the individual's name or any identification number.**
- Report whether the return bears a preparer declaration or signature.
- **Report whether the return is signed at all.** An unsigned return is not a valid filing in most regimes, and Filing Status carries that.
- Report any power of attorney or authorised representative designation referenced.
- **Report where the return was self-prepared or prepared internally, and note it.** A complex multi-jurisdiction return prepared without external advice is a reliability signal, and the workpapers may not exist in usable form.
- **Report where the preparer differs from the preparer of other periods**, where the documents show it. A change of adviser frequently accompanies a change of position or a dispute.
- Report any statement that the preparer relied on information supplied without verification.

## Fallback rules

- Return `Not stated` where the return identifies no preparer or signatory.
- Return `Unable to determine` where the details are illegible.

## Output format

`Preparer: [firm as printed] — [external | internal]; signed by: [role]; preparer declaration: [present | absent]; POA: [as stated or "none"]`

Return no more than 45 words. Do not name individuals or include identification numbers.
```

---

### 21. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this filing refers to that is not present. Feeds
  the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this filing that the documents in this unit refer to and that is not present.

## Scope

- **Include any schedule, statement, or attachment listed on the return but not present.**
- **Include any election statement referenced but not produced.**
- **Include any transfer pricing documentation, master file, or local file referenced.**
- Include any amended return referenced but absent.
- Include the return for any prior or subsequent period referenced, particularly where an attribute is carried between them.
- Include any federal or parent-jurisdiction return a state or subordinate return is based on.
- Include any filing confirmation, acknowledgement, or receipt referenced.
- Include any payment record, instalment agreement, or lien notice referenced.
- Include any examination report, adjustment notice, or closing agreement referenced.
- Include any waiver or extension of the limitation period referenced.
- Include any opinion, memorandum, or advice referenced in support of a position, **noting that these may be privileged**; report the reference and do not assess privilege.
- Include any tax sharing agreement or intercompany agreement referenced.
- Include any advance pricing agreement or ruling referenced.
- Exclude statutes, regulations, and published guidance.

## Rules

- Name each document as the referencing document names it, with its form number and date where stated.
- **Where a schedule listed on the return is absent, add `; return incomplete`.** Filter these first — the schedules carry the elections, the attributes, the group membership, and the related-party disclosures, so a return without them answers very little.
- **Where a waiver or extension of the limitation period is referenced and absent, add `; limitation period uncertain`.** The indemnity tail may be drafted from it.
- **Where an election statement is absent, add `; election unevidenced`.** A claimed election with no statement is not evidenced.
- Where transfer pricing documentation is absent, add `; penalty protection unevidenced`.
- Where a prior-period return carrying an attribute is absent, add `; attribute origin unverifiable`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon here — **returns list their own schedules, so a missing one is always identifiable.**

## Output format

One line per missing document:

`[Form number and name as referenced] — [YYYY-MM-DD or "date not stated"][; flag]`

Return no more than 15 lines and no more than 130 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Period closed or open** | Closed / Open / No period running / Tax adviser to confirm |
| **Attribute survives transaction** | Yes / Limited / Lost / Tax adviser to confirm |
| **Filing gap identified** | None / Identified (specify) / Unassessed |
| **Nexus exposure** | None / Identified (specify) / Unassessed |
| **Exposure estimate** | Free text |
| **Tax indemnity item** | Yes / No / Unassessed |
| **Escrow or holdback candidate** | Yes / No / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: taxpayer, period, filing status, elections,
carryforwards, limitation position, unpaid balances.

### Reconciliation work that never belongs in a column

- **The filing matrix.** Build a grid in Excel of entity by tax type by
  jurisdiction by period, populated from these rows. **The empty cells are the
  finding**, and they are invisible from inside any row. A period with no return is
  an open exposure with no limitation period running against it, which is worse
  than a filed period with an aggressive position.
- **The nexus and registration analysis.** Every jurisdiction from
  `Registration and Nexus Footprint` against the actual footprint from the Real
  Estate site list, the Employment jurisdictions of employment, and the Contracts
  customer locations. **The gap between where the business operates and where it
  files is the classic mid-market finding**, and economic nexus means remote sales
  create obligations without physical presence.
- **The attribute analysis.** Every carryforward from
  `Loss and Credit Carryforwards`, modelled by tax advisers against the ownership
  history and the transaction structure. **Attributes are commonly limited or lost
  on a change of ownership, and prior ownership changes may already have limited
  them.** No column does this.
- **The limitation matrix and the indemnity tail.** Every period's limitation
  position, established from the law and the filing dates by tax advisers, with
  every waiver and extension identified. **This is what the SPA tax indemnity
  survival period is drafted against**, and it is the output a corporate lawyer
  needs most from this workstream.
- **Election validity.** Every election from `Elections Made`, particularly any
  pass-through election, confirmed as validly made and continuously maintained.
  **An inadvertently terminated pass-through election is a significant exposure**
  affecting every year since.
- **Deconsolidation.** Every row where `Taxpayer Match` is
  `Filed by seller or an affiliate outside the group`, with the tax sharing
  agreement from the companion table. **Several liability for group tax commonly
  survives leaving the group**, and the agreement allocates it between the parties
  without removing it as against the authority.
- **Lien reconciliation.** Every tax lien from `Payment Status` against the
  Debt — Lien Filings table and the Real Estate title exceptions. **A tax lien
  outranks consensual security** and must be released at closing.
- **Related-party matching.** Every arrangement from
  `Related-Party Transactions Disclosed` against the related-party workstream and
  the Debt table's shareholder loans. **A related-party arrangement disclosed only
  on a tax return is a common finding.**
- **Provision reconciliation.** Reserves and uncertain positions against the tax
  provision in the accounts, with the finance workstream. **All arithmetic, none of
  it a column.**

---

## Test set

- [ ] Federal consolidated income return with schedules, filed with confirmation
- [ ] Federal income return present without its schedules
- [ ] Multi-state combined income return with an apportionment schedule
- [ ] State income return for a jurisdiction with nil apportionment
- [ ] Franchise tax return in a state with no income tax
- [ ] Sales and use return showing tax collected in three states
- [ ] Sales and use return indicating sales into states where no tax was collected
- [ ] Payroll return reporting employees in two states
- [ ] Property tax return
- [ ] Information return for a pass-through entity
- [ ] Non-US corporate return
- [ ] Withholding return on cross-border payments
- [ ] Return filed by the seller's parent with target entities as members
- [ ] Return filed by a disregarded entity
- [ ] Return filed under a target entity's former name
- [ ] Return for a short period following a prior acquisition
- [ ] Return filed after its due date
- [ ] Return filed within an extension
- [ ] Extension request with no return for the period
- [ ] Draft unsigned return
- [ ] Return with an amended return claiming a refund
- [ ] Return amended to conform to a federal adjustment
- [ ] Return with a net operating loss carryforward and stated expiry years
- [ ] Return with a carryforward subject to a limitation from a prior ownership change
- [ ] Return with research and foreign tax credit carryforwards
- [ ] Return disclosing a check-the-box election
- [ ] Return disclosing S corporation status with an effective date
- [ ] Return disclosing an election relating to a prior stock acquisition
- [ ] Return with an election referenced but the election statement not attached
- [ ] Return disclosing an uncertain tax position with a reserve
- [ ] Return with a reportable transaction disclosure
- [ ] Return disclosing a shareholder loan receivable
- [ ] Return disclosing management fees paid to an affiliate
- [ ] Return disclosing cross-border royalties with a stated transfer pricing method
- [ ] Return disclosing cross-border transactions with no documentation stated
- [ ] Return referencing an advance pricing agreement
- [ ] Return with a signed waiver extending the limitation period
- [ ] Return with an unpaid balance and a filed tax lien
- [ ] Return with an instalment agreement in place
- [ ] Return under examination
- [ ] Self-prepared multi-state return
- [ ] Return where the preparer differs from the prior year
- [ ] Individual return found in the data room

Then test the dependencies: change `Filing Type` from
`Federal or national income` to `Sales and use` and confirm
`Loss and Credit Carryforwards` and `Transfer Pricing` move to `Not applicable`
while `Return Position Summary` and `Registration and Nexus Footprint` re-run
against the sales tax rules. Change `Filing Date` to `Not stated` and confirm
`Statute of Limitations` reports that no period can be established. Change
`Taxpayer Entity` from a target entity to the seller's parent and confirm
`Taxpayer Match` moves to `Filed by seller or an affiliate outside the group`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
