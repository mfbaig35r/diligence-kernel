# Prompt Inventory — Debt: Facilities

Table 18 of the POC.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Finance`
- Review unit: **one facility** — the credit agreement, note, or instrument,
  every amendment, waiver, and consent, the related guaranties and security
  agreements, the most recent compliance certificates, and any payoff letter or
  release produced for it
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: finance and corporate/M&A teams; feeds
  the payoff and consent schedule, the closing funds flow, the lien release
  checklist, and the coverage register
- Inventory version: v1.0

### The three questions

1. **What has to be paid, and what does paying cost?** The outstanding balance
   with its as-of date, plus any make-whole, prepayment premium, breakage, or
   defeasance requirement. **A defeasance obligation is a timetable item, not just
   a cost.**
2. **Whose consent is needed?** The change-of-control consequence, whether it
   reaches indirect ownership, and whether the lender can be repaid instead of
   asked.
3. **What has to be released, and by whom?** Collateral, guaranties, deposit
   account control, and the lien filings that must come off the register.

### The arithmetic boundary

Every figure in this table is reported as stated with its source and date. **No
column computes a payoff, accrues interest, tests a covenant, or totals debt
across facilities.** The funds flow is built in Excel from the export and
confirmed by payoff letters from the lenders — a computed payoff figure looks
identical to a quoted one in a grid, and only one of them is bankable.

## Assumptions to confirm before running

1. One row is one facility. A credit agreement providing a term loan and a
   revolver is one row where the documents treat it as one facility, and two rows
   where the tranches have separate borrowers, maturities, or security. Decide once.
2. **Lien filings are a separate table.** The facility-to-filing match is the
   point of having both, and it cannot be done from one row set.
3. Capital and finance leases are rows here where the documents treat them as
   financing. Operating leases of real property are Real Estate rows.
4. Intercompany loans are rows here **and** in the Related-Party workstream if
   that scope decision is taken; note the duplication in the production log.
5. Buy-side review; the entities in the Table Instructions list are the target
   group.
6. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

38 Harvey columns plus 10 human columns. If your tenant's cap is lower, split into
**Facility Terms and Economics** (columns 1–21) and **Facility Covenants,
Security, and Exit** (columns 22–38) over the same project, joined on lender and
facility in the export.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side finance diligence on the target group listed below. This table reviews debt facilities and secured financing.

One row is one facility: the credit agreement, note, or instrument, every amendment, waiver, and consent, the related guaranties and security agreements, the most recent compliance certificates, and any payoff letter or release produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the facility or the lender.
- Where two documents in the unit address the same provision, report the provision as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- **Report figures only as the documents state them, always with the document and date they come from. Do not calculate anything.** Do not accrue interest, compute a payoff, apply a rate, total commitments or balances, net a revolver drawing against availability, test a covenant, or compute a ratio. Every figure in a funds flow must be traceable to a payoff letter, and a computed figure is indistinguishable from a quoted one in an export.
- **A compliance certificate states the borrower's own calculation as at its date.** Report it as the borrower's statement, not as a fact, and identify the certificate.
- Use entity names exactly as printed; do not shorten, expand, or correct them.
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
  Facility Type
  Borrower
  Obligor Group
  Lender or Agent
  Governing Law

Stage 2 — Record status
  Documents in Unit ──→ Execution Status
                        Chain Completeness
                        Referenced but Not Produced
  Obligor Group     ──→ Obligors Inside Group

Stage 3 — Economics
  Facility Type ──→ Original Commitment
                    Interest Rate
                    Amortization
  Outstanding Balance Stated ──→ Balance As-Of Date
  Default Rate, Maturity Date

Stage 4 — Covenants
  Financial Covenants ──→ Most Recent Tested Compliance
                          Equity Cure
  Negative Covenants, Restricted Payments, Permitted Debt and Liens,
  Reporting and Information Covenants

Stage 5 — Transaction triggers
  Change of Control Consequence ──→ CoC Definition and Threshold
                                    CoC Language
  Assignment by Borrower, Cross-Default and Cross-Acceleration,
  MAC or MAE Clause

Stage 6 — Security and exit
  Collateral Description ──→ Excluded Assets
                             IP Included in Collateral
  Deposit Account Control, Intercreditor and Subordination
  Prepayment Terms ──→ Make-Whole or Defeasance
  Payoff and Release Mechanics
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Execution Status; Chain Completeness; Referenced but Not Produced | v1.0 | draft |
| 2 | Facility Type | Classify | — | Original Commitment; Interest Rate; Amortization | v1.0 | draft |
| 3 | Borrower | Free Response | — | — | v1.0 | draft |
| 4 | Obligor Group | Free Response | — | Obligors Inside Group | v1.0 | draft |
| 5 | Obligors Inside Group | Classify | @Obligor Group | — | v1.0 | draft |
| 6 | Lender or Agent | Free Response | — | — | v1.0 | draft |
| 7 | Execution Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 8 | Chain Completeness | Classify | @Documents in Unit | — | v1.0 | draft |
| 9 | Original Commitment | Free Response | @Facility Type | — | v1.0 | draft |
| 10 | Outstanding Balance Stated | Free Response | — | Balance As-Of Date | v1.0 | draft |
| 11 | Balance As-Of Date | Date | @Outstanding Balance Stated | — | v1.0 | draft |
| 12 | Interest Rate | Free Response | @Facility Type | — | v1.0 | draft |
| 13 | Default Rate | Free Response | — | — | v1.0 | draft |
| 14 | Maturity Date | Date | — | — | v1.0 | draft |
| 15 | Amortization | Free Response | @Facility Type | — | v1.0 | draft |
| 16 | Financial Covenants | Free Response | — | Most Recent Tested Compliance; Equity Cure | v1.0 | draft |
| 17 | Most Recent Tested Compliance | Free Response | @Financial Covenants | — | v1.0 | draft |
| 18 | Equity Cure | Classify | @Financial Covenants | — | v1.0 | draft |
| 19 | Negative Covenants | Free Response | — | — | v1.0 | draft |
| 20 | Restricted Payments | Free Response | — | — | v1.0 | draft |
| 21 | Permitted Debt and Liens | Free Response | — | — | v1.0 | draft |
| 22 | Reporting and Information Covenants | Free Response | — | — | v1.0 | draft |
| 23 | Change of Control Consequence | Classify | — | CoC Definition and Threshold; CoC Language | v1.0 | draft |
| 24 | CoC Definition and Threshold | Free Response | @Change of Control Consequence | — | v1.0 | draft |
| 25 | CoC Language | Verbatim | @Change of Control Consequence | — | v1.0 | draft |
| 26 | Assignment by Borrower | Classify | — | — | v1.0 | draft |
| 27 | Cross-Default and Cross-Acceleration | Free Response | — | — | v1.0 | draft |
| 28 | MAC or MAE Clause | Classify | — | — | v1.0 | draft |
| 29 | Prepayment Terms | Free Response | — | Make-Whole or Defeasance | v1.0 | draft |
| 30 | Make-Whole or Defeasance | Free Response | @Prepayment Terms | — | v1.0 | draft |
| 31 | Collateral Description | Free Response | — | Excluded Assets; IP Included in Collateral | v1.0 | draft |
| 32 | Excluded Assets | Free Response | @Collateral Description | — | v1.0 | draft |
| 33 | IP Included in Collateral | Classify | @Collateral Description | — | v1.0 | draft |
| 34 | Deposit Account Control | Classify | — | — | v1.0 | draft |
| 35 | Intercreditor and Subordination | Free Response | — | — | v1.0 | draft |
| 36 | Payoff and Release Mechanics | Free Response | — | — | v1.0 | draft |
| 37 | Governing Law | Free Response | — | — | v1.0 | draft |
| 38 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Execution Status`, `Chain Completeness`, `Referenced but Not Produced`
- Purpose: inventory the facility file, including which security and compliance
  documents were produced.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the credit agreement, note, or instrument, every amendment, restatement, waiver, consent, and forbearance, joinder and accession agreements, guaranties, security and pledge agreements, mortgages and deeds of trust, deposit account control agreements, intercreditor and subordination agreements, compliance certificates, borrowing base certificates, notices of borrowing or prepayment, payoff letters, and releases.
- Treat schedules and exhibits bound into a document as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where none is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Credit agreement`, `Note`, `Amendment`, `Restatement`, `Waiver or consent`, `Forbearance`, `Joinder`, `Guaranty`, `Security agreement`, `Mortgage`, `Pledge`, `Account control`, `Intercreditor`, `Subordination`, `Compliance certificate`, `Borrowing base certificate`, `Notice`, `Payoff letter`, `Release`, or `Other`.
- Number amendments as the document numbers itself. Do not infer a sequence.
- **Where a waiver or forbearance appears, note in the evidence field what it waived.** A waiver is evidence that a covenant was breached, and it is often the only record of it.
- Where a document relates to a different facility, still list it and append ` [relates to [facility]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 25 lines and no more than 150 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Facility Type

- Native type: Classify
- Configured options, in UI order: `Revolving credit facility`, `Term loan`, `Delayed draw term loan`, `Promissory note`, `Asset-based revolver`, `Equipment or capital lease financing`, `Real estate mortgage loan`, `Mezzanine or subordinated debt`, `Shareholder or related-party loan`, `Letter of credit facility`, `Receivables or supply chain finance`, `Government or subsidised loan`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Original Commitment`, `Interest Rate`, `Amortization`
- Purpose: route the economics columns, since a revolver, a term loan, and a
  capital lease describe their amounts and rates differently.

```markdown
## Task

Classify the type of facility this review unit documents. Choose exactly one configured option.

## Classification rules

- Classify on the operative structure, not the title.
- `Revolving credit facility`: amounts may be drawn, repaid, and redrawn up to a commitment.
- `Asset-based revolver`: a revolver whose availability is limited by a borrowing base. **Distinguished because availability is a formula, not a number**, and the borrowing base certificate is the only statement of what can actually be drawn.
- `Term loan`: a single or multiple drawing repayable on a schedule, without redraw.
- `Delayed draw term loan`: a term loan drawable in tranches over a commitment period.
- `Promissory note`: a bilateral note, typically without the covenant architecture of a credit agreement.
- `Mezzanine or subordinated debt`: debt contractually or structurally junior to senior facilities. Note in the evidence field whether it carries warrants or equity features, since those interact with the Capitalization table.
- `Shareholder or related-party loan`: lent by a shareholder, founder, director, or affiliate. **Frequently repaid or capitalised at closing**, and it is also a related-party matter.
- `Government or subsidised loan`: lent or guaranteed by a public body, or carrying a subsidy or grant element. **These commonly carry change-of-control restrictions and clawback conditions that commercial facilities do not**, so the classification routes the reviewer to look for them.
- `Receivables or supply chain finance`: factoring, invoice discounting, or payables financing. Note in the evidence field whether it is disclosed or undisclosed and whether it is with or without recourse.

Where one agreement provides several tranches of different types, classify on the largest by commitment and report the others in the evidence field.

## Fallback rules

- Use `Other` where the structure is financing but none of the options describes it.
- Use `Unable to determine` where the operative terms are absent or illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Borrower

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which entity owes the money.

```markdown
## Task

State the borrower or obligor under this facility.

## Rules

- Report the name exactly as printed in the parties clause, including entity suffix.
- Use the review-subject list in the Table Instructions to determine whether it is a group entity.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- **Where the borrower name differs from any name used in a security agreement or a lien filing referenced in the unit, note that in the evidence field.** Name mismatches between the credit documents and the filings are where perfection problems live, and the Lien Filings table tests it directly.
- Where a later joinder or accession added a borrower, report the current borrowers and note the addition.
- Where the borrower is not on the review-subject list, report the name and append ` (not a listed entity)`. **A facility borrowed by an entity outside the acquired group may still be secured on the target's assets**, which is a different and worse problem.
- Where more than one borrower is jointly and severally liable, list each and note the joint and several character.

## Fallback rules

- Return `Unable to determine` where the borrower cannot be identified.

## Output format

`[Exact legal name]` per line, with any qualifier appended. Return no more than 40 words.
```

---

### 4. Obligor Group

- Native type: Free Response
- Upstream: none
- Downstream: `Obligors Inside Group`
- Purpose: everyone else on the hook — co-borrowers, guarantors, and pledgors.
  **Absent from the original schema**, and needed to confirm the transaction
  structure does not orphan a guaranty.

```markdown
## Task

List every party other than the primary borrower that is liable for, or has granted security for, this facility.

## Scope

- Include co-borrowers, co-obligors, guarantors, surety providers, and pledgors of collateral.
- Include any parent providing a guarantee, keep-well, comfort letter, or capital maintenance undertaking.
- Include any individual guarantor, including a founder or shareholder personal guarantee.
- Include any entity that has acceded by joinder.
- Exclude the agent, arranger, security trustee, and account bank.

## Rules

- Report each party's exact name and its role — co-borrower, guarantor, pledgor, or a combination.
- **Report the scope and any cap on each guarantee, since a capped guarantee is a materially different obligation from an unlimited one.**
- **Report any individual personal guarantee prominently.** These are frequently forgotten, they must be released at closing, and the individual will expect that release as a condition of cooperating.
- Report any guarantee stated to be limited to a stated amount, a stated tranche, or a stated period.
- Report any release mechanism — a covenant test, a stated date, or a disposal of the guarantor.
- Where a guaranty document for a named guarantor is not in the unit, note that; the Referenced but Not Produced column carries it.

## Fallback rules

- Return exactly `Borrower only` where no other party is liable or has granted security.
- Return `Unable to determine` where obligors conflict or are illegible.

## Output format

One line per party:

`[Exact name] — [role] — [scope or cap as stated] — [guaranty in unit: yes | no]`

Return no more than 10 lines and no more than 100 words.
```

---

### 5. Obligors Inside Group

- Native type: Classify
- Configured options, in UI order: `All obligors inside the acquired group`, `Seller or its affiliate is an obligor`, `An individual is an obligor`, `A third party is an obligor`, `Multiple external obligors`, `Borrower only`, `Unable to determine`
- Upstream: `@Obligor Group`
- Downstream: none
- Purpose: whether any obligation has to be replaced or released at closing.

**A guarantee from an entity or person that is not being acquired must be dealt
with at closing.** The seller will not leave it in place, the lender will not give
it up for nothing, and the fix is either a replacement guarantee from the buyer's
group or a payoff. Either way it is a closing item, and this column finds it.

```markdown
## Established result

- Obligor group: @Obligor Group

Use this result and the target group list in the Table Instructions. Confirm each party against the documents.

## Task

Classify whether every obligor and pledgor for this facility sits inside the acquired group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Borrower only`: Obligor Group returned `Borrower only`.
2. `Multiple external obligors`: more than one of the categories below applies.
3. `An individual is an obligor`: a natural person guarantees or has pledged collateral. **The individual's release is a closing condition** and it usually requires either a payoff or a replacement.
4. `Seller or its affiliate is an obligor`: the selling shareholder, its parent, or an affiliate outside the acquired group is an obligor. **The most common case in a carve-out** and it will always require replacement or payoff.
5. `A third party is an obligor`: an unrelated entity is an obligor.
6. `All obligors inside the acquired group`: every obligor and pledgor is a target entity on the review-subject list.

**Do not resolve a name variance by assuming.** Where an obligor's name is similar to a target entity but could be a different entity, treat it as external and note the similarity in the evidence field.

Report in the evidence field whether the documents provide any mechanism for releasing an external obligor, since a facility with an automatic release on a disposal is materially easier to deal with.

## Fallback rules

- Use `Unable to determine` where obligors cannot be identified or Obligor Group returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 6. Lender or Agent

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who has to be paid or asked. **The counterparty for the payoff letter
  and the consent request**, and the join key to the Lien Filings table.

```markdown
## Task

State the lender, lenders, or administrative agent for this facility.

## Rules

- Report the name exactly as printed, including entity suffix.
- **Where there is a syndicate, report the administrative agent and note in the evidence field whether a lender list or a register of lenders is in the unit.** The agent is who you deal with, but the consent thresholds in a syndicated facility depend on who the lenders actually are, and syndicates change hands without the borrower's involvement.
- Report each additional role separately where named: collateral agent, security trustee, issuing bank, swingline lender, account bank.
- **Where the facility has been assigned or transferred to a different lender, report the current holder and append ` (assigned from [prior lender], [YYYY-MM-DD])`.** A facility sold into a credit fund behaves very differently from one held by the originating bank, and the assignment notice may be the only evidence.
- Report any notice address or contact for consents and prepayments in the evidence field.
- **Report the lender name exactly, because it is the join key to the Lien Filings table** and a secured party name mismatch is how orphaned filings are found.

## Fallback rules

- Return `Unable to determine` where the lender cannot be identified.

## Output format

`[Role]: [exact legal name]` per line, with any qualifier appended. Return no more than 45 words.
```

---

### 7. Execution Status

- Native type: Classify
- Configured options, in UI order: `All documents executed`, `Principal agreement executed, security document unsigned`, `Principal agreement executed, guaranty unsigned`, `Principal agreement unsigned`, `Partially executed`, `Form or template`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: what the family proves about its own completion. **An unsigned security
  agreement grants nothing and an unsigned guaranty secures nothing**, and both
  appear in data rooms.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks in the current unit.

## Task

Classify the visible execution status of the documents in this review unit. Choose exactly one configured option.

## Scope

- The principal agreement is the credit agreement, note, or instrument creating the facility.
- Evaluate signature blocks, electronic-signature markers, conformed signatures, and counterpart pages visible in the documents.
- Exclude notary and witness blocks from the party count.
- **Treat each guaranty and each security or pledge agreement as requiring the signature of its own grantor.**

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the documents are unpopulated forms with bracketed placeholders or blank commercial terms.
2. `Principal agreement unsigned`: the principal agreement provides signature blocks and none bears a signature marker.
3. `Principal agreement executed, security document unsigned`: the principal agreement is signed and a security, pledge, or mortgage document in the unit is not. **The security interest may not have been granted at all**, which is a very different problem from a perfection defect.
4. `Principal agreement executed, guaranty unsigned`: the principal agreement is signed and a guaranty in the unit is not.
5. `Partially executed`: any document in the unit has at least one signed and at least one unsigned party signature block, other than the cases above.
6. `All documents executed`: every document in the unit bears a signature marker in every party signature block it provides.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated closing date is not a signature marker.

## Fallback rules

- Use `Unable to determine` where signature evidence exists but cannot be read, where a signature page is referenced but missing, or where documents conflict.
- Do not treat a lien filing, a funding notice, or a compliance certificate as evidence that the underlying document was signed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Principal agreement absent`, `Security document referenced but absent`, `Guaranty referenced but absent`, `Sequence gap`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: flag rows where the facility file is incomplete, so a reviewer knows
  before reading any term that the row may not show current terms.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether the facility file in this review unit appears complete. Choose exactly one configured option.

## Scope

- Consider documents constituting, amending, guaranteeing, or securing this facility.
- Exclude the lender's internal documents and third-party documents referenced for context.

## Classification rules

Apply the first rule that fits.

1. `Principal agreement absent`: the unit contains amendments, guaranties, or certificates but not the credit agreement, note, or instrument.
2. `Amendment referenced but absent`: a document in the unit refers to an amendment, waiver, consent, or restatement that is not present. **A compliance certificate reciting a covenant level that differs from the agreement is common evidence of this**, and it usually means a covenant was reset by an amendment nobody produced.
3. `Sequence gap`: amendments are numbered and a number in the sequence is missing.
4. `Security document referenced but absent`: the agreement requires or refers to a security agreement, pledge, mortgage, or account control agreement that is not present. **The collateral position cannot be read without it.**
5. `Guaranty referenced but absent`: a guarantor is named or a guaranty is required and the guaranty document is not present.
6. `Complete on its face`: the principal agreement is present, no amending document is missing, and each security document and guaranty the agreement requires is present.

`Complete on its face` states only that nothing in these documents reveals a gap.

## Fallback rules

- Use `Unable to determine` where a reference to a further document is too vague to tell whether it affects this facility, or where references are illegible.
- Do not use `Unable to determine` for a single unamended note with no security. That is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Original Commitment

- Native type: Free Response
- Upstream: `@Facility Type`
- Downstream: none
- Purpose: the size of the facility as committed, which is the ceiling rather than
  the amount owed.

```markdown
## Established result

- Facility Type: @Facility Type

## Task

Report the committed or principal amount of this facility.

## Rules by facility type

- `Revolving credit facility`, `Letter of credit facility`: the commitment amount, and any sublimit for letters of credit, swingline, or a currency.
- `Asset-based revolver`: the maximum commitment **and** the borrowing base formula as stated. **The commitment is not the availability**, and the formula is what determines what can be drawn.
- `Term loan`, `Delayed draw term loan`: the principal or commitment amount, and any tranche breakdown.
- `Promissory note`, `Mezzanine or subordinated debt`, `Shareholder or related-party loan`: the principal amount.
- `Equipment or capital lease financing`, `Receivables or supply chain finance`: the facility limit or the aggregate financed amount as stated.

## Rules

- Report the amount stated in the most recently dated document in the unit that states it, with the currency and the document and date.
- **Where an amendment increased or decreased the commitment, report the current amount and append ` (amended from [figure], [YYYY-MM-DD])`.**
- Report any accordion, incremental, or uncommitted increase facility separately, with its cap. **An accordion is capacity the buyer may inherit**, and it is not part of the commitment.
- Report multi-currency commitments as stated. **Do not convert.**
- **Do not total tranches, sublimits, or accordions**, and do not net anything.

## Fallback rules

- Return `Not stated` where no commitment or principal amount appears.
- Return `Incorporated terms` where the amount is stated to be set out in a schedule not present in the unit.
- Return `Unable to determine` where figures of the same date conflict.

## Output format

`[Figure] [currency] — per [document title], [YYYY-MM-DD]; tranches or sublimits: [as stated or "none"]; accordion: [as stated or "none"]`, with any qualifier appended.

Return no more than 60 words. Do not include totals you calculated.
```

---

### 10. Outstanding Balance Stated

- Native type: Free Response
- Upstream: none
- Downstream: `Balance As-Of Date`
- Purpose: **the payoff number, or the best available indication of it.**

The single most consequential figure in the table, and the one most likely to be
misused. Every figure here is reported as stated with its source, because the
closing funds flow must rest on a payoff letter rather than on anything derived in
a grid.

```markdown
## Task

Report every statement in this review unit of the amount outstanding under this facility.

## Rules

- **Report each figure separately with its source document, its date, and what it purports to measure** — principal outstanding, accrued interest, fees, letters of credit issued, or a total payoff amount.
- **Report a payoff letter figure first and label it as such**, since a payoff letter is a lender's binding quotation and is the only figure that belongs in a funds flow without further work.
- Report a compliance certificate or borrowing base figure as **the borrower's own statement**, not as a fact.
- For a revolver, report the drawn amount and any letters of credit issued separately, since undrawn commitment is not debt.
- **Do not calculate anything.** Do not accrue interest to any date, do not add principal and interest, do not total figures from different documents, do not net a revolver drawing against availability, and do not convert currency. If no document states a figure, the answer is `Not stated`.
- Where the most recent figure is materially different from an earlier one, report both. The movement is informative and reconciling it is the reviewer's job.

## Fallback rules

- Return `Not stated` where no document in the unit states an outstanding amount. **This is common and it is a coverage finding** — the payoff letter or the latest statement was not produced, and the funds flow cannot be built without it.
- Return `Unable to determine` where figures stated in documents of the same date conflict.

## Output format

One line per figure:

`[Figure] [currency] — [what it measures] — per [document title], [YYYY-MM-DD]`

Return no more than 6 lines and no more than 90 words. Do not include any figure you calculated.
```

---

### 11. Balance As-Of Date

- Native type: Date — confirm the type accepts `Not stated` and `Not applicable`
- Upstream: `@Outstanding Balance Stated`
- Downstream: none
- Purpose: the date the balance speaks as of. **A balance without a date is
  unusable**, and a stale one is worse than none because it looks authoritative.

```markdown
## Established result

- Outstanding balance stated: @Outstanding Balance Stated

## Task

If Outstanding Balance Stated reported one or more figures, identify the as-of date of the most recent figure.

If it returned `Not stated`, return exactly `Not applicable`.

If it returned `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the date the figure speaks as of, which is not necessarily the date of the document. **A payoff letter dated in March may quote a payoff good through a stated date in April; report the stated good-through date and note the letter's date in the evidence field.**
- Where a compliance certificate states a period end, use the period end rather than the certificate's signature date.
- Compare the reported date to the diligence as-of date in the Table Instructions and flag the gap:
  - more than one month: append ` [balance over 1 month old]`
  - more than three months: append ` [balance over 3 months old]`
- **A one-month threshold is deliberate.** On a revolver the balance moves weekly, and any figure more than a month old is indicative only. **No payoff should be built on a flagged figure** — a fresh payoff letter is required.
- Where a payoff letter states an expiry or good-through date that has passed, append ` [payoff quotation expired]`.

## Fallback rules

- Return `Not stated` where a figure is reported without any as-of date. **A dateless balance figure should not be relied on at all.**

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 12. Interest Rate

- Native type: Free Response
- Upstream: `@Facility Type`
- Downstream: none
- Purpose: the cost of the debt, and whether it moves. Relevant to whether the
  buyer would refinance rather than assume.

```markdown
## Established result

- Facility Type: @Facility Type

## Task

Report the interest rate or pricing applicable to this facility.

## Include where expressly stated

- The reference rate and the margin, as printed, for example `SOFR + 2.50%`
- **The reference rate's identity and any replacement or fallback mechanism.** Legacy facilities may still reference a discontinued benchmark, and the fallback language determines what applies now
- Any pricing grid linking the margin to a ratio or rating, with the levels as stated
- Any floor on the reference rate
- Any alternative base rate option, and any prime or base rate pricing
- Any fixed rate, and any period for which it is fixed
- Commitment fees, unused line fees, letter of credit fees, and utilisation fees
- Any upfront, arrangement, agency, or extension fee
- Any payment-in-kind or capitalised interest election
- Interest periods and payment dates
- Any hedging requirement, and any hedge in place referenced

## Rules

- Report the rate as printed. **Do not calculate an all-in rate, do not apply a pricing grid to any ratio, and do not accrue interest.**
- **Report any payment-in-kind feature prominently**, since capitalised interest increases the payoff amount over time and the stated principal understates the debt.
- **Report any hedging requirement**, since a swap breaking on prepayment is a cost and it is reported in Make-Whole or Defeasance.
- Where an amendment repriced the facility, report the current pricing and note the change.

## Fallback rules

- Return `Not stated` where no rate appears.
- Return `Incorporated terms` where pricing is stated to be set out in a schedule or fee letter not present in the unit. **A fee letter is routinely separate and routinely unproduced.**
- Return `Unable to determine` where rates conflict or are illegible.

## Output format

`Rate: [as printed]; floor: [as stated or "none"]; grid: [as stated or "none"]; fees: [brief]; PIK: [as stated or "none"]; hedging required: [yes | Not addressed]`

Return no more than 75 words.
```

---

### 13. Default Rate

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the rate becomes on a default, which sizes the cost of any
  covenant problem the transaction creates.

```markdown
## Task

Report the default rate of interest and any related consequence of non-payment.

## Include where expressly stated

- The default rate, as an increment over the applicable rate or as a stated rate
- Whether it applies automatically or only on the lender's election
- Whether it applies to all obligations or only to overdue amounts
- Whether it applies on any event of default or only on a payment default
- Any late payment fee or charge
- Any provision capitalising unpaid interest at the default rate

## Rules

- Report the rate as printed. **Do not calculate a resulting rate** or accrue anything.
- **Report whether the default rate applies to all obligations or only to the overdue amount.** The difference is large: a two percent uplift on an entire facility is a very different figure from the same uplift on a missed instalment.
- Report whether it applies automatically, since an automatic default rate can begin running before anyone notices the default.

## Fallback rules

- Return `Not addressed` where the documents state no default rate.
- Return `Incorporated terms` where it is stated to be set out in a document not present in the unit.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Rate: [as printed]; applies: [automatically | on election]; scope: [all obligations | overdue amounts only]; trigger: [any default | payment default only]; late fee: [as stated or "none"]`

Return no more than 55 words.
```

---

### 14. Maturity Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the facility must be repaid. **A maturity inside the deal period or
  shortly after closing is a refinancing the buyer inherits.**

```markdown
## Task

Identify the maturity or final repayment date of this facility.

## Rules

- Report the stated final maturity, termination, or expiry date from the most recently dated document in the unit that states one.
- Where an amendment extended or shortened maturity, report the current date and append ` (amended from [date], [YYYY-MM-DD])`.
- **Report any springing maturity separately in the evidence field** — a maturity that accelerates if another facility is not refinanced or repaid by a stated date. **A springing maturity can bring a distant maturity forward without anything else changing**, and it is the kind of term that surprises a buyer.
- Where different tranches have different maturities, report each and label it.
- **Where the documents state maturity by reference to a period from closing rather than a date, report the date only if a document states it.** Do not calculate.
- Compare the reported date to the diligence as-of date and flag it:
  - already passed: append ` [matured on record]`
  - within six months: append ` [matures within 6 months]`
  - within eighteen months: append ` [matures within 18 months]`
- **Where `[matured on record]` applies and no payoff or extension appears in the unit, this is a live default finding**, not merely a date.

## Output format

`YYYY-MM-DD`, with any bracketed flag or qualifier appended. Preserve partial precision as printed. Return `Not stated` where no maturity date can be reported without calculating.
```

---

### 15. Amortization

- Native type: Free Response
- Upstream: `@Facility Type`
- Downstream: none
- Purpose: the repayment profile, which determines the cash the business must
  service and how much is left at maturity.

```markdown
## Established result

- Facility Type: @Facility Type

## Task

Report the scheduled repayment profile of this facility.

## Applicability

- Applies to `Term loan`, `Delayed draw term loan`, `Promissory note`, `Real estate mortgage loan`, `Equipment or capital lease financing`, `Mezzanine or subordinated debt`, and `Shareholder or related-party loan`.
- For `Revolving credit facility`, `Asset-based revolver`, and `Letter of credit facility`, report any clean-down requirement or scheduled commitment reduction, and otherwise return `Not applicable — revolving`.
- For other types, report any schedule stated and otherwise return `Not applicable`.

## Include where expressly stated

- The instalment amount or percentage, and the frequency
- The amortisation schedule as printed, or its shape — level, stepped, or back-ended
- **Any balloon or bullet payment at maturity, and its amount.** A facility with minimal amortisation and a large bullet is a refinancing risk rather than a repayment plan
- Any interest-only period
- Any mandatory prepayment from excess cash flow, asset disposals, insurance proceeds, or debt or equity issuances, with the percentage
- Any cash sweep, and the sweep percentage and test
- Any clean-down requirement for a revolver, with the period and the level

## Rules

- **Report any mandatory prepayment from a disposal or an issuance prominently**, because it may be triggered by steps taken around the transaction itself.
- Report the schedule as stated. **Do not calculate a remaining balance, total the instalments, or compute a balloon from the schedule.**
- Where an amendment changed the schedule, report the current profile.

## Fallback rules

- Return `Not addressed` where the facility type amortises and the documents state no schedule.
- Return `Incorporated terms` where the schedule is in a document not present in the unit.
- Return `Unable to determine` where schedules conflict or are illegible.

## Output format

`Profile: [as stated]; instalments: [amount and frequency]; balloon: [as stated or "none"]; mandatory prepayments: [triggers and percentages]; cash sweep: [as stated or "none"]`

Return no more than 80 words. Do not include figures you calculated.
```

---

### 16. Financial Covenants

- Native type: Free Response
- Upstream: none
- Downstream: `Most Recent Tested Compliance`, `Equity Cure`
- Purpose: the tests the business must keep passing. **A covenant the transaction
  itself would breach is a consent item**, and one already close to its level is a
  post-closing constraint.

```markdown
## Task

Report the financial covenants this facility imposes.

## Include where expressly stated

- Each covenant by name — leverage, total net leverage, senior leverage, interest cover, fixed charge cover, debt service cover, minimum EBITDA, minimum liquidity, capital expenditure limit, minimum net worth, borrowing base coverage
- **The level required for each, and any step-down or step-up schedule with dates**
- The test frequency and the test dates
- **Whether the covenant is tested at all times or only on drawdown**, and for a revolver whether it is a springing covenant tested only above a stated utilisation
- The definition basis for any adjusted measure — whether EBITDA is defined with add-backs, and whether any add-back is capped
- Any covenant holiday, suspension, or waiver period stated
- Any pro forma or run-rate testing permitted

## Rules

- **Report the level and its step schedule as stated.** A covenant stepping down from 4.0x to 3.0x over two years is a tightening constraint, and the schedule is what tells a buyer when the pressure arrives.
- **Report whether the covenant is springing and at what utilisation.** A springing covenant on an undrawn revolver may never be tested, which is a materially different position.
- Report the add-back and adjustment definition in outline, since a permissive EBITDA definition changes what the level means. **Do not attempt to reproduce the full definition.**
- **Do not calculate or test any covenant, do not compute any ratio, and do not assess headroom.** Covenant testing is arithmetic against financial data and it belongs to the finance workstream.
- Where an amendment reset a level, report the current level and append ` (amended from [level], [YYYY-MM-DD])`. **An amendment resetting a covenant is usually evidence that it was about to be breached.**

## Fallback rules

- Return exactly `None` where the facility imposes no financial covenant. **Common in an asset-based or covenant-lite facility** and it is a real answer.
- Return `Incorporated terms` where the covenants are stated to be set out in a document not present in the unit.
- Return `Unable to determine` where covenants conflict or are illegible.

## Output format

One line per covenant:

`[Covenant] — [level and step schedule] — tested [frequency] — [always | springing at [utilisation]]`

Return no more than 8 lines and no more than 95 words. Do not include any calculation.
```

---

### 17. Most Recent Tested Compliance

- Native type: Free Response
- Upstream: `@Financial Covenants`
- Downstream: none
- Purpose: whether the covenants were being met, on the borrower's own statement.
  **A breach nobody flagged is a finding**, and a waiver in the file is evidence of
  one.

```markdown
## Established result

- Financial covenants: @Financial Covenants

## Task

If Financial Covenants reported one or more covenants, report the most recent compliance position the documents in this unit state.

If it returned `None`, return exactly `Not applicable`.

If it returned `Incorporated terms` or `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Report the position from the most recent compliance certificate, borrowing base certificate, or covenant statement in the unit, with the test date and the document.
- **Report the covenant level and the reported actual for each covenant, exactly as the certificate states them.** Do not calculate either, and do not compute headroom.
- **Report this as the borrower's own certification, not as a fact.** A compliance certificate is the borrower's calculation on its own definitions and it is not audited.
- **Report any breach, waiver, forbearance, or reservation-of-rights letter in the unit, with its date and what it related to.** A waiver is the clearest available evidence that a covenant was breached, and it is often the only record.
- **Report any certificate that reports compliance on a level differing from the agreement as amended**, and flag it: it usually means an amendment reset the covenant and was not produced.
- Compare the test date to the diligence as-of date. **Where the most recent certificate is more than one test period old, append ` [compliance evidence stale]`.**
- Where no certificate appears but the agreement requires them, say so under the fallback rules.

## Fallback rules

- Return `No compliance evidence in unit` where covenants exist and no certificate or statement was produced. **This is a coverage finding** — the certificates are required by the agreement, so they exist.
- Return `Unable to determine` where certificates conflict.

## Output format

One line per covenant:

`[Covenant] — required [level] — reported [actual] — as at [YYYY-MM-DD] per [document]`, then a final line: `Waivers or breaches: [brief or "none in unit"]`, with any bracketed flag appended.

Return no more than 8 lines and no more than 100 words. Do not include headroom or any calculation.
```

---

### 18. Equity Cure

- Native type: Classify
- Configured options, in UI order: `Equity cure permitted`, `Equity cure permitted with limits`, `Equity cure not permitted`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Financial Covenants`
- Downstream: none
- Purpose: whether a covenant breach can be fixed with cash rather than
  negotiated. **A cure right is a valuable option the buyer inherits**, and its
  limits determine how often it can be used.

```markdown
## Established result

- Financial covenants: @Financial Covenants

## Task

If Financial Covenants reported one or more covenants, classify whether the documents permit a financial covenant breach to be cured by an equity contribution.

If it returned `None`, return `Not applicable`.

If it returned `Incorporated terms` or `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

- `Equity cure permitted with limits`: a cure right subject to stated restrictions. **Report each limit in the evidence field** — the maximum number of cures over the life of the facility, the maximum in consecutive periods, a cap on the cure amount, whether the contribution must be applied to repay debt, and whether the cure counts toward EBITDA or reduces net debt. The limits are what determine whether the right is usable more than once.
- `Equity cure permitted`: a cure right with no material stated limit.
- `Equity cure not permitted`: the documents state expressly that no equity cure is available.

Report in the evidence field who may fund the cure — the sponsor, any shareholder, or the borrower's parent — since **a cure right exercisable only by a named sponsor may not be available to a new owner at all.**

## Fallback rules

- Use `Not addressed` where covenants exist and the documents say nothing about curing a breach.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Negative Covenants

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the business is prohibited from doing. **These constrain the
  buyer's plans directly if the facility survives closing**, and several of them
  are engaged by the transaction itself.

```markdown
## Task

Report the negative covenants and restrictions this facility imposes on the borrower and its group.

## Include where expressly stated

- Restrictions on incurring debt, granting liens, and giving guarantees
- **Restrictions on disposing of assets, and any threshold above which consent is required**
- Restrictions on acquisitions, investments, joint ventures, and loans
- **Restrictions on mergers, consolidations, reorganisations, and changes to corporate structure.** These are frequently engaged by pre-closing or post-closing restructuring steps rather than by the transaction itself
- Restrictions on changing the nature of the business, or on entering a new line of business
- Restrictions on affiliate and related-party transactions
- Restrictions on amending constitutional documents or material contracts
- Restrictions on changing accounting policies or the fiscal year
- Restrictions on capital expenditure
- Restrictions on entering into hedging or speculative transactions
- Any covenant to maintain a listing, a rating, or a stated ownership structure

## Rules

- Report each covenant in eight words or fewer, **with the threshold or basket where one is stated.** A prohibition subject to a large basket is a different constraint from an absolute one.
- **Report the merger and reorganisation restriction prominently**, since it is the covenant most often engaged by transaction steps a buyer plans without thinking of the debt.
- **Report any covenant to maintain a stated ownership structure**, which functions as a change-of-control restriction even where the change-of-control clause does not reach the transaction.
- Report no more than ten covenants. Where more exist, report the ten most constraining and append ` and [N] further covenants`.
- Report the covenants as stated. **Do not assess whether any planned step would breach one.**

## Fallback rules

- Return exactly `None` where the facility imposes no negative covenant.
- Return `Incorporated terms` where the covenants are in a document not present in the unit.
- Return `Unable to determine` where covenants conflict or are illegible.

## Output format

One line per covenant:

`[Covenant] — [threshold or basket, or "absolute"]`

Return no more than 10 lines and no more than 100 words.
```

---

### 20. Restricted Payments

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether cash can leave the group. **Determines whether the buyer can
  extract dividends, repay shareholder debt, or fund the acquisition group
  post-closing**, and it is routinely overlooked until it matters.

```markdown
## Task

Report the restrictions this facility imposes on payments to shareholders and on cash leaving the obligor group.

## Include where expressly stated

- Restrictions on dividends and distributions, and any permitted basket or amount
- Restrictions on share buybacks, redemptions, and returns of capital
- **Restrictions on repaying or prepaying shareholder, parent, or subordinated debt**
- Restrictions on management fees, monitoring fees, or payments to affiliates
- Restrictions on upstreaming cash, making intercompany loans, or transferring assets to non-obligors
- Any condition on making a restricted payment — a covenant test, a leverage level, pro forma compliance, or no default subsisting
- Any available amount, builder basket, or restricted payment basket, with its calculation basis as stated
- Any permitted tax distribution for a pass-through entity
- **Any cash pooling, sweep, or deposit concentration arrangement in favour of the lender**

## Rules

- **Report the conditions on a permitted payment as carefully as the prohibition.** A dividend basket conditional on leverage below a level is unavailable precisely when the buyer most wants it.
- **Report any restriction on repaying shareholder debt prominently**, since repaying or capitalising shareholder loans at closing is a routine step and this covenant can block it.
- **Report any restriction on transferring assets or cash to non-obligors**, which constrains post-closing integration and cash management across a wider buyer group.
- Report baskets and levels as stated. **Do not calculate an available amount.**

## Fallback rules

- Return exactly `None` where the facility imposes no restriction on payments to shareholders.
- Return `Incorporated terms` where the provisions are in a document not present in the unit.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Dividends: [as stated]; buybacks: [as stated]; shareholder debt repayment: [as stated]; affiliate payments: [as stated]; conditions: [brief]; basket: [as stated or "none"]; cash pooling: [as stated or "none"]`

Return no more than 85 words.
```

---

### 21. Permitted Debt and Liens

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the headroom for further borrowing and security. **Determines whether
  acquisition debt can sit alongside this facility** or whether it has to be
  refinanced.

```markdown
## Task

Report the permitted debt and permitted lien capacity this facility allows.

## Include where expressly stated

- Permitted debt baskets, with amounts and any ratio-based capacity
- Any general or basket amount for debt not otherwise permitted
- Permitted purchase money, equipment, and capital lease debt, with limits
- Permitted intercompany debt, and any subordination requirement attached
- Permitted guarantees
- **Any incremental or accordion facility capacity, and the conditions on using it**
- Permitted lien baskets and categories, including statutory, tax, landlord, and purchase money liens
- Any negative pledge, and whether it extends to all assets or only to specified ones
- **Any most-favoured-lender or pari passu provision requiring this facility to be given terms matching any new debt**
- Any restriction on debt at a parent or holding company level

## Rules

- **Report the ratio-based capacity separately from fixed baskets**, since ratio capacity moves with performance and a fixed basket does not.
- **Report any most-favoured-lender provision prominently**, since it can force terms from new acquisition debt back into this facility.
- **Report any restriction reaching parent or holdco debt**, which is where acquisition debt usually sits.
- Report baskets and levels as stated. **Do not total baskets or calculate available capacity.**

## Fallback rules

- Return exactly `None stated` where the facility imposes no restriction on further debt or liens.
- Return `Incorporated terms` where the provisions are in a document not present in the unit.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Debt baskets: [as stated]; ratio capacity: [as stated or "none"]; accordion: [as stated or "none"]; lien baskets: [as stated]; negative pledge: [scope]; MFL provision: [yes | Not addressed]; holdco debt: [as stated or "Not addressed"]`

Return no more than 85 words.
```

---

### 22. Reporting and Information Covenants

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the recurring obligations the buyer inherits, and the notifications the
  transaction itself triggers.

```markdown
## Task

Report the reporting and information obligations this facility imposes.

## Include where expressly stated

- Annual audited financial statements, and the delivery deadline
- Quarterly or monthly management accounts, and their deadlines
- Compliance certificates, and their frequency
- Borrowing base certificates, and their frequency
- Budgets, forecasts, or business plans required
- Any requirement to deliver auditors' management letters or reports
- **Event-driven notifications, and the period for each**: default or potential default, litigation above a threshold, change of control, change of auditors, material adverse change, ERISA or pension events, environmental incidents, and loss of a material contract or licence
- Any requirement to permit lender inspection, field examination, or audit, and who bears the cost
- Any requirement to hold lender meetings or calls
- Any requirement to notify a change in the obligor group or the corporate structure

## Rules

- **Report the event-driven notifications separately from the periodic ones, with the period for each.** These are what the transaction triggers, and a change-of-control notification obligation is separate from the change-of-control default and may bite even where the default does not.
- **Report any obligation to notify a change of auditors or a change in structure**, since post-closing integration commonly triggers them.
- **Report any field examination or inspection right with its cost bearer**, since it is an intrusive and recurring cost, particularly in asset-based facilities.
- Report periods and frequencies as stated. Do not calculate deadlines.

## Fallback rules

- Return exactly `None stated` where the facility imposes no reporting obligation.
- Return `Incorporated terms` where the obligations are in a document not present in the unit.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

`Periodic: [obligation — deadline]` per line, then `Event-driven: [event — period]` per line.

Return no more than 10 lines and no more than 100 words.
```

---

### 23. Change of Control Consequence

- Native type: Classify
- Configured options, in UI order: `Event of default`, `Mandatory prepayment`, `Put right or offer to repay`, `Consent required`, `Notice required`, `Commitment termination`, `Addressed, no consequence`, `Not addressed`, `Incorporated terms`, `Unable to determine`
- Upstream: none
- Downstream: `CoC Definition and Threshold`, `CoC Language`
- Purpose: what the transaction does to this facility. **The column the payoff and
  consent schedule is built from.**

```markdown
## Task

Classify what a change of control of the borrower or its parent triggers under this facility. Choose exactly one configured option.

## Scope

- Consider provisions triggered by a change in ownership, voting control, or board control of the borrower, a guarantor, or a parent.
- Include provisions triggered by a sale of all or substantially all assets where the documents treat it as a change of control.
- Exclude general merger and disposal covenants, which are reported in Negative Covenants.
- Where a later document in the unit changes the provision, classify on the most recently dated document that addresses it.

## Classification rules

Apply the first rule that fits.

1. `Event of default`: a change of control is an event of default, entitling the lender to accelerate. **The most severe form** and it puts the facility on the payoff schedule unless the lender consents.
2. `Mandatory prepayment`: the facility must be repaid on or within a stated period of a change of control, without the lender electing. Functionally a payoff, with a defined timetable.
3. `Put right or offer to repay`: the borrower must offer to repay and the lender may accept or decline. Common in note structures. **Report the offer period in the evidence field**, since it is a hard post-closing deadline.
4. `Commitment termination`: commitments terminate or availability ceases on a change of control, without existing drawings becoming due.
5. `Consent required`: the change of control requires the lender's prior consent, with no automatic default.
6. `Notice required`: notification only, with no consent, prepayment, or default.
7. `Addressed, no consequence`: change of control is defined or referenced with no consequence attached.

**Where a change of control both defaults the facility and requires prepayment, classify as `Event of default`** and describe both in the Language column.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses a change of control. **Uncommon in a credit agreement and worth checking against Chain Completeness** — it usually means the relevant section was not produced.
- Use `Incorporated terms` where the treatment is stated to be governed by a document not present in the unit.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. CoC Definition and Threshold

- Native type: Free Response
- Upstream: `@Change of Control Consequence`
- Downstream: none
- Purpose: whether the deal as structured actually trips the clause.

```markdown
## Established result

- Change of control consequence: @Change of Control Consequence

## Task

If Change of Control Consequence is any value other than `Not addressed`, `Incorporated terms`, or `Unable to determine`, report the definition and threshold of change of control.

If it is `Not addressed` or `Incorporated terms`, return exactly `Not applicable`.

If it is `Unable to determine`, return exactly `Unable to determine`.

## Include where expressly stated

- **The percentage of shares, voting power, or economic interest at which the provision triggers, and of which entity**
- Whether the provision reaches direct ownership only, or indirect and ultimate ownership
- **Whether the provision is triggered by a person acquiring control, or by a named person or sponsor ceasing to hold control.** The second form is very common in sponsor-backed facilities and it fires on the seller's exit regardless of who the buyer is
- Any board composition test — a change in a majority of the board, or the loss of a right to appoint
- Any test based on the ability to direct management and policies
- Any aggregation of holdings of connected persons or persons acting in concert
- Any permitted holder or permitted transferee carve-out, and who qualifies
- Any carve-out for an internal reorganisation, a listing, or a transfer among existing holders

## Rules

- **Report the permitted holder carve-out and its definition prominently.** A permitted holder concept that covers the existing sponsor and its affiliates will not cover a new buyer, and that is usually the whole answer.
- **Report the cessation-of-control form separately where present**, since a provision triggered by the sponsor ceasing to hold a stated percentage fires on any exit.
- Report the threshold and its base exactly as printed.
- **Do not state whether this transaction crosses the threshold.** That requires the ownership chain and the deal structure.

## Output format

`Threshold: [percentage] of [base]; reaches: [direct only | indirect and ultimate]; form: [acquisition of control | cessation of control by named holder | both]; board test: [as stated or "none"]; permitted holders: [as stated or "none"]; carve-outs: [brief or "none"]`

Return no more than 85 words.
```

---

### 25. CoC Language

- Native type: Verbatim
- Upstream: `@Change of Control Consequence`
- Downstream: none
- Purpose: the exact text, which the consent request or the payoff decision is
  taken on.

```markdown
## Established result

- Change of control consequence: @Change of Control Consequence

## Task

If Change of Control Consequence is any value other than `Not addressed`, `Incorporated terms`, or `Unable to determine`, quote the change of control provision exactly as written.

If it is `Not addressed` or `Incorporated terms`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever change of control language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the definition of Change of Control in full, including every limb, every threshold, and every carve-out**, where the definition appears in the unit. Whether this transaction falls inside it is decided there.
- **Quote the definition of any Permitted Holder, Permitted Transferee, or equivalent term the definition relies on.**
- Quote the operative consequence — the default, prepayment, put right, or consent requirement — including any grace period or offer period.
- Where the combined text exceeds 250 words, quote every limb and carve-out of the definition and the operative consequence, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction triggers the provision.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 26. Assignment by Borrower

- Native type: Classify
- Configured options, in UI order: `Prohibited absolutely`, `Consent required`, `Permitted to a successor`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the facility can move with the business in an asset deal or a
  reorganisation. **Distinct from the change-of-control question**, which is about
  the owner changing rather than the obligor.

```markdown
## Task

Classify whether the borrower may assign or transfer its obligations under this facility. Choose exactly one configured option.

## Scope

- Consider restrictions on the borrower assigning, transferring, or novating its rights or obligations.
- Consider any provision permitting an obligor to be substituted or released.
- **Exclude the lender's own right to assign or transfer**, which is reported in the evidence field.
- Exclude the change-of-control provision.

## Classification rules

- `Permitted to a successor`: the borrower may transfer to a successor by merger or to a purchaser of the business, whether or not on conditions.
- `Consent required`: transfer requires the lender's consent.
- `Prohibited absolutely`: no transfer is permitted, with no consent mechanism. **In an asset deal this means the facility cannot move and must be repaid.**

Report in the evidence field the lender's own assignment rights: whether the lender may transfer freely, whether borrower consent is required, and whether any transfer to a competitor or a distressed investor is restricted. **A facility freely transferable by the lender may end up held by someone with different objectives**, and a borrower consent right over transfers is worth knowing about.

## Fallback rules

- Use `Not addressed` where the documents do not address borrower assignment.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 27. Cross-Default and Cross-Acceleration

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether a problem elsewhere brings this facility down. **One tripped
  facility can cascade across the whole debt stack**, and the thresholds determine
  how easily.

```markdown
## Task

Report any cross-default, cross-acceleration, or related provision in this facility.

## Include where expressly stated

- Whether the provision is cross-**default** or cross-**acceleration**, and to which other obligations it applies
- **The monetary threshold above which other debt triggers it**
- Whether it applies to debt of the borrower only, or of any obligor or group member
- Whether it applies to any indebtedness, or only to financial indebtedness as defined
- Whether it extends to hedging obligations, capital leases, or guarantees
- Any grace period before the cross provision operates
- Any judgment default provision, with its threshold
- Any insolvency-related event of default and the events it covers
- Any ERISA, pension, or employee plan event of default
- Any material adverse change event of default, noting that it is also reported in its own column

## Rules

- **Report whether it is cross-default or cross-acceleration, since the difference is substantial.** Cross-default fires on a mere default under other debt; cross-acceleration only if the other lender actually accelerates, which is a much higher bar and a much better position for the borrower.
- **Report the threshold as stated**, since a low threshold makes any minor dispute with any creditor a potential default here.
- Report whether it reaches other group members, which determines whether a problem in a non-obligor subsidiary can trip this facility.
- Report the provisions as stated. **Do not assess whether any other facility is in default.**

## Fallback rules

- Return exactly `None` where the facility contains no cross provision.
- Return `Incorporated terms` where the provisions are in a document not present in the unit.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Type: [cross-default | cross-acceleration | both]; threshold: [as stated]; scope: [borrower | obligors | group]; grace: [as stated or "none"]; judgment default: [threshold or "none"]; other defaults: [brief]`

Return no more than 80 words.
```

---

### 28. MAC or MAE Clause

- Native type: Classify
- Configured options, in UI order: `MAC event of default`, `MAC drawdown condition only`, `MAC representation only`, `Both default and drawdown condition`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the lender has a discretionary exit. **A MAC event of default
  gives the lender a route to accelerate on a judgement call**, which matters most
  precisely when the business is under pressure.

```markdown
## Task

Classify whether and how this facility uses a material adverse change or material adverse effect provision. Choose exactly one configured option.

## Scope

- Consider any provision referring to a material adverse change, material adverse effect, or materially adverse development in the business, assets, condition, or prospects of the borrower or its group.
- Distinguish where the concept appears: as an event of default, as a condition to drawdown, or as a representation repeated on each drawdown.

## Classification rules

- `MAC event of default`: a material adverse change is itself an event of default. **The most consequential form**, because it is a discretionary acceleration right resting on the lender's judgement.
- `Both default and drawdown condition`: the concept appears both as a default and as a drawdown condition.
- `MAC drawdown condition only`: the absence of a material adverse change is a condition to further drawings. **On a revolver this can cut off liquidity without any default being declared**, which is often the first practical consequence.
- `MAC representation only`: a repeated representation that no material adverse change has occurred, without a standalone default.

Report in the evidence field whether the definition includes prospects, whether it is qualified by reference to the lender's opinion, and whether any carve-outs are stated. **A MAC determinable in the lender's sole opinion is materially wider** than one requiring an objective change, and a definition reaching prospects is wider than one limited to financial condition.

## Fallback rules

- Use `Not addressed` where the documents contain no material adverse change concept.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 29. Prepayment Terms

- Native type: Free Response
- Upstream: none
- Downstream: `Make-Whole or Defeasance`
- Purpose: whether the facility can be repaid at closing, and what that costs.
  **The core input to the decision to repay rather than seek consent.**

```markdown
## Task

Report the terms on which this facility may be voluntarily prepaid.

## Include where expressly stated

- Whether voluntary prepayment is permitted, and from what date
- Any lock-out or non-call period during which prepayment is prohibited
- Any minimum prepayment amount or increment
- The notice period required for prepayment
- **Any prepayment premium, call premium, or exit fee, and any step-down schedule**
- Any make-whole or yield maintenance requirement, which is reported in detail in the next column
- Whether prepayment permanently reduces the commitment or may be redrawn
- Any breakage or funding-loss cost for prepaying within an interest period
- Any requirement to pay accrued interest and fees on prepayment
- Whether prepayments apply to instalments in a stated order
- Any provision for prepayment out of the proceeds of a change of control at par

## Rules

- **Report the premium and any step-down schedule as stated.** A facility callable at 102 falling to par over two years has a very different closing cost depending on when the deal completes.
- **Report any lock-out or non-call period prominently.** Where prepayment is prohibited outright, the facility cannot be repaid at closing and consent becomes the only route.
- Report breakage costs, since prepaying mid-period carries a cost even where no premium applies.
- Report amounts and percentages as stated. **Do not calculate a premium or a total payoff.**

## Fallback rules

- Return `Not addressed` where the documents do not address voluntary prepayment.
- Return `Incorporated terms` where the terms are in a document not present in the unit.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Permitted: [as stated]; lock-out: [as stated or "none"]; premium: [as stated and step-down schedule]; notice: [period]; minimum: [as stated]; breakage: [as stated or "none"]; redrawable: [yes | no]`

Return no more than 80 words. Do not include any figure you calculated.
```

---

### 30. Make-Whole or Defeasance

- Native type: Free Response
- Upstream: `@Prepayment Terms`
- Downstream: none
- Purpose: the expensive and slow ways out. **A defeasance requirement is a
  timetable item, not just a cost** — it takes weeks, involves third parties, and
  cannot be done at short notice.

```markdown
## Established result

- Prepayment terms: @Prepayment Terms

## Task

If Prepayment Terms reported prepayment provisions, report any make-whole, yield maintenance, defeasance, or equivalent requirement.

If it returned `Not addressed`, report any such requirement stated elsewhere in the documents, and where none return exactly `None`.

If it returned `Incorporated terms` or `Unable to determine`, return exactly `Unable to determine`.

## Include where expressly stated

- Any make-whole or yield maintenance amount, and the formula for calculating it
- The discount rate or reference used in the formula, as stated
- **Any defeasance requirement, including whether it is legal or economic defeasance**, and what must be deposited
- Any requirement to substitute collateral or deposit securities
- Any requirement to involve a defeasance consultant, servicer, rating agency, or trustee
- **Any stated period required to complete a defeasance**
- Any fee payable to a servicer, trustee, or consultant
- Any hedge or swap breakage payable on prepayment, and how it is determined
- Any assumption alternative permitting a purchaser to take over the debt instead of repaying it, and any assumption fee or approval requirement

## Rules

- **Report the formula as printed and do not calculate the amount.** A make-whole depends on rates at the prepayment date and cannot be computed from the documents.
- **Report any defeasance requirement prominently, with its stated period.** Defeasance is common in securitised real estate lending, it is expensive, and it involves parties who work to their own timetables. **Discovering it late can move a closing date.**
- **Report any assumption alternative prominently**, since assuming the debt may be far cheaper than defeasing it and it changes the structure discussion.
- Report any swap breakage, since an in-the-money hedge for the lender is a real cost on early termination.

## Fallback rules

- Return exactly `None` where no make-whole, yield maintenance, or defeasance requirement applies.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Make-whole: [formula as stated or "none"]; defeasance: [type, requirements, period, or "none"]; third parties: [as stated]; fees: [as stated]; hedge breakage: [as stated or "none"]; assumption alternative: [as stated or "none"]`

Return no more than 85 words. Do not include any figure you calculated.
```

---

### 31. Collateral Description

- Native type: Free Response
- Upstream: none
- Downstream: `Excluded Assets`, `IP Included in Collateral`
- Purpose: what the lender holds security over, which determines what has to be
  released at closing.

```markdown
## Task

Report the collateral securing this facility, as described in the documents.

## Include where expressly stated

- Whether the security is over all assets or over specified categories
- The asset categories secured: accounts receivable, inventory, equipment, deposit accounts, investment property, general intangibles, intellectual property, real property, and equity interests
- **Any pledge of equity in subsidiaries, and whether it extends to all or only to specified subsidiaries.** A share pledge means the lender can take the shares of an entity the buyer is acquiring, and it must be released
- Any specified real property, by address
- Any specific equipment, vehicles, or assets identified by schedule or serial number
- Any assignment of rents, leases, insurance proceeds, or contract rights
- Any control agreement over a deposit or securities account, which is also reported in its own column
- Whether the security is a first or a junior ranking, as stated
- Any guarantee supported by security from a guarantor
- Any cash collateral or reserve held

## Rules

- **Report an all-assets grant as such, and then report the exclusions in the next column.** The exclusions are what define the perimeter, and an all-assets description on its own conveys little.
- **Report any equity pledge prominently, naming the pledged entities.** These are the releases most likely to be forgotten and most likely to block a transfer of shares at closing.
- Report the ranking as stated.
- Report the description as stated. **Do not assess perfection, priority, or enforceability**, and do not judge whether the description is adequate.

## Fallback rules

- Return exactly `Unsecured` where the documents state the facility is unsecured or grant no security.
- Return `Incorporated terms` where the collateral is described in a security agreement not present in the unit. **This is a significant gap** and it is reported in Referenced but Not Produced.
- Return `Unable to determine` where descriptions conflict or are illegible.

## Output format

`Grant: [all assets | specified]; categories: [list]; equity pledged: [entities or "none"]; real property: [addresses or "none"]; ranking: [as stated]; cash collateral: [as stated or "none"]`

Return no more than 85 words.
```

---

### 32. Excluded Assets

- Native type: Free Response
- Upstream: `@Collateral Description`
- Downstream: none
- Purpose: what the security does **not** reach. **In an all-assets grant the
  exclusions are the only thing that defines the perimeter**, and they are
  frequently more informative than the grant.

```markdown
## Established result

- Collateral description: @Collateral Description

## Task

If Collateral Description reported security, report the assets expressly excluded from it.

If it returned `Unsecured`, return exactly `Not applicable`.

If it returned `Incorporated terms` or `Unable to determine`, return exactly `Unable to determine`.

## Include where expressly stated

- Any asset category expressly excluded from the grant
- **Any exclusion of assets whose transfer or encumbrance would breach a contract, licence, or law.** This is standard and it means the security does not reach contracts with anti-assignment provisions, which can be a large part of the value
- Any exclusion of intellectual property, or of applications for intellectual property
- Any exclusion or limitation on the pledge of equity in foreign subsidiaries, including a stated percentage limit
- Any exclusion of specified real property, motor vehicles, or aircraft
- Any exclusion of deposit accounts below a stated threshold, or of payroll and trust accounts
- Any exclusion of assets subject to prior permitted liens
- Any exclusion of leasehold interests
- Any threshold below which assets need not be perfected or brought into the collateral

## Rules

- **Report the contract-breach exclusion where present.** It is standard drafting and its practical effect is significant: a security interest that does not reach the target's key customer contracts is a much weaker package than an all-assets grant suggests.
- **Report any percentage limit on a foreign subsidiary equity pledge**, since a partial pledge still requires a release.
- **Report any perfection threshold**, since assets below it may be within the grant but unperfected — a different problem from being excluded.
- Report the exclusions as stated. **Do not assess their effect on the lender's position.**

## Fallback rules

- Return exactly `None stated` where the documents state no exclusion. **For an all-assets grant this is unusual** and worth checking against Chain Completeness, since exclusions usually sit in a security agreement schedule.

## Output format

One line per exclusion category:

`[Exclusion as stated]`

Return no more than 10 lines and no more than 95 words.
```

---

### 33. IP Included in Collateral

- Native type: Classify
- Configured options, in UI order: `IP secured, recordation evidenced`, `IP secured, no recordation evidenced`, `IP secured, applications excluded`, `IP expressly excluded`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Collateral Description`
- Downstream: none
- Purpose: whether the lender has security over the core asset. **A security
  interest in core IP interacts directly with the IP workstream** and it must be
  released before the buyer's own financing can attach.

```markdown
## Established result

- Collateral description: @Collateral Description

## Task

If Collateral Description reported security, classify whether it extends to intellectual property.

If it returned `Unsecured`, return `Not applicable`.

If it returned `Incorporated terms` or `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `IP expressly excluded`: the documents exclude intellectual property from the collateral.
2. `IP secured, applications excluded`: IP is secured but pending applications, or specified categories, are excluded. **Common, because granting security over a trademark application can jeopardise it in some jurisdictions**, and the exclusion is deliberate.
3. `IP secured, recordation evidenced`: IP is secured and the unit contains evidence of recordation with the relevant IP office — a recorded security agreement, a recordation confirmation, or a reel and frame reference.
4. `IP secured, no recordation evidenced`: IP is secured and nothing in the unit evidences recordation. **This is the finding.** It means either that recordation was never made, or that the confirmation was not produced, and the IP Registrations table's `Encumbrances of Record` column is where it is tested.

Report in the evidence field which IP categories are secured — patents, trademarks, copyrights, domains, trade secrets, and software — and whether the grant includes proceeds and licence royalties.

**Cross-reference:** every row classified as secured should correspond to an encumbrance in the IP Registrations table, and any mismatch in either direction is a finding.

## Fallback rules

- Use `Not addressed` where the collateral description neither includes nor excludes IP.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 34. Deposit Account Control

- Native type: Classify
- Configured options, in UI order: `Springing control on default`, `Full control, blocked account`, `Cash dominion in place`, `Control agreements required, not evidenced`, `No account control`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the lender controls the cash. **Determines whether the business
  can operate normally after a default**, and every control agreement is a release
  and a re-documentation task at closing.

```markdown
## Task

Classify the lender's control over the borrower's bank accounts and cash. Choose exactly one configured option.

## Scope

- Consider deposit account control agreements, blocked account agreements, lockbox arrangements, cash dominion provisions, and any requirement to maintain accounts with the lender.
- Consider any requirement to sweep collections to a lender-controlled account.

## Classification rules

Apply the first rule that fits.

1. `Cash dominion in place`: collections are swept to a lender-controlled account and applied to the facility on an ongoing basis. **Standard in asset-based lending**, and it means the business's cash cycle runs through the lender daily. Replacing it at closing is a substantial operational exercise.
2. `Full control, blocked account`: the lender has present control over specified accounts, with the borrower's access restricted.
3. `Springing control on default`: control agreements are in place but the lender may only exercise control after a default. **The common arrangement** — the agreements exist and must be released, but day-to-day operations are unaffected.
4. `Control agreements required, not evidenced`: the facility requires control agreements and none appears in the unit. Report the accounts covered in the evidence field.
5. `No account control`: the facility requires no control over accounts.

Report in the evidence field the number of accounts covered where stated, the banks involved, any threshold below which accounts are excluded, and any requirement to maintain primary banking with the lender. **A requirement to bank with the lender is a relationship the buyer may not want to keep**, and unwinding it is a separate task from the payoff.

## Fallback rules

- Use `Not addressed` where the documents do not address account control.
- Use `Unable to determine` where provisions conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 35. Intercreditor and Subordination

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where this facility sits in the stack, and who controls enforcement.
  **Determines the order of payoff and whose consent is needed for what.**

```markdown
## Task

Report any intercreditor, subordination, or ranking arrangement affecting this facility.

## Include where expressly stated

- Whether this facility is senior, pari passu, second lien, or subordinated, and to what
- The parties to any intercreditor agreement, and whether that agreement is in the unit
- **Any payment blockage or standstill provision, and its trigger and duration**
- Any turnover obligation requiring a junior creditor to hand over recoveries
- Any restriction on a junior creditor enforcing, accelerating, or suing
- Any waterfall or order of application of enforcement proceeds
- **Which creditor group controls enforcement and instructs the security agent**
- Any restriction on amending this facility without another creditor's consent
- Any restriction on refinancing or repaying this facility ahead of another
- Any subordination of shareholder or intercompany debt, and any deed of subordination
- Any purchase or buy-out option in favour of a junior creditor

## Rules

- **Report any restriction on repaying this facility ahead of another prominently.** It can prevent a payoff at closing even where the facility itself permits prepayment, which is exactly the kind of constraint that is discovered late.
- **Report which group controls enforcement**, since that determines whose consent actually matters in a negotiation.
- **Report any restriction on amending this facility without third-party consent**, since it adds a party to any transaction-related waiver or consent.
- Report any subordination of shareholder debt, since repaying or capitalising it at closing is a routine step this can block.

## Fallback rules

- Return exactly `None` where no intercreditor or subordination arrangement is referenced.
- Return `Referenced but not produced` where an intercreditor agreement is referenced and absent. **A significant gap**, since the ranking and control provisions cannot be read.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Ranking: [as stated]; intercreditor parties: [as stated]; in unit: [yes | no]; standstill: [trigger and duration or "none"]; enforcement control: [as stated]; amendment consent: [as stated or "none"]; shareholder debt subordinated: [yes | Not addressed]`

Return no more than 85 words.
```

---

### 36. Payoff and Release Mechanics

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how the facility is actually discharged and the security actually
  released. **The operational detail the closing checklist is built from.**

```markdown
## Task

Report the mechanics for repaying this facility and obtaining release of the security and guarantees.

## Include where expressly stated

- Any requirement or process for obtaining a payoff letter, and any period the lender requires
- Any notice period for a full prepayment or termination
- **What the lender must deliver on payoff**: releases, terminations of lien filings, reconveyances, terminations of control agreements, discharges of guarantees, and returned notes or share certificates
- **Whether the lender is obliged to file lien terminations itself, or whether the borrower may file them**
- Any period within which the lender must deliver releases
- Any requirement for the lender to return pledged share certificates, stock powers, or original notes
- Any escrow, holdback, or indemnity the lender requires as a condition of release
- Any continuing indemnity or reimbursement obligation surviving payoff
- Any letters of credit that must be cash collateralised or replaced rather than simply repaid
- Any provision for release of a guarantor or of specified collateral short of full repayment
- **Any payoff letter, release, or termination already in the unit**

## Rules

- **Report any letters of credit outstanding, since they cannot be repaid — they must be replaced or cash collateralised**, and that is a separate arrangement with the buyer's own bank on its own timetable.
- **Report whether the lender or the borrower files the lien terminations.** Where the lender is not obliged to file, the terminations are the buyer's task and they are routinely missed, leaving stale filings on the register.
- **Report any obligation surviving payoff**, since a discharged facility can still leave an indemnity in place.
- Report any release already in the unit with its date and what it covered.

## Fallback rules

- Return `Not addressed` where the documents do not address payoff or release mechanics.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Payoff letter process: [as stated or "Not addressed"]; notice: [period]; lender deliverables: [list]; filing responsibility: [lender | borrower | Not addressed]; LCs outstanding: [as stated or "none"]; surviving obligations: [brief or "none"]; releases in unit: [as stated or "none"]`

Return no more than 90 words.
```

---

### 37. Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the governing law, which for a multi-jurisdictional security package
  may differ between the credit agreement and each security document.

```markdown
## Task

Identify the governing law of this facility and of its security documents.

## Rules

- Report the governing law of the principal credit agreement or instrument as stated.
- **Report separately the governing law of each security document where it differs.** Security over assets in another jurisdiction is normally governed by the law of that jurisdiction, and a facility with security in four countries has four release processes on four timetables.
- Report the jurisdiction only. Do not report the forum or the arbitral seat.
- Where the documents submit to a named court's jurisdiction, note it in the evidence field, since enforcement and any consent proceedings follow it.
- **Where any security document is governed by non-US law, append ` [non-US security]`**, so the row can be routed to local counsel for the release mechanics.

## Fallback rules

- Return `Not addressed` where no document contains a choice of law.
- Return `Unable to determine` where choices conflict irreconcilably.

## Output format

`Facility: [jurisdiction]; security documents: [jurisdiction(s) or "same"]`, with any flag appended. Return no more than 40 words.
```

---

### 38. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this facility file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this facility that the documents in this unit refer to and that is not present.

## Scope

- **Include the credit agreement or instrument where it is absent.**
- Include amendments, waivers, consents, and forbearance agreements referenced but absent.
- **Include security agreements, pledge agreements, mortgages, and deposit account control agreements referenced but absent.**
- **Include guaranties for each named guarantor where the guaranty document is absent.**
- Include schedules and exhibits listed as attached but not present, particularly collateral schedules, exclusion schedules, and permitted lien schedules.
- Include fee letters, which are routinely separate and routinely unproduced.
- Include compliance certificates and borrowing base certificates required by the agreement.
- Include the most recent audited and management accounts required to be delivered.
- Include intercreditor and subordination agreements referenced but absent.
- Include any lender list, register of lenders, or assignment notice referenced.
- Include payoff letters, releases, and lien terminations referenced but absent.
- Include hedging or swap documents referenced.
- Exclude statutes and regulations.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a security agreement or collateral schedule is absent, add `; collateral perimeter unknown`.** Filter these first — the release checklist cannot be built without them.
- **Where a guaranty for a named guarantor is absent, add `; guaranty unproven`.**
- **Where an amendment or waiver is referenced and absent, add `; current terms uncertain`.** A waiver is also evidence of a past breach.
- Where a fee letter is absent, add `; pricing incomplete`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

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
| **Operative version confirmed** | Yes / No, superseded / Chain incomplete |
| **Treatment at closing** | Repay / Refinance / Assume with consent / Leave in place / Unresolved |
| **Payoff amount confirmed by lender** | Yes (date) / No / Not applicable |
| **Consent required** | Yes / No / Ambiguous |
| **External obligor release required** | Yes (specify) / No |
| **Lien releases required** | None / Identified (specify) / Unresolved |
| **Covenant breach identified** | None / Identified (specify) / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: borrower, obligors, lender, outstanding
balance, maturity, change of control, collateral, prepayment terms.

### Reconciliation work that never belongs in a column

- **The funds flow.** Every payoff, premium, breakage, and fee, built in Excel and
  **confirmed by a payoff letter from each lender**. No figure from this table
  enters a funds flow without a lender's quotation behind it.
- **Debt to lien search.** Every facility against the Lien Filings table.
  **A filing with no corresponding facility means undisclosed debt or a stale
  filing; a facility with no filing may mean an unperfected lien.** Both need
  resolving and neither is visible from one table.
- **Guarantor tracing.** Every `Obligors Inside Group` row that is not
  `All obligors inside the acquired group`, against the transaction structure. Each
  needs a release, a replacement, or a payoff.
- **Covenant testing.** Every covenant against actual financial data, with the
  finance workstream. **Never a Harvey column.** Test pro forma for the transaction
  as well as historically.
- **Collateral to asset.** Collateral descriptions against material assets,
  particularly IP. Every `IP secured, no recordation evidenced` row against the IP
  Registrations `Encumbrances of Record` column, in both directions.
- **Consent versus payoff decision.** For each facility, price consent against
  payoff using the prepayment terms and the change-of-control consequence. **A
  lock-out period or a defeasance requirement can make payoff impossible**, and a
  MAC event of default can make leaving the facility in place unattractive.
- **Release checklist.** Every security document, control agreement, share
  certificate, and lien filing requiring release, with a named owner and the filing
  responsibility identified.
- **Letters of credit.** Every outstanding LC, with a replacement arranged through
  the buyer's own bank. These cannot be repaid.
- **Restricted payment capacity.** Where any facility survives closing, its
  restricted payment and permitted debt provisions against the buyer's post-closing
  cash and financing plans.

---

## Test set

- [ ] Syndicated revolving credit facility with agent, amendments, and compliance certificates
- [ ] Term loan with a springing maturity
- [ ] Asset-based revolver with a borrowing base certificate
- [ ] Promissory note with no covenants
- [ ] Mezzanine facility with warrants
- [ ] Shareholder loan from the selling shareholder
- [ ] Government-backed loan with change-of-control restrictions
- [ ] Capital lease financing
- [ ] Receivables facility, undisclosed and without recourse
- [ ] Facility with a personal guarantee from a founder
- [ ] Facility guaranteed by the seller's parent
- [ ] Facility where the borrower is outside the acquired group
- [ ] Facility with an unsigned security agreement
- [ ] Facility with a named guarantor and no guaranty document produced
- [ ] Facility with a compliance certificate reciting a covenant level differing from the agreement
- [ ] Facility with a waiver in the file
- [ ] Facility with a forbearance agreement
- [ ] Facility with a payoff letter stating a good-through date
- [ ] Facility with a payoff letter whose quotation has expired
- [ ] Facility with a balance stated only in a certificate four months old
- [ ] Facility with no balance figure produced at all
- [ ] Facility with PIK interest
- [ ] Facility referencing a discontinued benchmark with fallback language
- [ ] Facility with a pricing grid and a fee letter not produced
- [ ] Facility already matured on the record with no payoff or extension
- [ ] Facility maturing within six months of the as-of date
- [ ] Facility with a leverage covenant stepping down over two years
- [ ] Facility with a springing covenant tested above 30 percent utilisation
- [ ] Facility with an equity cure limited to two uses and funded only by a named sponsor
- [ ] Facility with a change of control event of default
- [ ] Facility with a change of control mandatory prepayment
- [ ] Facility with a put right and a stated offer period
- [ ] Facility whose change of control definition turns on the sponsor ceasing to hold 50 percent
- [ ] Facility with a permitted holder concept covering the existing sponsor only
- [ ] Facility with a change of control provision reaching direct ownership only
- [ ] Facility with cross-default at a low threshold
- [ ] Facility with cross-acceleration only
- [ ] Facility with a MAC event of default determinable in the lender's opinion
- [ ] Facility with a MAC drawdown condition only
- [ ] Facility with a non-call period prohibiting prepayment
- [ ] Facility with a call premium stepping down to par
- [ ] Facility requiring defeasance rather than permitting prepayment
- [ ] Facility with an assumption alternative and a stated fee
- [ ] Facility with an all-assets grant and a contract-breach exclusion
- [ ] Facility with an equity pledge over three named subsidiaries
- [ ] Facility with a 65 percent limit on a foreign subsidiary pledge
- [ ] Facility with IP secured and recordation evidenced
- [ ] Facility with IP secured and no recordation evidenced
- [ ] Facility with cash dominion in place
- [ ] Facility with springing account control
- [ ] Facility with control agreements required and none produced
- [ ] Second lien facility with an intercreditor agreement not produced
- [ ] Facility with outstanding letters of credit
- [ ] Facility with security governed by non-US law
- [ ] Facility with a collateral schedule referenced and not attached

Then test the dependencies: change `Financial Covenants` from stated covenants to
`None` and confirm `Most Recent Tested Compliance` and `Equity Cure` both move to
`Not applicable`. Change `Change of Control Consequence` from `Event of default`
to `Not addressed` and confirm the definition and Verbatim columns follow. Change
`Collateral Description` to `Unsecured` and confirm `Excluded Assets` and
`IP Included in Collateral` move to `Not applicable`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
