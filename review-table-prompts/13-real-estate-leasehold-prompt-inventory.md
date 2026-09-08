# Prompt Inventory — Real Estate: Leasehold

Table 13 of the POC. Second-largest table in the set.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Real Estate`
- Review unit: **one leased property** — the lease, every amendment and extension,
  any guaranty, estoppel certificate, subordination agreement, commencement or
  delivery letter, and any termination or surrender document produced for it
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: real estate and corporate/M&A teams;
  feeds the consent schedule, the site list reconciliation, the occupancy cost
  model, and the coverage register
- Inventory version: v1.0

### Why the property is the row

A lease that has run ten years has a first amendment extending the term, a second
adding a floor, a commencement letter fixing the dates that the lease left blank,
and an estoppel certificate from a refinancing that recites the current rent. One
row per document produces five rows that each look authoritative. One row per
property, grouped, produces the occupancy picture.

**The commencement letter matters more than it sounds.** Most leases state a
commencement date by formula — so many days after delivery of possession — and the
actual dates are fixed later in a separate letter. Without it in the unit, the
term dates are unknown rather than absent.

### The three questions

1. **Can we transfer it?** Assignment and change-of-control provisions, and above
   all whether the landlord holds a recapture right rather than merely a consent
   right. Feeds the consent schedule.
2. **What does it cost, and for how long?** Term, rent, escalation, additional
   rent, and the end-of-term liabilities that never appear in a rent roll.
3. **Can we leave, or must we stay?** Early termination rights, holdover
   exposure, continuous operation covenants, and restoration obligations.

## Assumptions to confirm before running

1. One row is one property. A master lease covering four buildings is one row if
   the documents treat it as one demise, and four rows if they set separate terms
   and rents per building. Decide once and apply consistently, because the site
   reconciliation depends on it.
2. Owned property is a separate table. Deeds, title reports, and surveys have a
   different row unit and different roles.
3. Subleases where the target is **landlord** are rows here, with the direction
   reported in `Interest Type`. They are income rather than cost and the reviewer
   needs to see them.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

38 Harvey columns plus 9 human columns. If your tenant's cap is lower, split into
**Lease Terms and Economics** (columns 1–24) and **Lease Transfer and Operations**
(columns 25–38) over the same project, joined on property address in the export.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side real estate diligence on the target group listed below. This table reviews leasehold interests.

One row is one leased property: the lease, every amendment and extension, any guaranty, estoppel certificate, subordination agreement, commencement or delivery letter, and any termination or surrender document produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the property or the parties.
- Where two documents in the unit address the same provision, report the provision as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- **An estoppel certificate states the parties' agreed position as at its date.** Where it conflicts with the lease as amended, report both and identify each source. Do not treat an estoppel as amending the lease.
- Report figures only as the documents state them. Do not calculate, total, annualize, apply an escalation, convert currency, or compute a rent per square foot.
- Use entity names exactly as printed in the documents; do not shorten, expand, or correct them.
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
  Property Address
  Interest Type
  Tenant Entity
  Landlord
  Governing Law

Stage 2 — Record status
  Documents in Unit ──→ Execution Status
                        Chain Completeness
                        Referenced but Not Produced

Stage 3 — Premises and term
  Interest Type ──→ Premises Description
                    Lease Structure
  Commencement Date, Rent Commencement Date, Current Term Expiry
  Current Term Expiry ──→ Term Status on Record
  Renewal Options ──→ Renewal Rent Determination

Stage 4 — Economics
  Lease Structure ──→ Base Rent
                      Additional Rent
  Rent Escalation, Percentage Rent, Landlord Concessions Outstanding
  Security Deposit and Credit Support
  Guaranty

Stage 5 — Transfer
  Assignment and Subletting ──→ Assignment Language
                                Landlord Recapture Right
                                Consent Conditions
                                Permitted Transfer Carve-Out
  CoC Treated as Assignment ──→ CoC Language

Stage 6 — Use, operations, and exit
  Permitted Use, Exclusive Use Right, Continuous Operation Covenant,
  Restoration and Surrender, Holdover, Early Termination and Event Triggers,
  Expansion and Preferential Rights, Lender-Related Obligations,
  Landlord Default Remedies
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Execution Status; Chain Completeness; Referenced but Not Produced | v1.0 | draft |
| 2 | Property Address | Free Response | — | — | v1.0 | draft |
| 3 | Interest Type | Classify | — | Premises Description; Lease Structure | v1.0 | draft |
| 4 | Tenant Entity | Free Response | — | — | v1.0 | draft |
| 5 | Landlord | Free Response | — | — | v1.0 | draft |
| 6 | Execution Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 7 | Chain Completeness | Classify | @Documents in Unit | — | v1.0 | draft |
| 8 | Premises Description | Free Response | @Interest Type | — | v1.0 | draft |
| 9 | Lease Structure | Classify | @Interest Type | Base Rent; Additional Rent | v1.0 | draft |
| 10 | Commencement Date | Date | — | — | v1.0 | draft |
| 11 | Rent Commencement Date | Date | — | — | v1.0 | draft |
| 12 | Current Term Expiry | Date | — | Term Status on Record | v1.0 | draft |
| 13 | Term Status on Record | Classify | @Current Term Expiry | — | v1.0 | draft |
| 14 | Renewal Options | Free Response | — | Renewal Rent Determination | v1.0 | draft |
| 15 | Renewal Rent Determination | Classify | @Renewal Options | — | v1.0 | draft |
| 16 | Base Rent | Free Response | @Lease Structure | — | v1.0 | draft |
| 17 | Rent Escalation | Free Response | — | — | v1.0 | draft |
| 18 | Additional Rent | Free Response | @Lease Structure | — | v1.0 | draft |
| 19 | Percentage Rent | Free Response | — | — | v1.0 | draft |
| 20 | Security Deposit and Credit Support | Free Response | — | — | v1.0 | draft |
| 21 | Guaranty | Free Response | — | — | v1.0 | draft |
| 22 | Landlord Concessions Outstanding | Free Response | — | — | v1.0 | draft |
| 23 | Assignment and Subletting | Classify | — | Assignment Language; Landlord Recapture Right; Consent Conditions; Permitted Transfer Carve-Out | v1.0 | draft |
| 24 | Assignment Language | Verbatim | @Assignment and Subletting | — | v1.0 | draft |
| 25 | Landlord Recapture Right | Classify | @Assignment and Subletting | — | v1.0 | draft |
| 26 | Consent Conditions | Free Response | @Assignment and Subletting | — | v1.0 | draft |
| 27 | Permitted Transfer Carve-Out | Classify | @Assignment and Subletting | — | v1.0 | draft |
| 28 | CoC Treated as Assignment | Classify | — | CoC Language | v1.0 | draft |
| 29 | CoC Language | Verbatim | @CoC Treated as Assignment | — | v1.0 | draft |
| 30 | Permitted Use | Free Response | — | — | v1.0 | draft |
| 31 | Exclusive Use Right | Classify | — | — | v1.0 | draft |
| 32 | Continuous Operation Covenant | Classify | — | — | v1.0 | draft |
| 33 | Restoration and Surrender | Free Response | — | — | v1.0 | draft |
| 34 | Holdover | Free Response | — | — | v1.0 | draft |
| 35 | Early Termination and Event Triggers | Free Response | — | — | v1.0 | draft |
| 36 | Expansion and Preferential Rights | Classify | — | — | v1.0 | draft |
| 37 | Lender-Related Obligations | Free Response | — | — | v1.0 | draft |
| 38 | Landlord Default Remedies | Free Response | — | — | v1.0 | draft |
| 39 | Governing Law | Free Response | — | — | v1.0 | draft |
| 40 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

40 columns — two more than estimated. `Landlord Default Remedies` and
`Landlord Concessions Outstanding` earned their place during drafting: unpaid
tenant improvement allowance is a receivable the buyer acquires, and a tenant's
self-help rights determine what it can do about a landlord who stops performing.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Execution Status`, `Chain Completeness`, `Referenced but Not Produced`
- Purpose: inventory the lease family, so a reviewer can see the amendment
  sequence and whether the dates were ever fixed.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the lease, every amendment, extension, renewal exercise, or modification, any guaranty, estoppel certificate, subordination or non-disturbance agreement, commencement or delivery letter, work letter, consent to assignment or sublease, notice of exercise of an option, and any termination or surrender agreement.
- Treat exhibits, floor plans, and work letters bound into a document as part of that document.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Lease`, `Amendment`, `Extension or renewal`, `Commencement letter`, `Work letter`, `Guaranty`, `Estoppel`, `SNDA or subordination`, `Consent`, `Option notice`, `Termination or surrender`, or `Other`.
- Number amendments as the document numbers itself. Do not infer a sequence.
- **Where a document relates to a different property than the subject of this row, still list it and append ` [relates to [address]]`.** A unit mixing two properties produces a merged row.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 25 lines and no more than 150 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Property Address

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the address, which is the join key to the site list, the licences, the
  insurance schedule, and the environmental reports.

```markdown
## Task

State the address of the leased premises.

## Rules

- Report the full street address as printed, including suite, unit, floor, or building designation.
- **Where the premises are part of a larger building or centre, report both the premises designation and the building or centre name as printed.** The building name is often how the property appears in the site list and the insurance schedule, and the suite number is how it appears in the lease.
- Where a later amendment adds, substitutes, or relinquishes space, report the current premises and append ` (as amended [YYYY-MM-DD])`.
- Report the city, state or province, postal code, and country as printed.
- Where the documents identify the premises only by a legal description or a lot and block reference with no street address, report that reference and add `(no street address stated)`.
- Do not correct, standardize, or complete an address, and do not add a postal code the documents do not state.

## Fallback rules

- Return `Unable to determine` where no document in the unit identifies the premises.

## Output format

`[Premises designation], [Building or centre name], [street address], [city], [state or province] [postal code], [country]`, with any qualifier appended.

Return no more than 40 words.
```

---

### 3. Interest Type

- Native type: Classify
- Configured options, in UI order: `Lease, target as tenant`, `Sublease, target as subtenant`, `Sublease, target as sublandlord`, `Ground lease, target as tenant`, `Licence or concession`, `Co-working or membership agreement`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Premises Description`, `Lease Structure`
- Purpose: what the interest is and which side of it the target sits on, which
  inverts the reading of almost every other column.

```markdown
## Task

Classify the nature of the target's interest in this property, and which side of it the target holds. Choose exactly one configured option.

## Scope

- Use the review-subject list in the Table Instructions to determine which party is a target entity.
- Where the target holds both a lease and a sublease of the same premises, classify the lease and note the sublease in the evidence field.

## Classification rules

- `Lease, target as tenant`: the target leases directly from the owner or its agent. The default case.
- `Sublease, target as subtenant`: the target's immediate landlord is itself a tenant. **Note the dependency: the sublease is only as secure as the head lease**, and the head lease is a document that should be produced.
- `Sublease, target as sublandlord`: the target has sublet space to a third party. **This is income, not cost**, and it is read in reverse — the consent, recapture, and use provisions constrain the target as landlord.
- `Ground lease, target as tenant`: the target leases land, typically long-term, and usually owns or is responsible for improvements on it. The economics and the end-of-term position differ substantially from a space lease.
- `Licence or concession`: a revocable or non-exclusive right of occupation rather than a leasehold estate. Note in the evidence field whether the document is stated to be a licence, since a document titled a licence may still create a lease.
- `Co-working or membership agreement`: a membership or service agreement for flexible space, typically short-term with no real property estate.

Classify on the substance of the interest as the documents create it, not on the title.

## Fallback rules

- Use `Unable to determine` where the documents do not establish the nature of the interest or which party the target is.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Tenant Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: which group entity holds the lease. **Decisive in a carve-out**, where a
  lease held by an entity that is not being acquired has to be assigned or
  replaced.

```markdown
## Task

State the target-group entity that holds the tenant's or subtenant's interest.

## Rules

- Take the tenant from the parties clause and the signature block. Where a later assignment, novation, or name-change document in the unit substitutes a different entity, report the current tenant.
- Use the review-subject list in the Table Instructions to determine whether it is a group entity.
- Report the name exactly as printed, including the entity suffix.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- **Where the tenant changed during the term, report the current tenant and append ` (assigned from [prior tenant], [YYYY-MM-DD])`.** Note in the evidence field whether the documents evidence landlord consent to that assignment, since an unconsented assignment is a subsisting breach.
- Where the tenant entity is not on the review-subject list, report the name and append ` (not a listed entity)`. This surfaces a lease held outside the acquired group.
- Where the target is the sublandlord, report the target entity here and report the subtenant in the Landlord column's evidence field.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the tenant.

## Output format

`[Exact legal name]`, with any qualifier appended. Return no more than 35 words.
```

---

### 5. Landlord

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the counterparty whose consent will be needed, by exact name.

```markdown
## Task

State the landlord, sublandlord, or licensor under this interest.

## Rules

- Report the name exactly as printed, including the entity suffix. Do not correct or expand it.
- **Where the landlord has changed — on a sale of the building, a foreclosure, or an assignment — report the current landlord and append ` (succeeded [prior landlord], [YYYY-MM-DD])`.** The consent request goes to the current owner, and an estoppel or notice of sale in the unit is usually the only evidence of the change.
- Where a managing agent is named as acting for the landlord, report the landlord and note the agent in the evidence field. **The agent is not the landlord** and consent from an agent without evidence of authority is a gap.
- Where the target is the sublandlord under `Interest Type`, report the subtenant here and label it `subtenant`.
- Where notices must be given to an address or party different from the landlord, note that in the evidence field.

## Fallback rules

- Return `Unable to determine` where no document in the unit names the landlord.

## Output format

`[Exact legal name]`, with any qualifier or label appended. Return no more than 35 words.
```

---

### 6. Execution Status

- Native type: Classify
- Configured options, in UI order: `All documents executed`, `Lease executed, later document unsigned`, `Lease unsigned`, `Partially executed`, `Form or template`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: what the family proves about its own completion.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks in the current unit.

## Task

Classify the visible execution status of the documents in this review unit. Choose exactly one configured option.

## Scope

- Evaluate signature blocks, electronic-signature markers, conformed signatures, and counterpart pages visible in the documents.
- Exclude notary, witness, and acknowledgement blocks from the party count.
- **Treat a guaranty as a document requiring the guarantor's signature.** An unsigned guaranty is worthless and it is a common gap.
- Exclude signature evidence on exhibits, work letters, and floor plans.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the documents are unpopulated forms with bracketed placeholders, blank party names, or blank rent fields.
2. `Lease unsigned`: the lease provides party signature blocks and none bears a signature marker.
3. `Partially executed`: any document in the unit has at least one signed and at least one unsigned party signature block.
4. `Lease executed, later document unsigned`: the lease is fully signed and at least one amendment, guaranty, consent, or other document in the unit is unsigned.
5. `All documents executed`: every document in the unit bears a signature marker in every party signature block it provides.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated commencement date is not a signature marker.

## Fallback rules

- Use `Unable to determine` where signature evidence exists but cannot be read, where a signature page is referenced but missing, or where documents conflict about execution.
- Do not treat an estoppel certificate reciting the lease, or a rent payment record, as evidence that the lease was signed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 7. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Lease absent`, `Commencement letter referenced but absent`, `Head lease absent`, `Sequence gap`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: flag rows where the family is incomplete, so a reviewer knows before
  reading any term that the row may not show current terms.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether the lease family in this review unit appears complete. Choose exactly one configured option.

## Scope

- Consider documents that constitute, amend, or fix the terms of this interest.
- Exclude the landlord's own mortgage documents and third-party documents referenced for context.

## Classification rules

Apply the first rule that fits.

1. `Lease absent`: the unit contains amendments, estoppels, or consents but not the lease itself.
2. `Head lease absent`: the target holds a sublease and the head lease is not present. **The sublease's security depends entirely on the head lease**, including its term, its assignment provisions, and whether it permits the sublease at all.
3. `Amendment referenced but absent`: a document in the unit refers to an amendment, extension, or modification that is not present. An estoppel reciting the amendment history is the most common source of this evidence.
4. `Sequence gap`: amendments are numbered and a number in the sequence is missing.
5. `Commencement letter referenced but absent`: the lease fixes the commencement or expiry date by reference to a letter, notice, or certificate confirming delivery of possession, and that document is not present. **The term dates are then unknown, not absent**, and the reviewer needs to see the difference.
6. `Complete on its face`: the lease is present, no amending document is missing, and any commencement mechanism has been resolved by a document in the unit or by stated dates.

`Complete on its face` states only that nothing in these documents reveals a gap.

## Fallback rules

- Use `Unable to determine` where a reference to a further document is too vague to tell whether it affects this interest, or where references are illegible.
- Do not use `Unable to determine` for a single unamended lease with stated dates. That is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Premises Description

- Native type: Free Response
- Upstream: `@Interest Type`
- Downstream: none
- Purpose: what is actually demised, including the rentable area the rent is
  calculated on and the ancillary rights that come with it.

```markdown
## Established result

- Interest Type: @Interest Type

## Task

Report the premises demised under this interest.

## Include where expressly stated

- The rentable area, and separately the usable area where both are stated
- **Any load factor, add-on factor, or gross-up applied to derive rentable from usable area.** The difference is what the tenant pays for and does not occupy, and it is frequently the largest single unexamined item in an occupancy cost
- The floors, suites, or units comprised, and whether the demise is contiguous
- Parking: the number of spaces, whether reserved or unreserved, and whether charged separately
- Storage, roof, riser, antenna, or basement rights
- Signage rights
- Any exclusive or shared right to common areas, loading, or amenities
- For a ground lease, the land area and any improvements stated to be included or excluded
- Any space added, substituted, or relinquished by a later document

## Rules

- **Report the rentable area as stated, and do not recalculate it from dimensions or a load factor.** Where the documents state areas that conflict, report each with its source.
- Report parking as stated. A number of spaces and a ratio per thousand square feet are different statements and should be reported as printed.
- Report the current position where a later amendment changed the premises, and note the change in the evidence field.
- Do not calculate a rent per square foot, and do not compare the area to anything.

## Fallback rules

- Return `Not stated` for any element the documents do not state.
- Return `Unable to determine` where the demise cannot be identified, or where stated areas conflict irreconcilably.

## Output format

`Area: [rentable] rentable[, [usable] usable][; load factor [as stated]]; premises: [floors or suites]; parking: [as stated]; ancillary: [brief or "none stated"]`

Return no more than 75 words. Do not include any figure you calculated.
```

---

### 9. Lease Structure

- Native type: Classify
- Configured options, in UI order: `Triple net`, `Double net`, `Full service gross`, `Modified gross with base year`, `Modified gross with expense stop`, `Absolute net`, `Not addressed`, `Unable to determine`
- Upstream: `@Interest Type`
- Downstream: `Base Rent`, `Additional Rent`
- Purpose: who bears which operating costs, which determines whether the base rent
  is close to the real occupancy cost or a small fraction of it.

```markdown
## Established result

- Interest Type: @Interest Type

## Task

Classify how operating costs are allocated between landlord and tenant. Choose exactly one configured option.

## Scope

- Consider the allocation of real property taxes, building insurance, common area maintenance, utilities, structural repair, and capital replacement.
- Classify from the target's perspective. Where the target is the sublandlord, classify the structure as it applies between the target and its subtenant, and note the head lease structure in the evidence field.

## Classification rules

- `Absolute net`: the tenant bears all costs including structure, roof, and capital replacement, with no landlord obligation. Common in ground leases and single-tenant industrial.
- `Triple net`: the tenant bears taxes, insurance, and maintenance, with the landlord typically retaining structural and capital obligations. **Confirm which structural items the landlord retains**, since the label is used loosely and the retained items are where the difference lies.
- `Double net`: the tenant bears taxes and insurance; the landlord bears maintenance.
- `Full service gross`: the rent is inclusive and the landlord bears operating costs, with no pass-through.
- `Modified gross with base year`: the tenant pays its share of operating costs to the extent they exceed those of a stated base year. **Report the base year in the Additional Rent column**, because a stale base year means large pass-throughs.
- `Modified gross with expense stop`: the tenant pays costs above a stated amount per unit of area.

Classify on the operative allocation, not on the label the lease uses. **A lease describing itself as triple net while making the landlord responsible for taxes is not triple net**, and the substance governs.

## Fallback rules

- Use `Not addressed` where the documents do not allocate operating costs.
- Use `Unable to determine` where the allocation is incomplete, conflicting, or illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Commencement Date

- Native type: Date — confirm the type accepts `Not stated` and `Incorporated terms`
- Upstream: none
- Downstream: none
- Purpose: when the term began, which anchors the expiry and every option deadline.

```markdown
## Task

Identify the date the term of this interest commenced.

## Date-selection hierarchy

1. Use a commencement date stated in a commencement letter, delivery notice, or confirmation of dates in the unit. **This is the most reliable source**, because it records the date actually fixed rather than the formula.
2. If none, use a fixed commencement date stated in the lease or in an amendment.
3. If neither, and the lease fixes commencement by formula — a stated number of days after delivery of possession, substantial completion, or issue of a certificate of occupancy — return `Not stated` and report the formula in the evidence field. **Do not calculate the date from the formula**, even where the triggering event's date appears in the unit.

## Excluded dates

- The date of the lease itself, where a separate commencement date is stated
- The rent commencement date, which has its own column and is frequently later
- The date of an amendment or an extension
- The date possession was delivered, unless the documents state that commencement occurred on it
- File name and metadata dates, and notarization and scan dates

## Rules

- **Report the commencement of the original term, not of a renewal term.** Where a renewal has been exercised, the renewal term's start is reported in the Renewal Options column and the current expiry carries the effect.
- Where an amendment restates the commencement date, report the restated date and note the change in the evidence field.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where the date is fixed only by an unresolved formula, or `Incorporated terms` where it is stated to be set by a document not present in the unit.
```

---

### 11. Rent Commencement Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when rent actually became payable, which is often months after
  commencement and is the date the occupancy cost model needs.

```markdown
## Task

Identify the date rent first became payable, or was scheduled to become payable, under this interest.

## Rules

- Where the documents state a rent commencement date distinct from the term commencement date, report it.
- **Where the documents grant a free rent or rent abatement period, report the date rent becomes payable after it** and note the length of the abatement in the evidence field.
- Where a commencement letter or confirmation of dates in the unit fixes the rent commencement date, prefer it over a formula in the lease.
- **Report the date even where it equals the commencement date.** A value the document states is never replaced by a fallback state, and two columns agreeing is information.
- Where rent commencement is fixed only by an unresolved formula, return `Not stated` and report the formula in the evidence field. Do not calculate it.
- Where a later amendment granted a further abatement — a rent deferral or concession, for example — report the date rent resumed or is due to resume and note the amendment.

## Fallback rules

- Return `Not applicable` where no rent is payable under the interest at all, which can arise in an intercompany or nominal-rent arrangement.
- Return `Not stated` where the documents state no rent commencement date and it cannot be reported without calculating.
- Return `Unable to determine` where stated dates conflict.

## Output format

`YYYY-MM-DD`, or one of the exact fallback values above. Preserve partial precision as printed.
```

---

### 12. Current Term Expiry

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: `Term Status on Record`
- Purpose: the end date of the term now running. **The single most important date
  in the table**, and it drives the site retention plan.

```markdown
## Task

Identify the end date of the term currently running under this interest.

## Rules

Apply in order.

1. If a document in the unit exercises or confirms a renewal or extension and states the new expiry, use that date.
2. If a commencement letter or confirmation of dates in the unit states the expiry, use it.
3. If the lease or an amendment states a fixed expiry date, use it.
4. If the documents state a commencement date and a term length and no expiry, report the expiry **only if a document in the unit states it**. Otherwise return `Not stated` and report the commencement date and term length in the evidence field. Do not calculate.
5. If the interest continues on a periodic or month-to-month basis with no fixed end, return `Not applicable — periodic tenancy`.

## Excluded dates

- The expiry of a renewal option that has not been exercised in the documents
- Option exercise deadlines and notice dates
- The expiry of a guaranty, a letter of credit, or an insurance policy
- The expiry stated in an estoppel certificate where a later amendment changed it — though where the estoppel is the later document, use it and identify the source
- Dates belonging to a head lease where the target is subtenant, unless the sublease expiry is fixed by reference to it

## Rules on conflicts

- **Where an estoppel certificate and the lease as amended state different expiry dates, report the date from the most recently dated document and append ` (estoppel states [date])` or ` (lease as amended states [date])` as applicable.** The conflict is a finding and the reviewer resolves it.

## Output format

`YYYY-MM-DD`, with any qualifier appended, or `Not applicable — periodic tenancy`. Preserve partial precision as printed. Return `Not stated` where no expiry can be reported without calculating.
```

---

### 13. Term Status on Record

- Native type: Classify
- Configured options, in UI order: `Within initial term`, `Within renewal term`, `Stated term has ended, no extension in unit`, `In holdover per documents`, `Terminated or surrendered`, `Periodic tenancy`, `Term not stated`, `Unable to determine`
- Upstream: `@Current Term Expiry`
- Downstream: none
- Purpose: surface leases whose term has ended with nothing in the file extending
  them. **Occupying without a current lease is one of the highest-value findings
  in this workstream**, and it is invisible in an expiry column alone.

**Scope discipline.** This reports what the documents show as at the diligence
as-of date. It does not state whether the target still occupies; occupancy is not
in the documents. A reviewer reads this cell against the site list.

```markdown
## Established result

- Current term expiry: @Current Term Expiry

Use this for routing. Confirm the classification against the documents in the current unit.

## Task

Classify the status of the term as at the diligence as-of date in the Table Instructions, based only on the documents in this review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Terminated or surrendered`: the unit contains a termination agreement, surrender, lease buyout, or notice of termination that has taken effect.
2. `Periodic tenancy`: Current Term Expiry is `Not applicable — periodic tenancy`.
3. `Term not stated`: Current Term Expiry is `Not stated`.
4. `In holdover per documents`: Current Term Expiry falls before the diligence as-of date **and** a document in the unit — an estoppel, a notice, or correspondence — states that the tenant remains in occupation or is holding over.
5. `Within renewal term`: Current Term Expiry falls on or after the diligence as-of date, and the unit contains a document evidencing that a renewal or extension has been exercised or taken effect.
6. `Within initial term`: Current Term Expiry falls on or after the diligence as-of date, and no renewal has taken effect on the record.
7. `Stated term has ended, no extension in unit`: Current Term Expiry falls before the diligence as-of date and no document extends, renews, or confirms occupation.

**Where a renewal option exists but the documents do not evidence its exercise, do not treat it as exercised**, even where the expiry has passed and the option deadline has also passed. Report `Stated term has ended, no extension in unit` and let the reviewer establish the position.

## Fallback rules

- Use `Unable to determine` where Current Term Expiry is `Unable to determine`, or where documents conflict about whether the lease was terminated.
- Do not use `Unable to determine` merely because the term has ended. That is a finding, not an uncertainty.

## Output format

Return only the exact configured option and no explanation.
```

---

### 14. Renewal Options

- Native type: Free Response
- Upstream: none
- Downstream: `Renewal Rent Determination`
- Purpose: how much longer the target can stay, and what it must do to secure it.
  **A missed option notice cannot usually be recovered.**

```markdown
## Task

Report the renewal, extension, and option rights this interest confers on the tenant.

## Include where expressly stated

- The number of options remaining and the length of each
- **The notice window for exercising each option**: the earliest and latest dates or periods before expiry
- Whether notice must be given in a stated form or to a stated address
- Whether the option is personal to the named tenant and lost on assignment. **A personal option does not pass to a buyer or an assignee**, and that is what makes it worth reporting separately
- Any condition on exercise: no subsisting default, minimum occupancy, or continuous operation
- Whether any option has already been exercised, and by which document
- Any automatic extension where no notice to terminate is given

## Rules

- **Report options already exercised separately from options remaining**, using the documents in the unit as evidence.
- **Report any personal-to-tenant limitation prominently.** It converts an apparent term extension into nothing at all for the buyer.
- Report the notice window as stated and calculate no dates from it. The reviewer diaries it against the expiry.
- Report the no-default condition where present, since a subsisting breach can defeat an option that otherwise looks secure.
- Where a later amendment added, removed, or altered options, report the current position.

## Fallback rules

- Return exactly `None` where the documents confer no renewal or extension right.
- Return `Incorporated terms` where the options are stated to be set out in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Remaining: [N] × [length]; notice window: [as stated]; personal to tenant: [yes | Not addressed]; conditions: [brief or "none stated"]; exercised to date: [as evidenced or "none"]`

Return no more than 80 words.
```

---

### 15. Renewal Rent Determination

- Native type: Classify
- Configured options, in UI order: `Fixed amount or schedule`, `Fair market rent`, `Index-linked`, `Greater of fixed and fair market`, `Agreement between parties`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Renewal Options`
- Downstream: none
- Purpose: what the rent will be if the option is exercised. **A fair-market
  renewal is an unquantified future cost**, and a fixed schedule is a known one.

```markdown
## Established result

- Renewal options: @Renewal Options

## Task

If Renewal Options reported one or more remaining options, classify how the rent for a renewal term is determined. Choose exactly one configured option.

If Renewal Options returned `None`, return `Not applicable`.

If it returned `Incorporated terms` or `Unable to determine`, return `Unable to determine`.

## Classification rules

- `Fixed amount or schedule`: the renewal rent is stated as an amount or a schedule of amounts.
- `Index-linked`: the renewal rent is the current rent adjusted by a named index.
- `Fair market rent`: the renewal rent is the market rent at the time, however determined. **Report the determination mechanism in the evidence field** — appraisal, broker opinion, or arbitration — together with whether a floor applies.
- `Greater of fixed and fair market`: a floor at the current or a stated rent, with market above it. **This is the landlord-favourable formulation and the most common**, and it means the rent can only go up.
- `Agreement between parties`: the renewal rent is subject to agreement, with no mechanism if the parties fail to agree. **This is not an option in any practical sense**, because the landlord can defeat it by declining to agree, and the reviewer should see that.

Where different options carry different mechanisms, classify on the next option to arise and report the others in the evidence field.

## Fallback rules

- Use `Not addressed` where an option exists and the documents state no rent mechanism for it.
- Use `Unable to determine` where the mechanism is incomplete or conflicting.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Base Rent

- Native type: Free Response
- Upstream: `@Lease Structure`
- Downstream: none
- Purpose: the current rent, as stated, reported so it can be reconciled against
  the rent roll and the accounts.

```markdown
## Established result

- Lease Structure: @Lease Structure

## Task

Report the base or minimum rent currently payable under this interest.

## Rules

- Report the amount stated in the most recently dated document in the unit that states a current rent, with the currency, the period, and the document and date it comes from.
- **Where an estoppel certificate states a current rent that differs from the lease as amended, report both and identify each source.** The estoppel usually reflects the position the parties actually operate on, and the discrepancy is the finding.
- Where the documents state a schedule of rents over the term, report the amount currently payable as at the diligence as-of date, and note in the evidence field that a schedule applies.
- **Do not calculate.** Do not annualize a monthly rent, do not apply an escalation to reach a current figure, do not convert currency, and do not compute a rent per unit of area. Where the documents state a rate per square foot, report it as printed alongside the amount.
- Where rent is abated or reduced as at the as-of date, report the payable amount and note the abatement.
- Where the target is the sublandlord, report the rent receivable and label it.

## Fallback rules

- Return `Not stated` where no document in the unit states a rent amount.
- Return `Not applicable` where the interest is stated to be rent-free or nominal, and report the nominal amount in the evidence field.
- Return `Incorporated terms` where the rent is stated to be set out in a schedule or rider not present in the unit.
- Return `Unable to determine` where amounts stated in documents of the same date conflict.

## Output format

`[Amount] [currency] per [period][ ([rate] per [unit] as stated)] — per [document title], [YYYY-MM-DD]`, with any qualifier appended.

Return no more than 50 words. Do not include annualized or converted figures you derived.
```

---

### 17. Rent Escalation

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how the rent moves over the remaining term, which the occupancy cost
  model needs and which an uncapped index link can make significant.

```markdown
## Task

Report how the base rent changes over the term.

## Include where expressly stated

- The escalation mechanism: fixed percentage, fixed amount, stepped schedule, index-linked, or market review
- The frequency and the next escalation date
- **Any index named, and any cap or collar on the increase.** An uncapped index link is a materially different exposure from one capped at three percent, and the cap is the finding
- Any base index figure or base date stated
- Whether escalation compounds or applies to the original rent
- Any market rent review during the term, and its mechanism
- Any provision for rent to decrease

## Rules

- **Report the cap and the index separately and prominently.**
- Report the mechanism and the schedule as stated. **Do not calculate any future rent, do not compute a compound effect, and do not apply an index.**
- Report the next escalation date where stated, and where the documents give a formula rather than a date, report the formula.
- Where a later amendment reset or altered the escalation, report the current mechanism.

## Fallback rules

- Return exactly `None` where the rent is fixed for the whole term with no escalation.
- Return `Incorporated terms` where the mechanism is stated to sit in a schedule or rider not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Mechanism: [as stated]; frequency: [as stated]; next: [date or formula]; index: [name or "none"]; cap: [as stated or "uncapped"]; compounding: [yes | no | Not addressed]`

Return no more than 70 words. Do not include future rents you calculated.
```

---

### 18. Additional Rent

- Native type: Free Response
- Upstream: `@Lease Structure`
- Downstream: none
- Purpose: everything payable beyond base rent. **In a triple net or base-year
  lease this can approach or exceed the base rent**, and it is where unbudgeted
  cost sits.

```markdown
## Established result

- Lease Structure: @Lease Structure

## Task

Report the amounts payable by the tenant in addition to base rent.

## Include where expressly stated

- The tenant's proportionate share, as a percentage or as a stated basis of calculation
- The cost categories passed through: real property taxes, building insurance, common area maintenance, utilities, management fees, security
- **The base year or expense stop, where Lease Structure is a modified gross variant.** A base year several years old means large pass-throughs, and the year itself is the finding
- **Any cap on controllable operating expense increases**, and whether the cap is annual or cumulative
- Any category expressly excluded from pass-through, particularly capital expenditure, structural repair, and landlord's own financing costs
- Any right to audit the landlord's operating statements, and any time limit on exercising it
- Any administrative or management fee charged on top of actual costs, as a percentage
- Any separately metered or directly contracted utilities
- Any current amount stated for additional rent or estimated monthly payments

## Rules

- **Report the capital expenditure position explicitly.** Whether capital items can be passed through, and whether they must be amortised over their useful life, is often the largest single variable in a net lease and it is frequently silent.
- Report the audit right and its deadline, since it is the tenant's only protection against an inflated statement and the deadline is usually short.
- Report amounts and percentages as stated. **Do not calculate the tenant's share, total the categories, or estimate an annual figure.**

## Fallback rules

- Return exactly `None` where no additional rent is payable, which should follow from a full service gross structure.
- Return `Incorporated terms` where the provisions are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

`Share: [as stated]; categories: [list]; base year or stop: [as stated or "Not applicable"]; cap: [as stated or "none"]; capital expenditure: [passed through | excluded | Not addressed]; audit right: [period or "Not addressed"]; current amount: [as stated or "Not stated"]`

Return no more than 90 words.
```

---

### 19. Percentage Rent

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: turnover rent, which links occupancy cost to trading performance and
  carries reporting obligations that survive closing.

```markdown
## Task

Report any rent calculated by reference to the tenant's sales or turnover.

## Include where expressly stated

- The percentage rate, and any tiered rates
- The breakpoint or natural breakpoint above which percentage rent is payable
- The definition of gross sales, and any stated exclusions such as returns, taxes, or online sales
- **Whether online, e-commerce, or click-and-collect sales attributable to the location are included.** This is the most contested definitional point in modern retail leases and it is frequently ambiguous
- The reporting frequency and the form of statement required
- Any audit right the landlord holds over the tenant's records, and any consequence of an understatement
- The payment frequency and any reconciliation

## Rules

- Report the rate and breakpoint as stated. **Do not calculate a breakpoint from the base rent and the rate**, even where both appear.
- **Report the landlord's audit right and any penalty for understatement**, since it is an obligation the buyer inherits and an unremediated understatement is a liability.
- Report the reporting obligations, since failure to report is a common technical default.

## Fallback rules

- Return exactly `None` where no percentage or turnover rent is payable. **This is the expected answer outside retail and hospitality.**
- Return `Incorporated terms` where the provisions sit in a document not present in the unit.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Rate: [as stated]; breakpoint: [as stated]; sales definition: [brief]; online sales: [included | excluded | Not addressed]; reporting: [frequency]; landlord audit: [as stated or "Not addressed"]`

Return no more than 70 words.
```

---

### 20. Security Deposit and Credit Support

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the target has put up, and in what form. **A letter of credit is a
  financing item**, it consumes facility capacity, and its issuer's consent may be
  needed on a change of control.

```markdown
## Task

Report any security deposit, letter of credit, or other credit support given for this interest.

## Include where expressly stated

- The amount and the form: cash deposit, letter of credit, bank guarantee, surety bond, or prepaid rent
- **For a letter of credit or bank guarantee: the issuing bank, the expiry date, whether it is evergreen or automatically renewing, and any obligation to replace or top it up**
- Any provision reducing or burning down the security over time on stated conditions
- Any obligation to increase the security on a stated event, including a deterioration in the tenant's or guarantor's financial position
- Any obligation to replenish after a draw
- Whether the deposit is stated to be held in trust or as the landlord's property
- Any interest payable on a cash deposit
- The conditions for return at the end of the term, and any deadline
- Any statement of the current amount held, particularly in an estoppel certificate

## Rules

- **Report the letter of credit expiry and any evergreen provision prominently.** An LC expiring during or shortly after the deal is a task with a bank lead time, and a failure to renew is usually a lease default.
- **Report any obligation to increase the security on a change of control or on a covenant test**, since it is a cash cost triggered by the transaction.
- Report amounts as stated. Do not calculate a number of months' rent from the amount, or the reverse.
- Where an estoppel states a current amount differing from the lease, report both and identify each source.

## Fallback rules

- Return exactly `None` where no security was given.
- Return `Incorporated terms` where the terms sit in a document not present in the unit.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Amount: [as stated]; form: [as stated]; issuer: [bank or "n/a"]; expiry: [date or "n/a"]; evergreen: [yes | no | n/a]; burn-down: [brief or "none"]; increase triggers: [brief or "none"]`

Return no more than 75 words.
```

---

### 21. Guaranty

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who else stands behind the lease. **Where a parent guarantees a lease,
  confirm the guarantor survives the transaction structure** — a guaranty from an
  entity left behind in a carve-out will usually have to be replaced.

```markdown
## Task

Report any guaranty, indemnity, or other third-party credit support of the tenant's obligations.

## Include where expressly stated

- The guarantor's exact legal name, and whether it is a target-group entity, the seller, a parent outside the group, or an individual
- The scope: all tenant obligations, rent only, or a capped amount
- Any cap on the guarantor's liability, and whether it is a fixed sum or a number of months' rent
- The duration: the whole term, a stated period, or a rolling period
- **Any provision releasing the guarantor on an assignment, on a covenant test, or after a stated period**
- Any obligation to provide a replacement guarantor
- Whether the guaranty is stated to survive an assignment of the lease
- Any requirement for the guarantor to deliver financial statements
- Whether the guaranty document is present in the unit and executed by the guarantor

## Rules

- **State whether the guarantor is inside or outside the target group**, using the review-subject list. A guaranty from an entity that is not being acquired must be dealt with at closing, and that is the finding.
- **Report any release mechanism prominently.** A guaranty releasable on an assignment or on the tenant meeting a net worth test can be discharged as part of the transaction, which is usually to the buyer's advantage.
- Report whether the guaranty is executed. **An unsigned guaranty secures nothing.**

## Fallback rules

- Return exactly `None` where the documents contain and reference no guaranty.
- Return `Referenced but not produced` where the lease requires a guaranty and no guaranty document is in the unit. **This is a coverage finding** and it is also reported in Referenced but Not Produced.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Guarantor: [name] ([inside group | outside group | individual]); scope: [as stated]; cap: [as stated or "uncapped"]; duration: [as stated]; release: [brief or "none stated"]; executed: [yes | no]`

Return no more than 75 words.
```

---

### 22. Landlord Concessions Outstanding

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the landlord still owes. **An unpaid tenant improvement allowance
  is a receivable the buyer acquires**, and it is routinely missed because it
  appears nowhere in a rent roll.

```markdown
## Task

Report any allowance, contribution, abatement, or other concession the landlord has agreed to provide, and whether the documents show it as delivered.

## Include where expressly stated

- Tenant improvement or fit-out allowance: the amount, the basis, and the conditions for drawing it
- **Any deadline by which the allowance must be claimed or spent, after which it is forfeited.** A large allowance with a passed deadline is worth nothing, and the deadline is the finding
- Free rent or abatement periods, whether taken or still to come
- Any moving allowance, broker commission contribution, or contribution to the tenant's costs elsewhere
- Landlord works or base building works agreed, and whether the documents record them as complete
- Any right of set-off against rent if the landlord fails to pay an allowance
- Any statement in an estoppel or a commencement letter confirming that concessions have been satisfied or remain outstanding

## Rules

- **Report the documents' evidence of delivery, and where the documents are silent say so.** An estoppel certificate confirming that all landlord obligations are satisfied is strong evidence; silence is not.
- Report any claim deadline and compare it to the diligence as-of date. **Where a deadline has passed with no evidence the allowance was drawn, append ` [claim deadline passed]`.**
- Report any set-off right, since it is the tenant's practical remedy and it survives to the buyer.
- Report amounts as stated. Do not calculate a remaining balance.

## Fallback rules

- Return exactly `None identified` where the documents record no concession.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

One line per concession:

`[Concession] — [amount or period] — [delivered per documents | outstanding | not stated]`, with any bracketed flag appended.

Return no more than 5 lines and no more than 80 words.
```

---

### 23. Assignment and Subletting

- Native type: Classify
- Configured options, in UI order: `Freely permitted`, `Consent required, no standard`, `Consent required, not to be unreasonably withheld`, `Consent required with deemed approval`, `Prohibited absolutely`, `Permitted to affiliate only`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Assignment Language`, `Landlord Recapture Right`, `Consent Conditions`, `Permitted Transfer Carve-Out`
- Purpose: whether the leasehold can be transferred, and on what condition. Feeds
  the consent schedule.

```markdown
## Task

Classify the restriction on assignment of this lease, or subletting of the premises, **by the tenant**. Choose exactly one configured option.

## Scope

- Analyze the restriction as it applies to the target as tenant. Where the target is the sublandlord under Interest Type, analyze the restriction binding its subtenant and note the direction in the evidence field.
- Include assignment, transfer, subletting, licensing of occupation, mortgaging or charging the leasehold, and any restriction on transfer by operation of law.
- Exclude restrictions on sharing occupation with a group company where the lease expressly permits it without consent; report that in the Permitted Transfer Carve-Out column.
- Where a later document in the unit replaces the clause, classify on the most recently dated document that addresses it.

## Classification rules

Apply the first rule that fits.

1. `Prohibited absolutely`: assignment and subletting are prohibited with no consent mechanism.
2. `Permitted to affiliate only`: transfer is permitted without consent to a group company, and otherwise prohibited or subject to consent.
3. `Consent required with deemed approval`: consent is required and the lease provides that consent is deemed given if the landlord does not respond within a stated period. **A useful provision, because it gives a hard timetable**, and the period should be reported in Consent Conditions.
4. `Consent required, not to be unreasonably withheld`: consent is required and the clause qualifies it with a reasonableness, good-faith, or non-delay standard.
5. `Consent required, no standard`: consent is required with no stated limit on the landlord's discretion. **The landlord can refuse for any reason**, which makes this the hardest position for a transaction.
6. `Freely permitted`: the lease addresses transfer and permits it without consent.

Report in the evidence field whether the restriction on subletting differs from the restriction on assignment, since they are frequently treated differently.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses transfer by the tenant.
- Use `Unable to determine` where the clause is illegible, incomplete, conflicting, or incorporated from a document not present in the unit.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. Assignment Language

- Native type: Verbatim
- Upstream: `@Assignment and Subletting`
- Downstream: none
- Purpose: the exact clause text, which is what the consent request is drafted
  against and what a partner reads before the consent schedule goes out.

```markdown
## Established result

- Assignment and subletting: @Assignment and Subletting

## Task

If Assignment and Subletting is any value other than `Not addressed` or `Unable to determine`, quote the assignment and subletting provision exactly as written.

If it is `Not addressed`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever transfer language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative restriction, the consent standard, any deemed-approval mechanism, **any recapture or termination right**, and any permitted-transfer carve-out. Include the sentence containing each.
- Quote the definition of any defined term the provision relies on — `Transfer`, `Affiliate`, `Permitted Transferee`, `Control` — where the definition appears in the unit.
- Where the clause exceeds 250 words, quote the operative restriction, the consent standard, the recapture right, and each carve-out, replacing intervening procedural text with `[...]` between sentences.
- Do not quote the change of control provision separately here; it has its own column, but where the same sentence covers both, quote it in full.
- Do not add analysis, and do not indicate whether this transaction triggers the clause.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 25. Landlord Recapture Right

- Native type: Classify
- Configured options, in UI order: `Recapture of whole premises`, `Recapture of affected space only`, `Termination right on request for consent`, `Right to profit share only`, `No recapture right`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Assignment and Subletting`
- Downstream: none
- Purpose: **worse than a consent requirement.** A recapture right lets the
  landlord take the space back instead of consenting, which turns a transfer
  request into a loss of the site.

Where the target's plan depends on retaining a location, a recapture right changes
the strategy: you do not ask for consent until you have to, and you may not ask at
all.

```markdown
## Established result

- Assignment and subletting: @Assignment and Subletting

## Task

If Assignment and Subletting is any value other than `Freely permitted`, `Not addressed`, or `Unable to determine`, classify whether the landlord may recapture the premises or terminate in response to a request to transfer.

If it is `Freely permitted`, return `Not applicable`.

If it is `Not addressed` or `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Recapture of whole premises`: on a request for consent, the landlord may take back the entire premises and terminate the lease. **The most severe form**, and it applies even where the tenant sought to sublet only part.
2. `Recapture of affected space only`: the landlord may take back only the space proposed to be assigned or sublet.
3. `Termination right on request for consent`: the landlord may terminate the lease rather than consent, without a recapture mechanism as such.
4. `Right to profit share only`: the landlord takes a share of any premium, profit rent, or consideration on the transfer, with no right to take the space. Report the share in Consent Conditions.
5. `No recapture right`: the lease addresses transfer and gives the landlord no right to recapture, terminate, or share profit.

Report in the evidence field any period within which the landlord must exercise the right, and any right the tenant has to withdraw its request and so defeat the recapture. **A withdrawal right is what makes a recapture provision manageable**, because the tenant can test the landlord's position without committing.

## Fallback rules

- Use `Unable to determine` where the provision is illegible or incomplete.

## Output format

Return only the exact configured option and no explanation.
```

---

### 26. Consent Conditions

- Native type: Free Response
- Upstream: `@Assignment and Subletting`
- Downstream: none
- Purpose: the mechanics and the price of obtaining consent, which set the
  timetable and the cost for the consent schedule.

```markdown
## Established result

- Assignment and subletting: @Assignment and Subletting

## Task

If Assignment and Subletting requires consent, report the conditions and mechanics for obtaining it.

If it is `Freely permitted` or `Not addressed`, return exactly `Not applicable`.

If it is `Prohibited absolutely`, report any conditions on which the landlord may nonetheless agree, and where none are stated return `Not applicable — prohibited`.

If it is `Unable to determine`, return exactly `Unable to determine — upstream restriction is unresolved`.

## Include where expressly stated

- The information the tenant must provide with a request, including financial statements of the proposed transferee
- **The period within which the landlord must respond, and any deemed-approval or deemed-refusal consequence**
- The landlord's costs the tenant must pay: legal fees, surveyor's fees, administrative charges, and whether they are capped
- Any financial test the transferee must satisfy: net worth, credit rating, or trading history
- Any requirement that the transferee use the premises for the same use
- **Any requirement that the tenant remain liable after assignment**, by guarantee, authorised guarantee agreement, or direct covenant
- Any profit share or premium payable to the landlord, with the percentage
- Any requirement to offer the space back to the landlord first
- Any requirement for the transferee to enter into a direct covenant or a new guaranty

## Rules

- **Report the response period and the continuing-liability requirement as the two most consequential items.** The first sets the timetable; the second determines whether the seller's group is released at all.
- Report cost obligations as stated, including whether uncapped.
- Report the terms as stated. Do not assess reasonableness and do not predict whether consent would be given.

## Output format

`Response period: [as stated or "none"]; deemed outcome: [approval | refusal | none]; landlord costs: [as stated]; transferee test: [brief or "none"]; tenant remains liable: [yes | no | Not addressed]; profit share: [as stated or "none"]`

Return no more than 85 words.
```

---

### 27. Permitted Transfer Carve-Out

- Native type: Classify
- Configured options, in UI order: `Successor and affiliate transfers permitted`, `Affiliate transfers permitted only`, `Successor transfers permitted only`, `Permitted subject to conditions`, `No carve-out`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Assignment and Subletting`
- Downstream: none
- Purpose: **whether the transaction needs consent at all.**

Same pattern as the succession carve-out in Contracts Core, and the same
significance: a consent-required lease with a carve-out for transfers to a
successor by merger or a purchaser of the business does not go on the consent
schedule. Filtering this column against `Assignment and Subletting` produces the
consent list.

```markdown
## Established result

- Assignment and subletting: @Assignment and Subletting

## Task

If Assignment and Subletting is `Consent required, no standard`, `Consent required, not to be unreasonably withheld`, `Consent required with deemed approval`, `Prohibited absolutely`, or `Permitted to affiliate only`, classify whether the lease permits transfers to a successor or an affiliate without consent.

If it is `Freely permitted` or `Not addressed`, return `Not applicable`.

If it is `Unable to determine`, return `Unable to determine`.

Choose exactly one configured option.

## Classification rules

- `Successor and affiliate transfers permitted`: the lease permits transfer without consent both to a successor by merger, consolidation, or purchase of all or substantially all of the tenant's assets or business, and to a group company.
- `Successor transfers permitted only`: a successor carve-out with no affiliate carve-out. **This is the one that matters for the transaction**, because it is what takes the lease off the consent schedule.
- `Affiliate transfers permitted only`: a group-company carve-out with nothing covering a successor. **An affiliate carve-out does not help a third-party acquisition**, and conflating the two is the standard error here.
- `Permitted subject to conditions`: a carve-out exists but is conditional — on prior notice, on the transferee meeting a net worth test, on the transferee assuming the obligations in writing, or on the tenant remaining liable. Report the conditions in the evidence field, since an unmet condition means consent is required after all.
- `No carve-out`: the lease addresses transfer and provides no exception for successors or affiliates.

Apply these boundaries:

- **A provision that the lease binds successors and permitted assigns is boilerplate about who is bound. It is not a permission to assign** and it does not support a carve-out classification.
- A right to share occupation with a group company, without transferring the lease, is not a transfer carve-out. Note it in the evidence field.
- Where a carve-out exists but the change of control provision separately captures the transaction, classify the carve-out here as stated; the CoC columns carry the separate trigger.

## Fallback rules

- Use `Unable to determine` where the carve-out language is illegible or incomplete.
- Do not use `No carve-out` where the lease addresses succession in terms you find ambiguous. That is `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 28. CoC Treated as Assignment

- Native type: Classify
- Configured options, in UI order: `Deemed assignment requiring consent`, `Consent required directly`, `Notice required`, `Landlord termination right`, `Addressed, no consequence`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `CoC Language`
- Purpose: whether a change of control of the tenant trips the lease independently
  of any actual transfer. **In a share purchase, this is usually the only lease
  provision the transaction engages.**

```markdown
## Task

Classify how this lease treats a change of ownership or control **of the tenant**. Choose exactly one configured option.

## Scope

- Consider provisions triggered by a change in the ownership, shareholding, voting control, or management control of the tenant, however described.
- Include a provision deeming such a change to be an assignment or transfer.
- Include a provision triggered by a change in control of a guarantor.
- Exclude provisions triggered only by a change of control of the landlord.
- Exclude insolvency provisions not tied to a control change.
- Where a later document in the unit changes the provision, classify on the most recently dated document that addresses it.

## Classification rules

Apply the first rule that fits.

1. `Landlord termination right`: the landlord may terminate the lease on a change of control of the tenant.
2. `Deemed assignment requiring consent`: the lease deems a change of control to be an assignment, so the assignment consent machinery applies. **Report this rather than `Consent required directly` where the mechanism is deeming**, because the recapture right and the consent conditions then apply too, and that is a materially worse position.
3. `Consent required directly`: the change of control itself requires the landlord's consent, without being deemed an assignment.
4. `Notice required`: the tenant must notify the landlord, with no consent or termination right attached.
5. `Addressed, no consequence`: a change of control is referenced or defined and no obligation attaches to it.

Report in the evidence field any threshold percentage stated, whether the provision reaches indirect or ultimate parent ownership, and any carve-out for a transfer to a group company or for a listing.

**Where the provision reaches only a transfer of the tenant's own shares and says nothing about indirect ownership, note that.** A holdco-level transaction may fall outside it entirely.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses a change of control of the tenant. **This is a common and welcome answer** — many leases are silent, and silence means the share purchase does not engage the lease.
- Use `Unable to determine` where the provision is illegible, incomplete, or conflicting.

## Output format

Return only the exact configured option and no explanation.
```

---

### 29. CoC Language

- Native type: Verbatim
- Upstream: `@CoC Treated as Assignment`
- Downstream: none
- Purpose: the exact trigger text, including the threshold and the definition of
  control, which decides whether the deal as structured falls inside it.

```markdown
## Established result

- CoC treated as assignment: @CoC Treated as Assignment

## Task

If CoC Treated as Assignment is any value other than `Not addressed` or `Unable to determine`, quote the change of control provision exactly as written.

If it is `Not addressed`, return exactly `Not addressed`.

If it is `Unable to determine`, quote whatever change of control language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the trigger together with the definition of control or change of control the provision relies on, including any percentage threshold and any reference to direct or indirect ownership**, where the definition appears in the unit. Whether this transaction falls inside the clause is decided there.
- Quote any carve-out — for a transfer to a group company, an internal reorganisation, a listing, or a transfer among existing shareholders.
- Quote any deeming words, since they are what pull in the assignment machinery.
- Where the combined text exceeds 250 words, quote the operative provision and every limb and carve-out of the control definition, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction triggers the provision.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 30. Permitted Use

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the target may do at the premises, which constrains the buyer's
  operational plans and can block a change of use or a sublet.

```markdown
## Task

Report the permitted use of the premises and any restriction on it.

## Include where expressly stated

- The permitted use as printed, and whether it is narrow and specific or broad and general
- **Any requirement for landlord consent to a change of use**, and any standard on that consent
- Any prohibited use, whether specific or by category
- Any restriction imposed by the building's rules, a centre's tenant mix policy, or a superior lease
- Any restriction arising from another tenant's exclusive right, where the lease discloses it
- Any hours-of-operation restriction
- Any restriction on hazardous materials, cooking, or noise
- Any requirement that the tenant hold and maintain a licence or permit for the use

## Rules

- **Report the breadth of the use clause explicitly.** A use clause naming one specific trade prevents a sublet to anyone in a different business, which is what turns a surplus site into a stranded cost. A general office or general retail use clause does not.
- Report any licence or permit requirement, since it joins this row to the Regulatory table and a lapsed permit can be a lease default as well as a regulatory one.
- Report the terms as stated. Do not assess whether the target's current operations fall within the permitted use.

## Fallback rules

- Return `Not addressed` where the documents state no permitted use.
- Return `Incorporated terms` where the use is stated to be governed by rules or a superior document not present in the unit.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Permitted use: [as printed]; breadth: [specific | general]; change of use: [consent required and standard, or "Not addressed"]; prohibited: [brief or "none stated"]; licence required: [as stated or "Not addressed"]`

Return no more than 75 words.
```

---

### 31. Exclusive Use Right

- Native type: Classify
- Configured options, in UI order: `Exclusive granted to tenant`, `Exclusive granted, subject to exceptions`, `Other tenant's exclusive disclosed`, `Expressly no exclusive`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the target has protection from competing uses in the same
  building or centre, or is itself constrained by another tenant's protection.

```markdown
## Task

Classify any exclusive use right relating to these premises. Choose exactly one configured option.

## Scope

- Consider rights preventing the landlord from letting other space in the building, centre, or development for a competing use.
- Consider disclosures of other tenants' exclusive rights that constrain the target's use.
- Exclude the permitted use clause itself, which has its own column.
- Exclude radius restrictions preventing the tenant opening nearby, which are reported in the evidence field.

## Classification rules

- `Exclusive granted to tenant`: the landlord covenants not to permit a competing use, with no material exception. **A valuable right and one that may be lost on an assignment**, so note in the evidence field whether it is personal to the named tenant.
- `Exclusive granted, subject to exceptions`: an exclusive with carve-outs for existing tenants, anchor tenants, incidental sales, or a stated proportion of another tenant's floor area. Report the exceptions in the evidence field, since a widely carved-out exclusive is worth little.
- `Other tenant's exclusive disclosed`: the lease discloses an exclusive held by another tenant which restricts what the target may do. **This is a constraint, not a benefit**, and it belongs in the same column so the two are never confused.
- `Expressly no exclusive`: the lease states that the tenant has no exclusive right and the landlord may let to competitors.
- `Not applicable`: the premises are not part of a multi-tenant building or centre.

Report in the evidence field the tenant's remedy for a breach of its exclusive — rent abatement, self-help, injunction, or termination — since an exclusive with no remedy is close to unenforceable in practice.

## Fallback rules

- Use `Not addressed` where the documents address neither the tenant's nor any other tenant's exclusive rights.
- Use `Unable to determine` where provisions conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 32. Continuous Operation Covenant

- Native type: Classify
- Configured options, in UI order: `Keep-open covenant with stated hours`, `Keep-open covenant, hours not stated`, `Trading covenant with termination remedy`, `Expressly no keep-open obligation`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the target **must** trade from the premises. **A keep-open
  covenant prevents closing a loss-making site**, which is the opposite problem
  from a lease you cannot get out of and is easily missed in an integration plan.

```markdown
## Task

Classify any obligation on the tenant to keep the premises open and trading. Choose exactly one configured option.

## Scope

- Consider covenants to keep open, to trade continuously, to operate during stated hours, or to maintain a stated level of staffing or stock.
- Consider any consequence of ceasing to trade: landlord termination right, recapture, loss of an exclusive, or increased rent.
- Exclude a covenant not to leave the premises vacant or unattended for security purposes.
- Exclude the permitted use clause.

## Classification rules

- `Keep-open covenant with stated hours`: the tenant must trade during specified hours or days. **Most restrictive**, and it constrains the buyer's operating model directly.
- `Keep-open covenant, hours not stated`: an obligation to trade continuously without specified hours.
- `Trading covenant with termination remedy`: the tenant may cease trading but the landlord may then terminate, recapture, or take a stated remedy. **This is the manageable form**: closing the site is possible, at the cost of the lease.
- `Expressly no keep-open obligation`: the lease states that the tenant is not required to trade.
- `Not applicable`: the premises are office, industrial, or warehouse space where no trading obligation could arise, and the documents impose none.

Report in the evidence field whether percentage rent is payable, since a keep-open covenant alongside turnover rent is the standard retail combination and the two interact.

## Fallback rules

- Use `Not addressed` where the documents impose no trading obligation and do not disclaim one.
- Use `Unable to determine` where provisions conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 33. Restoration and Surrender

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what must be done at the end of the term. **An end-of-term liability
  that belongs in the price and appears in no rent roll**, and on a fitted-out
  office or a ground lease it can be substantial.

```markdown
## Task

Report the tenant's obligations at the end of the term.

## Include where expressly stated

- **Any obligation to remove alterations, improvements, fixtures, or cabling, and to reinstate the premises to a stated condition**
- Whether the obligation extends to the landlord's own base building works or only to the tenant's alterations
- Whether the landlord may elect whether removal is required, and when that election must be made
- Any obligation to remove specific items identified in a licence for alterations or a work letter
- The standard the premises must be returned in: original condition, base building, shell and core, or good repair and condition
- Any obligation to pay a sum in lieu of reinstatement
- Any dilapidations, repairing, or redecoration obligation at the end of the term
- For a ground lease, whether improvements pass to the landlord or must be removed
- Any obligation to remove signage or to restore a facade
- Any obligation to deliver up free of subleases and occupants

## Rules

- **Report whether the landlord holds an election and by when.** An unexercised election means the liability is contingent and unquantified, and the deadline is what a buyer would want to know.
- **Report the reinstatement standard as printed**, since original condition and good repair are materially different obligations.
- Report any obligation to deliver up free of occupants, since it means a sublease must be terminated first.
- Report the obligations as stated. **Do not estimate a cost.** Quantification is a surveyor's exercise.

## Fallback rules

- Return exactly `None` where the documents impose no end-of-term restoration or reinstatement obligation.
- Return `Incorporated terms` where the obligations sit in a licence for alterations or a schedule of condition not present in the unit. **This is a common and important gap**, because the schedule of condition defines the standard.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Removal obligation: [as stated]; standard: [as printed]; landlord election: [yes, by [date or trigger] | no | Not addressed]; sum in lieu: [as stated or "none"]; free of occupants: [yes | Not addressed]`

Return no more than 80 words. Do not include a cost estimate.
```

---

### 34. Holdover

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what happens if the target stays past expiry. **Holdover rent at 150 or
  200 percent is a real and immediate cost** where a site cannot be vacated on
  time, which is common during an integration.

```markdown
## Task

Report the consequences of the tenant remaining in occupation after the term ends.

## Include where expressly stated

- The holdover rent, as a multiple or percentage of the last base rent, and whether additional rent is also multiplied
- Whether the multiple escalates over successive holdover periods
- The tenancy that arises on holdover: month-to-month, periodic, at will, or none
- Any notice required to terminate a holdover tenancy
- **Any liability for the landlord's consequential losses**, including losses to an incoming tenant. This is the exposure that dwarfs the rent multiple, and it is frequently uncapped
- Any indemnity given to the landlord in respect of holdover
- Whether holdover requires the landlord's consent, and whether occupation without consent is a trespass

## Rules

- **Report the consequential loss exposure prominently and separately from the rent multiple.** A 150 percent rent is quantifiable; an uncapped indemnity for the landlord's losses to a replacement tenant is not, and it is the larger risk.
- Report the multiple as stated. Do not calculate the resulting amount.
- Report whether the multiple applies to additional rent as well as base rent, since in a net lease that roughly doubles the effect.

## Fallback rules

- Return `Not addressed` where the documents do not address holdover. Note in the evidence field that the position is then governed by local law, which the reviewer establishes.
- Return `Incorporated terms` where the provisions sit in a document not present in the unit.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Rent: [multiple or percentage][, applies to additional rent: yes | no]; tenancy: [as stated]; consequential losses: [as stated or "Not addressed"]; indemnity: [yes | Not addressed]`

Return no more than 65 words.
```

---

### 35. Early Termination and Event Triggers

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: every route out of the lease before expiry, whether elective or
  event-driven. **A break right is an asset in an integration**, and a casualty
  termination right can be exercised by the landlord against the target.

```markdown
## Task

Report every right to terminate this interest before the end of the term, and every event that triggers termination.

## Include where expressly stated

- **Any elective break or termination option, who holds it, the exercise date or window, the notice required, and any termination payment or penalty.** Where the tenant holds it, this is an exit route worth quantifying
- Any condition on exercising a break right, such as no subsisting default or the return of the premises in a stated condition
- Casualty or damage: which party may terminate, at what damage threshold, and any obligation to rebuild
- Condemnation or compulsory purchase: which party may terminate, and any apportionment of the award
- Any termination right on the landlord's failure to deliver possession by a stated date
- Any termination right on failure to obtain a permit, licence, or consent
- Any landlord right to terminate to redevelop, refurbish, or relocate the tenant
- Any relocation right permitting the landlord to move the tenant within the building

## Rules

- **Report the holder of each right, and the exercise window as stated.** A tenant break right whose window has already passed is worth nothing, so compare each window to the diligence as-of date and append ` [window passed]` where it has, or ` [window open]` where it is current.
- **Report any landlord redevelopment or relocation right prominently.** It is a risk to site continuity that no other column captures.
- Report casualty and condemnation thresholds as stated. Do not assess likelihood.
- Report termination payments as stated. Do not calculate.

## Fallback rules

- Return exactly `None` where no early termination right or trigger exists.
- Return `Incorporated terms` where the provisions sit in a document not present in the unit.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

One line per right or trigger:

`[Right or trigger] — holder: [party]; window: [as stated]; notice: [period]; payment: [as stated or "none"]`, with any bracketed flag appended.

Return no more than 6 lines and no more than 90 words.
```

---

### 36. Expansion and Preferential Rights

- Native type: Classify
- Configured options, in UI order: `Expansion option`, `Right of first refusal`, `Right of first offer`, `Multiple preferential rights`, `None`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: rights over additional space, which are assets in a growth plan and can
  be lost by inaction or on an assignment.

```markdown
## Task

Classify any right the tenant holds over additional space in the building or development. Choose exactly one configured option.

## Scope

- Consider expansion options, rights of first refusal, rights of first offer, must-take space, and rights over specifically identified space.
- Exclude renewal and extension rights over the existing premises, which have their own column.
- Exclude any right to purchase the building, which is reported in the evidence field.

## Classification rules

- `Expansion option`: a right to take identified additional space on stated terms, exercisable by notice.
- `Right of first refusal`: a right to take space on the terms of an offer the landlord has received from a third party. Weaker than an option because it is reactive and usually time-limited.
- `Right of first offer`: a right to be offered space before it is marketed.
- `Multiple preferential rights`: more than one of the above. Report each in the evidence field.
- `None`: the lease addresses additional space and confers no right.

Report in the evidence field the space identified, the exercise window, the rent basis for the additional space, whether the right is personal to the named tenant, and whether it lapses if not exercised on a first opportunity. **A right personal to the named tenant does not pass on the transaction**, which is the same trap as in the renewal column.

Where a must-take obligation exists — an obligation rather than a right to take further space — report it here and note that it is an obligation, since it is a committed future cost.

## Fallback rules

- Use `Not addressed` where the documents say nothing about additional space.
- Use `Unable to determine` where provisions conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 37. Lender-Related Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the tenant's obligations towards the landlord's lender, and the
  protection it has from a foreclosure. **A lease subordinated with no
  non-disturbance protection can be terminated by a foreclosing lender.**

```markdown
## Task

Report the tenant's obligations and protections relating to the landlord's financing.

## Include where expressly stated

- Whether the lease is subordinate to existing or future mortgages, and whether subordination is automatic or requires a document
- **Whether the tenant has the benefit of a non-disturbance covenant**, and whether it is conditional on the tenant not being in default
- Any obligation to enter into a subordination, non-disturbance, and attornment agreement, and any deadline for doing so
- Any obligation to attorn to a successor landlord or a foreclosing lender
- **Any obligation to deliver an estoppel certificate on request, the period for responding, and any deemed-certification consequence of failing to respond**
- Any obligation to give the lender notice of a landlord default and an opportunity to cure
- Any restriction on amending the lease without the lender's consent
- Any mortgagee named in the documents, and whether an SNDA is present in the unit
- Any obligation to deliver the tenant's financial statements to the landlord or its lender

## Rules

- **Report the non-disturbance position explicitly, and report its absence where the lease subordinates without it.** Subordination without non-disturbance is the finding, and it is exactly the case an SNDA is obtained to fix.
- Report the estoppel response period and any deemed-certification provision, because a short deadline with deemed effect is an operational trap for the buyer after closing.
- Report any lender consent requirement for lease amendments, since it adds a party to any future variation.
- Report the obligations as stated. Do not assess the effect of a foreclosure.

## Fallback rules

- Return `Not addressed` where the documents address none of these matters.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Subordination: [automatic | on request | Not addressed]; non-disturbance: [unconditional | conditional | absent]; SNDA obligation: [as stated]; estoppel: [period and deemed effect]; lender consent to amendment: [yes | Not addressed]; mortgagee named: [name or "none"]`

Return no more than 80 words.
```

---

### 38. Landlord Default Remedies

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the target can do if the landlord stops performing. **Usually very
  little**, and knowing that shapes how a dispute over services or repairs is
  handled after closing.

```markdown
## Task

Report the tenant's remedies for a landlord default, and any limitation on them.

## Include where expressly stated

- Any notice and cure period the tenant must give before a remedy arises
- Any self-help right to perform the landlord's obligations, and any cap on recoverable cost
- **Any right of set-off, abatement, or deduction from rent**, and any express prohibition on set-off
- Any right to terminate for a landlord default, and the threshold
- Any rent abatement for interruption of services, access, or utilities, and the period after which it applies
- Any cap or exclusion of the landlord's liability, including exclusion of consequential loss
- Any limitation of the landlord's liability to its interest in the property, or to a stated amount
- Any obligation on the tenant to notify the landlord's lender and allow it to cure
- Any waiver of the tenant's statutory remedies

## Rules

- **Report any express prohibition on set-off prominently.** It is very common and it means the tenant must keep paying rent in full while pursuing the landlord separately, which is the practical answer to most service failures.
- **Report any limitation of the landlord's liability to its interest in the property.** Where the landlord is a single-asset entity, that limitation makes a damages claim close to worthless.
- Report any service-interruption abatement and the qualifying period, since it is the one remedy that usually operates automatically.
- Report the terms as stated. Do not assess whether a remedy would be effective or whether a waiver is enforceable.

## Fallback rules

- Return `Not addressed` where the documents provide no tenant remedy and impose no limitation.
- Return `Unable to determine` where provisions conflict, or are illegible.

## Output format

`Cure period: [as stated or "none"]; self-help: [as stated or "none"]; set-off: [permitted | prohibited | Not addressed]; abatement: [as stated or "none"]; termination right: [as stated or "none"]; landlord liability limit: [as stated or "none"]`

Return no more than 80 words.
```

---

### 39. Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the governing law, which for real property is usually the situs but is
  worth confirming for a ground lease or a cross-border portfolio.

```markdown
## Task

Identify the governing law of this interest.

## Rules

- Report the jurisdiction chosen to govern, as stated.
- Report the jurisdiction only. Do not report the forum, venue, or arbitral seat.
- **Where the governing law differs from the jurisdiction in which the property is located, append ` [differs from situs]`.** Real property matters are generally governed by the law of the situs regardless of the parties' choice, so a mismatch is worth flagging rather than accepting.
- Where the documents state no choice of law, note in the evidence field the jurisdiction the property is in, taken from the Property Address column.
- Where different documents in the unit choose different law, report the choice in the most recently dated document and note the difference.

## Fallback rules

- Return `Not addressed` where no document in the unit contains a choice of law. **This is common for a lease and it is not a defect**, since the situs governs.
- Return `Unable to determine` where choices conflict irreconcilably.

## Output format

`[Jurisdiction]`, with any flag appended. Return no more than 25 words.
```

---

### 40. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this lease family refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this interest that the documents in this unit refer to and that is not present.

## Scope

- Include amendments, extensions, and modifications referenced but absent.
- **Include any commencement letter, delivery notice, or confirmation of dates referenced as fixing the term dates.** Without it the dates are unknown.
- **Include the head lease where the target is a subtenant.** The sublease's security depends on it entirely.
- Include guaranties required or referenced but not produced.
- Include estoppel certificates and SNDAs referenced or required but not produced.
- Include exhibits, floor plans, work letters, schedules of condition, and licences for alterations listed as attached but not present.
- Include building rules and regulations, tenant handbooks, and centre rules incorporated by reference.
- Include consents to prior assignments or subleases referenced but absent, **since an unconsented prior transfer is a subsisting breach**.
- Include any superior lease, reciprocal easement agreement, declaration, or CC&Rs the lease is stated to be subject to.
- Include notices of exercise of any option referenced but absent.
- Include insurance certificates the lease requires the tenant or landlord to deliver.
- Exclude statutes, regulations, and building codes.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Rules and Regulations`, report it as printed and add `(no date stated)`.
- **Where a commencement letter or confirmation of dates is referenced and absent, add `; term dates unresolved`.**
- **Where a consent to a prior assignment or sublease is referenced and absent, add `; prior transfer consent`.**
- **Where a head lease is absent, add `; sublease depends on it`.**
- Where a schedule of condition or licence for alterations is absent, add `; reinstatement standard unknown`.
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
| **Consent required for this structure** | Yes / No / Ambiguous |
| **Recapture risk on consent request** | None / Affected space / Whole premises / Unclear |
| **Site criticality** | Critical / Important / Replaceable |
| **Estoppel required** | Yes / No |
| **End-of-term liability estimate** | Free text |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: property address, tenant entity, expiry,
rent, assignment and change of control, guaranty.

### Reconciliation work that never belongs in a column

- **Site list completeness, both directions.** Every row against the operations
  site list, and every operating location against these rows. Cross-check
  addresses against licences, permits, insurance schedules, environmental reports,
  and payroll locations. **A site with operations and no lease is the finding**, and
  a lease for a site nobody operates from is a stranded cost.
- **Consent schedule.** Filter `Assignment and Subletting` to consent-required
  states, then filter out rows where `Permitted Transfer Carve-Out` is
  `Successor and affiliate transfers permitted` or `Successor transfers permitted
  only`. Add every row where `CoC Treated as Assignment` is anything other than
  `Not addressed`. **Then check `Landlord Recapture Right` on every surviving row
  before deciding whether to ask.**
- **Occupancy cost model.** Base rent, escalation, and additional rent exported to
  Excel and modelled against the term. **All of it is arithmetic and none of it is
  a column.**
- **End-of-term liabilities.** Every row with a restoration obligation, priced by
  a surveyor. This is usually the largest unbooked real estate liability.
- **Guarantor survival.** Every row where the guarantor is outside the target
  group, against the transaction structure. Each needs a replacement guaranty or a
  release.
- **Letter of credit inventory.** Every row with an LC, against the facility
  documents in the Debt table. LCs consume facility capacity and expiries need
  diarising.
- **Option calendar.** Every renewal, break, expansion, and preferential right
  window, sequenced against the deal and integration timetable, with a named
  owner. **A missed option notice is usually irrecoverable.**
- **Estoppel programme.** Material leases where an estoppel is required or where
  the lease and any existing estoppel conflict.

---

## Test set

- [ ] Office lease with amendments, estoppel, and commencement letter, complete
- [ ] Lease fixing commencement by formula, with no commencement letter produced
- [ ] Lease where the estoppel states a rent differing from the lease as amended
- [ ] Sublease with the head lease not produced
- [ ] Sublease where the target is sublandlord
- [ ] Ground lease with improvements reverting to the landlord
- [ ] Co-working membership agreement
- [ ] Triple net lease that makes the landlord responsible for taxes
- [ ] Modified gross lease with a base year eight years old
- [ ] Lease with an uncapped index-linked escalation
- [ ] Lease with a cap on controllable operating expenses only
- [ ] Lease with capital expenditure expressly passed through
- [ ] Retail lease with percentage rent and an ambiguous online sales definition
- [ ] Lease with a letter of credit expiring within six months of the as-of date
- [ ] Lease with an evergreen letter of credit and a burn-down schedule
- [ ] Lease requiring increased security on a change of control
- [ ] Lease guaranteed by a parent outside the acquired group
- [ ] Lease requiring a guaranty with no guaranty document produced
- [ ] Lease with an unsigned guaranty
- [ ] Lease with an unclaimed tenant improvement allowance and a passed deadline
- [ ] Lease with consent required, no reasonableness standard
- [ ] Lease with consent required and deemed approval after thirty days
- [ ] Lease with a landlord recapture right over the whole premises
- [ ] Lease with a profit share on assignment and no recapture
- [ ] Lease with a successor carve-out and no affiliate carve-out
- [ ] Lease with an affiliate carve-out only
- [ ] Lease whose only transfer language is successors-and-assigns boilerplate
- [ ] Lease deeming a change of control to be an assignment
- [ ] Lease with a change of control provision reaching indirect ownership
- [ ] Lease silent on change of control
- [ ] Retail lease with a keep-open covenant and stated hours
- [ ] Lease with a specific single-trade permitted use
- [ ] Lease disclosing another tenant's exclusive
- [ ] Lease with a landlord redevelopment termination right
- [ ] Lease with a tenant break right whose window has passed
- [ ] Lease with a tenant break right currently exercisable
- [ ] Lease with holdover rent at 200 percent plus uncapped consequential losses
- [ ] Lease with a full restoration obligation and a landlord election not yet made
- [ ] Lease referencing a schedule of condition not produced
- [ ] Lease subordinated with no non-disturbance covenant
- [ ] Lease prohibiting set-off with the landlord's liability limited to the property
- [ ] Lease whose term expired two years before the as-of date, no extension produced
- [ ] Lease with an estoppel confirming the tenant is holding over
- [ ] Terminated lease with a surrender agreement
- [ ] Unit mistakenly containing two properties

Then test the dependencies: change `Assignment and Subletting` from
`Consent required, no standard` to `Freely permitted` and confirm
`Landlord Recapture Right`, `Consent Conditions`, and
`Permitted Transfer Carve-Out` all move to `Not applicable` after rerun, and that a
locked `Assignment Language` cell does not retain the old quotation. Change
`Interest Type` from `Lease, target as tenant` to
`Sublease, target as subtenant` and confirm `Chain Completeness` can reach
`Head lease absent`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
