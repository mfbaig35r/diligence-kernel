# Prompt Inventory — Capitalization and Securities

Platform-ready Harvey Review Table. Third reference table, built to the same
standard as Contracts Core and Corporate.

Keep this file outside Harvey. Exports omit Table Instructions and Harvey does not
version prompts, so this is the authoritative history.

## Table

- Matter: `[Project name]`
- Platform: Harvey Review Tables (UI)
- Project: `[Matter] - Corporate` (same project as the Corporate table)
- Review unit: **one security instrument** — the instrument itself, any amendment
  to it, and any board consent or resolution expressly authorizing it
- Grouping used: **yes**, small units of 1–3 documents
- Intended reviewers and downstream use: corporate/M&A team; feeds the cap table
  reconciliation, the approval and consent schedule, the transaction payments
  schedule, and the coverage register
- Inventory version: v1.0
- Last full run: —
- Last evaluated: —

### Three things that make this table different

**It is deliberately sparse.** `Instrument Type` routes almost every substantive
column, and most columns are `Not applicable` for most rows. Liquidation
preference is meaningless for an option; vesting is meaningless for a warrant held
by a lender. A grid where 60% of substantive cells read `Not applicable` is this
table working correctly, not failing. Tell the reviewers before they see it.

Note also that conditional routing here shapes the **output**, not the execution.
Every column still runs against every row, so the sparseness buys clarity, not
speed.

**`Incorporated terms` finally earns its keep.** Grant agreements routinely say
that vesting, acceleration, transfer restrictions, and post-termination exercise
are "as set forth in the Plan." The correct answer is `Incorporated terms`, not
`Not addressed` — which would falsely tell the reviewer the instrument is silent
and send them looking for a missing provision — and certainly not the plan's terms
supplied from anywhere else. Five columns carry this state explicitly.

**No arithmetic, of any kind.** This is the table where the temptation is
strongest and the consequence worst. Nothing here totals classes, computes vested
amounts from a schedule and a date, derives fully diluted counts, nets
cancellations, converts percentages to unit counts, or models a waterfall. Every
figure is reported as stated, with the document and date it came from, and the
reconciliation happens in Excel against the certified cap table. `Vested Amount as
Stated` exists precisely to hold the line: it reports what a document asserts and
forbids deriving anything.

## Assumptions to confirm before running

1. One row is one instrument. Where a single document grants awards to several
   individuals — a consent approving twelve option grants, or an omnibus
   subscription — it is a compilation and must be split before upload, or it
   produces one averaged row that is worse than nothing.
2. Buy-side review; the issuers in the Table Instructions list are the review
   subjects.
3. Equity plan documents are **not** rows in this table. They are a separate small
   row set — see the appendix — because a plan is one document governing hundreds
   of instruments, and mixing it into the instrument rows breaks the schema.
4. The certified cap table exists and will be the reconciliation baseline. This
   table produces the instrument-level evidence to reconcile against it, not a
   substitute for it.
5. `[Project name]`, the issuer list, and the diligence as-of date are real matter
   parameters.

## Pre-run verification

- [ ] Every Classify column's options configured in the UI, in the order listed in
      each record. **9 Classify columns.** `Instrument Type` has 13 options and is
      the one to check most carefully, since every routed column depends on the
      exact labels.
- [ ] Typed columns tested with one row of each fallback. Test `Grant or Issue
      Date`, `Vesting Commencement Date`, and `Expiration or Maturity` (Date) with
      `Not stated`, `Not applicable`, and `Incorporated terms`. **This column type
      is carrying three different fallback strings here, more than in either other
      table.** Record what the type accepts: ______
- [ ] Verbatim column behaviour confirmed on three known documents.
- [ ] Table Instructions pasted from this file, issuer list and as-of date set.
- [ ] Dependency index re-derived from the prompts.
- [ ] Routing tested with one row of each of: option, warrant, SAFE, convertible
      note, preferred stock, restricted stock, and LLC unit. Confirm the routed
      columns return `Not applicable` where they should and do not reach for the
      nearest analogous term.
- [ ] A grant agreement that incorporates plan terms tested against the five
      `Incorporated terms` columns.
- [ ] Legal choices confirmed by the team: the `Instrument Type` option set, the
      single-versus-double-trigger definitions, and the decision that a profits
      interest is classified separately rather than as an LLC unit.

### Column count

34 Harvey columns plus 9 human columns. If your tenant's practical cap is lower,
split into **Instrument Terms** (columns 1–23) and **Transaction Triggers and
Authorization** (columns 24–34) over the same project, joined on holder and
instrument in the export. Do not drop columns to fit.

---

## Table Instructions

- Version: v1.0
- Last changed: —

About 2,700 characters. The no-arithmetic rule and the plan-incorporation rule are
here rather than in each column because they are true of every column, and
repeating them thirty-four times would crowd out the rules that are not.

```markdown
## Matter

[Project name]. Buyer-side capitalization and securities diligence on the target group listed below.

One row is one security instrument: the instrument itself, any amendment to it, and any board consent or resolution expressly authorizing it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Issuers

Use these names exactly as written when an issuer is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Terminology

Columns refer to `units` generically. Read this as shares for a corporation, and as membership interests, units, or percentage interests for a limited liability company or partnership.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the holders or the issuer.
- **Report figures only as the documents state them. Do not calculate anything.** Do not total classes, do not sum multiple issuances, do not net cancellations or repurchases, do not compute a vested amount from a schedule and a date, do not derive a unit count from a percentage or a percentage from a unit count, and do not compute a fully diluted total or a distribution waterfall. Where a figure is not stated, say so.
- Where the instrument states that a term is governed by an equity incentive plan, stockholders agreement, or other document that is not in the current review unit, return `Incorporated terms` for that term. Do not treat the instrument as silent, and do not supply the other document's terms.
- Where two documents in the unit address the same term, report the term as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Use holder, issuer, and individual names exactly as printed; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Write currency amounts with the currency as printed, for example `$0.001` or `USD 1,250,000`.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

`Instrument Type` is the spine. Fifteen columns route on it, because the
qualifying evidence for a term genuinely differs between an option and a
convertible note — not merely its name.

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Instrument Type
  Issuer
  Holder
  Class or Series
  Holder Consent or Veto Right
  Voting or Support Obligation
  Securities Exemption Referenced
  Plan or Governing Document Referenced

Stage 2 — Record status
  Documents in Unit ──→ Execution Status
                        Board Approval Referenced
                        Referenced but Not Produced
  Holder            ──→ Holder Type

Stage 3 — Routed on instrument type
  Instrument Type ──→ Quantity and Unit
                      Grant or Issue Date
                      Price Terms
                      Expiration or Maturity
                      Vesting Commencement Date
                      Vesting Schedule
                      Post-Termination Exercise Period
                      Repurchase or Forfeiture on Termination
                      Early Exercise and 83(b) Election
                      Conversion Mechanics
                      Liquidation Preference
                      Participation Rights
                      Anti-Dilution Protection
                      Dividend Rights
                      Redemption Rights
                      Acceleration on Change of Control
                      Transfer Restrictions
                      Valuation Referenced

Stage 4 — Conditional detail and quotation
  Vesting Schedule                 ──→ Vested Amount as Stated
  Acceleration on Change of Control ──→ Acceleration Language
  Holder Consent or Veto Right      ──→ Consent Right Language
```

`Execution Status` is referenced by `Board Approval Referenced` only, and not by
the substantive term columns — the same choice as in the other two tables.
Execution evidence changes what a cell proves, not what the document says.

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Documents in Unit | Free Response | — | Execution Status; Board Approval Referenced; Referenced but Not Produced | v1.0 | draft |
| 2 | Instrument Type | Classify | — | 18 columns — see map | v1.0 | draft |
| 3 | Issuer | Free Response | — | — | v1.0 | draft |
| 4 | Holder | Free Response | — | Holder Type | v1.0 | draft |
| 5 | Holder Type | Classify | @Holder | — | v1.0 | draft |
| 6 | Execution Status | Classify | @Documents in Unit | Board Approval Referenced | v1.0 | draft |
| 7 | Class or Series | Free Response | — | — | v1.0 | draft |
| 8 | Quantity and Unit | Free Response | @Instrument Type | — | v1.0 | draft |
| 9 | Grant or Issue Date | Date | @Instrument Type | — | v1.0 | draft |
| 10 | Price Terms | Free Response | @Instrument Type | — | v1.0 | draft |
| 11 | Expiration or Maturity | Date | @Instrument Type | — | v1.0 | draft |
| 12 | Vesting Commencement Date | Date | @Instrument Type | — | v1.0 | draft |
| 13 | Vesting Schedule | Free Response | @Instrument Type | Vested Amount as Stated | v1.0 | draft |
| 14 | Vested Amount as Stated | Free Response | @Vesting Schedule | — | v1.0 | draft |
| 15 | Post-Termination Exercise Period | Free Response | @Instrument Type | — | v1.0 | draft |
| 16 | Repurchase or Forfeiture on Termination | Free Response | @Instrument Type | — | v1.0 | draft |
| 17 | Early Exercise and 83(b) Election | Classify | @Instrument Type | — | v1.0 | draft |
| 18 | Conversion Mechanics | Free Response | @Instrument Type | — | v1.0 | draft |
| 19 | Liquidation Preference | Free Response | @Instrument Type | — | v1.0 | draft |
| 20 | Participation Rights | Classify | @Instrument Type | — | v1.0 | draft |
| 21 | Anti-Dilution Protection | Classify | @Instrument Type | — | v1.0 | draft |
| 22 | Dividend Rights | Free Response | @Instrument Type | — | v1.0 | draft |
| 23 | Redemption Rights | Classify | @Instrument Type | — | v1.0 | draft |
| 24 | Acceleration on Change of Control | Classify | @Instrument Type | Acceleration Language | v1.0 | draft |
| 25 | Acceleration Language | Verbatim | @Acceleration on Change of Control | — | v1.0 | draft |
| 26 | Holder Consent or Veto Right | Free Response | — | Consent Right Language | v1.0 | draft |
| 27 | Consent Right Language | Verbatim | @Holder Consent or Veto Right | — | v1.0 | draft |
| 28 | Transfer Restrictions | Free Response | @Instrument Type | — | v1.0 | draft |
| 29 | Voting or Support Obligation | Classify | — | — | v1.0 | draft |
| 30 | Board Approval Referenced | Free Response | @Documents in Unit; @Execution Status | — | v1.0 | draft |
| 31 | Plan or Governing Document Referenced | Free Response | — | — | v1.0 | draft |
| 32 | Valuation Referenced | Free Response | @Instrument Type | — | v1.0 | draft |
| 33 | Securities Exemption Referenced | Free Response | — | — | v1.0 | draft |
| 34 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Execution Status`, `Board Approval Referenced`, `Referenced but Not Produced`
- Purpose: inventory the small document set behind the row, so a reviewer can see
  whether an authorizing consent was produced alongside the instrument.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the instrument itself, any amendment, cancellation, or repurchase agreement affecting it, any board or owner consent or resolution authorizing it, and any exercise or conversion notice.
- Treat exhibits and schedules physically attached to a document as part of that document.
- Do not include documents that are only referenced but not present. Those belong to the Referenced but Not Produced column.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Instrument`, `Amendment`, `Board consent`, `Owner consent`, `Exercise notice`, `Conversion notice`, `Cancellation or repurchase`, or `Other`.
- Where a document relates to a holder or instrument other than the subject of this row, still list it and append ` [relates to [holder or instrument]]`. This is how a misassembled unit surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 8 lines and no more than 80 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Instrument Type

- Native type: Classify
- Configured options, in UI order: `Common stock`, `Preferred stock`, `Stock option`, `Restricted stock`, `Restricted stock unit`, `Warrant`, `SAFE`, `Convertible note`, `Stock appreciation right or phantom`, `LLC unit or membership interest`, `Profits interest`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: eighteen columns — see the map
- Purpose: route every term column, since the qualifying evidence for a term
  differs by instrument form.

**Get this column right before anything else.** Every routed column reads its
exact label, so a misclassification here propagates a plausible but wrong answer
across fifteen cells.

```markdown
## Task

Classify the security instrument that is the subject of this review unit. Choose exactly one configured option.

## Scope

- Classify the instrument the unit documents. Where a consent authorizes an instrument, classify the instrument authorized, not the consent.
- Exclude instruments merely referenced, such as the class into which a note converts.

## Classification rules

Classify on the operative rights the document creates, not on its title.

- `Common stock`: issued and outstanding common or ordinary units with no preference.
- `Preferred stock`: issued units carrying a liquidation preference, a dividend preference, or class voting rights.
- `Stock option`: a right to purchase units at a stated exercise price, granted for services.
- `Restricted stock`: units issued outright and subject to forfeiture or repurchase until vested. The holder owns them now. This is not the same as a restricted stock unit.
- `Restricted stock unit`: a contractual right to receive units on vesting or settlement. The holder owns nothing yet.
- `Warrant`: a right to purchase units at a stated price, issued other than for services — commonly to a lender, investor, or commercial partner.
- `SAFE`: a simple agreement for future equity, converting on a future financing, with no maturity date and no interest.
- `Convertible note`: a debt instrument convertible into units, with a maturity date and usually interest.
- `Stock appreciation right or phantom`: a cash-settled or notional right measured by unit value, conferring no unit ownership.
- `Profits interest`: an interest in future profits and appreciation of a partnership or LLC, with no right to existing capital. Classify here rather than as an LLC unit, because the economics and the tax treatment differ.
- `LLC unit or membership interest`: an issued membership interest, whether expressed as units or a percentage.

A convertible instrument with both a maturity date and stated interest is a `Convertible note` even where it is titled a SAFE, and the reverse.

An option granted under a plan is a `Stock option` whether or not the document uses that word.

## Fallback rules

- Use `Other` where the document creates rights none of the options describes.
- Use `Unable to determine` where the operative rights are incorporated from a document not in the unit, or are illegible or internally inconsistent.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Issuer

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity issued the instrument, since instruments issued by a
  subsidiary are a different problem from instruments issued by the parent.

```markdown
## Task

State the entity that issued or granted the instrument.

## Scope

- Take the issuer from the instrument's own parties clause, signature block, or grant notice.
- Use the issuer list in the Table Instructions to determine whether it is a group entity.
- Exclude the holder, any parent or affiliate of the issuer named only in a definition, any plan sponsor named as administrator rather than issuer, and any transfer agent.

## Rules

- Report the name exactly as printed, including the entity suffix.
- Where the printed name differs from the issuer list in the Table Instructions, report the printed name and append ` (variant of [listed name])`.
- Where the instrument is issued by an entity that is not on the issuer list, report the name and append ` (not a listed issuer)`. This surfaces an instrument in the wrong project or an entity missing from the group.
- Where the issuer changed by amendment, assumption, or merger recorded in the unit, report the current issuer and append ` (assumed from [prior issuer], [YYYY-MM-DD])`.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the issuer, or the name is illegible.

## Output format

`[Exact legal name]`, with any qualifier appended as described above. Return no more than 25 words.
```

---

### 4. Holder

- Native type: Free Response
- Upstream: none
- Downstream: `Holder Type`
- Purpose: the holder's exact name, which is the join key for the cap table
  reconciliation, the employment table, and the consent list.

```markdown
## Task

State the current holder of the instrument.

## Scope

- Take the holder from the instrument's parties clause or grant notice, and from any transfer, assignment, or assumption recorded in the unit.
- Exclude the issuer, plan administrator, trustee acting only as custodian, escrow agent, and any beneficiary named only for death or disability.

## Rules

- Report the name exactly as printed. Where the holder is an individual, report the name as printed without adding a title.
- Where the holder is an entity, include the entity suffix as printed.
- Where the instrument was transferred and the unit records it, report the current holder and append ` (transferred from [prior holder], [YYYY-MM-DD])`.
- Where the instrument is held jointly or by a trust, report the holder exactly as the document styles it, for example `[Name], as trustee of the [Name] Revocable Trust`.
- Do not report the individual behind an entity holder, and do not report a beneficial owner not named as the holder.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the holder, or the name is illegible.

## Output format

`[Exact name]`, with any qualifier appended as described above. Return no more than 30 words. Do not include addresses, taxpayer identifiers, or citation markers.
```

---

### 5. Holder Type

- Native type: Classify
- Configured options, in UI order: `Founder`, `Current employee`, `Former employee`, `Director or officer`, `Consultant or advisor`, `Institutional investor`, `Individual investor`, `Lender`, `Commercial counterparty`, `Entity, relationship not stated`, `Unable to determine`
- Upstream: `@Holder`
- Downstream: none
- Purpose: filter the grid by the population each holder belongs to, which drives
  the consent strategy, the 280G analysis, and the employment cross-check.

```markdown
## Established result

- Holder: @Holder

Use this to identify the holder being classified. Determine the relationship from the documents in the current unit.

## Task

Classify the holder's stated relationship to the issuer. Choose exactly one configured option.

## Classification rules

- Classify on what the documents in this unit state about the relationship. Do not infer a relationship from a name, a domain, or general knowledge.
- `Founder`: the documents describe the holder as a founder, or the instrument is an early common or restricted stock issuance at nominal price with a founder-style vesting schedule.
- `Current employee`: the documents describe an employment relationship with no termination recorded.
- `Former employee`: the documents record a termination of employment, or the instrument is a post-termination exercise or a separation-related award.
- `Director or officer`: the documents describe the holder as a director, manager, or officer. Where the holder is both an officer and an employee, use this option, because it is the population the 280G and D&O analyses need.
- `Consultant or advisor`: services are described as consulting or advisory rather than employment.
- `Institutional investor`: an entity holding for investment, such as a fund, a corporate investor, or a strategic investor.
- `Lender`: the holder is a lender or noteholder, or the instrument was issued in connection with a debt facility.
- `Commercial counterparty`: the instrument was issued in connection with a commercial agreement rather than services or investment.
- `Entity, relationship not stated`: the holder is an entity and the documents state no relationship.

## Fallback rules

- Use `Unable to determine` where the holder is an individual and the documents state no relationship, or where stated relationships conflict.
- Do not use `Individual investor` as a default for an unidentified individual. Use `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 6. Execution Status

- Native type: Classify
- Configured options, in UI order: `Fully executed`, `Issuer signed only`, `Holder signed only`, `Unsigned`, `Form or template`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Board Approval Referenced`
- Purpose: state what the instrument visibly proves about its own completion. **An
  unsigned grant agreement for an option on the cap table is a defect**, and it is
  common.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks in the current unit.

## Task

Classify the visible execution status of the instrument in this review unit. Choose exactly one configured option.

## Scope

- Evaluate the instrument itself and any amendment to it. Where they differ, classify on the least complete.
- Exclude the execution status of a board consent in the unit; whether the consent was signed is reported in Board Approval Referenced.
- Exclude notary, witness, and spousal-consent blocks from the party count. Where a spousal consent block is provided and unsigned, report it in Board Approval Referenced rather than here.
- Evaluate only signature blocks, electronic-signature markers, and conformed signatures visible in the documents.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the document is an unpopulated form, containing bracketed placeholders, a blank holder name, or blank quantity or price fields.
2. `Unsigned`: the document provides signature blocks and none bears a signature marker.
3. `Issuer signed only`: the issuer's block bears a signature marker and the holder's does not.
4. `Holder signed only`: the holder's block bears a signature marker and the issuer's does not.
5. `Fully executed`: every signature block the document provides bears a signature marker.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated grant date is not a signature marker.

Where the instrument provides no signature block at all — as some warrants issued by the company alone do — classify as `Fully executed` if the issuer has signed, and `Unsigned` if not.

## Fallback rules

- Use `Unable to determine` where a signature is present but illegible, where a signature page is referenced but missing, or where documents in the unit conflict about execution.
- Do not treat a stated grant date, a `duly authorized` recital, or a cap table listing the instrument as evidence that signatures were completed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 7. Class or Series

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the exact class or series designation, which must match the authorized
  classes in the charter for the instrument to be validly issued.

```markdown
## Task

State the class or series of units the instrument relates to.

## Rules

- Report the designation exactly as printed, for example `Series A Preferred Stock`, `Class B Common Stock`, `Series Seed-1 Preferred Stock`, `Class A Units`.
- For an option, warrant, restricted stock unit, or convertible instrument, report the class the instrument is exercisable for, settles into, or converts into.
- Where a convertible instrument converts into a class to be created in a future financing, report the class as described, for example `preferred stock to be issued in a Qualified Financing`.
- Where the instrument relates to more than one class, list each.
- Do not abbreviate, expand, or normalize the designation. `Series A` and `Series A-1` are different classes and the difference matters.

## Fallback rules

- Return `Not addressed` where the instrument states no class or series designation.
- Return `Not applicable` where the instrument confers no right to units, such as a cash-settled appreciation right.
- Return `Incorporated terms` where the class is stated to be determined under a document not present in the unit.
- Return `Unable to determine` where the designation is illegible, or where documents in the unit conflict.

## Output format

`[Exact designation]` per line. Return no more than 4 lines and no more than 30 words.
```

---

### 8. Quantity and Unit

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: how much of what the instrument covers, reported exactly as stated so a
  reviewer can reconcile it against the certified cap table.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the quantity the instrument covers, and the unit that quantity is expressed in.

## Rules by instrument type

- `Common stock`, `Preferred stock`, `Restricted stock`, `LLC unit or membership interest`: the number of units issued.
- `Stock option`, `Warrant`, `Restricted stock unit`, `Stock appreciation right or phantom`: the number of units the instrument covers, is exercisable for, or settles into.
- `SAFE`, `Convertible note`: the principal or purchase amount, expressed as currency. State the currency.
- `Profits interest`: the number of units or the percentage interest as stated.

## Rules

- Report the figure exactly as printed, with the unit or currency.
- **Do not calculate.** Do not convert a percentage into a unit count or a unit count into a percentage. Do not total anything. Do not adjust for a stock split, recapitalization, or conversion ratio, even where the documents state the ratio. Report the figure as stated and let the reviewer adjust.
- Where an amendment in the unit changes the quantity, report the quantity in the most recently dated document that addresses it and append ` (amended from [figure], [YYYY-MM-DD])`.
- Where a cancellation or partial repurchase is recorded in the unit, report the original quantity and append ` ([quantity] cancelled [YYYY-MM-DD])`. Do not net them.
- Where the instrument states both a number of units and a percentage, report both as printed.

## Fallback rules

- Return `Not stated` where no quantity or amount is stated.
- Return `Incorporated terms` where the quantity is stated to be set by a grant notice, schedule, or plan not present in the unit.
- Return `Unable to determine` where figures in the unit conflict, or are illegible.

## Output format

`[Figure] [unit or currency]`, with any qualifier appended as described above. Return no more than 35 words. Do not include percentages you derived, totals, section numbers, or citation markers.
```

---

### 9. Grant or Issue Date

- Native type: Date — **confirm the type accepts `Not stated` and `Incorporated terms` before use**
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the date the instrument was granted or issued, which anchors vesting,
  the 409A valuation it should rely on, and the securities-law analysis.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Identify the date the instrument was granted or issued.

## Date-selection hierarchy

### Stock option, restricted stock unit, restricted stock, stock appreciation right or phantom, profits interest

1. Use the grant date the document states for itself.
2. If none is stated, use the date of board approval recorded in the unit.
3. If neither is available, use the date of the last party signature.

### Common stock, preferred stock, LLC unit or membership interest, warrant

1. Use the issue date the document states for itself.
2. If none is stated, use the date of the last party signature.

### SAFE, convertible note

1. Use the date the instrument states for itself.
2. If none is stated, use the date of the last party signature.

## Excluded dates

- The vesting commencement date, which is a separate column and frequently differs
- The date of the equity plan, or of a board consent adopting the plan rather than approving this grant
- The exercise, conversion, or settlement date
- The date of the 409A valuation relied on
- File name and metadata dates, and notarization, transmittal, and scan dates

## Rules

- A stated grant date is reported even where it precedes the signature dates, and even where it equals another date in the row. A value the document states is never replaced by a fallback state.
- Where the stated grant date precedes the board approval date recorded in the unit, report the stated grant date. The discrepancy is a finding and the reviewer will see both cells.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy, or `Incorporated terms` where the date is stated to be set by a grant notice not present in the unit.
```

---

### 10. Price Terms

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: what the holder paid or must pay, which drives the option-pricing
  analysis, the transaction proceeds per instrument, and the 409A cross-check.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the price terms of the instrument.

## Rules by instrument type

- `Stock option`, `Warrant`: the exercise or strike price per unit, and the aggregate exercise price where stated.
- `Common stock`, `Preferred stock`, `Restricted stock`, `LLC unit or membership interest`: the purchase price per unit and the aggregate consideration, including any non-cash consideration described.
- `Restricted stock unit`, `Stock appreciation right or phantom`: any purchase price or base price. Most have none; see the fallback rules.
- `SAFE`, `Convertible note`: return `Not applicable` — the valuation cap, discount, and conversion price belong to Conversion Mechanics.
- `Profits interest`: any capital contribution and the threshold or hurdle amount as stated.

## Rules

- Report the price exactly as printed, with the currency.
- Report non-cash consideration as described, for example `services rendered`, `cancellation of indebtedness`, `contribution of assets`, in six words or fewer.
- Report a nominal or par-value price as printed rather than describing it as nominal.
- **Do not calculate.** Do not multiply a per-unit price by the quantity to derive an aggregate, and do not compare the price to any valuation.
- Where an amendment repriced the instrument, report the current price and append ` (repriced from [price], [YYYY-MM-DD])`. A repricing is a finding in its own right.

## Fallback rules

- Return `Not addressed` where the instrument states no price and none is required by its nature, as with most restricted stock units.
- Return `Not stated` where a price is required by the instrument's nature but no figure appears.
- Return `Incorporated terms` where the price is stated to be set by a grant notice, schedule, or plan not present in the unit.
- Return `Unable to determine` where figures in the unit conflict, or are illegible.

## Output format

`[Price] per unit[; aggregate [amount]]`, with any qualifier appended as described above. Return no more than 35 words.
```

---

### 11. Expiration or Maturity

- Native type: Date — **confirm the type accepts `Not applicable` and `Incorporated terms` before use**
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the outside date by which the instrument must be exercised, converted,
  or repaid. An option expiring during the deal, or a note maturing before closing,
  is a timetable item.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Identify the date on which the instrument expires, matures, or terminates by its own terms.

## Rules by instrument type

- `Stock option`, `Warrant`: the expiration date of the exercise period.
- `Convertible note`: the maturity date.
- `Restricted stock unit`, `Stock appreciation right or phantom`: any outside settlement or expiration date.
- `SAFE`: return `Not applicable` unless the instrument states an expiration or termination date, which most do not.
- `Common stock`, `Preferred stock`, `Restricted stock`, `LLC unit or membership interest`, `Profits interest`: return `Not applicable`. Issued units do not expire.

## Rules

- Report the date as stated. Where the instrument states a term rather than a date — for example ten years from the grant date — report the resulting date only if the document itself states it; otherwise return `Not stated` and let the reviewer derive it. Do not calculate a date from a term.
- Do not report the post-termination exercise deadline, which is a separate column and is usually much earlier.
- Where an amendment extends or shortens the date, report the date in the most recently dated document that addresses it.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where it falls before that date, report it and append ` [expired on record]`.

## Fallback rules

- Return `Not stated` where the instrument's nature requires an outside date but none is stated and none can be reported without calculating.
- Return `Incorporated terms` where the term is stated to be set by a plan not present in the unit.
- Return `Unable to determine` where dates in the unit conflict, or are illegible.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 12. Vesting Commencement Date

- Native type: Date — **confirm the type accepts `Not applicable` and `Incorporated terms` before use**
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the date vesting runs from, which is frequently earlier than the grant
  date — commonly the holder's start date. **The gap between the two is where
  vesting errors and 409A problems live.**

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Identify the date from which vesting is measured.

## Applicability

- Applies to `Stock option`, `Restricted stock`, `Restricted stock unit`, `Stock appreciation right or phantom`, and `Profits interest`.
- For `Common stock`, `Preferred stock`, `LLC unit or membership interest`, `Warrant`, `SAFE`, and `Convertible note`, return `Not applicable` unless the instrument states a vesting schedule, in which case report the commencement date.

## Rules

- Report the vesting commencement date the document states, however it is labelled — vesting start date, vesting commencement date, or service inception date.
- Report it even where it equals the grant date. A value the document states is never replaced by a fallback state, and two columns agreeing is information.
- Where the commencement date precedes the grant date, report it as stated. That is common for grants backdated to a start date, and the reviewer needs to see it.
- Do not report the grant date, the employment start date recited as background, or the date of the first vesting instalment, unless the document identifies it as the vesting commencement date.

## Fallback rules

- Return `Not applicable` where the instrument states no vesting schedule and its type does not carry one.
- Return `Not stated` where the instrument states a vesting schedule but no commencement date.
- Return `Incorporated terms` where the commencement date is stated to be set by a grant notice, schedule, or plan not present in the unit.
- Return `Unable to determine` where dates in the unit conflict, or are illegible.

## Output format

`YYYY-MM-DD`, or one of the exact fallback values above. Preserve partial precision as printed.
```

---

### 13. Vesting Schedule

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: `Vested Amount as Stated`
- Purpose: the vesting terms exactly as written, which the reviewer uses to compute
  vested amounts outside the table.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the vesting or forfeiture schedule the instrument states.

## Applicability

- Applies to `Stock option`, `Restricted stock`, `Restricted stock unit`, `Stock appreciation right or phantom`, and `Profits interest`.
- For other instrument types, report a vesting schedule only where the instrument states one, and otherwise return `Not applicable`.

## Rules

- Report the schedule as written: the total vesting period, the cliff, the instalment frequency, and the proportion vesting at each point.
- Report performance or milestone conditions as stated, in eight words or fewer per condition.
- Report any provision for vesting to continue, pause, or terminate on a leave of absence or a change in service status.
- Where the instrument is stated to be fully vested at grant, return `Fully vested at grant`.
- **Do not calculate.** Do not state how much has vested, do not convert the schedule into unit counts, and do not apply the schedule to any date.
- Where an amendment changes the schedule, report the schedule in the most recently dated document that addresses it and append ` (amended [YYYY-MM-DD])`.

## Fallback rules

- Return `Not applicable` where the instrument type carries no vesting and none is stated.
- Return `Not addressed` where the instrument type would normally carry vesting and the document states none.
- Return `Incorporated terms — schedule set out in [document name as referenced]` where vesting is stated to be governed by a grant notice, schedule, or plan not present in the unit. **This is the expected answer for many grant agreements** and it is not a defect in the instrument.
- Return `Unable to determine` where schedules in the unit conflict, or are illegible.

## Output format

`[Total period]; cliff: [period or "none"]; instalments: [frequency and proportion]; conditions: [brief or "none stated"]`

Return no more than 70 words. Do not include vested amounts, calculated figures, section numbers, or citation markers.
```

---

### 14. Vested Amount as Stated

- Native type: Free Response
- Upstream: `@Vesting Schedule`
- Downstream: none
- Purpose: capture a vested figure **only where a document asserts one**, with the
  date it speaks as of.

**This column exists to hold a line.** A vested amount is the single most tempting
figure to derive, and a derived figure looks identical to a stated one in an export.
Everything here is reported as asserted, and the reviewer computes vesting in Excel
from the schedule and the commencement date.

```markdown
## Established result

- Vesting schedule: @Vesting Schedule

## Task

If Vesting Schedule reported a schedule, or returned `Incorporated terms`, report any vested, unvested, or exercisable amount that a document in this review unit expressly states, together with the date that statement speaks as of.

If Vesting Schedule returned `Fully vested at grant`, return `Fully vested at grant per instrument`.

If Vesting Schedule returned `Not applicable`, return exactly `Not applicable`.

If Vesting Schedule returned `Not addressed` or `Unable to determine`, return exactly `Not stated`.

## Rules

- **Do not calculate anything.** Do not apply the vesting schedule to the vesting commencement date, to the diligence as-of date, or to any other date. Do not derive an unvested amount by subtraction. Do not interpolate between instalments. If a document does not state a figure, the answer is `Not stated`.
- Report only figures a document in the unit expressly asserts, such as an exercise notice reciting the vested amount, an amendment reciting the position, or a statement of account included in the unit.
- Give the figure, what it describes, and the date the document states it as of.
- Where more than one document states a figure, report the most recently dated and append ` (also stated as [figure] at [YYYY-MM-DD])`.
- Where a figure is stated with no as-of date, report it and append ` (no as-of date stated)`. A vested figure without a date is nearly useless and the reviewer should see that.

## Fallback rules

- Return `Not stated` where no document in the unit asserts a vested, unvested, or exercisable figure. **This is the expected answer for most rows** and it is not a gap in the extraction.

## Output format

`[Figure] [vested | unvested | exercisable] as of [YYYY-MM-DD]`, with any qualifier appended, or one of the exact fallback values above.

Return no more than 35 words. Do not include any figure you derived.
```

---

### 15. Post-Termination Exercise Period

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: how long a departing holder has to exercise. A short window means
  options quietly expire; a long one means the buyer inherits a larger overhang
  than the cap table suggests.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the period within which the instrument may be exercised or settled after the holder's service ends, and any variation by reason for termination.

## Applicability

- Applies to `Stock option`, `Restricted stock unit`, `Stock appreciation right or phantom`, and `Profits interest`.
- For `Warrant`, apply only where the warrant is tied to service. Otherwise return `Not applicable`.
- For all other instrument types, return `Not applicable`.

## Rules

- Report the general period, and then any different period stated for termination without cause, resignation with or without good reason, termination for cause, death, disability, or retirement.
- Report where the instrument states that the award terminates immediately on termination for cause, since that is a common and consequential term.
- Report the period as stated. Do not calculate a resulting date.
- Where the period is stated to run from a date other than the termination date, say which date.
- Do not report the instrument's outside expiration date, which is a separate column, except where the instrument states that the post-termination period cannot extend beyond it.

## Fallback rules

- Return `Not applicable` where the instrument type carries no exercise period.
- Return `Not addressed` where the instrument type carries one and the document states none.
- Return `Incorporated terms — set out in [document name as referenced]` where the period is stated to be governed by a plan not present in the unit.
- Return `Unable to determine` where periods in the unit conflict, or are illegible.

## Output format

`General: [period]; cause: [period or "immediate forfeiture"]; death or disability: [period]; other variations: [brief or "none stated"]`

Return no more than 60 words. Do not include calculated dates, section numbers, or citation markers.
```

---

### 16. Repurchase or Forfeiture on Termination

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: whether the issuer can buy units back or forfeit them when service
  ends, which determines whether the holder appears on the closing payments list at
  all.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report any right of the issuer or another party to repurchase, redeem, or forfeit the units on termination of the holder's service or on another stated event.

## Applicability

- Applies to `Restricted stock`, `Common stock`, `LLC unit or membership interest`, and `Profits interest`, where the instrument was issued in connection with services.
- For `Stock option`, `Restricted stock unit`, and `Stock appreciation right or phantom`, report any forfeiture of unvested amounts and any right to repurchase units acquired on exercise or settlement.
- For `Preferred stock`, `Warrant`, `SAFE`, and `Convertible note`, return `Not applicable` unless a service-related repurchase or forfeiture right is stated.

## Rules

- State who holds the right, what it applies to — unvested units, all units, or units acquired on exercise — and the price payable.
- Distinguish repurchase at cost from repurchase at fair market value, since the difference decides whether the holder receives value at closing.
- Report whether the price or the applicability differs for termination for cause, and report any lapse or expiry of the right.
- Report any period within which the right must be exercised.
- Do not report a right of first refusal on a voluntary transfer; that belongs to Transfer Restrictions.
- Do not state whether the right survives or is triggered by this transaction.

## Fallback rules

- Return `Not applicable` where the instrument type carries no such right and none is stated.
- Return `Not addressed` where the instrument type would normally carry one and the document states none.
- Return `Incorporated terms — set out in [document name as referenced]` where the right is stated to sit in a plan or agreement not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Holder of right: [who]; applies to: [what]; price: [basis]; cause variation: [brief or "none stated"]; window: [period or "none stated"]`

Return no more than 70 words. Do not include quotations, section numbers, or citation markers.
```

---

### 17. Early Exercise and 83(b) Election

- Native type: Classify
- Configured options, in UI order: `Early exercise permitted`, `Early exercise not permitted`, `Election referenced as filed`, `Election referenced, filing not evidenced`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: flag the population where an unfiled or late election creates a tax
  exposure the buyer may inherit, and where early-exercised units sit on the cap
  table as issued shares rather than as options.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Classify what this review unit shows about early exercise and any Section 83(b) election. Choose exactly one configured option.

## Applicability

- Applies to `Stock option`, `Restricted stock`, and `Profits interest`.
- For all other instrument types, return `Not applicable`.

## Classification rules

Apply the first rule that fits.

1. `Election referenced as filed`: a document in the unit is a completed election, or states that an election was filed, and gives a filing date or attaches filing evidence.
2. `Election referenced, filing not evidenced`: a document refers to an election — including an unexecuted election form attached as an exhibit — without evidence that it was filed. **This is a finding**, because the election is only effective if filed within the statutory window.
3. `Early exercise permitted`: the instrument permits exercise before vesting, with unvested units subject to repurchase, and no election is referenced.
4. `Early exercise not permitted`: the instrument expressly limits exercise to vested units.

Where the instrument is `Restricted stock` or `Profits interest`, the election question arises from the issuance itself rather than from early exercise, so use rules 1 and 2 and otherwise `Not addressed`.

## Fallback rules

- Use `Not addressed` where the instrument type is in scope and the documents address neither early exercise nor an election.
- Use `Unable to determine` where an election form is present but illegible or incomplete in a way that prevents telling whether it was filed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 18. Conversion Mechanics

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: how a convertible instrument turns into equity, and on what terms. These
  are the instruments most likely to convert at closing, and the terms drive the
  price allocation.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the conversion terms of the instrument.

## Applicability

- Applies to `SAFE`, `Convertible note`, and `Preferred stock`.
- For `Warrant`, report any provision converting the warrant into units other than by exercise at the stated price, and otherwise return `Not applicable`.
- For all other instrument types, return `Not applicable`.

## Include where expressly stated

- Valuation cap, and whether it is pre-money or post-money
- Discount rate to the price of the qualifying round
- Conversion price or ratio, and any stated adjustment mechanism
- The conversion triggers: a qualifying financing and its threshold amount, a change of control or liquidity event, maturity, and any holder election
- **Treatment on a change of control specifically**: whether the holder receives the greater of a conversion or a cash payment, a stated multiple of principal, or converts at the cap
- Interest rate and whether interest converts or is paid, for a convertible note
- Maturity date behaviour: automatic conversion, repayment, or holder election
- Most favoured nation provisions
- Any pro rata or participation right on a future round

## Rules

- Report each element as stated, using the document's own figures.
- **Do not calculate.** Do not compute a conversion price from a cap and a share count, do not accrue interest, and do not model the number of units the instrument would convert into.
- Where an amendment changes any term, report the term in the most recently dated document that addresses it.
- Report the change-of-control treatment even where it duplicates part of the general conversion terms. It is the element the transaction turns on.

## Fallback rules

- Return `Not applicable` where the instrument type is not convertible.
- Return `Not addressed` for an individual element the document does not state; do not omit it silently.
- Return `Incorporated terms` where conversion terms are stated to sit in a document not present in the unit.
- Return `Unable to determine` where terms in the unit conflict, or are illegible.

## Output format

`Cap: [amount and basis]; discount: [rate]; triggers: [list]; CoC treatment: [as stated]; interest: [rate and treatment]; maturity: [date and behaviour]; MFN: [yes or "none stated"]`

Return no more than 110 words. Use `Not addressed` for any element the document does not state. Do not include calculated figures, quotations, section numbers, or citation markers.
```

---

### 19. Liquidation Preference

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: what the holder receives before common holders on a sale, which is the
  first input to the distribution waterfall.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the liquidation preference the instrument carries.

## Applicability

- Applies to `Preferred stock` and to `LLC unit or membership interest` where the instrument states a preference.
- For `SAFE` and `Convertible note`, report any liquidation or change-of-control payment stated for the instrument as unconverted, and otherwise return `Not applicable`.
- For all other instrument types, return `Not applicable`.

## Include where expressly stated

- The preference amount, as a multiple of the original issue price or as a stated amount per unit
- Whether accrued and unpaid dividends are added to the preference
- The seniority or ranking of this class relative to other classes, as stated
- The definition of the events triggering the preference, including whether a change of control or merger is a deemed liquidation
- Any cap on the total amount payable

## Rules

- Report the preference as stated, for example `1x original issue price plus accrued dividends`.
- Report the ranking exactly as the document expresses it, for example `pari passu with Series A`, `senior to all Common Stock`. Ranking language is where preferred stacks go wrong.
- **Do not calculate.** Do not compute the aggregate preference, and do not model the waterfall.
- Do not report participation rights here; those are a separate column.
- Do not state what the holder would receive in this transaction.

## Fallback rules

- Return `Not applicable` where the instrument type carries no preference.
- Return `Not addressed` where the instrument type would normally carry one and the document states none.
- Return `Incorporated terms` where the preference is stated to be set out in a charter or agreement not present in the unit. **This is a common answer for a stock purchase agreement**, since the preference usually lives in the charter.
- Return `Unable to determine` where terms in the unit conflict, or are illegible.

## Output format

`[Multiple or amount][; plus accrued dividends]; ranking: [as stated]; deemed liquidation: [as stated or "Not addressed"]; cap: [amount or "none stated"]`

Return no more than 70 words. Do not include calculated figures, quotations, section numbers, or citation markers.
```

---

### 20. Participation Rights

- Native type: Classify
- Configured options, in UI order: `Non-participating`, `Fully participating`, `Participating subject to cap`, `Not addressed`, `Not applicable`, `Incorporated terms`, `Unable to determine`
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: whether the holder takes its preference **and** shares in the remainder,
  which changes the distribution to common holders more than almost any other term.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Classify whether the instrument participates with common holders in proceeds remaining after its liquidation preference is paid. Choose exactly one configured option.

## Applicability

- Applies to `Preferred stock` and to `LLC unit or membership interest` where the instrument states a preference.
- For all other instrument types, return `Not applicable`.

## Classification rules

- `Non-participating`: the holder receives the greater of its preference or its as-converted share, but not both. This is the most common structure and the one to expect.
- `Fully participating`: the holder receives its preference **and** shares in the remaining proceeds on an as-converted basis, without limit.
- `Participating subject to cap`: the holder participates until total proceeds reach a stated multiple or amount, after which participation stops or the holder converts.

Classify on the operative distribution mechanics, not on whether the document uses the word "participating". Language giving the holder the greater of two outcomes is `Non-participating`. Language giving the holder its preference and then a share of the balance is participating.

## Fallback rules

- Use `Not addressed` where the instrument states a preference but says nothing about the treatment of remaining proceeds.
- Use `Incorporated terms` where participation is stated to be set out in a charter or agreement not present in the unit.
- Use `Unable to determine` where the mechanics are stated but cannot be reliably read, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 21. Anti-Dilution Protection

- Native type: Classify
- Configured options, in UI order: `Broad-based weighted average`, `Narrow-based weighted average`, `Full ratchet`, `Adjustment for splits and recapitalizations only`, `Not addressed`, `Not applicable`, `Incorporated terms`, `Unable to determine`
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the protection against a lower-priced issuance, which matters wherever
  the transaction involves a new issuance or a down-round recapitalization.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Classify the anti-dilution protection the instrument carries against a subsequent issuance at a lower price. Choose exactly one configured option.

## Applicability

- Applies to `Preferred stock`, `Warrant`, `Convertible note`, and `SAFE`.
- For `LLC unit or membership interest`, apply where the instrument states a conversion price subject to adjustment.
- For all other instrument types, return `Not applicable`.

## Classification rules

- `Full ratchet`: the conversion price adjusts down to the price of the lower-priced issuance, regardless of size.
- `Broad-based weighted average`: a weighted-average adjustment whose denominator includes options, warrants, and other convertible securities as well as outstanding units.
- `Narrow-based weighted average`: a weighted-average adjustment whose denominator is limited to outstanding units, or to the units of the protected class.
- `Adjustment for splits and recapitalizations only`: the instrument adjusts for splits, combinations, dividends, and recapitalizations, but provides no price-based protection. **This is a distinct answer from silence** and it is the most common outcome for warrants.

Where the formula is stated but the document does not name it, classify on the denominator. Where the denominator cannot be identified, use `Unable to determine`.

Do not classify a pay-to-play or shadow-preferred provision as an anti-dilution formula; report it in the evidence field only.

## Fallback rules

- Use `Not addressed` where the instrument addresses neither price adjustment nor structural adjustment.
- Use `Incorporated terms` where the adjustment is stated to be set out in a charter or agreement not present in the unit.
- Use `Unable to determine` where the formula is illegible or incomplete, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 22. Dividend Rights

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: whether a dividend accrues, since accrued and unpaid dividends increase
  the amount payable at closing and are routinely missed.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the dividend or distribution rights the instrument carries.

## Applicability

- Applies to `Preferred stock`, `Common stock`, and `LLC unit or membership interest`.
- For `Restricted stock`, report any provision about dividends on unvested units.
- For `Restricted stock unit`, report any dividend equivalent right.
- For all other instrument types, return `Not applicable` unless a dividend or distribution right is stated.

## Include where expressly stated

- The rate, as a percentage of the original issue price or a stated amount per unit
- **Whether dividends are cumulative or non-cumulative**, which is the element that determines whether an unpaid amount builds up
- Whether dividends accrue automatically or only when declared
- Whether accrued dividends are payable on a liquidation or deemed liquidation, or are added to the liquidation preference
- Any preference or priority over other classes
- For a limited liability company, any mandatory tax distribution

## Rules

- Report each element as stated.
- **Do not calculate.** Do not compute accrued dividends to any date.
- Report whether any dividend has in fact been declared or paid only where a document in the unit states it.
- Do not state what would be payable in this transaction.

## Fallback rules

- Return `Not applicable` where the instrument type carries no dividend right.
- Return `Not addressed` where the instrument type would normally carry one and the document states none.
- Return `Incorporated terms` where dividend rights are stated to be set out in a charter or agreement not present in the unit.
- Return `Unable to determine` where terms in the unit conflict, or are illegible.

## Output format

`Rate: [as stated]; [cumulative | non-cumulative]; accrual: [automatic | when declared]; on liquidation: [treatment]; priority: [as stated or "none stated"]`

Return no more than 65 words. Do not include calculated amounts, section numbers, or citation markers.
```

---

### 23. Redemption Rights

- Native type: Classify
- Configured options, in UI order: `Holder may require redemption`, `Issuer may redeem at its option`, `Mandatory redemption on a stated date or event`, `Both holder and issuer rights`, `Not addressed`, `Not applicable`, `Incorporated terms`, `Unable to determine`
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: a redeemable instrument behaves like debt in the price model and can
  create a payment obligation independent of the transaction.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Classify any right or obligation to redeem or repurchase the instrument, other than a service-related repurchase. Choose exactly one configured option.

## Applicability

- Applies to `Preferred stock`, `LLC unit or membership interest`, `Warrant`, and `Convertible note`.
- For all other instrument types, return `Not applicable`.

## Scope

- Include put rights held by the holder, call rights held by the issuer, and mandatory redemption on a stated date or on a stated event.
- **Exclude repurchase or forfeiture on termination of service**, which is a separate column. That is a service condition, not a redemption feature.
- Exclude a right of first refusal on a voluntary transfer.
- Exclude repayment of a convertible note at maturity where the instrument treats it as repayment of debt rather than redemption; that belongs to Conversion Mechanics.

## Classification rules

- `Holder may require redemption`: the holder can compel the issuer to buy the instrument back. This is the option that makes the instrument debt-like.
- `Mandatory redemption on a stated date or event`: redemption occurs without either party electing.
- `Both holder and issuer rights`: both a put and a call are stated.

## Fallback rules

- Use `Not addressed` where the instrument type is in scope and the documents state no redemption right.
- Use `Incorporated terms` where redemption rights are stated to be set out in a charter or agreement not present in the unit.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. Acceleration on Change of Control

- Native type: Classify
- Configured options, in UI order: `Single trigger`, `Double trigger`, `Partial acceleration`, `Discretionary acceleration`, `No acceleration`, `Not addressed`, `Not applicable`, `Incorporated terms`, `Unable to determine`
- Upstream: `@Instrument Type`
- Downstream: `Acceleration Language`
- Purpose: whether the transaction itself accelerates vesting. **Aggregated across
  rows, this column is the transaction payments schedule** and it feeds the 280G
  analysis.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Classify how the instrument's vesting is affected by a change of control of the issuer. Choose exactly one configured option.

## Applicability

- Applies to `Stock option`, `Restricted stock`, `Restricted stock unit`, `Stock appreciation right or phantom`, and `Profits interest`.
- For `Warrant`, apply where the warrant is subject to vesting.
- For instruments carrying no vesting, return `Not applicable`.

## Classification rules

Apply the first rule that fits.

1. `Single trigger`: vesting accelerates on the change of control itself, with no further condition.
2. `Double trigger`: vesting accelerates only if the change of control is followed by a qualifying termination of the holder's service, whether within a stated window or at any time.
3. `Partial acceleration`: a stated proportion or number of units accelerates, or vesting accelerates by a stated period such as twelve months, rather than in full. Use this whether the trigger is single or double, and state which in the Language column.
4. `Discretionary acceleration`: acceleration depends on a decision of the board, the plan administrator, or the acquirer, including a provision that awards accelerate only if not assumed or substituted by the acquirer.
5. `No acceleration`: the instrument addresses a change of control and expressly provides that vesting does not accelerate.

A provision that awards accelerate **unless** the acquirer assumes or substitutes them is `Discretionary acceleration`, because the outcome turns on the acquirer's election rather than on the transaction.

Classify on the operative mechanics, not on whether the document uses the words single or double trigger.

## Fallback rules

- Use `Not addressed` where the instrument carries vesting and the documents say nothing about a change of control.
- Use `Incorporated terms` where acceleration is stated to be governed by a plan or agreement not present in the unit. **This is the expected answer for many grant agreements**, and the plan must then be reviewed for this term.
- Use `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 25. Acceleration Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Acceleration on Change of Control`
- Downstream: none
- Purpose: the exact text. Acceleration drives a payment, so a partner reads the
  words before the number goes into the price model.

```markdown
## Established result

- Acceleration on change of control: @Acceleration on Change of Control

## Task

If Acceleration on Change of Control is `Single trigger`, `Double trigger`, `Partial acceleration`, `Discretionary acceleration`, or `No acceleration`, quote the acceleration provision exactly as written.

If it is `Not addressed`, `Not applicable`, or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever acceleration language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the trigger, the proportion accelerating, and any qualifying-termination condition, together with the definitions of `Change of Control`, `Cause`, and `Good Reason` that the provision relies on where those definitions appear in the unit. **The good reason definition is what makes a double trigger operative** and it is frequently the reason an acceleration does or does not fire.
- Where the combined text exceeds 250 words, quote the operative provision in full and the parts of each definition stating the trigger and the qualifying conditions, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction would accelerate the award.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 26. Holder Consent or Veto Right

- Native type: Free Response
- Upstream: none
- Downstream: `Consent Right Language`
- Purpose: any right this holder has to approve or block the transaction.
  **Aggregated, this column produces the list of holders whose signature the deal
  needs**, which is the closing checklist item with the longest lead time.

```markdown
## Task

Report any right the instrument gives the holder to consent to, approve, veto, or block a merger, sale of the entity, sale of substantially all assets, liquidation, recapitalization, charter amendment, or new issuance.

## Scope

- Include class or series voting rights, protective provisions conferred on this holder or class, and contractual consent rights stated in the instrument.
- Include a right conferred on the holder in its capacity as a member of a voting group, where the instrument states it.
- Include a right to appoint a director or manager, since board consent then depends on this holder.
- Include an information or inspection right only where the instrument makes it a condition of a transaction.
- Exclude ordinary voting rights on units, meaning one vote per unit voting with the common, unless the instrument confers a separate class vote.
- Exclude preemptive and participation rights over new issuances, which are separate concepts reported elsewhere in the corporate schema.
- Exclude anti-dilution adjustments.

## Response labels

Begin with exactly one of:

- `Consent right`
- `Class vote`
- `Board appointment right`
- `Not addressed`
- `Incorporated terms`
- `Unable to determine`

## Rules

- State each right, the matters it covers, and the threshold required where the right is exercisable by a class rather than by this holder alone.
- Where the right is held by a class, report the threshold as stated, for example `holders of a majority of the Series A voting as a separate class`. A holder with a small position in a class that votes together does not hold an individual veto, and the reviewer needs to see the difference.
- Consolidate substantially similar matters. Report no more than six.
- Do not state whether this transaction requires the consent, and do not state whether it has been obtained or is achievable.

## Fallback rules

- Return exactly `Not addressed` where the instrument confers no such right.
- Return `Incorporated terms — rights set out in [document name as referenced]` where consent rights are stated to sit in a charter, stockholders agreement, or investor rights agreement not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`[Response label] — matters: [list]; exercisable by: [this holder | class and threshold]`

Return no more than 70 words. Do not include quotations, section numbers, or citation markers.
```

---

### 27. Consent Right Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Holder Consent or Veto Right`
- Downstream: none
- Purpose: the exact text, which is what the consent or waiver is drafted against.

```markdown
## Established result

- Holder consent or veto right: @Holder Consent or Veto Right

## Task

If Holder Consent or Veto Right identified a `Consent right`, `Class vote`, or `Board appointment right`, quote the operative provision exactly as written.

If it returned `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If it returned `Unable to determine`, quote whatever consent language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the lead-in identifying whose consent is required and the threshold, together with the enumerated matters. Prioritize the matters bearing on a sale of the entity.
- Where the enumeration exceeds 200 words, quote the lead-in and the matters bearing on a sale, replacing intervening items with `[...]`.
- Do not add analysis, and do not indicate whether this transaction triggers the right.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 28. Transfer Restrictions

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the restrictions on the holder transferring the instrument, which set
  the mechanics for delivering it at closing.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report the restrictions the instrument imposes on the holder transferring it.

## Scope

- Include prohibitions on transfer, consent requirements, rights of first refusal and first offer, market stand-off and lock-up provisions, and permitted-transferee carve-outs.
- Include any requirement that a transferee accede to a stockholders or similar agreement.
- Exclude repurchase and forfeiture on termination of service, which is a separate column.
- Exclude drag-along and tag-along obligations, which are reported in Voting or Support Obligation.
- Exclude a securities-law legend that restates statutory restrictions without adding a contractual one.

## Rules

- State each restriction, who holds any right arising under it, and any notice or exercise period.
- Report the permitted transferees the instrument exempts, in six words or fewer.
- For an unvested instrument, report separately where the restriction differs for vested and unvested amounts.
- Where the instrument states that it is non-transferable other than by will or intestacy — the standard position for an option — report that, since it determines that the holder must exercise rather than transfer.
- Do not state whether any restriction applies to this transaction or whether a waiver has been obtained.

## Fallback rules

- Return `Not addressed` where the instrument imposes no transfer restriction.
- Return `Incorporated terms — restrictions set out in [document name as referenced]` where transfer restrictions are stated to sit in a plan, charter, or stockholders agreement not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per restriction:

`[Restriction] — right holder: [who or "n/a"]; period: [as stated or "none stated"]; permitted transferees: [brief or "none stated"]`

Return no more than 4 lines and no more than 80 words. Do not include quotations, section numbers, or citation markers.
```

---

### 29. Voting or Support Obligation

- Native type: Classify
- Configured options, in UI order: `Drag-along obligation`, `Voting agreement obligation`, `Both drag-along and voting obligation`, `Tag-along right only`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether this holder is **contractually obliged to support the
  transaction**. This is the other side of the corporate drag-along, read from the
  holder's instrument, and it tells you which holders you do not have to persuade.

```markdown
## Task

Classify whether the instrument obliges the holder to vote for, consent to, or participate in a sale of the entity. Choose exactly one configured option.

## Scope

- Include drag-along and bring-along obligations, obligations to vote as directed or in accordance with a board or majority recommendation, proxies granted for that purpose, and obligations to execute transaction documents, give a release, or refrain from exercising appraisal or dissenters' rights.
- **Distinguish direction carefully.** A drag-along obliges the holder to sell. A tag-along entitles the holder to join a sale. Reporting one as the other inverts the finding, and the two frequently appear in the same clause.
- Exclude ordinary voting rights on units, which confer discretion rather than obligation.
- Exclude transfer restrictions and rights of first refusal.

## Classification rules

- `Drag-along obligation`: the holder can be compelled to sell or to participate in an approved sale.
- `Voting agreement obligation`: the holder is obliged to vote in a stated way, or has granted a proxy for that purpose, without being compellable to sell.
- `Tag-along right only`: the instrument confers a right to join a sale and imposes no obligation to support one. This is a right, not an obligation, and it does not help the transaction proceed.

## Fallback rules

- Use `Not addressed` where the instrument imposes no such obligation and confers no such right.
- Use `Incorporated terms` where the obligation is stated to sit in a stockholders, voting, or co-sale agreement not present in the unit. **This is a coverage finding**, and the agreement is reported in Referenced but Not Produced.
- Use `Unable to determine` where the provision is incomplete or illegible, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 30. Board Approval Referenced

- Native type: Free Response
- Upstream: `@Documents in Unit`, `@Execution Status`
- Downstream: none
- Purpose: whether the issuance was authorized, and whether the authorizing
  document was produced. **An instrument on the cap table with no producible board
  approval is the classic corporate housekeeping finding**, and it is what
  ratification at closing exists to fix.

```markdown
## Established results

- Documents in unit: @Documents in Unit
- Execution status: @Execution Status

Use the inventory to identify any consent or resolution in the unit. Use the execution status to describe what the approval evidence proves.

## Task

Report the board or owner approval authorizing this instrument, and whether the authorizing document is present in the review unit.

## Response labels

Begin with exactly one of:

- `Approval in unit`
- `Approval referenced, not produced`
- `No approval referenced`
- `Unable to determine`

## Rules

- Use `Approval in unit` where a consent or resolution present in the unit expressly authorizes this instrument or this grant. Give the document title, its date, the approving body, and whether it is signed.
- Use `Approval referenced, not produced` where the instrument recites that the grant was approved — for example by reference to a board consent, a resolution, or an approved grant date — and that document is not in the unit. Name it as referenced.
- Use `No approval referenced` where nothing in the unit refers to an authorizing approval.
- **Do not describe an unsigned consent as an approval.** Where a consent in the unit is unsigned, report it and state `unsigned` rather than describing the action as approved. An unsigned consent authorizes nothing.
- Where the approval in the unit covers a different instrument, holder, or quantity than this row, report it and append ` [does not match this instrument]`.
- Where the approval date falls after the grant date stated on the instrument, append ` [approval postdates grant]`.
- Do not state whether the approval was validly given, whether it was sufficient, or whether ratification is needed. Those are human columns.

## Output format

`[Response label] — [document title], [YYYY-MM-DD], [approving body], [signed | unsigned]` followed by any bracketed flags.

Return no more than 50 words. Do not include quotations, section numbers, or citation markers.
```

---

### 31. Plan or Governing Document Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: name the documents whose terms this instrument incorporates. **This is
  the key that tells a reviewer which plan or agreement to read** for every column
  that returned `Incorporated terms`.

```markdown
## Task

List every plan, charter, or agreement whose terms this instrument states are incorporated into it or govern it.

## Scope

- Include the equity incentive or option plan the instrument is granted under.
- Include any stockholders, investor rights, voting, co-sale, or right of first refusal agreement the instrument makes the holder subject to or a party to.
- Include the charter, certificate of designation, or operating agreement where the instrument states that the units' terms are set out in it.
- Include any employment or consulting agreement the instrument states governs vesting or acceleration.
- Exclude documents referenced only as background, and statutes and regulations.

## Rules

- Name each document as the instrument names it, with its date and version where stated.
- For each document, state in five words or fewer which terms it is stated to supply, for example `vesting and acceleration`, `transfer restrictions`, `liquidation preference`.
- Where the instrument states that it prevails over the named document, or that the named document prevails, report which.
- Where the instrument requires the holder to become a party to an agreement as a condition of the grant, report it and add `(accession required)`.
- Do not report whether the named document was produced; that is Referenced but Not Produced.

## Fallback rules

- Return exactly `None referenced` where the instrument is self-contained and incorporates nothing.

## Output format

One line per document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"] — supplies: [terms]`

Return no more than 6 lines and no more than 70 words.
```

---

### 32. Valuation Referenced

- Native type: Free Response
- Upstream: `@Instrument Type`
- Downstream: none
- Purpose: the valuation the exercise price was set against. **A grant priced
  against a stale or absent valuation is a tax exposure the buyer may inherit**,
  and it is one of the most common findings in a private-company option pool.

```markdown
## Established result

- Instrument Type: @Instrument Type

## Task

Report any valuation, appraisal, or fair market value determination the documents state the instrument's price was set against.

## Applicability

- Applies to `Stock option`, `Restricted stock`, `Stock appreciation right or phantom`, and `Profits interest`.
- For `Common stock` and `LLC unit or membership interest`, apply where the instrument was issued for services.
- For all other instrument types, return `Not applicable`.

## Rules

- Report the valuation as identified: its type, its date, and its preparer where stated. A Section 409A valuation, an independent appraisal, and a board determination are three different things and should be reported as stated rather than normalized.
- Report the per-unit value the valuation established, where the documents state it.
- Where the documents state only that the board determined fair market value, report `board determination` with the determination date, and add `(no independent valuation referenced)`.
- Compare the valuation date to the grant date. Where the valuation predates the grant by more than twelve months, append ` [valuation over 12 months before grant]`.
- Do not compare the valuation to the exercise price, and do not state whether the pricing was correct or whether an exposure exists.

## Fallback rules

- Return `Not applicable` where the instrument type is out of scope.
- Return `Not addressed` where the instrument type is in scope and no valuation or determination is referenced. **This is itself a finding** and the reviewer will treat it as one.
- Return `Unable to determine` where references in the unit conflict, or are illegible.

## Output format

`[Valuation type] — [YYYY-MM-DD] — [preparer or "board"] — [value per unit or "value not stated"]` followed by any bracketed flag.

Return no more than 45 words.
```

---

### 33. Securities Exemption Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the exemption the issuance relied on, which is the first input to the
  securities-compliance review and to the rep the seller will be asked to give.

```markdown
## Task

Report any securities law exemption, registration position, or holder qualification the documents state the issuance relied on.

## Scope

- Include an exemption recited in the instrument or in an authorizing consent, for example Regulation D, Rule 701, Section 4(a)(2), or a state exemption.
- Include a holder representation as to accredited investor status, sophistication, or investment intent.
- Include any statement that a filing was made, such as a Form D, with the filing date where stated.
- Include a restrictive legend where it states the basis of the restriction.
- Exclude generic transfer-restriction language that identifies no exemption or basis.

## Rules

- Report the exemption or position as stated, using the document's own reference.
- Report holder representations in six words or fewer, for example `accredited investor representation given`.
- Where a filing is referenced, state whether the documents evidence that it was made or only that it would be.
- Do not state whether the exemption was available, whether it was properly relied on, or whether a violation occurred. That is a legal conclusion.

## Fallback rules

- Return `Not addressed` where the documents identify no exemption, representation, or filing.

## Output format

`Exemption: [as stated or "Not addressed"]; representations: [brief or "none stated"]; filing: [as stated or "none referenced"]`

Return no more than 45 words. Do not include quotations, section numbers, or citation markers.
```

---

### 34. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this instrument refers to that is not in the unit.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document the documents in this unit refer to and that is not present in the unit.

## Scope

- Include the equity incentive plan and every amendment to it, grant notices, and vesting schedules referenced but absent.
- Include board or owner consents and resolutions referenced as authorizing the instrument, but not produced.
- Include stockholders, investor rights, voting, and co-sale agreements the holder is stated to be subject to.
- Include the charter or certificate of designation where the instrument states the units' terms are set out in it.
- Include exercise notices, conversion notices, 83(b) elections, spousal consents, and Form D filings referenced but absent.
- Include the valuation referenced as the basis for the price.
- Exclude statutes, regulations, and published standards.
- Exclude documents relating to other holders or instruments.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Plan`, report it as printed and add `(no date stated)`.
- Where a consent is referenced as authorizing this instrument, add `; authorizes this grant`, because an issuance with no producible approval is the finding.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; authorizes this grant]`

Return no more than 12 lines and no more than 110 words.
```

---

## Human-review fields

Separate table columns, never populated by Harvey.

| Column | Values |
| --- | --- |
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Reconciles to certified cap table** | Yes / No, delta / Not on cap table / Not yet checked |
| **Holder consent required** | Yes / No / Unclear |
| **Transaction treatment** | Cash out / Assume / Accelerate / Cancel / Convert / Unresolved |
| **Approval defect** | None / Ratification needed / Unresolved |
| **280G implicated** | Yes / No / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: holder, quantity, class, price, vesting,
acceleration, consent rights, board approval.

### Reconciliation work that never belongs in a column

All of this is arithmetic against an authoritative source, and all of it happens
in Excel from the export:

- Every instrument in this table matched against the certified cap table. **Every
  unexplained delta is a finding.**
- Issued and outstanding units by class, against the authorized classes in the
  Corporate table's charter reading. Units issued beyond what the charter
  authorizes is a validity problem, and it happens.
- The fully diluted count, which feeds the purchase price allocation, so a partner
  signs it.
- Total acceleration cost, from the rows classified `Single trigger`, `Double
  trigger`, and `Partial acceleration`, which feeds the purchase price mechanics
  and the 280G analysis.
- The consent list, from the rows with a `Consent right` or `Class vote`, aggregated
  by class against the thresholds in the Corporate table.
- Individuals in this table matched against the Employment table. **Equity on the
  cap table with no grant agreement, or a grant agreement for someone absent from
  the census, is a gap in both directions.**

---

## Test set

- [ ] Option granted under a plan, with vesting and acceleration incorporated by reference
- [ ] Option with vesting stated in full in the grant agreement itself
- [ ] Option with a vesting commencement date preceding the grant date
- [ ] Option with a grant date preceding the board approval date
- [ ] Option, unsigned by the holder
- [ ] Option with early exercise permitted and an 83(b) election form attached but unexecuted
- [ ] Restricted stock with an 83(b) election showing a filing date
- [ ] Restricted stock unit with a dividend equivalent right
- [ ] Warrant issued to a lender, with no vesting
- [ ] Warrant with full ratchet anti-dilution
- [ ] SAFE with a post-money valuation cap and no discount
- [ ] SAFE with an MFN provision
- [ ] Convertible note with interest, a maturity date, and a change-of-control multiple
- [ ] Series A preferred: non-participating, 1x, broad-based weighted average
- [ ] Series B preferred: participating subject to a cap, with a separate class vote on merger
- [ ] Preferred stock purchase agreement where the preference sits in the charter, not the agreement
- [ ] Preferred with a holder put right
- [ ] LLC units expressed as percentage interests, with no authorized count
- [ ] Profits interest with a hurdle amount
- [ ] Stock appreciation right, cash-settled, conferring no units
- [ ] Instrument amended to change the quantity
- [ ] Instrument repriced by amendment
- [ ] Instrument with a partial cancellation recorded
- [ ] Instrument transferred to a family trust
- [ ] Instrument issued by a subsidiary rather than the parent
- [ ] Board consent in the unit that covers a different holder
- [ ] Instrument with a drag-along obligation
- [ ] Instrument with a tag-along right and no drag, to confirm the direction is not inverted
- [ ] Instrument referencing a stockholders agreement not in the unit
- [ ] Unpopulated grant agreement template
- [ ] Compilation: one consent approving twelve separate option grants

Then test the dependencies directly: change `Instrument Type` on a row from
`Stock option` to `Warrant` and confirm the eighteen dependent columns re-run,
with `Vesting Commencement Date`, `Post-Termination Exercise Period`, and
`Early Exercise and 83(b) Election` moving to `Not applicable`, and
`Anti-Dilution Protection` becoming applicable. Change `Acceleration on Change of
Control` from `Single trigger` to `Not addressed` and confirm `Acceleration
Language` moves to `Not addressed` and that a locked cell does not silently retain
the old quotation.

---

## Appendix: the Equity Plans row set

A plan is one document governing hundreds of instruments, so it does not belong in
the instrument rows. It needs a small separate table — usually three to six rows
per matter — because five columns above return `Incorporated terms` and point
here. Build it immediately after this table, or the incorporated terms have
nowhere to resolve to.

Columns, in the same house style, prompts not yet drafted:

| Column | Type | Captures |
| --- | --- | --- |
| Plan name and version | FR | Exact title, adoption date, and every amendment and restatement |
| Adopting entity | FR | The issuer that adopted it |
| Board and owner approval | FR | Adoption and approval evidence, and whether produced |
| Units reserved | FR | As stated, by class, with every increase and its date |
| Evergreen provision | C | Automatic annual increase: present or not addressed |
| Award types permitted | FR | Options, restricted stock, RSUs, SARs, and any limits |
| Default vesting | FR | The schedule applying where a grant notice is silent |
| **Default acceleration on change of control** | C | Single / double / partial / discretionary / none — **this is the term most grant agreements incorporate** |
| Acceleration language | V | Quoted, with the Change of Control, Cause, and Good Reason definitions |
| Assumption and substitution | FR | What happens to awards if the acquirer assumes, substitutes, or terminates them |
| Default post-termination exercise | FR | General period and variations by reason |
| Transfer restrictions | FR | Default restrictions on award transfer |
| Administrator discretion | FR | What the administrator may amend, accelerate, or cash out unilaterally |
| Amendment and termination | FR | Who may amend or terminate the plan, and whose consent is needed |
| Section 409A and 422 provisions | FR | ISO limits, ten-year terms, and any 409A compliance language |
| Referenced but not produced | FR | Sub-plans, award agreement forms, and amendments referenced but absent |

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
| --- | --- | --- | --- | --- | --- | --- |
| | | v1.0 | Initial draft | — | — | — |
