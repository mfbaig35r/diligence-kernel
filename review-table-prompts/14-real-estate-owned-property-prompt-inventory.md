# Prompt Inventory — Real Estate: Owned Property

Table 14 of the POC. Companion to Leasehold.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Real Estate`
- Review unit: **one owned property** — the acquisition deed, any title report or
  commitment, the survey, any easement or restrictive covenant document,
  recorded mortgages and releases, and the current property tax statement
- Grouping used: **yes**, typically 3–8 documents per unit
- Row count: usually 0 to 15 per matter, and often 0
- Intended reviewers and downstream use: real estate and corporate/M&A teams;
  feeds the title exception schedule, the lien release checklist, the transfer tax
  analysis, and the coverage register
- Inventory version: v1.0

### Roles in one unit, handled deliberately

Unlike the other tables, this row set genuinely mixes roles: the deed is an
Instrument, the title report and survey are Analysis, the mortgage is an
Instrument, and the tax statement is a Record. That is acceptable here for the
same reason it is in the Corporate table — **the row is the property, not the
document**, and the property cannot be understood from any one of them.

The discipline that makes it work: **every substantive column names which document
it reads from, and reports the source in its answer.** A vesting statement from a
title report and a grantee named in a deed are different evidence with different
weight, and the reviewer must be able to tell which one produced the cell.

### The three questions

1. **Does the target own it, and how is title held?** Vesting per the title
   report, tested against the target group.
2. **What is title subject to?** Exceptions, liens, easements, and restrictive
   covenants — and which of them a purchaser would object to.
3. **What does the transaction cost or trigger?** Mortgage releases, transfer
   restrictions, and above all **real property transfer tax on an indirect
   change of control**, which is a genuine and frequently missed M&A cost.

## Assumptions to confirm before running

1. Most targets own no real property. **An empty table is a legitimate and common
   result**, and it should be recorded as such rather than left unbuilt, because
   the coverage register needs to show that owned property was considered.
2. One row is one property as the title report treats it. Several contiguous
   parcels under one title commitment are one row; separate commitments are
   separate rows.
3. Leased property is a separate table. Where the target owns a property and
   leases part of it out, the lease is a Leasehold row with the target as
   sublandlord, and the property is a row here.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

21 Harvey columns plus 8 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side real estate diligence on the target group listed below. This table reviews owned real property.

One row is one owned property: the acquisition deed, any title report or commitment, the survey, any easement or restrictive covenant document, recorded mortgages and releases, and the current property tax statement. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the property or the parties.
- **Name the source document for every substantive answer.** A title report, a deed, a survey, and a tax statement are different kinds of evidence, and a reviewer must be able to tell which produced each cell. Use the format `[answer] — per [document title], [YYYY-MM-DD]`.
- **A title report states the position as at its effective date and nothing later.** Where it conflicts with a deed or a recorded instrument in the unit, report both and identify each source. Do not treat one as correcting the other.
- **Report what the documents state. Do not opine on title, marketability, or the effect of any exception.** A title opinion is a lawyer's work product and it is not in a commitment.
- Report figures only as the documents state them. Do not calculate, total, or convert.
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
  Property Address
  Interest Type
  Legal Description

Stage 2 — Evidence available
  Documents in Unit ──→ Title Evidence Available
                        Recording Evidence
                        Referenced but Not Produced

Stage 3 — Ownership
  Title Evidence Available ──→ Vesting as Reported
                               Title Exceptions
  Vesting as Reported      ──→ Owner Matches Target Entity
  Acquisition Instrument                            (no upstream)

Stage 4 — Encumbrances
  Monetary Liens
  Easements and Access
  Restrictive Covenants and Declarations
  Survey Findings
  Mortgage and Financing

Stage 5 — Regulatory and cost
  Zoning and Permitted Use
  Property Tax Status
  Transfer Restrictions and Change of Control
  Transfer Tax Exposure
  Environmental Documents Referenced
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Title Evidence Available; Recording Evidence; Referenced but Not Produced | v1.0 | draft |
| 2 | Property Address | Free Response | — | — | v1.0 | draft |
| 3 | Interest Type | Classify | — | — | v1.0 | draft |
| 4 | Legal Description | Free Response | — | — | v1.0 | draft |
| 5 | Title Evidence Available | Classify | @Documents in Unit | Vesting as Reported; Title Exceptions | v1.0 | draft |
| 6 | Acquisition Instrument | Free Response | — | — | v1.0 | draft |
| 7 | Recording Evidence | Free Response | @Documents in Unit | — | v1.0 | draft |
| 8 | Vesting as Reported | Free Response | @Title Evidence Available | Owner Matches Target Entity | v1.0 | draft |
| 9 | Owner Matches Target Entity | Classify | @Vesting as Reported | — | v1.0 | draft |
| 10 | Title Exceptions | Free Response | @Title Evidence Available | — | v1.0 | draft |
| 11 | Monetary Liens | Free Response | — | — | v1.0 | draft |
| 12 | Easements and Access | Free Response | — | — | v1.0 | draft |
| 13 | Restrictive Covenants and Declarations | Free Response | — | — | v1.0 | draft |
| 14 | Survey Findings | Free Response | — | — | v1.0 | draft |
| 15 | Mortgage and Financing | Free Response | — | — | v1.0 | draft |
| 16 | Zoning and Permitted Use | Free Response | — | — | v1.0 | draft |
| 17 | Property Tax Status | Free Response | — | — | v1.0 | draft |
| 18 | Transfer Restrictions and Change of Control | Classify | — | — | v1.0 | draft |
| 19 | Transfer Tax Exposure | Free Response | — | — | v1.0 | draft |
| 20 | Environmental Documents Referenced | Free Response | — | — | v1.0 | draft |
| 21 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Title Evidence Available`, `Recording Evidence`, `Referenced but Not Produced`
- Purpose: inventory the property file, so a reviewer can see which kinds of
  evidence are present before reading any answer.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the acquisition deed, any prior deeds in the chain, title reports, title commitments, title insurance policies, surveys, easement and restrictive covenant documents, declarations and CC&Rs, recorded mortgages and deeds of trust, releases and reconveyances, property tax statements, assessment notices, and zoning letters or certificates.
- Treat exhibits and legal descriptions attached to a document as part of that document.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- **Give each document's own stated date, and for a title report or commitment give its effective or search date rather than its issue date.** The effective date is what limits the report, and it is often weeks earlier.
- State the function as one of `Deed`, `Prior deed`, `Title report or commitment`, `Title policy`, `Survey`, `Easement`, `Declaration or CC&Rs`, `Mortgage or deed of trust`, `Release or reconveyance`, `Tax statement`, `Zoning document`, or `Other`.
- **Where a document relates to a different property or parcel than the subject of this row, still list it and append ` [relates to [property or parcel]]`.**

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 15 lines and no more than 120 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Property Address

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the address, which is the join key to the site list, the environmental
  reports, the insurance schedule, and the permits.

```markdown
## Task

State the address and identifiers of the property.

## Rules

- Report the street address as printed, with city, state or province, postal code, and country.
- **Report the parcel, assessor's, or folio number where any document states one.** It is the identifier the tax authority and the register use, and it is what a search is run against.
- Report the county, borough, or registry district, since recording is by district.
- Where several parcels are comprised in one row, report each parcel identifier.
- Where the property has no street address — vacant land, for example — report the parcel identifier and the nearest stated location reference, and add `(no street address stated)`.
- Do not standardize, correct, or complete an address, and do not add a parcel number the documents do not state.

## Fallback rules

- Return `Unable to determine` where no document identifies the property's location.

## Output format

`[Street address], [city], [state or province] [postal code], [country]; parcel: [identifier(s) or "not stated"]; county or district: [as stated]`

Return no more than 50 words.
```

---

### 3. Interest Type

- Native type: Classify
- Configured options, in UI order: `Fee simple`, `Fee simple with ground lease out`, `Ground leasehold`, `Condominium unit`, `Co-ownership or tenancy in common`, `Easement or right of way only`, `Mineral or air rights only`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: what estate the target holds, which changes what the other columns
  mean.

```markdown
## Task

Classify the estate or interest the target holds in this property. Choose exactly one configured option.

## Scope

- Use the review-subject list in the Table Instructions to determine which party is a target entity.
- Classify the interest the documents show the target holding, as at the most recent document in the unit.

## Classification rules

- `Fee simple`: outright ownership of land and improvements.
- `Fee simple with ground lease out`: the target owns the land and has granted a ground lease to a third party. **The economics are those of a landlord**, and the ground lease itself should be a Leasehold row with the target as landlord.
- `Ground leasehold`: the target holds a long leasehold of land, typically owning the improvements. **Where this appears, confirm the interest is also captured in the Leasehold table** — a ground leasehold has both a title dimension and a lease dimension, and it needs both rows.
- `Condominium unit`: ownership of a unit within a condominium or strata regime, with an interest in common elements. Report the association and any assessment obligation in the evidence field.
- `Co-ownership or tenancy in common`: the target holds an undivided share with a third party. **Report the share and the co-owner in the evidence field** — a co-owner's consent is usually needed to sell or encumber, and it is a consent nobody expects.
- `Easement or right of way only`: the target holds an easement or access right rather than a possessory estate.
- `Mineral or air rights only`: a severed interest in subsurface or air rights.

## Fallback rules

- Use `Unable to determine` where the documents do not establish what interest the target holds.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Legal Description

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the description of what is actually owned, and whether the documents
  agree on it.

**The finding here is inconsistency.** A deed, a title report, a survey, and a
mortgage should describe the same land. Where they do not, the discrepancy has to
be resolved before anyone relies on any of them.

```markdown
## Task

Report the legal description of the property and whether the documents in the unit describe it consistently.

## Rules

- Report the form of the description as used: metes and bounds, lot and block with a recorded plat reference, section-township-range, a torrens or land registry title number, or a condominium unit and building designation.
- **Report the plat, map, or survey the description refers to, with its recording reference.** That reference is the definitive record of the boundary.
- Report the stated area — acres, square feet, hectares — as printed, and its source.
- **Where two documents in the unit contain legal descriptions, state whether they are the same or differ, and where they differ append ` [description discrepancy]`.** Do not attempt to reconcile them, plot them, or judge which is correct. A boundary discrepancy is a surveyor's and a title lawyer's question.
- Where a description in a mortgage covers more or less land than the deed, report that.
- Do not reproduce a lengthy metes and bounds description. Report its form, its opening point of beginning reference where stated, and its recording reference.

## Fallback rules

- Return `Not stated` where no document contains a legal description. **For an owned property this is a fundamental gap** — the property cannot be identified for a conveyance.
- Return `Unable to determine` where descriptions are illegible.

## Output format

`Form: [as used]; plat or map reference: [as stated]; area: [as stated] — per [document title], [YYYY-MM-DD]; consistency: [consistent across documents | [description discrepancy]]`

Return no more than 60 words. Do not reproduce the full description.
```

---

### 5. Title Evidence Available

- Native type: Classify
- Configured options, in UI order: `Current title report or commitment`, `Title report over 6 months old`, `Title insurance policy only`, `Deed only, no title evidence`, `Prior owner's title evidence only`, `No title evidence`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Vesting as Reported`, `Title Exceptions`
- Purpose: what quality of title evidence exists, which governs how much weight
  every ownership and encumbrance answer can carry.

**A deed proves a conveyance happened; it does not prove the grantor owned
anything, and it says nothing about what has happened since.** Only a title report
does that, and only as at its own effective date.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the title evidence present. Confirm the effective dates against the documents.

## Task

Classify the title evidence available for this property. Choose exactly one configured option.

## Scope

- Consider title reports, title commitments, preliminary reports, abstracts of title, title opinions, and title insurance policies.
- Consider the effective or search date of each, not its issue date.
- Exclude deeds, which are conveyances rather than title evidence, and exclude surveys.

## Classification rules

Apply the first rule that fits.

1. `No title evidence`: the unit contains no title report, commitment, abstract, or policy.
2. `Prior owner's title evidence only`: the title evidence in the unit was issued to or for a prior owner and predates the target's acquisition. **It says nothing about the target's title** and is effectively no evidence for this purpose.
3. `Deed only, no title evidence`: a deed is present and no title report, commitment, or policy is.
4. `Title insurance policy only`: an owner's policy is present with no current report or commitment. Note in the evidence field the policy amount and date, since a policy is protection rather than a current statement of title.
5. `Title report over 6 months old`: a report or commitment naming the target is present with an effective date more than six months before the diligence as-of date. **Report the gap in the evidence field.** Anything recorded in the gap is invisible.
6. `Current title report or commitment`: a report or commitment naming the target with an effective date within six months of the as-of date.

## Fallback rules

- Use `Unable to determine` where title evidence is present but its effective date or its subject cannot be read.

## Output format

Return only the exact configured option and no explanation.
```

---

### 6. Acquisition Instrument

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: how the target acquired the property, and what warranty of title it
  received.

```markdown
## Task

Report the instrument by which the target acquired this property.

## Include where expressly stated

- **The type of deed, exactly as titled**: general warranty, special or limited warranty, grant deed, bargain and sale, quitclaim, trustee's deed, sheriff's or tax deed, or a deed in lieu of foreclosure
- The grantor's exact name, and the grantee's exact name
- The date of the deed, and its recording date and reference
- The consideration recited
- Any reservation, exception, or condition in the granting clause
- Any covenant of warranty, and any express disclaimer of warranty
- Whether the deed is signed and, where the jurisdiction requires it, acknowledged or notarised

## Rules

- **Report the deed type as titled, and do not translate it.** The type is the finding: a general warranty deed carries covenants of title, a quitclaim carries none, and a **trustee's, sheriff's, or tax deed signals that the property came out of a foreclosure or a tax sale**, which raises a distinct set of title questions the reviewer must pursue.
- Report the grantor and grantee names exactly as printed. Do not correct or normalize.
- Report any reservation in the granting clause — mineral rights, easements retained, or life estates — since they are exceptions created by the deed itself rather than found on the register.
- Do not assess whether the deed conveyed good title.

## Fallback rules

- Return `Not in unit` where no acquisition deed is present. **This is a coverage finding** and it is also reported in Referenced but Not Produced.
- Return `Unable to determine` where the deed is illegible or its parties cannot be identified.

## Output format

`[Deed type] — grantor: [name]; grantee: [name]; dated [YYYY-MM-DD]; recorded [YYYY-MM-DD, reference]; consideration: [as recited]; reservations: [brief or "none"]; executed: [yes | no]; acknowledged: [yes | Not addressed]`

Return no more than 75 words.
```

---

### 7. Recording Evidence

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the instruments were recorded. **An unrecorded deed can be
  defeated by a later purchaser who records**, and an unrecorded release leaves a
  lien on the register regardless of whether the debt was paid.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify each recordable instrument. Confirm the recording evidence on each.

## Task

Report the recording status of each recordable instrument in this review unit.

## Scope

- Consider deeds, mortgages and deeds of trust, releases and reconveyances, easements, declarations, restrictive covenants, memoranda of lease, and liens.
- Recording evidence is a recorder's stamp, a book and page or instrument number with a recording date, or a registry entry number.
- Exclude title reports, surveys, tax statements, and policies, which are not recorded instruments.

## Rules

- For each instrument, report its type, whether recording evidence is present, and the recording reference and date where it is.
- **Where a recordable instrument bears no recording evidence, append ` [no recording evidence]`.** For a deed this is a priority risk; for a release it means the lien still appears on the register.
- **Where a release or reconveyance is present but unrecorded, flag it separately as ` [unrecorded release]`**, because the debt may be discharged while the encumbrance remains of record and has to be cleared before closing.
- Compare each instrument's date to its recording date. **Where the gap exceeds sixty days, append ` [recording delay]`.**
- Do not assess the effect of non-recording, which differs by jurisdiction.

## Fallback rules

- Return `Not applicable` where the unit contains no recordable instrument.
- Return `Unable to determine` where recording stamps are illegible.

## Output format

One line per instrument:

`[Instrument type] — [recorded [YYYY-MM-DD], [reference] | no recording evidence]`, with any bracketed flag appended.

Return no more than 10 lines and no more than 90 words.
```

---

### 8. Vesting as Reported

- Native type: Free Response
- Upstream: `@Title Evidence Available`
- Downstream: `Owner Matches Target Entity`
- Purpose: in whom title is reported to vest, and by what evidence.

```markdown
## Established result

- Title evidence available: @Title Evidence Available

## Task

Report the party in whom title to this property is stated to vest, and the source of that statement.

## Rules by title evidence available

- `Current title report or commitment`, `Title report over 6 months old`: report the vested owner exactly as the report names it, together with the report's effective date. **The effective date is part of the answer**, because the report speaks as of it and nothing later.
- `Title insurance policy only`: report the insured owner as named in the policy, with the policy date.
- `Deed only, no title evidence`: report the grantee named in the most recent deed in the unit, with the deed's recording date, and append ` [vesting from deed only]`. **A deed shows a conveyance, not current title**, and the flag records that limitation.
- `Prior owner's title evidence only`: report the owner the evidence names, append ` [predates target acquisition]`, and note that it does not evidence the target's title.
- `No title evidence`: return `Not stated — no title evidence in unit`.

## Rules

- **Report the name exactly as printed, including entity suffix, punctuation, and any misspelling or outdated form. Do not correct or normalize it.** The next column depends entirely on this one reporting what the document actually says.
- **Report the manner of holding where stated**: sole ownership, tenancy in common with a stated share, joint tenancy, or as trustee. Report any trust or nominee capacity as printed.
- Where the documents in the unit state different owners, report each with its source and append ` [vesting conflict]`.
- Do not opine on whether title is good, marketable, or insurable.

## Fallback rules

- Return `Unable to determine` where the vesting statement is illegible.

## Output format

`[Owner name exactly as printed][, [manner of holding]] — per [document title], effective [YYYY-MM-DD]`, with any bracketed flag appended.

Return no more than 55 words.
```

---

### 9. Owner Matches Target Entity

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Vested in a former name of a target entity`, `Vested in an individual`, `Vested in a third party`, `Co-owned with a third party`, `Vested in a trust or nominee`, `No vesting stated`, `Unable to determine`
- Upstream: `@Vesting as Reported`
- Downstream: none
- Purpose: whether the property sits inside the acquired group. Same pattern as
  the IP registrations column, and the same separation of problems.

```markdown
## Established result

- Vesting as reported: @Vesting as Reported

Use this result and the target group list in the Table Instructions. Confirm the name against the documents in the current unit.

## Task

Classify the relationship between the reported owner and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No vesting stated`: Vesting as Reported returned `Not stated — no title evidence in unit`.
2. `Co-owned with a third party`: title is reported as held with a party that is not a target entity, whether as tenants in common or joint tenants. **A co-owner's consent is usually required to sell or encumber**, and it is a consent nobody plans for.
3. `Vested in a trust or nominee`: title is held by a trustee or nominee. Report in the evidence field whether the documents identify the beneficiary, since the nominee arrangement may be the only thing standing between the register and the target.
4. `Vested in an individual`: the reported owner is a natural person. Property held personally by a founder is outside the business being bought.
5. `Vested in a former name of a target entity`: the reported name matches a prior name of a target entity as disclosed in the documents in this unit.
6. `Vested in a third party`: the reported owner is an entity that is not a target entity and is not a former name of one.
7. `Matches with name variance`: the reported name is the same entity as one on the target group list but differs in form.
8. `Matches a target entity exactly`: the name is character-for-character a name on the target group list.

**Do not resolve a variance by assuming.** Where the reported name is similar to a target entity but could be a different entity, use `Vested in a third party` and note the similarity in the evidence field.

Where a target entity's former name is not disclosed in this unit, you cannot use `Vested in a former name of a target entity`. Use `Vested in a third party`; the Corporate table's `Prior Names` column resolves it.

## Fallback rules

- Use `Unable to determine` where the name is illegible, or where Vesting as Reported returned `Unable to determine` or reported a conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Title Exceptions

- Native type: Free Response
- Upstream: `@Title Evidence Available`
- Downstream: none
- Purpose: what title is subject to. **This is the substance of a title review**,
  and the distinction between a standard printed exception and a specific
  recorded matter is the whole point.

```markdown
## Established result

- Title evidence available: @Title Evidence Available

## Task

Report the exceptions to title stated in the title report, commitment, or policy.

## Applicability

- Applies where Title Evidence Available is `Current title report or commitment`, `Title report over 6 months old`, `Title insurance policy only`, or `Prior owner's title evidence only`.
- Where it is `Deed only, no title evidence` or `No title evidence`, return `Not applicable — no title evidence in unit`. **Encumbrances may still exist**; they simply cannot be established from these documents.
- Where it is `Unable to determine`, return `Unable to determine`.

## Rules

- **Separate the standard or printed exceptions from the specific exceptions.** Standard exceptions — rights of parties in possession, unrecorded easements, mechanics' liens, taxes not yet due, matters a survey would disclose — appear on every commitment and are usually deleted at closing. **The specific exceptions are the actual encumbrances on this property** and they are what a reviewer reads.
- For each specific exception, report its nature in six words or fewer, its recording date, and its recording reference.
- Report the exception number as printed, so the reviewer can find it in the commitment.
- **Report any requirement listed in a commitment's requirements schedule as distinct from an exception**, since requirements are things that must be done before the policy issues and they are frequently the actionable items.
- Report no more than twelve specific exceptions. Where more exist, report the twelve most substantive — monetary liens first, then use restrictions, then easements — and append ` and [N] further exceptions`.
- **Do not assess whether any exception is objectionable, material, or removable, and do not opine on marketability.** That is a title lawyer's judgement and it is the human column.

## Fallback rules

- Return `None specific` where the evidence lists only standard printed exceptions.
- Return `Unable to determine` where the exception schedule is illegible or incomplete.

## Output format

`Standard exceptions: [count as listed]` followed by one line per specific exception:

`[No.] [nature] — recorded [YYYY-MM-DD], [reference]`

Return no more than 12 lines and no more than 120 words. Do not include an assessment of your own.
```

---

### 11. Monetary Liens

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the encumbrances that have to be paid or released at closing. **Feeds
  the payoff and lien-release checklist directly.**

```markdown
## Task

Report every monetary lien or charge against this property that the documents disclose.

## Scope

- Include mortgages, deeds of trust, and other security instruments.
- Include mechanics', materialmen's, and construction liens.
- Include judgment liens, tax liens, and assessment liens.
- Include HOA or condominium association liens and unpaid assessments.
- Include any UCC fixture filing against the property.
- **Exclude taxes not yet due and payable**, which are reported in Property Tax Status.
- Exclude easements and restrictive covenants, which are non-monetary and have their own columns.

## Rules

- For each lien, report its type, the secured party or claimant exactly as named, the stated amount where given, the recording date, and the recording reference.
- **Report whether a release, satisfaction, or reconveyance is present in the unit for each lien, and whether that release is recorded.** A lien with no release of record must be cleared at closing regardless of whether the underlying debt was paid.
- **Where a lien appears with no release, append ` [no release of record]`.** This is the flag the lien-release checklist is built from.
- Report any mechanics' lien separately and prominently, since it usually signals a dispute with a contractor and there may be more to come — the filing period often extends months past completion of work.
- Report amounts as stated. **Do not total the liens and do not calculate a payoff.**
- Do not assess priority, perfection, or enforceability.

## Fallback rules

- Return exactly `None disclosed` where the documents disclose no monetary lien.

Note: `None disclosed` is a positive finding, not a fallback state. **It reflects these documents only**, and where `Title Evidence Available` is anything other than a current report, it establishes very little. A current search does that.

- Return `Unable to determine` where lien entries are illegible or conflicting.

## Output format

One line per lien:

`[Type] — [secured party] — [amount or "not stated"] — recorded [YYYY-MM-DD], [reference] — [released and recorded | release unrecorded | no release of record]`

Return no more than 10 lines and no more than 110 words. Do not include totals.
```

---

### 12. Easements and Access

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: rights over the land and, critically, **whether the property has legal
  access to a public road.** A landlocked parcel is a serious defect and it is not
  obvious from a deed.

```markdown
## Task

Report the easements and access rights affecting this property.

## Scope

- Include easements burdening the property, granted to utilities, neighbours, or public bodies.
- Include easements benefiting the property, particularly access, parking, drainage, and utility easements over adjoining land.
- Include any licence, encroachment agreement, or party wall agreement.
- Include any reciprocal easement agreement or shared-facilities arrangement.
- Exclude restrictive covenants, which have their own column.

## Rules

- Distinguish easements that **burden** the property from those that **benefit** it, and label each. **Confusing the two inverts the finding**: a burden is a constraint, a benefit is an asset the property may not function without.
- For each, report its nature in six words or fewer, the benefited or burdened party, the recording date, and the recording reference.
- **Report whether the documents establish legal access to a publicly dedicated road, and where they do not, append ` [access not established]`.** Access may be by direct frontage or by a recorded access easement. **A property without established legal access is materially impaired**, and a survey or a title report is usually the only place this surfaces.
- Report any easement whose location the documents state is undefined or "blanket", since an undefined utility easement can in principle affect any part of the site.
- Report any encroachment onto or from adjoining land where the documents identify one, and note that the detail is in Survey Findings.
- Do not assess whether an easement interferes with the property's use.

## Fallback rules

- Return exactly `None disclosed` where the documents disclose no easement.
- Return `Unable to determine` where entries are illegible.

## Output format

One line per easement:

`[Burden | Benefit] — [nature] — [party] — recorded [YYYY-MM-DD], [reference]`, followed by a final line: `Legal access to public road: [established per [document] | [access not established]]`

Return no more than 10 lines and no more than 100 words.
```

---

### 13. Restrictive Covenants and Declarations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: private restrictions on how the land may be used or developed, which
  bind regardless of what zoning permits.

```markdown
## Task

Report the restrictive covenants, declarations, and private use restrictions affecting this property.

## Scope

- Include recorded restrictive covenants, conditions, and restrictions, whether in a declaration, a deed, or a separate instrument.
- Include condominium or owners' association declarations, bylaws, and rules.
- Include development agreements, subdivision conditions, and plat notes imposing obligations.
- Include reverter, right of re-entry, or reversionary provisions.
- Include any use restriction imposed by a former owner, a neighbouring owner, or a competitor.
- Exclude zoning and public land-use controls, which have their own column.
- Exclude easements.

## Rules

- For each restriction, report its nature in eight words or fewer, its source document, its recording date, and its recording reference.
- **Report any use restriction that would constrain the target's current or planned operations, as stated.** A covenant restricting the site to a stated trade, or prohibiting a category of use, does not appear in a zoning search and binds independently of it.
- **Report any restriction on transfer, subdivision, or development**, including any consent requirement from an association or a former owner.
- **Report any reverter or right of re-entry prominently.** A condition that title reverts on breach or on cessation of a stated use is a catastrophic risk and it is rare enough to be overlooked.
- Report any association assessment obligation, any special assessment, and any approval requirement for alterations.
- Report whether the declaration is stated to be enforceable by an association, by other owners, or by a named party.
- Do not assess enforceability, and do not judge whether the target is in compliance.

## Fallback rules

- Return exactly `None disclosed` where the documents disclose no private restriction.
- Return `Unable to determine` where entries are illegible.

## Output format

One line per restriction:

`[Nature] — [source document] — recorded [YYYY-MM-DD], [reference] — enforceable by: [as stated]`

Return no more than 8 lines and no more than 100 words.
```

---

### 14. Survey Findings

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the survey found on the ground, which is where physical problems
  appear that no register discloses.

```markdown
## Task

Report the matters the survey identifies.

## Applicability

- Applies where a survey, plat of survey, or ALTA survey is present in the review unit.
- Where none is present, return `No survey in unit`. **This is a coverage finding**, since encroachments, access problems, and boundary discrepancies are usually invisible without one.

## Include where expressly stated

- The survey type and standard applied, and the survey date
- The surveyor and any certification, and to whom the certification is addressed
- **Any encroachment onto the property from adjoining land, and any encroachment by the property's improvements onto adjoining land or into an easement**
- Any improvement located over a recorded easement
- Any boundary discrepancy, gap, gore, or overlap with the legal description or with adjoining parcels
- Any setback, height, or coverage non-conformity the survey notes
- Access points and their relationship to a public right of way
- Any flood zone designation stated
- The parking count as surveyed
- Any area calculation, and whether it agrees with the legal description
- Any matter the survey flags as unresolved or requiring further investigation

## Rules

- **Report encroachments in both directions and label each.** An encroachment onto the property is a defect in what is owned; an encroachment by the property is a liability to the neighbour, and the two are remedied differently.
- **Report any improvement sitting over an easement**, since the easement holder can in principle require its removal.
- **Report to whom the survey is certified.** A survey certified only to the seller or its lender may not be relied on by the buyer, and a recertification is usually straightforward to obtain.
- Report the survey date and compare it to the diligence as-of date. **Where the gap exceeds five years, append ` [survey over 5 years old]`**, since improvements may have changed.
- Report the findings as stated. **Do not measure, plot, calculate an area, or judge whether a non-conformity is material.**

## Fallback rules

- Return `No survey in unit` where none is present.
- Return exactly `No adverse matters noted` where a survey is present and identifies none.
- Return `Unable to determine` where the survey is illegible or its notes cannot be read.

## Output format

`Survey: [type], [YYYY-MM-DD], certified to [parties]` followed by one line per finding:

`[Finding as stated]`

Return no more than 10 lines and no more than 110 words.
```

---

### 15. Mortgage and Financing

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the financing secured on the property, and what it requires on a sale
  or a change of control. **Joins this row to the Debt table.**

```markdown
## Task

Report the mortgages, deeds of trust, and related financing documents affecting this property.

## Include where expressly stated

- The lender or beneficiary exactly as named, and any trustee
- The original principal amount, and any current balance stated
- The recording date and reference
- The maturity date
- **Any due-on-sale or due-on-encumbrance clause**, and whether it is triggered by a transfer of the property or by a change of control of the borrower
- **Any restriction on transferring the property or on a change of control of the borrower, and any consent requirement**
- Any prepayment premium, yield maintenance, or defeasance requirement
- Any assumption right permitting a purchaser to take over the loan, and any assumption fee
- Any cross-collateralisation with other properties
- Any assignment of rents or leases
- Any lockbox or cash management requirement
- Any single-purpose-entity covenant restricting what the borrowing entity may do
- Whether a release or reconveyance is present in the unit

## Rules

- **Report the due-on-sale and change-of-control position prominently.** In a share purchase, a due-on-sale clause reaching a change of control of the borrower converts the mortgage into a consent item or a payoff, and this is the column where that surfaces.
- **Report any defeasance requirement**, since defeasance is expensive, takes weeks, and cannot be done at short notice — it is a timetable item, not just a cost.
- Report any single-purpose-entity covenant, since it may restrict the post-closing structure.
- Report amounts as stated. **Do not calculate a payoff, accrue interest, or estimate a prepayment premium.**
- Cross-reference: the facility itself is a Debt table row, and the reviewer joins them on the lender name and the property.

## Fallback rules

- Return exactly `None disclosed` where the documents disclose no mortgage or secured financing.
- Return `Unable to determine` where entries are illegible or conflicting.

## Output format

One line per instrument:

`[Lender] — [original amount] — recorded [YYYY-MM-DD], [reference] — maturity [date]; due on sale: [as stated or "Not addressed"]; CoC consent: [as stated or "Not addressed"]; prepayment: [as stated]; released: [yes | no]`

Return no more than 6 lines and no more than 110 words.
```

---

### 16. Zoning and Permitted Use

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what public land-use controls permit, and whether the current use
  complies.

```markdown
## Task

Report the zoning and public land-use position for this property as the documents state it.

## Include where expressly stated

- The zoning classification or district, as designated
- The permitted uses under that classification, as stated
- Any special exception, conditional use permit, variance, or planned development approval, with its date and any conditions
- **Any statement that the current use is legal non-conforming or grandfathered**, and any condition on which that status is lost
- Any setback, height, density, coverage, or parking requirement stated, and any stated non-conformity
- Any certificate of occupancy referenced, with its date and the use it certifies
- Any open code violation, notice, or enforcement action stated
- Any development agreement, impact fee, or exaction obligation
- Any pending rezoning, downzoning, or planning proposal affecting the property

## Rules

- **Report the source of the zoning statement.** A municipal zoning letter is evidence; a statement in a title report or a seller's summary is a recital. The weight differs and the reviewer must be able to tell.
- **Report any legal non-conforming status prominently, together with any condition on which it lapses** — commonly discontinuance of the use for a stated period, or destruction of the improvements beyond a stated proportion. **Non-conforming status that lapses on a casualty is a serious constraint on rebuilding** and it is easy to miss.
- Report any certificate of occupancy and the use it certifies, since a mismatch with the actual use is a compliance finding.
- Report the position as stated. **Do not assess compliance, do not interpret a zoning ordinance, and do not opine on whether a use is permitted.**

## Fallback rules

- Return `Not stated` where the documents state no zoning information. **For an owned property this is a coverage gap**, and a zoning letter is usually obtainable quickly.
- Return `Unable to determine` where statements conflict, or are illegible.

## Output format

`Classification: [as designated] — per [document title], [YYYY-MM-DD]; permitted uses: [as stated]; approvals: [brief or "none"]; non-conforming: [as stated or "Not addressed"]; certificate of occupancy: [date and use, or "not referenced"]; violations: [brief or "none stated"]`

Return no more than 85 words.
```

---

### 17. Property Tax Status

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether taxes are current, and whether an assessment or an appeal is
  pending. **Unpaid property tax is a lien with priority over almost everything
  else.**

```markdown
## Task

Report the property tax position for this property as the documents state it.

## Include where expressly stated

- The assessed value and the assessment year
- The annual tax amount, and the taxing authorities
- **Whether taxes are stated as paid, due, or delinquent, and as at what date**
- Any delinquent amount, with penalties and interest as stated
- Any tax lien or tax sale certificate
- Any instalment due dates
- Any special assessment, improvement district levy, or supplemental assessment
- **Any pending assessment appeal or protest, and any pending reassessment**
- Any exemption, abatement, or preferential assessment the property enjoys, and any condition or clawback attached to it
- Any statement that the property is subject to reassessment on a change of ownership

## Rules

- **Report the as-of date of the tax statement.** A statement from an earlier year says nothing about the current position, and this is the most common weakness in this column.
- **Report any exemption or abatement together with its clawback condition.** An abatement that terminates or is recaptured on a change of ownership is a transaction cost, and it interacts directly with the Transfer Tax Exposure column.
- **Report any statement that the property is reassessed on a change of ownership**, since a reassessment to current market value can increase the annual tax substantially and permanently.
- Report amounts as stated. **Do not total, prorate, or calculate accrued penalties.**
- Do not assess whether the assessed value is reasonable, and do not estimate a future tax.

## Fallback rules

- Return `Not stated` where the documents contain no tax information.
- Return `Unable to determine` where statements conflict, or are illegible.

## Output format

`Assessed value: [as stated] ([year]); annual tax: [as stated]; status: [paid | due | delinquent] as at [YYYY-MM-DD]; delinquency: [amount or "none"]; special assessments: [brief or "none"]; appeal pending: [yes | no | Not addressed]; exemption: [brief and clawback, or "none"]; reassessment on transfer: [as stated or "Not addressed"]`

Return no more than 90 words.
```

---

### 18. Transfer Restrictions and Change of Control

- Native type: Classify
- Configured options, in UI order: `Lender consent required`, `Co-owner or association consent required`, `Public body or grant consent required`, `Right of first refusal held by third party`, `Multiple consents required`, `No restriction disclosed`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whose consent is needed, and whether a change of control of the owning
  entity triggers it. **Feeds the consent schedule.**

```markdown
## Task

Classify the restrictions on transferring this property, or on a change of control of the entity that owns it. Choose exactly one configured option.

## Scope

- Consider consent requirements and transfer restrictions arising from mortgages, co-ownership arrangements, association declarations, ground leases, development agreements, grant or subsidy conditions, and deed restrictions.
- **Consider restrictions triggered by a change of control of the owning entity as well as by a transfer of the property itself.** In a share purchase, only the former is engaged.
- Exclude general zoning and regulatory approvals for a change of use.

## Classification rules

Apply the first rule that fits.

1. `Multiple consents required`: more than one of the categories below applies. Report each in the evidence field.
2. `Right of first refusal held by third party`: a co-owner, association, tenant, former owner, or public body holds a pre-emptive right on a sale. **This is worse than a consent requirement**, because the property may have to be offered elsewhere before it can be transferred, and in a share purchase it may or may not be triggered depending on its wording.
3. `Public body or grant consent required`: a grant, subsidy, tax abatement, or development agreement requires consent to a transfer or change of control, or imposes a clawback on one.
4. `Co-owner or association consent required`: a tenancy in common agreement, condominium declaration, or association requires consent.
5. `Lender consent required`: a mortgage or deed of trust requires consent to a transfer or contains a due-on-sale clause reaching a change of control.
6. `No restriction disclosed`: the documents address transfer and disclose no consent requirement or pre-emptive right.

**Report in the evidence field, for each restriction, whether it is triggered by a transfer of the property, by a change of control of the owner, or by both.** That distinction determines whether a share purchase engages it at all, and it is the single most useful thing this cell can carry.

## Fallback rules

- Use `Not addressed` where the documents do not address transfer restrictions.
- Use `Unable to determine` where provisions conflict, or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Transfer Tax Exposure

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: whether the transaction triggers a real property transfer tax.

**A genuine and frequently missed M&A cost.** Several jurisdictions impose realty
transfer tax, stamp duty, or a mansion tax on an **indirect** transfer — the sale
of shares in an entity holding real property — not only on a deed. New York,
Pennsylvania, Washington, Maryland, and a number of non-US jurisdictions have
provisions of this kind, and the tax can be a material sum on a valuable property.
No other table in the set asks the question.

```markdown
## Task

Report anything in the documents bearing on real property transfer tax, stamp duty, or a similar transaction tax on this property.

## Include where expressly stated

- Any transfer tax, stamp duty, deed tax, or recording tax stated to have been paid on the target's own acquisition, with the amount and the rate
- Any transfer tax declaration, affidavit, or exemption certificate filed on that acquisition
- **Any exemption claimed, and any condition or holding period attached to it**, since an early transfer can trigger a recapture
- Any statement in the documents that a transfer of a controlling interest in an entity holding real property is treated as a transfer of the property
- The assessed or stated value used for any transfer tax calculation
- Any local, county, or municipal transfer tax in addition to a state or national one
- Any tax abatement or preferential assessment that terminates or is recaptured on a transfer or change of ownership

## Rules

- **Report the amount and rate paid on the target's own acquisition where stated.** It is the best available indication of the rate and base that would apply again, and it is often the only figure in the file.
- **Report any holding-period condition on an exemption prominently.** A transfer within the period can recapture the whole exemption.
- Report any abatement clawback here as well as in Property Tax Status, since the two are read together when the transaction is priced.
- Report only what the documents state. **Do not calculate any tax, do not apply a rate, and do not determine whether this transaction is taxable.** Whether a change of control constitutes a taxable transfer is a jurisdiction-specific question for tax counsel, and this column exists to make sure it gets asked.

## Fallback rules

- Return `Not addressed` where the documents contain nothing on transfer tax. **This is a common answer and it is not a closed question** — the exposure depends on the jurisdiction and the deal structure, not on what the data room contains. The human column carries the assessment.
- Return `Unable to determine` where statements are illegible or conflicting.

## Output format

`Paid on acquisition: [amount and rate, or "Not addressed"]; exemption claimed: [brief and any holding period, or "none"]; controlling-interest provision referenced: [yes | Not addressed]; abatement clawback: [brief or "none"]`

Return no more than 70 words. Do not include any tax you calculated.
```

---

### 20. Environmental Documents Referenced

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: link the property to the Environmental tables, and surface where no
  environmental work exists for an owned site.

**Owned property is where environmental liability attaches.** A tenant's exposure
is usually limited by its lease; an owner's is not, and for owned industrial or
former industrial land this is often the largest single risk on the property.

```markdown
## Task

Report any environmental document, condition, or obligation the documents in this unit identify for this property.

## Scope

- Include any environmental site assessment, remediation plan, or environmental report referenced or present.
- Include any environmental permit, registration, or licence referenced for the site.
- Include any recorded environmental land use restriction, activity and use limitation, deed restriction, or environmental covenant.
- Include any notice of violation, enforcement order, consent order, or remediation obligation.
- Include any environmental indemnity, escrow, or insurance referenced in the acquisition documents.
- Include any storage tank, well, or landfill the documents identify on the site.
- Include any flood zone, wetland, or protected habitat designation.
- Exclude general environmental representations in an acquisition agreement without a specific condition identified.

## Rules

- For each item, report what it is, its date, and whether the document itself is present in this unit.
- **Report any recorded environmental land use restriction or activity and use limitation prominently.** These bind the land, restrict what may be done on it, and commonly require ongoing monitoring and reporting — obligations the buyer inherits with the title.
- **Report any environmental indemnity given by a former owner, since it may be an asset**, and note whether it is stated to be assignable and whether it has a time limit.
- **Where the property is owned and no environmental assessment is referenced anywhere, say so under the fallback rules.** For owned land, particularly industrial or formerly industrial land, the absence is itself the finding.
- Cross-reference: any assessment identified here should be a row in the Environmental — Assessments table, and the reviewer joins them on the address.
- Do not assess environmental risk, and do not estimate remediation cost.

## Fallback rules

- Return exactly `None referenced` where the documents identify no environmental document, condition, or obligation.

Note: for an owned property this is a coverage finding rather than a clean result, and the coverage register should carry a row for the missing assessment.

- Return `Unable to determine` where references are illegible.

## Output format

One line per item:

`[Item] — [date or "date not stated"] — [in unit | not produced]`

Return no more than 8 lines and no more than 85 words.
```

---

### 21. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this property file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this property that the documents in this unit refer to and that is not present.

## Scope

- **Include every instrument listed as a title exception but not produced.** These are the encumbrances the reviewer cannot read, and they are the highest-value gaps in this table
- Include the acquisition deed where it is absent.
- Include prior deeds in the chain referenced but absent.
- Include any title report, commitment, or policy referenced but absent.
- Include the survey where referenced but absent, and any prior survey referenced.
- Include recorded plats, maps, and subdivision plans referenced in the legal description.
- Include declarations, CC&Rs, association bylaws, and rules referenced but absent.
- Include easement instruments referenced but absent.
- Include mortgages, releases, and reconveyances referenced but absent.
- Include zoning letters, certificates of occupancy, permits, and variances referenced but absent.
- Include property tax statements for the current year where only earlier ones are present.
- Include environmental reports and recorded restrictions referenced but absent.
- Include any ground lease, reciprocal easement agreement, or development agreement the property is stated to be subject to.
- Exclude statutes, ordinances, and building codes.

## Rules

- Name each document as the referencing document names it, with its recording reference and date where stated. **The recording reference is what an order for a copy is placed against**, so report it exactly.
- **Where a title exception instrument is not produced, add `; exception not readable`.** The exception's nature is known from the schedule but its terms are not, and terms are what matter for an easement or a restrictive covenant.
- Where a plat or map referenced in the legal description is absent, add `; boundary reference missing`.
- Where a release or reconveyance is referenced but absent, add `; lien clearance unproven`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon in this table — a title commitment routinely lists a dozen exception instruments and produces none of them.

## Output format

One line per missing document:

`[Name as referenced] — [recording reference and date, or "date not stated"][; flag]`

Return no more than 15 lines and no more than 130 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Title acceptable** | Yes / Objections raised / Not assessed |
| **Objectionable exceptions** | None / Identified (specify) / Not assessed |
| **Lien clearance required at closing** | None / Identified (specify) / Unresolved |
| **Consent required for this structure** | Yes / No / Ambiguous |
| **Transfer tax triggered** | Yes (estimate) / No / Tax counsel to confirm |
| **Site criticality** | Critical / Important / Disposable |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** Owned property rows are few and each carries a large,
non-diversifiable exposure.

### Reconciliation work that never belongs in a column

- **The title review itself.** Every specific exception read against its
  underlying instrument, with objections raised. **Reporting an exception is
  extraction; deciding whether it is objectionable is a title lawyer's judgement**,
  and no column should attempt it.
- **Current searches.** Every row where `Title Evidence Available` is anything
  other than `Current title report or commitment` needs a fresh commitment. The
  documents in a data room establish the position at their own dates and nothing
  since.
- **Lien clearance checklist.** Every `[no release of record]` and
  `[unrecorded release]` flag from `Monetary Liens` and `Recording Evidence`,
  against the Debt table's payoff schedule.
- **Transfer tax analysis.** Every row, referred to tax counsel with the
  jurisdiction and the deal structure. **This is the item most likely to be missed
  entirely**, and the exposure is a real cash cost on a valuable property.
- **Access and encroachment resolution.** Every `[access not established]` flag
  and every encroachment from `Survey Findings`, referred to a surveyor and a
  title lawyer.
- **Environmental coverage.** Every owned row where
  `Environmental Documents Referenced` returns `None referenced`, into the
  coverage register as a missing assessment.
- **Site list reconciliation.** These rows plus the Leasehold rows against the
  operations site list, so that every location has either a lease row or an owned
  row.
- **Zoning verification.** Every row where zoning is stated only in a title report
  or a seller summary, verified by a municipal letter.

---

## Test set

Where the target owns no property, record the table as built and empty. The
following assumes owned property exists.

- [ ] Fee simple property with a current commitment, survey, deed, and tax statement
- [ ] Property with a title commitment effective two years before the as-of date
- [ ] Property with a deed and no title evidence at all
- [ ] Property with an owner's policy and no current commitment
- [ ] Property with title evidence issued to the prior owner
- [ ] Property acquired by general warranty deed
- [ ] Property acquired by quitclaim deed
- [ ] Property acquired by trustee's deed following a foreclosure
- [ ] Deed with a mineral rights reservation in the granting clause
- [ ] Deed present with no recording stamp
- [ ] Property vested in a target entity's former name
- [ ] Property vested in a founder individually
- [ ] Property held as tenants in common with a third party
- [ ] Property held by a nominee or trustee
- [ ] Commitment with twelve specific exceptions and none of the instruments produced
- [ ] Commitment with a requirements schedule
- [ ] Property with an unreleased mortgage of record
- [ ] Property with a recorded release that is itself unrecorded in the unit
- [ ] Property with a mechanics' lien
- [ ] Property with a delinquent tax lien
- [ ] Property with a blanket utility easement of undefined location
- [ ] Property with no established legal access to a public road
- [ ] Property with an improvement encroaching over a recorded easement
- [ ] Property encroached upon by a neighbour's improvement
- [ ] Survey certified only to the seller and its lender
- [ ] Survey more than five years old
- [ ] Property with no survey in the unit
- [ ] Property subject to a declaration with an association consent requirement
- [ ] Property subject to a reverter on cessation of a stated use
- [ ] Property with a deed restriction limiting it to a single trade
- [ ] Property with legal non-conforming use status lapsing on casualty
- [ ] Property with a tax abatement recaptured on a change of ownership
- [ ] Property with a pending assessment appeal
- [ ] Mortgage with a due-on-sale clause reaching a change of control of the borrower
- [ ] Mortgage requiring defeasance rather than permitting prepayment
- [ ] Mortgage with a single-purpose-entity covenant
- [ ] Property with a third-party right of first refusal on a sale
- [ ] Property with transfer tax paid on acquisition and an exemption claimed
- [ ] Property with a recorded activity and use limitation
- [ ] Owned industrial property with no environmental assessment referenced
- [ ] Ground leasehold, to confirm it also appears in the Leasehold table
- [ ] Condominium unit with association assessments
- [ ] Legal descriptions in the deed and the mortgage covering different land

Then test the dependencies: change `Title Evidence Available` from
`Current title report or commitment` to `No title evidence` and confirm
`Vesting as Reported` returns `Not stated — no title evidence in unit` and
`Title Exceptions` moves to `Not applicable — no title evidence in unit`. Change
`Vesting as Reported` from a target entity to an individual and confirm
`Owner Matches Target Entity` moves to `Vested in an individual`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
