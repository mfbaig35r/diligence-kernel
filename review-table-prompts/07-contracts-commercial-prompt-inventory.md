# Prompt Inventory — Contracts Commercial

Table 7 of the POC. The second half of the Contracts pair. Runs over the same
project as Contracts Core, with the same row unit, and is joined to it on file
name in the export.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Contracts` — same project as Contracts Core
- Review unit: **one agreement family** — identical to Contracts Core, so the two
  tables produce matching row sets
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: corporate/M&A team; feeds the issues
  list, the indemnity and liability analysis, the revenue-quality discussion, and
  the IP and privacy workstreams
- Inventory version: v1.0

### Why the split

Contracts needs roughly 50 columns to do the job and no tenant will take that in
one grid. The division is by question, not arbitrarily:

- **Contracts Core** answers *can the deal happen* — identity, term, termination,
  assignment, change of control. It is the consent-schedule feeder.
- **Contracts Commercial** answers *what are we buying* — economics, liability,
  IP, data, and the obligations that survive closing.

Run Core first. It is the one with a closing dependency; Commercial can be built
and reviewed on a slower clock.

### Joining the two tables

Both tables use the same review unit, so a base agreement's file name appears once
in each. Join on it in Excel. Two consequences:

- **Assemble families identically in both projects.** If Core groups an amendment
  into a family and Commercial does not, the join produces phantom rows.
- Core's `Chain Completeness` governs both. Commercial does not repeat it, so a
  reviewer reading a Commercial row must check the Core row's completeness flag
  before relying on any provision. This is the one place the split costs
  something, and it is worth stating in the demo.

### Columns carried from Core

Commercial repeats only `Counterparty` and `Execution Status`, so its rows are
identifiable and interpretable standalone. Everything else — subject entity,
dates, term, termination, assignment, change of control, chain completeness,
referenced but not produced — lives in Core and is picked up by the join.

## Assumptions to confirm before running

1. Contracts Core has been built and run over the same project, with the same
   families. Commercial is not a standalone table.
2. Buy-side review; the entities in the Table Instructions list are the target
   group.
3. Revenue and cost data will come from the financial workstream for the
   concentration analysis. This table extracts stated contract economics only.
4. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

22 Harvey columns plus 6 human columns.

---

## Table Instructions

- Version: v1.0

Identical to Contracts Core's, so that both tables read the same families the same
way. **Paste the same text into both tables.** If you amend one, amend the other,
or the two halves of a row will disagree about which document supplies a term.

```markdown
## Matter

[Project name]. Buyer-side commercial contract diligence on the target group listed below.

One row is one agreement family: a base agreement together with every amendment, restatement, statement of work, order form, and side letter produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer. It is not a review subject unless a column expressly asks about the buyer.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the parties.
- Where two documents in the unit address the same provision, report the provision as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Report figures only as the documents state them. Do not calculate, total, annualize, convert currency, or apply an escalation to any figure.
- Use entity and individual names exactly as printed in the documents; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Write currency amounts with the currency as printed.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

Lighter than Core's. Most commercial terms are read directly; only the paired
detail and quote columns depend on anything.

```
Stage 1 — Orientation (no upstream)
  Counterparty
  Execution Status
  Commercial Direction

Stage 2 — Economics (routed on direction)
  Commercial Direction ──→ Pricing Basis
                           Stated Contract Value
                           Price Adjustment Mechanism
                           Minimum Commitment
                           Payment Terms

Stage 3 — Risk allocation (independent)
  Liability Cap
  Liability Carve-Outs
  Indemnity Direction ──→ Indemnity Scope
  Insurance Required of Target
  Warranty and Service Levels

Stage 4 — Restrictive covenants
  Exclusivity ──→ Exclusivity Language
  Most Favoured Nation
  Non-Compete Binding Target

Stage 5 — IP, data, and continuity
  IP Granted to Counterparty ──→ IP Grant Language
  Source Code Escrow
  Data Protection Terms
  Audit Rights
  Dispute Resolution
  Surviving Obligations
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Counterparty | Free Response | — | — | v1.0 | draft |
| 2 | Execution Status | Classify | — | — | v1.0 | draft |
| 3 | Commercial Direction | Classify | — | Pricing Basis; Stated Contract Value; Price Adjustment Mechanism; Minimum Commitment; Payment Terms | v1.0 | draft |
| 4 | Pricing Basis | Free Response | @Commercial Direction | — | v1.0 | draft |
| 5 | Stated Contract Value | Free Response | @Commercial Direction | — | v1.0 | draft |
| 6 | Price Adjustment Mechanism | Free Response | @Commercial Direction | — | v1.0 | draft |
| 7 | Minimum Commitment | Free Response | @Commercial Direction | — | v1.0 | draft |
| 8 | Payment Terms | Free Response | @Commercial Direction | — | v1.0 | draft |
| 9 | Liability Cap | Free Response | — | — | v1.0 | draft |
| 10 | Liability Carve-Outs | Free Response | — | — | v1.0 | draft |
| 11 | Indemnity Direction | Classify | — | Indemnity Scope | v1.0 | draft |
| 12 | Indemnity Scope | Free Response | @Indemnity Direction | — | v1.0 | draft |
| 13 | Insurance Required of Target | Free Response | — | — | v1.0 | draft |
| 14 | Warranty and Service Levels | Free Response | — | — | v1.0 | draft |
| 15 | Exclusivity | Classify | — | Exclusivity Language | v1.0 | draft |
| 16 | Exclusivity Language | Verbatim | @Exclusivity | — | v1.0 | draft |
| 17 | Most Favoured Nation | Classify | — | — | v1.0 | draft |
| 18 | Non-Compete Binding Target | Free Response | — | — | v1.0 | draft |
| 19 | IP Granted to Counterparty | Classify | — | IP Grant Language | v1.0 | draft |
| 20 | IP Grant Language | Verbatim | @IP Granted to Counterparty | — | v1.0 | draft |
| 21 | Source Code Escrow | Classify | — | — | v1.0 | draft |
| 22 | Data Protection Terms | Classify | — | — | v1.0 | draft |
| 23 | Audit Rights | Classify | — | — | v1.0 | draft |
| 24 | Dispute Resolution | Free Response | — | — | v1.0 | draft |
| 25 | Surviving Obligations | Free Response | — | — | v1.0 | draft |

25 columns — three more than estimated in the build plan, because `Payment
Terms`, `Warranty and Service Levels`, and `Surviving Obligations` earned their
place during drafting.

---

## Column records

### 1. Counterparty

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: identical to the Core column, repeated so Commercial rows are
  identifiable standalone and so the join can be checked.

```markdown
## Task

Identify the non-target contracting party or parties to this agreement family.

## Scope

- Every party to the base agreement other than a target-group entity listed in the Table Instructions.
- Include a party added or substituted by an assignment, novation, or joinder in a later document in the unit.
- Exclude affiliates of the counterparty merely permitted to receive services or place orders, guarantors, and third-party beneficiaries.

## Rules

- Report the name exactly as printed, including the entity suffix. Do not correct spelling or expand abbreviations.
- If a later document substitutes a counterparty, report the current party and append ` (assigned from [prior party], [YYYY-MM-DD])`.
- If the counterparty is described by a trade name with the legal name given elsewhere in the document, report the legal name and append ` (t/a [trade name])`.
- Where there are multiple non-target parties, list each on its own line.

## Fallback rules

- If the parties clause is missing or the name is illegible, return `Unable to determine — [brief reason]`.

## Output format

`[Exact legal name]` per line, with any qualifier appended as described above. Return no more than 40 words. Do not include addresses, roles, or citation markers.
```

---

### 2. Execution Status

- Native type: Classify
- Configured options, in UI order: `All documents executed`, `Base executed, later document unsigned`, `Base unsigned`, `Partially executed`, `Form or template`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: identical to the Core column. Repeated because a reviewer reading a
  liability cap needs to know whether the document stating it was signed, without
  crossing to another table to find out.

```markdown
## Task

Classify the visible execution status of the documents in this review unit. Choose exactly one configured option.

## Scope

- Evaluate only signature blocks, electronic-signature markers, conformed signatures, and counterpart signature pages visible in the documents in this unit.
- Exclude signature evidence appearing on exhibits, attachments, or referenced documents.
- Exclude notary, witness, and attestation blocks. Do not count them toward execution.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the documents are unpopulated forms, containing bracketed placeholders, blank party names, or `[•]` fields in place of terms.
2. `Base unsigned`: the base agreement provides party signature blocks and none bears a signature marker.
3. `Partially executed`: any document in the unit has at least one signed and at least one unsigned party signature block.
4. `Base executed, later document unsigned`: the base agreement is fully signed and at least one amendment, SOW, order form, or side letter in the unit is unsigned.
5. `All documents executed`: every document in the unit has a signature marker in every party signature block it provides.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated effective date is not a signature marker.

## Fallback rules

- Use `Unable to determine` only where signature evidence exists but cannot be read, where a signature page is referenced but missing, or where documents conflict about execution.
- Do not treat a `duly executed` recital or a stated effective date as evidence that signatures were completed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Commercial Direction

- Native type: Classify
- Configured options, in UI order: `Target is paid`, `Target pays`, `Both directions`, `No payment obligation`, `Unable to determine`
- Upstream: none
- Downstream: five economics columns
- Purpose: routes every economics column, because "pricing" means the target's
  revenue in one direction and its cost in the other, and the reviewer reads them
  differently.

**This is the column that separates revenue quality from cost base.** Filter on it
and the grid splits into the two populations the deal team actually discusses.

```markdown
## Task

Classify the direction of payment under this agreement, from the target's perspective. Choose exactly one configured option.

## Classification rules

- `Target is paid`: the counterparty pays the target for goods, services, or a licence. Customer, reseller, and distributor agreements where the target supplies.
- `Target pays`: the target pays the counterparty. Vendor, supplier, SaaS, outsourcing, and professional services agreements.
- `Both directions`: each party has a payment obligation to the other under the operative terms — a reseller arrangement with reciprocal fees, or a joint venture with cross-charges. Do not use this for a one-directional payment with an indemnity or expense-reimbursement obligation running the other way.
- `No payment obligation`: neither party pays the other. A standalone NDA, a standalone data processing agreement, or a memorandum of understanding.

Classify on the operative terms, not the title. An agreement titled a services agreement under which the target is paid is `Target is paid`.

Where a later document in the unit changes the direction — for example an order form under a framework agreement that runs the other way — classify on the base agreement's direction and note the exception in the evidence field.

## Fallback rules

- Use `Unable to determine` where the documents do not state which party pays, or where the pricing terms are incorporated from a document not present in the unit.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Pricing Basis

- Native type: Free Response
- Upstream: `@Commercial Direction`
- Downstream: none
- Purpose: how the price is calculated, which determines how the revenue or cost
  behaves after closing.

```markdown
## Established result

- Commercial direction: @Commercial Direction

## Task

Report how amounts payable under this agreement are calculated.

## Applicability

- Applies where Commercial Direction is `Target is paid`, `Target pays`, or `Both directions`. Where it is `Both directions`, report the basis for each direction and label them.
- Where Commercial Direction is `No payment obligation`, return exactly `Not applicable`.
- Where Commercial Direction is `Unable to determine`, return exactly `Unable to determine — payment direction unresolved`.

## Include where expressly stated

- The pricing model: fixed fee, subscription, per seat or per user, usage or consumption based, time and materials, per unit, commission or revenue share, or milestone based
- The rate, unit, and billing frequency as printed
- Any tiered or volume-based rate structure
- Any component priced separately, such as implementation, support, or overage
- The currency

## Rules

- Report the basis as stated, using the document's own model where it names one.
- **Do not calculate.** Do not annualize a monthly rate, total a tiered schedule, convert currency, or derive an effective rate.
- Where a later document in the unit changes the pricing, report the basis in the most recently dated document that addresses it.
- Where pricing is set per order or per statement of work rather than in the base agreement, say so and report the basis from any order in the unit.

## Fallback rules

- Return `Not addressed` where the documents state a payment obligation but no basis for calculating it.
- Return `Incorporated terms — pricing set out in [document name as referenced]` where pricing sits in a rate card, schedule, or order not present in the unit. **This is common and it is not a defect** — it tells the reviewer which document to get.
- Return `Unable to determine` where pricing terms in the unit conflict, or are illegible.

## Output format

`[Model]: [rate and unit], billed [frequency], [currency]; separately priced: [components or "none"]`

Return no more than 60 words. Do not include totals or annualized figures you derived.
```

---

### 5. Stated Contract Value

- Native type: Free Response
- Upstream: `@Commercial Direction`
- Downstream: none
- Purpose: any total or committed value the documents state, which is the input to
  the revenue concentration and cost-base analyses.

```markdown
## Established result

- Commercial direction: @Commercial Direction

## Task

Report any total, aggregate, annual, or committed contract value the documents expressly state.

## Applicability

- Applies where Commercial Direction is `Target is paid`, `Target pays`, or `Both directions`.
- Where Commercial Direction is `No payment obligation`, return exactly `Not applicable`.
- Where Commercial Direction is `Unable to determine`, return exactly `Unable to determine — payment direction unresolved`.

## Rules

- Report only a figure a document **states**: a total contract value, an annual contract value, an aggregate fee, a not-to-exceed amount, an order total, or a budget.
- Give the figure, what it describes, the period it covers, and the document and date stating it.
- **Do not calculate.** Do not multiply a rate by a term, sum orders, annualize, or estimate. If no document states a value, the answer is `Not stated`.
- Where several documents in the unit state values — a base agreement with three orders — report each separately with its document, and **do not total them**.
- Where a figure is stated as a maximum or a not-to-exceed rather than a commitment, say which.

## Fallback rules

- Return `Not stated` where no document states an aggregate or total value. **This is the expected answer for most usage-based and per-seat agreements**, and it is not a gap. The reviewer derives value from the rate and the term outside the table.
- Return `Unable to determine` where stated values conflict within one document.

## Output format

One line per stated value:

`[Figure] [currency] — [what it describes] — [period] — per [document title], [YYYY-MM-DD]`

Return no more than 5 lines and no more than 70 words. Do not include any figure you derived.
```

---

### 6. Price Adjustment Mechanism

- Native type: Free Response
- Upstream: `@Commercial Direction`
- Downstream: none
- Purpose: whether and how the price can move. A supplier with an uncapped
  index-linked uplift is a cost risk the buyer inherits; a customer contract with
  no uplift right is a margin risk.

```markdown
## Established result

- Commercial direction: @Commercial Direction

## Task

Report how the price may be changed during the term, and by whom.

## Applicability

- Applies where Commercial Direction is `Target is paid`, `Target pays`, or `Both directions`.
- Where Commercial Direction is `No payment obligation`, return exactly `Not applicable`.
- Where Commercial Direction is `Unable to determine`, return exactly `Unable to determine — payment direction unresolved`.

## Include where expressly stated

- Which party may increase the price, and whether the other's consent is required
- Any cap on the increase, expressed as a percentage or an amount
- Any index the increase is tied to, named as printed
- The frequency of permitted increases, and any notice period
- Any right of the other party to terminate or reject on an increase
- Any fixed-price or price-hold period
- Any benchmarking or market-review mechanism

## Rules

- **Report the cap and the index separately and prominently.** An index-linked uplift with no cap is a materially different risk from one capped at three percent, and the difference is the finding.
- Report the mechanism as stated. Do not calculate any resulting price.
- Where a later document in the unit changes the mechanism, report the mechanism in the most recently dated document that addresses it.

## Fallback rules

- Return `Not addressed` where the documents provide no mechanism for changing the price. Note that for a customer contract this means the target cannot raise prices during the term, which is itself worth a reviewer's attention.
- Return `Incorporated terms` where the mechanism is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Increase by: [party]; cap: [as stated or "uncapped"]; index: [name or "none"]; frequency: [as stated]; notice: [period]; counterparty remedy: [brief or "none stated"]`

Return no more than 65 words.
```

---

### 7. Minimum Commitment

- Native type: Free Response
- Upstream: `@Commercial Direction`
- Downstream: none
- Purpose: any volume, spend, or purchase commitment. A take-or-pay obligation the
  target cannot meet is a liability; one the counterparty owes is committed
  revenue.

```markdown
## Established result

- Commercial direction: @Commercial Direction

## Task

Report any minimum volume, spend, purchase, or capacity commitment the agreement imposes, and on which party.

## Applicability

- Applies where Commercial Direction is `Target is paid`, `Target pays`, or `Both directions`.
- Where Commercial Direction is `No payment obligation`, return exactly `Not applicable`.
- Where Commercial Direction is `Unable to determine`, return exactly `Unable to determine — payment direction unresolved`.

## Include where expressly stated

- The committing party, the amount or volume, and the period it applies over
- The consequence of a shortfall: a true-up payment, a rate increase, loss of a discount, or a termination right
- Any carry-forward, rollover, or make-good provision
- Any exclusivity or wallet-share commitment expressed as a proportion of the party's requirements
- Any ramp or step-up schedule

## Rules

- **State clearly which party owes the commitment.** Reporting it as the counterparty's when it is the target's inverts the finding, and the two appear in similar language.
- Report the shortfall consequence even where the commitment looks comfortable. It is what makes the commitment a liability rather than a target.
- Report figures as stated. Do not calculate a shortfall, a remaining commitment, or a total over the term.
- Where a wallet-share or requirements commitment overlaps with an exclusivity obligation, report the volume element here and leave the exclusivity to its own column.

## Fallback rules

- Return exactly `None` where the agreement imposes no minimum commitment on either party.
- Return `Incorporated terms` where commitments are stated to sit in an order or schedule not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Committing party: [target | counterparty]; amount: [figure or volume]; period: [as stated]; shortfall consequence: [as stated]; carry-forward: [brief or "none stated"]`

Return no more than 65 words.
```

---

### 8. Payment Terms

- Native type: Free Response
- Upstream: `@Commercial Direction`
- Downstream: none
- Purpose: when payment falls due and what happens if it does not. Feeds working
  capital, and a right to suspend service on non-payment is an operational risk at
  closing.

```markdown
## Established result

- Commercial direction: @Commercial Direction

## Task

Report the payment timing and non-payment consequences the agreement states.

## Applicability

- Applies where Commercial Direction is `Target is paid`, `Target pays`, or `Both directions`.
- Where Commercial Direction is `No payment obligation`, return exactly `Not applicable`.
- Where Commercial Direction is `Unable to determine`, return exactly `Unable to determine — payment direction unresolved`.

## Include where expressly stated

- The payment period, for example `net 30` or `net 60 from invoice date`
- Whether amounts are payable in advance or in arrears
- Any prepayment, deposit, or upfront fee
- Interest or late-payment charges
- Any right to suspend performance, withhold delivery, or terminate on non-payment, with any cure period
- Any set-off or withholding right, and any prohibition on set-off
- Any disputed-amounts mechanism permitting payment to be withheld
- Tax gross-up or withholding provisions

## Rules

- Report the period as stated. Do not calculate a due date.
- **Report any suspension right prominently.** A vendor entitled to suspend a critical service on non-payment is an operational exposure, and the cure period is the whole question.
- Report advance versus arrears explicitly. It determines whether the target holds customer cash or funds the counterparty.
- Where a later document in the unit changes the terms, report those in the most recently dated document that addresses them.

## Fallback rules

- Return `Not addressed` where the documents state a payment obligation with no timing.
- Return `Incorporated terms` where payment terms are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Terms: [period]; timing: [advance | arrears]; late charge: [as stated or "none"]; suspension right: [party and cure period, or "none stated"]; set-off: [permitted | prohibited | Not addressed]`

Return no more than 65 words.
```

---

### 9. Liability Cap

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the limit on the target's exposure, which is the first input to the
  risk-allocation discussion.

```markdown
## Task

Report the limitation of liability as it applies to the target.

## Scope

- Report the cap binding the target. Where the cap is mutual, say so.
- Where the cap binding the counterparty differs, report both and label each.
- Exclude carve-outs from the cap, which are a separate column.
- Exclude the exclusion of consequential and indirect losses, unless the documents express it as part of the cap. Report it in the evidence field where it is separate.

## Include where expressly stated

- The cap amount, or the formula — commonly fees paid or payable in a stated preceding period
- Whether the cap is per claim, per event, or aggregate across the agreement
- Any separate, higher cap for particular claim types
- Any super-cap or aggregate ceiling across all caps

## Rules

- Report the formula as printed, for example `fees paid in the 12 months preceding the claim`. **Do not calculate the resulting figure**, even where the fee data is in the unit.
- Report `Uncapped` where the documents expressly state that liability is unlimited.
- Where per-claim and aggregate caps both exist, report both.
- Where a later document in the unit changes the cap, report the cap in the most recently dated document that addresses it.

## Fallback rules

- Return `Not addressed` where the documents contain no limitation of liability. For a customer contract this is a significant exposure and the reviewer will treat it as one.
- Return `Incorporated terms` where the cap is stated to sit in a document not present in the unit.
- Return `Unable to determine` where caps in the unit conflict, or are illegible.

## Output format

`[Amount or formula]; basis: [per claim | per event | aggregate]; mutual: [yes | no, target only | no, differs]; separate caps: [brief or "none"]`

Return no more than 60 words. Do not include any figure you derived.
```

---

### 10. Liability Carve-Outs

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what sits **outside** the cap. **This is where the real exposure is** —
  an agreement with a modest cap and uncapped IP indemnity carries more risk than
  one with a large cap and no carve-outs, and the cap column alone hides that
  completely.

```markdown
## Task

List the liabilities the agreement places outside the limitation of liability.

## Scope

- Include every claim type excluded from the cap, or subject to no cap.
- Include carve-outs from an exclusion of consequential or indirect loss.
- Exclude carve-outs binding only the counterparty, unless the agreement is mutual, in which case say so.
- Exclude claim types merely mentioned in the indemnity without being carved out of the cap.

## Rules

- Report each carve-out in three words or fewer, using the agreement's own category. The usual set is: breach of confidentiality, intellectual property infringement, data protection or security breach, indemnity obligations, gross negligence or wilful misconduct, death or personal injury, fraud, breach of restrictive covenants, and payment obligations.
- **State for each whether it is uncapped or subject to a separate higher cap**, with the amount or formula where stated. The distinction is what determines the exposure.
- Report no more than eight carve-outs; where more exist, report the eight with the widest exposure and append ` and [N] further carve-outs`.
- Do not assess the size of any exposure and do not rank the carve-outs by risk.

## Fallback rules

- Return exactly `None` where the cap applies to all liabilities without exception.
- Return `Not applicable` where the agreement contains no cap for anything to be carved out of.
- Return `Incorporated terms` where the carve-outs are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per carve-out:

`[Category] — [uncapped | separate cap of [amount or formula]]`

Return no more than 8 lines and no more than 80 words.
```

---

### 11. Indemnity Direction

- Native type: Classify
- Configured options, in UI order: `Target indemnifies only`, `Counterparty indemnifies only`, `Mutual`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `Indemnity Scope`
- Purpose: who owes whom. Direction errors here are among the most consequential a
  contract grid can produce, because they invert the risk.

```markdown
## Task

Classify the direction of the indemnity obligations in this agreement. Choose exactly one configured option.

## Scope

- Consider indemnity, hold harmless, and defence obligations.
- Use the Table Instructions review-subject list to determine which party is the target.
- Exclude the limitation of liability and any exclusion of consequential loss.
- Exclude a contribution provision between joint defendants.
- Exclude an obligation to procure insurance, which is a separate column.

## Classification rules

- `Mutual`: both parties owe indemnities, whether or not their scope is symmetrical. **Report the asymmetry in the Scope column** — mutual indemnities are frequently mutual in form and one-sided in substance.
- `Target indemnifies only`: the target owes an indemnity and the counterparty owes none.
- `Counterparty indemnifies only`: the reverse.

Classify on who bears the obligation, not on who drafted the clause or whose name appears first. Where the clause is drafted reciprocally using defined party terms, resolve the terms to the actual parties before classifying.

An obligation to indemnify the counterparty's affiliates, customers, or end users is still the target indemnifying. Report the extended beneficiaries in the Scope column.

## Fallback rules

- Use `Not addressed` where the documents contain no indemnity.
- Use `Incorporated terms` where the indemnity is stated to sit in a document not present in the unit.
- Use `Unable to determine` where the direction cannot be resolved from the defined terms, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Indemnity Scope

- Native type: Free Response
- Upstream: `@Indemnity Direction`
- Downstream: none
- Purpose: what is indemnified, in each direction, with the procedural conditions
  that determine whether the indemnity is worth anything.

```markdown
## Established result

- Indemnity direction: @Indemnity Direction

## Task

If Indemnity Direction is `Target indemnifies only`, `Counterparty indemnifies only`, or `Mutual`, report what is indemnified in each direction.

If Indemnity Direction is `Not addressed`, return exactly `Not applicable`.

If Indemnity Direction is `Incorporated terms`, return `Incorporated terms — indemnity set out in [document name as referenced]`.

If Indemnity Direction is `Unable to determine`, return exactly `Unable to determine — upstream direction is unresolved`.

## Rules

- Use the established result for routing, but confirm each obligation against the documents in the current unit.
- **One line per direction**, so the asymmetry in a mutual indemnity is visible.
- For each direction, report the claim categories in three words or fewer each — the usual set is third-party IP infringement, data breach, personal injury and property damage, breach of confidentiality, breach of law, employment claims, and taxes.
- Report the beneficiaries where they extend beyond the contracting party, for example affiliates, customers, or end users.
- Report the procedural conditions: notice period, whether the indemnifying party controls the defence, and whether settlement requires the indemnified party's consent. **An indemnity whose conditions were never met is unenforceable in practice**, and control of defence is what determines who runs the risk.
- Report any cap or sub-limit stated for the indemnity specifically.
- Do not assess enforceability, and do not state whether any indemnity has been triggered.

## Output format

One line per direction:

`[Target indemnifies | Counterparty indemnifies] — [categories]; beneficiaries: [as stated or "party only"]; defence controlled by: [party or "Not addressed"]; notice: [period or "none stated"]`

Return no more than 90 words. Do not include quotations, section numbers, or citation markers.
```

---

### 13. Insurance Required of Target

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: coverage the agreement obliges the target to carry. Cross-checked
  against the Insurance table, a requirement the target does not meet is a breach
  nobody has noticed.

```markdown
## Task

Report any insurance the agreement requires the target to maintain.

## Include where expressly stated

- The coverage types required, using the agreement's own labels
- The limits required for each, per occurrence and in aggregate
- Any requirement to name the counterparty as an additional insured
- Any requirement for a waiver of subrogation
- Any requirement that coverage be primary and non-contributory
- Any minimum insurer rating requirement
- Any obligation to provide certificates of insurance, and on what frequency
- Any requirement to maintain coverage for a period after the term ends

## Rules

- Report requirements binding the **target**. Where the agreement imposes requirements on the counterparty as well, note that in the evidence field rather than the cell.
- Report limits as stated, with the currency. Do not total or compare them to anything.
- **Report any additional-insured or waiver-of-subrogation requirement explicitly**, because both require action on the policy itself and are commonly agreed and never implemented.
- Report any post-term or tail requirement, since it survives closing.
- Do not state whether the target's actual coverage satisfies the requirement. That comparison happens against the Insurance table.

## Fallback rules

- Return exactly `None` where the agreement imposes no insurance obligation on the target.
- Return `Incorporated terms` where the requirements are stated to sit in a schedule or exhibit not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per coverage type:

`[Coverage] — [limits]` followed by a final line: `Additional insured: [yes | Not addressed]; waiver of subrogation: [yes | Not addressed]; certificates: [as stated]; post-term: [period or "none"]`

Return no more than 8 lines and no more than 85 words.
```

---

### 14. Warranty and Service Levels

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the target promises about performance and what it owes when it
  misses. Service credits are a revenue leakage the buyer inherits.

```markdown
## Task

Report the performance warranties and service level commitments the agreement contains, and the remedies for failure.

## Include where expressly stated

- Performance, availability, or uptime commitments, with the metric and target as printed
- Response and resolution time commitments
- Product or service warranties, and the warranty period
- Service credits or liquidated damages payable for a miss, with the amount or formula
- Any cap on credits, and whether credits are the sole remedy
- Any right to terminate for repeated or chronic failure, with the threshold
- Any warranty disclaimer or `as is` provision
- Any acceptance testing regime and the consequence of rejection

## Rules

- Report which party owes each commitment. Where the target is paid, the commitments will usually bind the target; where the target pays, the reverse.
- **Report whether service credits are the sole remedy.** Sole-remedy credits cap the exposure; credits alongside a termination right and damages do not, and the difference is the finding.
- Report figures and formulas as stated. Do not calculate any credit or exposure.
- Where a later document in the unit changes the commitments, report those in the most recently dated document that addresses them.

## Fallback rules

- Return `Not addressed` where the agreement contains no performance commitment or warranty.
- Return `Incorporated terms — set out in [document name as referenced]` where commitments sit in an SLA, schedule, or hosted terms not present in the unit. **This is very common** and it tells the reviewer which document to request.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Owed by: [party]; commitments: [metric and target]; credits: [amount or formula or "none"]; sole remedy: [yes | no | Not addressed]; chronic failure termination: [threshold or "Not addressed"]; warranty period: [as stated]`

Return no more than 80 words.
```

---

### 15. Exclusivity

- Native type: Classify
- Configured options, in UI order: `Binds target`, `Binds counterparty`, `Mutual`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `Exclusivity Language`
- Purpose: whether either party is restricted from dealing with others. An
  exclusivity binding the target can constrain the buyer's whole commercial
  strategy post-closing.

```markdown
## Task

Classify any exclusivity obligation in this agreement and which party it binds. Choose exactly one configured option.

## Scope

- Include exclusive supply, exclusive purchase, sole-source, exclusive distribution, exclusive territory, and requirements obligations.
- Include an obligation to source a stated proportion of requirements from one party, since it is exclusivity in substance.
- **Exclude most favoured nation provisions**, which are a separate column. An MFN constrains price, not counterparty choice, and conflating them is the common error here.
- Exclude non-compete obligations, which have their own column.
- Exclude an exclusive licence grant of intellectual property, which belongs to the IP columns.
- Exclude a no-shop or exclusivity provision in a deal document.

## Classification rules

- `Binds target`: the target is restricted from dealing with, supplying, or purchasing from third parties.
- `Binds counterparty`: the counterparty is so restricted, which is usually a benefit to the target.
- `Mutual`: both are restricted.

Classify on who is restricted, not on who benefits. An exclusive distribution appointment in which the target is the exclusive distributor for a territory restricts the **counterparty** from appointing others; if it also obliges the target to buy only from that counterparty, it is `Mutual`.

## Fallback rules

- Use `Not addressed` where neither party is restricted from dealing with third parties.
- Use `Incorporated terms` where the obligation is stated to sit in a document not present in the unit.
- Use `Unable to determine` where the restricted party cannot be resolved, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Exclusivity Language

- Native type: Verbatim
- Upstream: `@Exclusivity`
- Downstream: none
- Purpose: the exact text, because the scope of an exclusivity — product,
  territory, channel, field of use — is what determines whether it actually
  constrains the business.

```markdown
## Established result

- Exclusivity: @Exclusivity

## Task

If Exclusivity is `Binds target`, `Binds counterparty`, or `Mutual`, quote the exclusivity provision exactly as written.

If Exclusivity is `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If Exclusivity is `Unable to determine`, quote whatever exclusivity language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative restriction together with every scope limb it depends on: the products or services covered, the territory, the channel or customer segment, the field of use, and the duration. **The scope limbs are the point** — an exclusivity limited to one product in one country is a different fact from a general one.
- Quote any carve-out or exception, and any definition of a defined product or territory term the provision relies on where that definition appears in the unit.
- Where the combined text exceeds 200 words, quote the operative restriction and each scope limb and carve-out, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether the provision constrains the buyer's plans.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 17. Most Favoured Nation

- Native type: Classify
- Configured options, in UI order: `Target owes MFN`, `Counterparty owes MFN`, `Mutual`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: a price-parity obligation, kept separate from exclusivity because it
  constrains price rather than counterparty choice. An MFN owed by the target can
  cascade a single discount across an entire customer base.

```markdown
## Task

Classify any most favoured nation, price parity, or best-pricing obligation in this agreement, and which party owes it. Choose exactly one configured option.

## Scope

- Include obligations to offer terms no less favourable than those offered to any other party, whether framed as pricing, terms, or both.
- Include benchmarking provisions that require an adjustment to match market rates.
- **Exclude exclusivity and requirements obligations**, which restrict who a party may deal with rather than what it may charge.
- Exclude a volume discount schedule, which prices tiers rather than promising parity.
- Exclude a price adjustment mechanism, which is its own column.

## Classification rules

- `Target owes MFN`: the target must offer the counterparty terms at least as good as those it offers others. **This is the direction that matters most**, because one discount granted elsewhere can trigger repricing across every contract carrying the same obligation.
- `Counterparty owes MFN`: the reverse.
- `Mutual`: both owe parity obligations.

Report the comparator set and any audit or certification obligation in the evidence field: an MFN measured against all customers is far wider than one measured against a named peer group.

## Fallback rules

- Use `Not addressed` where the agreement contains no parity obligation.
- Use `Incorporated terms` where the obligation is stated to sit in a document not present in the unit.
- Use `Unable to determine` where the obligated party cannot be resolved, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 18. Non-Compete Binding Target

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any restriction on the target competing or serving particular customers
  or markets. **This is a constraint on the buyer's business after closing**, and
  it can reach the buyer's existing operations.

```markdown
## Task

Report any obligation restricting the target from competing, or from serving particular customers, markets, or fields.

## Scope

- Include non-compete, non-solicitation of the counterparty's customers or employees, non-circumvention, and field-of-use restrictions binding the target.
- Include any restriction that extends to the target's affiliates or to a successor, since that is what reaches the buyer's group.
- Exclude restrictions binding the counterparty.
- Exclude exclusivity and requirements obligations, which are a separate column, unless the provision also restricts the target from competing generally.
- Exclude employee restrictive covenants, which belong to the Employment table.

## Include where expressly stated

- The restricted activity, in eight words or fewer
- The geographic scope
- The duration, and whether it extends past termination
- **Whether the restriction binds the target's affiliates, group companies, or successors**
- Any carve-out for existing business or for a stated line of activity
- Any liquidated damages or specific-remedy provision for breach

## Rules

- Report the scope limbs separately. A restriction on one field in one country for one year is a different fact from a general one.
- **Report the affiliate and successor reach prominently.** A non-compete binding the target's affiliates becomes a restriction on the buyer's whole group at closing, and it is the element most often missed.
- Report the post-termination duration even where the term has not ended.
- Do not assess enforceability, which varies by jurisdiction and is a human column.

## Fallback rules

- Return exactly `None` where the agreement imposes no such restriction on the target.
- Return `Incorporated terms` where the restriction is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Activity: [brief]; territory: [as stated]; duration: [as stated]; post-term: [period or "none"]; binds affiliates or successors: [yes | Not addressed]; carve-outs: [brief or "none stated"]`

Return no more than 75 words.
```

---

### 19. IP Granted to Counterparty

- Native type: Classify
- Configured options, in UI order: `Non-exclusive licence`, `Exclusive licence`, `Assignment of deliverables`, `Joint ownership`, `Assignment of background IP`, `No grant`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `IP Grant Language`
- Purpose: what intellectual property leaves the target under this agreement. **A
  customer contract that assigns deliverable IP away is an IP finding, not a
  contracts finding**, and it will not surface anywhere else.

```markdown
## Task

Classify the most significant grant of the target's intellectual property to the counterparty under this agreement. Choose exactly one configured option.

## Scope

- Consider grants of the target's IP **to** the counterparty.
- Exclude inbound licences of the counterparty's IP to the target. Note them in the evidence field; they belong to the IP workstream's licence review.
- Exclude a trademark licence granted solely for the counterparty to reference the relationship or use the target's logo in marketing.
- Exclude feedback and suggestions clauses assigning the counterparty's feedback to the target, which run the other way.
- Exclude a bare covenant not to sue, unless it operates as a licence in substance.

## Classification rules

Apply the first rule that fits — the order is by severity of what leaves the target.

1. `Assignment of background IP`: the target assigns pre-existing IP, not merely what is created under the agreement. The most severe outcome and the rarest.
2. `Joint ownership`: IP created under the agreement is jointly owned. **Treat this as severe**: joint ownership usually means neither party can exploit or license without the other, which constrains the business permanently.
3. `Assignment of deliverables`: IP in work product or deliverables created under the agreement is assigned to the counterparty.
4. `Exclusive licence`: an exclusive licence of the target's IP, whether or not limited by field or territory. Exclusive means the target itself may be excluded.
5. `Non-exclusive licence`: a non-exclusive licence, including the ordinary right to use a product or service the target supplies.
6. `No grant`: the agreement expressly reserves all of the target's IP and grants nothing.

Where the agreement contains more than one grant, classify on the most severe under this order and report the others in the Language column.

## Fallback rules

- Use `Not addressed` where the agreement says nothing about the target's IP.
- Use `Incorporated terms` where the grant is stated to sit in a document not present in the unit.
- Use `Unable to determine` where the nature of the grant cannot be resolved, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 20. IP Grant Language

- Native type: Verbatim
- Upstream: `@IP Granted to Counterparty`
- Downstream: none
- Purpose: the exact grant text. IP grants turn on precise wording, and the
  difference between a licence to use and an assignment can be a single verb.

```markdown
## Established result

- IP granted to counterparty: @IP Granted to Counterparty

## Task

If IP Granted to Counterparty is `Assignment of background IP`, `Joint ownership`, `Assignment of deliverables`, `Exclusive licence`, or `Non-exclusive licence`, quote the grant provision exactly as written.

If it is `No grant`, `Not addressed`, or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever grant language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative granting words and every limb qualifying the grant: the subject matter, the field of use, the territory, the term, whether it is sublicensable and transferable, and whether it is irrevocable or perpetual.
- Quote the reservation of rights and any background-IP carve-out where present. **The carve-out is what determines how much actually leaves**, and a grant of deliverables with a wide background reservation is a much smaller fact than one without.
- Where the agreement contains more than one grant, quote each and label it.
- Where the combined text exceeds 200 words, quote the granting words, the scope limbs, and the reservation, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not state whether the grant is transferable in this transaction.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 21. Source Code Escrow

- Native type: Classify
- Configured options, in UI order: `Escrow in place`, `Escrow agreed, not evidenced`, `Escrow on request`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the counterparty can obtain the target's source code, and on
  what trigger. Release triggers frequently include insolvency and sometimes a
  change of control.

```markdown
## Task

Classify whether this agreement provides for the target's source code or technical materials to be held in escrow for the counterparty. Choose exactly one configured option.

## Scope

- Include escrow of source code, build scripts, technical documentation, and data.
- Include any obligation to deposit materials with a third-party agent.
- Exclude escrow of funds, and exclude a data return or portability obligation on termination.
- Exclude escrow arrangements under which the **target** is the beneficiary of a supplier's code. Note those in the evidence field; they belong to the vendor review.

## Classification rules

- `Escrow in place`: an escrow agreement or a deposit is evidenced in the documents in the unit.
- `Escrow agreed, not evidenced`: the agreement obliges the target to establish or maintain escrow and no escrow agreement or deposit confirmation is present in the unit. **This is the finding**: an unperformed escrow obligation is a live breach and it is common.
- `Escrow on request`: the counterparty may require escrow to be established in future but has not, on the face of the documents.
- `Not applicable`: the agreement involves no software or technical materials the target supplies.

Report the release triggers in the evidence field, and note especially whether they include insolvency, discontinuation of the product, material breach, or a change of control. **A change-of-control release trigger is a transaction issue** and should also be flagged to the Contracts Core reviewer.

## Fallback rules

- Use `Not addressed` where the agreement involves software the target supplies and says nothing about escrow.
- Use `Unable to determine` where escrow provisions in the unit conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 22. Data Protection Terms

- Native type: Classify
- Configured options, in UI order: `DPA in unit`, `DPA referenced, not produced`, `Terms in body of agreement`, `Incorporated terms`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether personal data flows under this agreement and whether the
  processing terms exist. Feeds the privacy workstream and the coverage register.

```markdown
## Task

Classify how this agreement addresses the processing of personal data. Choose exactly one configured option.

## Scope

- Consider provisions governing personal data, personal information, or equivalent, including processing terms, security obligations, breach notification, subprocessing, international transfer mechanisms, and data subject rights.
- Exclude confidentiality provisions that do not address personal data specifically.
- Exclude data ownership and data licence provisions concerning non-personal or aggregated data. Note those in the evidence field.

## Classification rules

Apply the first rule that fits.

1. `Not applicable`: the agreement involves no processing of personal data by either party — for example a supply agreement for goods with no personal data flow.
2. `DPA in unit`: a data processing agreement, addendum, or exhibit is present in this review unit.
3. `DPA referenced, not produced`: the agreement requires or refers to a data processing agreement or addendum that is not in the unit. **A coverage finding**, and the document is reported in the Contracts Core `Referenced but Not Produced` column.
4. `Incorporated terms`: processing terms are stated to be governed by terms hosted at a URL or by a standard addendum not present in the unit.
5. `Terms in body of agreement`: substantive processing terms appear in the agreement itself rather than in a separate document.
6. `Not addressed`: personal data plainly flows under the agreement and no processing terms exist anywhere in it. **This is the most significant answer this column can return** and it is a compliance gap, not a drafting preference.

Report in the evidence field which party is stated to be controller and which processor, and whether any international transfer mechanism is named.

## Fallback rules

- Use `Unable to determine` where it cannot be established from the documents whether personal data is processed, or where provisions conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 23. Audit Rights

- Native type: Classify
- Configured options, in UI order: `Counterparty may audit target`, `Target may audit counterparty`, `Mutual`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: who can inspect whom. An audit right exercisable against the target is
  an operational burden and a disclosure exposure that survives closing.

```markdown
## Task

Classify any right to audit, inspect, or examine the other party under this agreement. Choose exactly one configured option.

## Scope

- Include rights to audit records, books, facilities, systems, security controls, or compliance with the agreement.
- Include a right exercisable by the counterparty's regulator or its appointed auditor.
- Exclude a right to verify an invoice or a single disputed amount.
- Exclude a right to receive reports or certifications without an inspection right.
- Exclude regulatory inspection powers arising by law rather than by the agreement.

## Classification rules

- `Counterparty may audit target`: the counterparty, its auditors, or its regulator may inspect the target.
- `Target may audit counterparty`: the reverse. Where the target pays under the agreement, this is usually a benefit.
- `Mutual`: both hold rights.

Report in the evidence field the frequency, the notice period, who bears the cost, and any right to audit on suspicion of breach without notice. **An unlimited, no-notice, counterparty-cost audit right is a materially different obligation from an annual audit at the auditing party's expense**, and the frequency and cost terms are where that shows.

## Fallback rules

- Use `Not addressed` where the agreement confers no audit or inspection right.
- Use `Incorporated terms` where the right is stated to sit in a document not present in the unit.
- Use `Unable to determine` where the holder of the right cannot be resolved, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. Dispute Resolution

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where and how disputes are resolved, which determines the cost and
  forum of any inherited dispute and interacts with the Litigation table.

```markdown
## Task

Report the dispute resolution mechanism the agreement provides.

## Include where expressly stated

- The forum: named courts, arbitration, or expert determination
- For arbitration: the seat, the rules and administering body, the number of arbitrators, and the language
- Any escalation or negotiation step required before proceedings
- Any mandatory mediation step
- Any class action or collective proceeding waiver
- Any jury trial waiver
- Any exception permitting injunctive relief in any court
- Any limitation period shorter than the statutory one
- Any provision on costs or fee-shifting

## Rules

- Report the forum and the seat separately. Governing law is a different concept and lives in the Contracts Core table; do not report it here.
- **Report any shortened limitation period prominently.** A contractual twelve-month bar can extinguish a claim the buyer would otherwise inherit, and it is easy to miss.
- Report the class waiver and jury waiver where present, since both bear on exposure in consumer-facing and employment-adjacent agreements.
- Where a later document in the unit changes the mechanism, report the mechanism in the most recently dated document that addresses it.

## Fallback rules

- Return `Not addressed` where the agreement provides no dispute resolution mechanism.
- Return `Incorporated terms` where the mechanism is stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Forum: [courts and jurisdiction | arbitration]; seat and rules: [as stated]; pre-action steps: [brief or "none"]; class waiver: [yes | Not addressed]; jury waiver: [yes | Not addressed]; limitation period: [as stated or "Not addressed"]`

Return no more than 70 words.
```

---

### 25. Surviving Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what continues after the agreement ends. **Obligations that survive
  termination follow the business to the buyer**, and they are invisible in a grid
  that only records term and termination.

```markdown
## Task

Report the obligations the agreement states survive its expiry or termination, and for how long.

## Scope

- Include obligations expressly stated to survive, whether in a survival clause or in the individual provision.
- Include post-termination transition, migration, data return or deletion, and wind-down assistance obligations.
- Include continuing confidentiality, IP, indemnity, non-compete, and non-solicit obligations.
- Include any continuing licence granted to the counterparty that outlasts the term.
- Include any run-off insurance obligation.
- Exclude obligations that merely accrued before termination, such as unpaid invoices, unless the agreement addresses them in the survival provision.

## Rules

- Report each surviving obligation with its duration as stated: a stated period, `perpetual`, or `duration not stated`.
- **Flag any obligation that survives perpetually.** A perpetual confidentiality obligation is ordinary; a perpetual licence of the target's IP, or a perpetual indemnity, is a permanent constraint on the buyer.
- Report any transition or migration assistance obligation with the period and whether it is chargeable, since it is an operational commitment the buyer inherits.
- Consolidate substantially similar obligations. Report no more than eight.
- Do not state whether any obligation would survive this transaction, and do not assess enforceability.

## Fallback rules

- Return `Not addressed` where the agreement contains no survival provision and no provision stated to continue after termination.
- Return `Incorporated terms` where survival is stated to be governed by a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per obligation:

`[Obligation] — [period | perpetual | duration not stated]`

Return no more than 8 lines and no more than 80 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Revenue or cost significance** | Top 10 / Top 50 / Other / Unknown |
| **Off-market terms** | None / Identified (specify) / Unassessed |
| **Post-closing constraint** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: liability cap and carve-outs, indemnity
direction, IP grants, exclusivity, non-compete.

### Cross-table work that never belongs in a column

- **Revenue concentration.** Match `Counterparty` against revenue data from the
  financial workstream, in Excel. Name variants make this manual, it is the
  highest-value cross-workstream check in legal diligence, and it does not
  automate here.
- **Insurance compliance.** `Insurance Required of Target` against the Insurance
  table. Requirements the target does not meet are live breaches.
- **IP leakage.** Rows classified `Assignment of deliverables`,
  `Assignment of background IP`, or `Joint ownership`, against the IP chain of
  title. IP assigned away under a customer contract will not appear in the
  registrations table at all.
- **Privacy coverage.** Rows classified `DPA referenced, not produced` or
  `Not addressed` on data protection, against the privacy workstream and the
  coverage register.
- **Escrow triggers.** Rows classified `Escrow agreed, not evidenced`, and any
  escrow with a change-of-control release trigger, back to Contracts Core.
- **Defined term drift.** For the largest agreements, spot-check that `Affiliate`
  and `Change of Control` carry consistent definitions across the family. Ask
  Assistant over the project; do not build a column.

---

## Test set

- [ ] Customer MSA where the target is paid, subscription pricing
- [ ] Vendor SaaS agreement where the target pays, per-seat pricing
- [ ] Reseller agreement with payment obligations in both directions
- [ ] Standalone NDA with no payment obligation
- [ ] Agreement with pricing set only in an order form not in the unit
- [ ] Agreement with an uncapped index-linked price increase
- [ ] Agreement with a take-or-pay minimum owed by the target
- [ ] Agreement with a minimum commitment owed by the counterparty
- [ ] Agreement with a vendor right to suspend service on non-payment
- [ ] Agreement with a fees-paid liability cap and uncapped IP indemnity
- [ ] Agreement with expressly unlimited liability
- [ ] Agreement with no limitation of liability at all
- [ ] Mutual indemnity that is asymmetrical in substance
- [ ] Indemnity extending to the counterparty's customers and end users
- [ ] Agreement requiring the target to name the counterparty as additional insured
- [ ] Agreement with service credits as the sole remedy
- [ ] Agreement with service credits plus a chronic-failure termination right
- [ ] SLA referenced but not produced
- [ ] Exclusive distribution appointment restricting the counterparty
- [ ] Requirements obligation restricting the target
- [ ] MFN owed by the target, measured against all customers
- [ ] Agreement with both an exclusivity and an MFN, to confirm they are not conflated
- [ ] Non-compete binding the target's affiliates and successors
- [ ] Customer agreement assigning deliverable IP to the counterparty
- [ ] Agreement creating joint ownership of developed IP
- [ ] Agreement granting an exclusive field-limited licence
- [ ] Agreement reserving all IP with a wide background carve-out
- [ ] Agreement with an escrow obligation and no escrow agreement produced
- [ ] Agreement with a change-of-control escrow release trigger
- [ ] Agreement processing personal data with no DPA anywhere
- [ ] Agreement with a DPA as an exhibit in the unit
- [ ] Agreement with hosted terms incorporated by URL
- [ ] Agreement with a no-notice audit right exercisable at the target's cost
- [ ] Agreement with a contractual twelve-month limitation period
- [ ] Agreement with a perpetual licence surviving termination
- [ ] Family where an amendment replaces the liability cap

Then test the dependencies: change `Commercial Direction` on a row from
`Target is paid` to `No payment obligation` and confirm the five economics columns
move to `Not applicable`. Change `Exclusivity` from `Binds target` to
`Not addressed` and confirm `Exclusivity Language` follows.

Finally, test the join: export both Contracts tables and confirm the row sets
match on file name with no orphans in either direction. **An orphan means the
families were assembled differently in the two tables**, which is the failure mode
this split introduces.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
