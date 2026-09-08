# Prompt Inventory — Contracts Core

Platform-ready Harvey Review Table. This is the reference pattern for the
remaining eleven tables: build it, test it, redline it, then extend by pattern.

Keep this file outside Harvey. Exports omit Table Instructions and Harvey does not
version prompts, so this is the authoritative history. Update the record and the
change log on every prompt change, including one-word fixes.

## Table

- Matter: `[Project name]`
- Platform: Harvey Review Tables (UI)
- Review unit: **one agreement family** — a base agreement together with every
  amendment, restatement, statement of work, order form, and side letter produced
  for it
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: corporate/M&A team; feeds the consent
  schedule, the coverage register, and the issues list
- Inventory version: v1.0
- Last full run: —
- Last evaluated: —

### Why the family is the row

One row per document produces three rows for an amended MSA, each looking
authoritative, and the assignment clause in the base agreement may have been
replaced by Amendment 2. Grouping puts the family in one unit.

**The limit matters.** Grouping lets Harvey read the family together. It does not
establish which document controls. Every provision column below reports the
provision as stated in the most recently dated document in the unit that
addresses it, and names that document. That is a factual observation about the
documents present. Whether that version legally governs is `Operative Version
Confirmed`, a human column.

## Assumptions to confirm before running

Each one changes the table if wrong.

1. Families are assembled correctly at upload, per the file-naming convention.
   A missing amendment produces a confidently wrong row, and `Chain Completeness`
   is the only guard against it.
2. Buy-side review; the target group entities are the review subjects.
3. This table's job is substantive extraction of term, termination, and transfer
   provisions. Economics, liability, IP, and data terms are in Contracts
   Commercial, a separate table over the same project.
4. `[Project name]`, the entity list, and the diligence as-of date in Table
   Instructions are real matter parameters, not placeholders.
5. Compilations were split before upload. A single PDF holding twenty agreements
   cannot be a row.

## Pre-run verification

Do these on a two-row test table before pasting the full suite.

- [ ] Every Classify column's options configured in the UI, in the order listed
      in each record. **17 Classify columns.**
- [ ] Typed columns tested with one row of each fallback the prompt can return.
      **This is the highest-risk unknown.** Test: `Current Term Expiry` (Date)
      with `Not stated`; `Initial Term` and `Renewal Notice Period` (Duration)
      with `Not stated`, and with a non-numeric term such as `perpetual`. Record
      what each type accepts:
      - Date accepts: ______
      - Duration accepts: ______
      - If a type rejects the fallback, switch that column to Free Response with a
        strict format and give up native sorting. Do not change the meaning of the
        fallback to suit the type.
- [ ] Verbatim column behaviour confirmed on three known documents — does it
      return true verbatim text, and does it accept `Not addressed`? The entire
      spot-check design rests on this.
- [ ] Table Instructions pasted from this file, and the diligence as-of date set.
- [ ] Dependency index re-derived from the prompts.
- [ ] Grouping tested with a family containing a base agreement plus two
      amendments where the second amendment restates the assignment clause.
- [ ] Legal choices confirmed by the team: the `Succession Carve-Out` option
      definitions, and the decision that affiliate-only assignment permissions do
      not count as successor permissions.

---

## Table Instructions

- Version: v1.0
- Last changed: —

About 1,900 characters. Note what is absent: no decision thresholds, no
column-specific exclusions, no output templates. Those belong to the columns that
own them. Harvey exports omit this text, which is why it lives here.

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
- Use entity and individual names exactly as printed in the documents; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written when a document gives less precision.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

Four stages. Orientation is stable and controlled; nothing narrative controls
downstream routing.

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Target Contracting Entity
  Counterparty
  Agreement Type
  Governing Law

Stage 2 — Status and dates
  Documents in Unit ──→ Chain Completeness
  Documents in Unit ──→ Execution Status
  Documents in Unit ──→ Referenced but Not Produced
  Counterparty      ──→ Counterparty Type
  Agreement Type    ──→ Effective Date
                        Initial Term
                        Current Term Expiry
                        Renewal Mechanism

Stage 3 — Conditional detail
  Renewal Mechanism ──→ Renewal Notice Period
  Current Term Expiry + Renewal Mechanism ──→ Term Status on Record
  Termination for Convenience — Holder ──→ Termination for Convenience — Detail
  Assignment Restriction ──→ Succession Carve-Out
                             Assignment Language
  Change of Control Treatment ──→ CoC Indirect Changes
                                  CoC Threshold
                                  CoC Language

Stage 4 — Synthesis
  Assignment Restriction + Succession Carve-Out + Change of Control Treatment
                        ──→ Consent Trigger Profile
```

`Execution Status` is deliberately **not** referenced by the provision columns.
Execution evidence changes what a finding proves, not what the document says, and
a reviewer reads the two cells side by side. Referencing it everywhere would add
27 inputs that no rule consumes. It is referenced by `Consent Trigger Profile`,
which is the cell that feeds an external request.

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Documents in Unit | Free Response | — | Chain Completeness; Execution Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Chain Completeness | Classify | @Documents in Unit | — | v1.0 | draft |
| 3 | Execution Status | Classify | @Documents in Unit | Consent Trigger Profile | v1.0 | draft |
| 4 | Target Contracting Entity | Free Response | — | — | v1.0 | draft |
| 5 | Counterparty | Free Response | — | Counterparty Type | v1.0 | draft |
| 6 | Counterparty Type | Classify | @Counterparty | — | v1.0 | draft |
| 7 | Agreement Type | Classify | — | Effective Date; Initial Term; Current Term Expiry; Renewal Mechanism | v1.0 | draft |
| 8 | Governing Law | Free Response | — | — | v1.0 | draft |
| 9 | Effective Date | Date | @Agreement Type | — | v1.0 | draft |
| 10 | Initial Term | Duration | @Agreement Type | — | v1.0 | draft |
| 11 | Current Term Expiry | Date | @Agreement Type | Term Status on Record | v1.0 | draft |
| 12 | Renewal Mechanism | Classify | @Agreement Type | Renewal Notice Period; Term Status on Record | v1.0 | draft |
| 13 | Renewal Notice Period | Duration | @Renewal Mechanism | — | v1.0 | draft |
| 14 | Term Status on Record | Classify | @Current Term Expiry; @Renewal Mechanism | — | v1.0 | draft |
| 15 | Termination for Convenience — Holder | Classify | — | Termination for Convenience — Detail | v1.0 | draft |
| 16 | Termination for Convenience — Detail | Free Response | @Termination for Convenience — Holder | — | v1.0 | draft |
| 17 | Termination for Cause | Free Response | — | — | v1.0 | draft |
| 18 | Termination on Insolvency | Classify | — | — | v1.0 | draft |
| 19 | Assignment Restriction | Classify | — | Succession Carve-Out; Assignment Language; Consent Trigger Profile | v1.0 | draft |
| 20 | Succession Carve-Out | Classify | @Assignment Restriction | Consent Trigger Profile | v1.0 | draft |
| 21 | Assignment Language | Verbatim | @Assignment Restriction | — | v1.0 | draft |
| 22 | Change of Control Treatment | Classify | — | CoC Indirect Changes; CoC Threshold; CoC Language; Consent Trigger Profile | v1.0 | draft |
| 23 | CoC Indirect Changes | Classify | @Change of Control Treatment | — | v1.0 | draft |
| 24 | CoC Threshold | Free Response | @Change of Control Treatment | — | v1.0 | draft |
| 25 | CoC Language | Verbatim | @Change of Control Treatment | — | v1.0 | draft |
| 26 | Consent Trigger Profile | Free Response | @Assignment Restriction; @Succession Carve-Out; @Change of Control Treatment; @Execution Status | — | v1.0 | draft |
| 27 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

Status values: `draft`, `testing`, `verified`, `retired`.

**Change log convention.** Every column starts at v1.0, dated on first run.
Rather than 27 empty change logs, log changes in the shared log at the end of this
file, one row per change, and increment the version in the index above.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Chain Completeness`, `Execution Status`, `Referenced but Not Produced`
- Purpose: inventory the family so a reviewer can see at a glance what the row was
  built from, and so later columns can reason about what is present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its relationship to the base agreement.

## Scope

- Include every separately titled document in the unit, including the base agreement, amendments, amended and restated agreements, statements of work, order forms, side letters, and addenda.
- Treat exhibits, schedules, and annexes physically attached to a document as part of that document, not as separate documents.
- Do not include documents that are only referenced but are not present in the unit. Those belong to the Referenced but Not Produced column.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in three words or fewer and add `(untitled)`.
- Give each document's date as printed. Use the date the document states for itself, not a filing, transmittal, or notarization date.
- State the relationship as one of `Base`, `Amendment`, `Restatement`, `SOW`, `Order form`, `Side letter`, or `Addendum`.
- Number amendments as the document numbers itself. Do not renumber or infer a sequence.
- If a document's date is absent, write `date not stated` rather than estimating from adjacent documents.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Relationship])`

Return no more than 25 lines and no more than 150 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Base agreement absent`, `Sequence gap`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: flag rows where the family is incomplete, so a reviewer knows before
  reading any provision cell that the row may not show the current terms.

**This is the guard on the whole table.** A row with a missing amendment produces
confidently wrong provision cells and nothing else detects it.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether the agreement family in this review unit appears complete. Choose exactly one configured option.

## Scope

- Consider only documents that amend, restate, supplement, or are issued under the base agreement.
- Exclude referenced third-party documents, policies, codes of conduct, and standard terms hosted elsewhere. Those are not part of the chain.
- Exclude exhibits and schedules to a document that is present.

## Classification rules

Apply the first rule that fits.

1. `Base agreement absent`: the unit contains amendments, SOWs, or order forms but the base agreement they are issued under is not present.
2. `Amendment referenced but absent`: a document in the unit refers to an amendment, restatement, or side letter that is not present in the unit. A recital reciting the amendment history is the most common source of this evidence.
3. `Sequence gap`: amendments are numbered and a number in the sequence is missing, for example Amendment 1 and Amendment 3 are present and Amendment 2 is not.
4. `Complete on its face`: the base agreement is present, and no document in the unit refers to an amending document that is absent.

`Complete on its face` states only that nothing in these documents reveals a gap. It does not state that no further amendments exist.

## Fallback rules

- Use `Unable to determine` when a document refers to a prior or subsequent agreement in terms too vague to tell whether it amends this agreement, or when amendment references are illegible.
- Do not use `Unable to determine` because the unit contains a single unamended agreement. A single complete base agreement is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Execution Status

- Native type: Classify
- Configured options, in UI order: `All documents executed`, `Base executed, later document unsigned`, `Base unsigned`, `Partially executed`, `Form or template`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: `Consent Trigger Profile`
- Purpose: state what the family visibly proves about its own completion, so a
  reviewer never reads a provision from an unsigned draft as a binding obligation.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks in the current unit.

## Task

Classify the visible execution status of the documents in this review unit. Choose exactly one configured option.

## Scope

- Evaluate only signature blocks, electronic-signature markers, conformed signatures, and counterpart signature pages visible in the documents in this unit.
- Exclude signature evidence appearing on exhibits, attachments, or referenced documents; that evidence describes those documents.
- Exclude notary, witness, and attestation blocks. Do not count them toward execution.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the documents are unpopulated forms, containing bracketed placeholders, blank party names, or `[•]` fields in place of terms.
2. `Base unsigned`: the base agreement provides party signature blocks and none bears a signature marker.
3. `Partially executed`: any document in the unit has at least one signed and at least one unsigned party signature block.
4. `Base executed, later document unsigned`: the base agreement is fully signed and at least one amendment, SOW, order form, or side letter in the unit is unsigned.
5. `All documents executed`: every document in the unit has a signature marker in every party signature block it provides.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name without one of these, a blank signature line, a `DRAFT` watermark, or a stated effective date is not a signature marker.

## Fallback rules

- Use `Unable to determine` only when signature evidence exists but cannot be read, when a signature page is referenced but missing from a document, or when a document conflicts with itself about execution.
- Do not treat a `duly executed` recital, a stated effective date, or a later document reciting that the base agreement was signed as evidence that signatures were completed on the document in front of you.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Target Contracting Entity

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: identify which target-group entity is the contracting party, so the
  contract matrix can be reconciled to the corporate chart and so a carve-out or
  intra-group restructuring can be assessed.

```markdown
## Task

Identify which target-group entity is a contracting party to this agreement family.

## Scope

- Use the review-subject entity list in the Table Instructions to determine which party is a target-group entity.
- Read the parties clause and the signature blocks of the base agreement, and any assignment or novation in a later document in the unit that substitutes a different entity.
- Exclude parents, affiliates, and subsidiaries merely mentioned in the text, named as beneficiaries, or listed as permitted affiliate users.

## Rules

- Report the entity name exactly as printed in the agreement, including the entity suffix, even where it differs from the name in the Table Instructions list.
- If the printed name differs from the review-subject list, append ` (variant of [listed name])` so the reviewer can see the mismatch.
- If a later document in the unit assigns or novates the agreement to a different target entity, report the current entity and append ` (assigned from [prior entity], [YYYY-MM-DD])`.
- If more than one target entity is a party, list each on its own line.
- If the contracting party is not a target-group entity, return `Not applicable — no target entity is a party` and name the parties.

## Fallback rules

- If a party name is illegible or the parties clause is missing, return `Unable to determine — [brief reason]`.

## Output format

`[Exact entity name]` per line, with any qualifier appended as described above. Return no more than 40 words. Do not include addresses, section numbers, or citation markers.
```

---

### 5. Counterparty

- Native type: Free Response
- Upstream: none
- Downstream: `Counterparty Type`
- Purpose: identify the non-target party by exact legal name, which is the join
  key for revenue concentration and for the consent request itself.

```markdown
## Task

Identify the non-target contracting party or parties to this agreement family.

## Scope

- Every party to the base agreement other than a target-group entity listed in the Table Instructions.
- Include a party added or substituted by an assignment, novation, or joinder in a later document in the unit.
- Exclude affiliates of the counterparty that are merely permitted to receive services or place orders, guarantors, and third-party beneficiaries.

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

### 6. Counterparty Type

- Native type: Classify
- Configured options, in UI order: `Customer`, `Vendor or supplier`, `Reseller or distributor`, `Partner or collaborator`, `Affiliate or related party`, `Other`, `Unable to determine`
- Upstream: `@Counterparty`
- Downstream: none
- Purpose: let the grid be filtered by commercial direction, which is what
  separates revenue contracts from cost contracts in the issues list.

```markdown
## Established results

- Counterparty: @Counterparty

Use this to identify the party being classified. Determine its role from the operative terms of the documents in the current unit.

## Task

Classify the commercial role of the counterparty relative to the target entity. Choose exactly one configured option.

## Classification rules

- `Customer`: the counterparty pays the target for goods, services, or a licence.
- `Vendor or supplier`: the target pays the counterparty for goods, services, or a licence.
- `Reseller or distributor`: the counterparty resells, distributes, or sublicenses the target's offering to third parties.
- `Partner or collaborator`: the parties jointly develop, market, or deliver something, without one simply paying the other.
- `Affiliate or related party`: the counterparty is stated to be under common ownership or control with a target entity, or is a founder, officer, director, or an entity they are stated to control.
- `Other`: a mutual arrangement with no payment direction, such as a standalone NDA.

Classify on the payment and delivery direction in the operative terms, not on the agreement's title. An agreement titled a services agreement under which the target is paid is a `Customer` contract.

Where the target both pays and is paid, classify on the primary commercial purpose stated in the recitals or scope.

`Affiliate or related party` takes precedence over every other option when the relationship is stated in the documents.

## Fallback rules

- Use `Unable to determine` when the documents do not show which party pays or delivers, or when the direction conflicts between documents in the unit.

## Output format

Return only the exact configured option and no explanation.
```

---

### 7. Agreement Type

- Native type: Classify
- Configured options, in UI order: `Master services agreement`, `Customer or subscription agreement`, `Statement of work or order form`, `Reseller or distribution agreement`, `Supply or manufacturing agreement`, `SaaS or cloud services agreement`, `Non-disclosure agreement`, `Data processing agreement`, `Licence agreement`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Effective Date`, `Initial Term`, `Current Term Expiry`, `Renewal Mechanism`
- Purpose: route the date and term columns, which use different hierarchies for a
  master agreement than for an order form.

```markdown
## Task

Classify the base agreement in this review unit. Choose exactly one configured option.

## Scope

- Classify the base agreement, not the amendments, statements of work, or order forms issued under it.
- Where the unit contains an amended and restated agreement, classify the restated agreement.
- Where the unit's base document is itself a standalone order form or SOW with no master agreement present, classify it as `Statement of work or order form`.

## Classification rules

- Classify on the operative structure, not the printed title. A document titled a services agreement that sets framework terms for future orders is a `Master services agreement`.
- `Master services agreement`: sets framework terms and contemplates separate orders or statements of work for the actual scope.
- `Customer or subscription agreement`: a single agreement containing both the framework and the scope, under which the counterparty pays for the target's offering.
- `Statement of work or order form`: defines scope, pricing, or quantity under a master agreement.
- `Licence agreement`: the operative grant is a licence of intellectual property, distinct from a service delivered.
- `Data processing agreement`: the operative subject is personal-data processing terms. Use this only where the DPA is the base agreement, not where it is an exhibit to another agreement.
- `Non-disclosure agreement`: confidentiality is the only substantive obligation.
- Use `Other` where none of the options describes the operative structure, and where the agreement is a hybrid, classify on its principal commercial purpose.

## Fallback rules

- Use `Unable to determine` when the operative terms are missing, incorporated from a document not in the unit, or too incomplete to identify the structure.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the choice-of-law jurisdiction, which drives covenant enforceability
  and local counsel routing.

```markdown
## Task

Identify the governing law of the agreement.

## Rules

- Report the jurisdiction chosen to govern the agreement, as stated.
- Report the jurisdiction only. Do not report the forum, venue, arbitral seat, or service-of-process provisions.
- Where different documents in the unit choose different law, report the choice in the most recently dated document that addresses it and append ` (amended from [prior jurisdiction])`.
- Where a document chooses different law for different subject matter, report both, each with the subject in three words or fewer.

## Fallback rules

- Return `Not addressed` where no document in the unit contains a choice of law.
- Return `Incorporated terms` where governing law is stated to be set by a document not present in the unit.

## Output format

`[Jurisdiction]`, for example `New York` or `England and Wales`. Return no more than 20 words. Do not include section numbers or citation markers.
```

---

### 9. Effective Date

- Native type: Date — **confirm the type accepts `Not stated` before use**
- Upstream: `@Agreement Type`
- Downstream: none
- Purpose: the date the agreement takes effect, for the contract matrix and the
  term calculation.

```markdown
## Established results

- Agreement type: @Agreement Type

Use the agreement type to select the applicable hierarchy below. Confirm the date against the documents in the current unit.

## Task

Identify the date the base agreement took effect.

## Date-selection hierarchy

### Master, customer, licence, supply, SaaS, NDA, and DPA agreements

1. Use the effective date the agreement states for itself.
2. If none is stated, use the date of the last party signature.
3. If neither is available, use the date printed in the preamble.

### Statement of work or order form

1. Use the effective date or service commencement date the document states for itself.
2. If none is stated, use the date of the last party signature.

### Where the unit contains an amended and restated agreement

Use the effective date of the restated agreement, not of the original.

## Excluded dates

- File name and document metadata dates
- Notarization, transmittal, download, and scan dates
- Dates belonging only to a referenced document
- Renewal, amendment, and order dates, which belong to those documents
- A billing or invoice commencement date that the document distinguishes from the effective date

## Rules

- A stated effective date is reported even where it precedes the signature dates, and even where it equals a signature date. A value the document states is never replaced by a fallback state.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 10. Initial Term

- Native type: Duration — **confirm the type accepts `Not stated` and non-numeric values before use**
- Upstream: `@Agreement Type`
- Downstream: none
- Purpose: the length of the first committed term, distinct from the expiry date.

```markdown
## Established results

- Agreement type: @Agreement Type

## Task

Identify the length of the initial term of the base agreement, as stated.

## Scope

- Report the initial or first term only. Renewal and extension periods belong to the Renewal columns.
- For a statement of work or order form, report the term of that document where it states one distinct from the master agreement.
- Where a later document in the unit extends or replaces the initial term, report the term as stated in the most recently dated document that addresses it.

## Rules

- Report the duration as stated, for example `3 years`, `12 months`, `36 months`.
- Where the agreement states a start and end date but no duration, calculate nothing. Return `Not stated` and let the Current Term Expiry column carry the date.
- Where the agreement is stated to continue until terminated with no fixed term, return `Perpetual until terminated`.
- Where the term runs to the completion of the described work rather than a period, return `Until completion of scope`.

## Fallback rules

- Return `Not stated` where no term length is stated.
- Return `Incorporated terms` where the term is stated to be set by a document not present in the unit.

## Output format

The duration as stated, or one of the exact phrases above. Do not include dates, section numbers, or citation markers.
```

---

### 11. Current Term Expiry

- Native type: Date — **confirm the type accepts `Not stated` before use**
- Upstream: `@Agreement Type`
- Downstream: `Term Status on Record`
- Purpose: the end date of the term now running on the face of the documents,
  which is the date the deal team diaries.

```markdown
## Established results

- Agreement type: @Agreement Type

## Task

Identify the end date of the term currently running according to the documents in this review unit.

## Rules

Apply in order.

0. If Agreement Type is `Statement of work or order form`, report the end date of that document's own term. Do not report the master agreement's end date, which outlasts the order.
1. If a document in the unit states an expiry, end, or termination date for the current term, use the date in the most recently dated document that states one.
2. If a document in the unit exercises or evidences a renewal or extension and states the new end date, use that date.
3. If no end date is stated but a start date and a term length are both stated, report the end date those two produce and append nothing. Use the stated start date, not a signature date.
4. If the agreement continues until terminated with no fixed end, return `Not applicable — continues until terminated`.

## Excluded dates

- The expiry of a renewal option that has not been exercised in the documents
- Notice deadlines and cure periods
- Expiry dates belonging to a statement of work or order form when the base agreement is being reported, and the reverse
- Dates belonging only to a referenced document

## Fallback rules

- Return `Not stated` where no end date is stated and the start date or term length needed to derive one is missing.
- Return `Unable to determine` where two documents in the unit state end dates that conflict and neither is later in date than the other.

## Output format

`YYYY-MM-DD`, or one of the exact phrases above. Preserve partial precision as printed.
```

---

### 12. Renewal Mechanism

- Native type: Classify
- Configured options, in UI order: `Automatic renewal`, `Renewal on notice by target`, `Renewal on notice by counterparty`, `Renewal by mutual agreement`, `No renewal provision`, `Not addressed`, `Unable to determine`
- Upstream: `@Agreement Type`
- Downstream: `Renewal Notice Period`, `Term Status on Record`
- Purpose: whether the agreement renews itself, which decides whether a missed
  notice date extends a contract the buyer does not want.

```markdown
## Established results

- Agreement type: @Agreement Type

## Task

Classify how the agreement renews after the current term. Choose exactly one configured option.

## Scope

- Report the renewal mechanism of the base agreement, unless the agreement type is `Statement of work or order form`, in which case report that document's own renewal mechanism.
- Where a later document in the unit changes the renewal mechanism, classify on the most recently dated document that addresses it.

## Classification rules

- `Automatic renewal`: the term extends without action unless a party gives notice to prevent it. This is sometimes called evergreen renewal.
- `Renewal on notice by target`: renewal requires the target entity to give notice or exercise an option.
- `Renewal on notice by counterparty`: renewal requires the counterparty to give notice or exercise an option.
- `Renewal by mutual agreement`: renewal requires both parties to agree, including where renewal is stated to be subject to agreement on price.
- `No renewal provision`: the agreement addresses the end of the term and provides no renewal or extension, expiring at the end of the stated term.

Where the agreement renews automatically but also gives one party an option to extend further, classify as `Automatic renewal`.

Where the agreement continues until terminated with no term to renew, classify as `No renewal provision`.

## Fallback rules

- Use `Not addressed` where the documents are silent on what happens at the end of the term.
- Use `Unable to determine` where renewal provisions in the unit conflict, or where the provision is illegible or incomplete.

## Output format

Return only the exact configured option and no explanation.
```

---

### 13. Renewal Notice Period

- Native type: Duration — **confirm the type accepts `Not stated` and `Not applicable` before use**
- Upstream: `@Renewal Mechanism`
- Downstream: none
- Purpose: how long before expiry notice must be given, which is the date that
  goes in the diary and the reason auto-renewals catch buyers out.

```markdown
## Established results

- Renewal mechanism: @Renewal Mechanism

## Task

If Renewal Mechanism is `Automatic renewal`, identify the notice period required to prevent renewal.

If Renewal Mechanism is `Renewal on notice by target`, `Renewal on notice by counterparty`, or `Renewal by mutual agreement`, identify the notice period required to exercise or initiate renewal.

If Renewal Mechanism is `No renewal provision` or `Not addressed`, return exactly `Not applicable`.

If Renewal Mechanism is `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Use the established result for routing, but confirm the notice period against the documents in the current unit.
- Report the period as stated, for example `90 days`, `3 months`, `60 days prior to the end of the then-current term`.
- Report the period as a duration only. Do not calculate the resulting calendar date.
- Where the period differs by party, report the period applying to the target entity.
- Where a later document in the unit changes the period, report the period in the most recently dated document that addresses it.

## Fallback rules

- Return `Not stated` where renewal is provided for but no notice period is stated.
- Do not convert `Not applicable` or `Not addressed` upstream into a positive finding.

## Output format

The period as stated, or one of the exact fallback values above. Return no more than 15 words. Do not include dates, section numbers, or citation markers.
```

---

### 14. Term Status on Record

- Native type: Classify
- Configured options, in UI order: `Within initial term`, `Within renewal term`, `Stated term has ended, no extension in unit`, `Terminated`, `Continues until terminated`, `Term not stated`, `Unable to determine`
- Upstream: `@Current Term Expiry`, `@Renewal Mechanism`
- Downstream: none
- Purpose: surface agreements whose stated term has ended with nothing in the file
  extending them — the population most likely to be performing without a current
  contract.

**Scope discipline.** This column reports what the documents show as at the
diligence as-of date. It does not state whether the parties are still performing;
performance is not in the documents. An attorney reads this cell against the
operations data.

```markdown
## Established results

- Current term expiry: @Current Term Expiry
- Renewal mechanism: @Renewal Mechanism

Use these for routing. Confirm the classification against the documents in the current unit.

## Task

Classify the status of the term as at the diligence as-of date in the Table Instructions, based only on the documents in this review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Terminated`: the unit contains a termination notice, termination agreement, or mutual release ending the agreement, whether or not the stated term had expired.
2. `Continues until terminated`: Current Term Expiry is `Not applicable — continues until terminated`.
3. `Term not stated`: Current Term Expiry is `Not stated`.
4. `Within renewal term`: Current Term Expiry falls on or after the diligence as-of date, and the unit contains a document evidencing that a renewal or extension has been exercised or has taken effect.
5. `Within initial term`: Current Term Expiry falls on or after the diligence as-of date, and no renewal or extension has taken effect on the record.
6. `Stated term has ended, no extension in unit`: Current Term Expiry falls before the diligence as-of date, and the unit contains no document extending, renewing, or replacing the term.

Where Renewal Mechanism is `Automatic renewal` and Current Term Expiry falls before the diligence as-of date, still use `Stated term has ended, no extension in unit`. Whether an automatic renewal in fact operated is a legal conclusion and belongs to the reviewer.

## Fallback rules

- Use `Unable to determine` when Current Term Expiry is `Unable to determine`, or when the documents conflict about whether the agreement was terminated.
- Do not use `Unable to determine` merely because the term has ended. An ended term is a finding, not an uncertainty.

## Output format

Return only the exact configured option and no explanation.
```

---

### 15. Termination for Convenience — Holder

- Native type: Classify
- Configured options, in UI order: `Target only`, `Counterparty only`, `Either party`, `Neither party`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Termination for Convenience — Detail`
- Purpose: who can walk away without cause, which decides whether a revenue
  contract is as secure as it looks.

```markdown
## Task

Classify which party may terminate this agreement for convenience, meaning without cause and without a breach by the other party. Choose exactly one configured option.

## Scope

- Include rights described as termination for convenience, termination without cause, termination at will, and termination on notice with no stated grounds.
- Exclude termination for cause, for breach, for insolvency, for change of control, for force majeure, and for failure to agree on renewal pricing. Those are addressed in other columns.
- Exclude a right to terminate a single statement of work or order form while the master agreement continues, unless the agreement type being reported is that order form.
- Where a later document in the unit changes the right, classify on the most recently dated document that addresses it.

## Classification rules

- Use the Table Instructions review-subject list to determine which party is the target entity.
- `Either party`: both parties hold the right, whether or not the notice periods differ.
- `Neither party`: the agreement addresses termination and provides no right to terminate without cause.

A right exercisable only during a stated window, or only after a minimum period has run, is still a termination for convenience right. Report it here and state the limitation in the Detail column.

A right to terminate on notice that is available only on the counterparty's failure to meet a service level is termination for cause, not convenience.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses termination without cause.
- Use `Unable to determine` where the provision is illegible or incomplete, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Termination for Convenience — Detail

- Native type: Free Response
- Upstream: `@Termination for Convenience — Holder`
- Downstream: none
- Purpose: the notice period and any conditions or exit fees, so the consent and
  integration workstreams can price the exit.

```markdown
## Established result

- Termination for convenience holder: @Termination for Convenience — Holder

## Task

If Termination for Convenience — Holder is `Target only`, `Counterparty only`, or `Either party`, extract the notice period and any conditions attached to the right, for each party that holds it.

If Termination for Convenience — Holder is `Neither party` or `Not addressed`, return exactly `Not applicable`.

If Termination for Convenience — Holder is `Unable to determine`, return exactly `Unable to determine — upstream holder is unresolved`.

## Rules

- Use the established result for routing, but confirm each period and condition against the documents in the current unit.
- Report the notice period as stated. Do not calculate a date.
- Report any termination fee, wind-down payment, or minimum-commitment shortfall payable on exercise, with the amount or formula as stated.
- Report any limitation on when the right may be exercised, such as a lock-in period or a window tied to the anniversary date.
- Report any obligation surviving exercise only where the document ties it to termination for convenience specifically.
- Do not state whether the right is enforceable, or what its exercise would mean for this transaction.

## Output format

One line per party holding the right:

`[Target | Counterparty] — [notice period]; fee: [amount, formula, or "none stated"]; conditions: [brief, or "none stated"]`

Return no more than 60 words. Do not include section numbers, quotations, or citation markers.
```

---

### 17. Termination for Cause

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the grounds and cure period, which set how quickly a counterparty
  could exit if performance slips during or after the transaction.

```markdown
## Task

Identify the grounds on which this agreement may be terminated for cause, and the cure period.

## Scope

- Include material breach, repeated breach, failure to pay, failure to meet a service level, regulatory or legal violation, and loss of a required licence or certification.
- Exclude termination for convenience, insolvency, change of control, and force majeure. Those are addressed in other columns.
- Where a later document in the unit changes the grounds, report the grounds in the most recently dated document that addresses them.

## Response labels

Begin with exactly one of:

- `Mutual`
- `Target only`
- `Counterparty only`
- `Not addressed`
- `Incorporated terms`
- `Unable to determine`

## Rules

- Consolidate substantially similar grounds. Report no more than five.
- Report the cure period as stated, and state where a ground is stated to be non-curable.
- Where cure periods differ by ground, report the shortest and name the ground it applies to.
- Do not report the notice mechanics for giving a cure notice.

## Fallback rules

- If no document in the unit addresses termination for cause, return exactly `Not addressed`.
- If the grounds are stated to be set by a document not present in the unit, return `Incorporated terms — grounds not stated in current documents`.

## Output format

`[Response label] — grounds: [list]; cure: [period or "none stated"]`

Return no more than 70 words. Do not include section numbers, quotations, or citation markers.
```

---

### 18. Termination on Insolvency

- Native type: Classify
- Configured options, in UI order: `Either party may terminate`, `Counterparty may terminate on target insolvency`, `Target may terminate on counterparty insolvency`, `Automatic termination`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: an insolvency trigger interacts with pre-closing restructuring and with
  the debt workstream, and it can be tripped by a solvent reorganisation.

```markdown
## Task

Classify how this agreement treats the insolvency of a party. Choose exactly one configured option.

## Scope

- Include bankruptcy, insolvency, administration, receivership, liquidation, winding-up, assignment for the benefit of creditors, and the appointment of a trustee or administrator.
- Include a general inability-to-pay-debts trigger.
- Exclude payment default and material breach, which belong to the Termination for Cause column.
- Exclude change of control and reorganisation triggers that are not tied to insolvency; those belong to the change of control columns.

## Classification rules

- Use the Table Instructions review-subject list to determine which party is the target entity.
- `Automatic termination`: the agreement states that it terminates on the insolvency event without any party giving notice.
- Where an insolvency event is listed as a ground for termination for cause rather than in a separate clause, still classify it here.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses insolvency.
- Use `Unable to determine` where the provision is illegible or incomplete, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 19. Assignment Restriction

- Native type: Classify
- Configured options, in UI order: `No restriction`, `Consent required`, `Consent required, not to be unreasonably withheld`, `Assignment prohibited`, `Permitted to affiliate only`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Succession Carve-Out`, `Assignment Language`, `Consent Trigger Profile`
- Purpose: whether the target can transfer the agreement, and on what condition.

```markdown
## Task

Classify the restriction on assignment or transfer of this agreement **by the target entity**. Choose exactly one configured option.

## Scope

- Analyze the restriction as it applies to the target entity. Where the clause is mutual, classify on the restriction binding the target.
- Include assignment, transfer, novation, delegation of the agreement or of rights under it, and any restriction on transferring by operation of law.
- Exclude restrictions on subcontracting performance, on delegating individual obligations while remaining liable, and on assigning receivables only, unless the clause treats those as assignment of the agreement.
- Exclude restrictions binding only the counterparty.
- Where a later document in the unit replaces or amends the clause, classify on the most recently dated document that addresses it.

## Classification rules

Apply the first rule that fits.

1. `Assignment prohibited`: assignment by the target is prohibited outright, with no consent mechanism.
2. `Permitted to affiliate only`: assignment is permitted without consent to an affiliate or group company, and otherwise prohibited or subject to consent.
3. `Consent required, not to be unreasonably withheld`: consent is required and the clause qualifies it with a reasonableness, good-faith, or non-delay standard.
4. `Consent required`: consent is required with no stated standard limiting the counterparty's discretion.
5. `No restriction`: the agreement addresses assignment and permits it freely, or expressly provides that it binds successors and assigns without restricting assignment.

A clause providing only that the agreement binds successors and permitted assigns, without restricting assignment, is `No restriction`.

Consent that is deemed given after a stated period of silence is still `Consent required`; report the deeming mechanism in the Language column.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses assignment or transfer by the target.
- Use `Unable to determine` where the clause is illegible or incomplete, where documents in the unit conflict, or where the clause is incorporated from a document not present in the unit. This column is a Classify column, so it cannot return `Incorporated terms`; the incorporation is reported in Referenced but Not Produced.

## Output format

Return only the exact configured option and no explanation.
```

---

### 20. Succession Carve-Out

- Native type: Classify
- Configured options, in UI order: `Successor permitted without consent`, `Successor expressly captured`, `Silent on succession`, `Not applicable`, `Unable to determine`
- Upstream: `@Assignment Restriction`
- Downstream: `Consent Trigger Profile`
- Purpose: whether the assignment restriction expressly permits or expressly
  captures a transfer to a successor by merger or by sale of the business.

**This is the highest-value cell in the table.** A consent-required contract with
a successor carve-out needs no consent. A consent-required contract that expressly
captures transfers by operation of law does, and it goes on the schedule. `Silent
on succession` is the population that needs a lawyer, because whether a merger
constitutes an assignment is then a question of law.

```markdown
## Established result

- Assignment restriction: @Assignment Restriction

## Task

If Assignment Restriction is `Consent required`, `Consent required, not to be unreasonably withheld`, `Assignment prohibited`, or `Permitted to affiliate only`, classify how the assignment provision treats a transfer to a successor.

If Assignment Restriction is `No restriction` or `Not addressed`, return exactly `Not applicable`.

If Assignment Restriction is `Unable to determine`, return exactly `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Use the established result for routing. Read the assignment provision in the current unit to classify.

- `Successor permitted without consent`: the provision expressly permits assignment or transfer, without consent, to a successor by merger or consolidation, or to a purchaser of all or substantially all of the assets, equity, or business of the target or the relevant business line.
- `Successor expressly captured`: the provision expressly brings such a transfer within the restriction, using language such as assignment by operation of law, by merger, by consolidation, by change of control, or whether voluntary or involuntary.
- `Silent on succession`: the provision restricts assignment but says nothing about operation of law, merger, consolidation, change of control, or successors.

Apply these boundaries:

- A permission to assign to an **affiliate** is not a successor permission. Where the provision permits affiliate assignment only, classify as `Silent on succession` unless it separately addresses successors.
- A statement that the agreement **binds successors and permitted assigns** is boilerplate about who is bound. It is not a permission to assign. It does not support `Successor permitted without consent`.
- Where a successor permission is conditional, for example on the successor assuming the obligations in writing, on notice being given, or on the successor not being a competitor, classify as `Successor permitted without consent` and report the condition in the Language column.
- Where the provision both permits succession and separately requires consent for a change of control, classify as `Successor permitted without consent` here. The change of control columns carry the separate trigger.

## Fallback rules

- Use `Unable to determine` where the succession language is illegible or incomplete, or where documents in the unit conflict about it.
- Do not use `Silent on succession` where the provision addresses succession in terms you find ambiguous. That is `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 21. Assignment Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Assignment Restriction`
- Downstream: none
- Purpose: the exact clause text, so a reviewer can check the classification
  without opening the document and can draft the consent request from it.

```markdown
## Established result

- Assignment restriction: @Assignment Restriction

## Task

If Assignment Restriction is any value other than `Not addressed` or `Unable to determine`, quote the operative assignment and transfer language exactly as written.

If Assignment Restriction is `Not addressed`, return exactly `Not addressed`.

If Assignment Restriction is `Unable to determine`, quote whatever assignment language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the operative restriction, any successor or affiliate carve-out, and any consent standard or deeming mechanism. Include the sentence containing each.
- Where the clause exceeds 150 words, quote the operative restriction and each carve-out, and replace intervening non-operative text with `[...]` between sentences.
- Do not quote the successors-and-assigns boilerplate unless it is the only assignment language in the documents.
- Do not add analysis, and do not indicate whether the clause is triggered by this transaction.

## Output format

The quoted text, followed by the source tag. Return no more than 200 words. Do not include section numbers or citation markers inside the quotation beyond what the document itself prints.
```

---

### 22. Change of Control Treatment

- Native type: Classify
- Configured options, in UI order: `Consent required`, `Notice required`, `Termination right`, `Deemed assignment`, `No consequence stated`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `CoC Indirect Changes`, `CoC Threshold`, `CoC Language`, `Consent Trigger Profile`
- Purpose: what a change of control of the target triggers under this agreement.
  With `Succession Carve-Out`, this is what the consent schedule is built from.

```markdown
## Task

Classify what a change of control **of the target entity** triggers under this agreement. Choose exactly one configured option.

## Scope

- Analyze provisions triggered by a change of ownership, voting control, or management control of the target entity, however described, including change of control, change in control, transfer of control, and deemed liquidation.
- Include a provision that treats a change of control as an assignment.
- Exclude provisions triggered only by a change of control of the counterparty.
- Exclude insolvency and reorganisation provisions not tied to a control change.
- Exclude a change in the individuals performing services, and change-of-key-personnel provisions.
- Where a later document in the unit changes the provision, classify on the most recently dated document that addresses it.

## Classification rules

Apply the first rule that fits.

1. `Termination right`: the counterparty may terminate, or the agreement terminates, on a change of control of the target.
2. `Consent required`: the change of control requires the counterparty's prior consent or approval.
3. `Deemed assignment`: the agreement states that a change of control constitutes, or is deemed to be, an assignment, without separately stating a consequence. The consequence then follows the assignment clause.
4. `Notice required`: the target must notify the counterparty, with no consent, approval, or termination right attached.
5. `No consequence stated`: a change of control is defined or referenced in the agreement but no obligation, consent, notice, or right attaches to it.

Where a change of control both requires consent and gives a termination right on failure to obtain it, classify as `Termination right`, which is the more severe consequence, and describe both in the Language column.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses a change of control of the target.
- Use `Unable to determine` where the provision is illegible or incomplete, where documents in the unit conflict, or where the provision is incorporated from a document not in the unit.

## Output format

Return only the exact configured option and no explanation.
```

---

### 23. CoC Indirect Changes

- Native type: Classify
- Configured options, in UI order: `Direct transfer only`, `Indirect or ultimate control captured`, `Not applicable`, `Unable to determine`
- Upstream: `@Change of Control Treatment`
- Downstream: none
- Purpose: whether a change at a parent level triggers the clause, which decides
  whether a holdco-level deal reaches this contract at all.

```markdown
## Established result

- Change of control treatment: @Change of Control Treatment

## Task

If Change of Control Treatment is `Consent required`, `Notice required`, `Termination right`, `Deemed assignment`, or `No consequence stated`, classify whether the provision captures indirect changes of control.

If Change of Control Treatment is `Not addressed`, return exactly `Not applicable`.

If Change of Control Treatment is `Unable to determine`, return exactly `Unable to determine`.

Choose exactly one configured option.

## Classification rules

Use the established result for routing. Read the change of control definition and the operative provision in the current unit to classify.

- `Indirect or ultimate control captured`: the provision reaches a change at a level above the contracting entity, using language such as direct or indirect, ultimate parent, ultimate beneficial ownership, person controlling the party, or a defined `Control` term that extends up the ownership chain.
- `Direct transfer only`: the provision reaches only a transfer of the contracting entity's own equity or a transaction to which the contracting entity is itself party, with no reference to indirect or upstream ownership.

Where the definition refers to a change in the ownership of the party **or any of its parent entities**, classify as `Indirect or ultimate control captured`.

Where the provision is triggered by a sale of all or substantially all assets only, and says nothing about equity ownership at any level, classify as `Direct transfer only`.

## Fallback rules

- Use `Unable to determine` where the definition is incorporated from a document not present in the unit, is illegible, or is drafted so that it cannot be told which level it reaches.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. CoC Threshold

- Native type: Free Response
- Upstream: `@Change of Control Treatment`
- Downstream: none
- Purpose: the ownership or voting percentage that triggers the provision, which
  is the input the threshold analysis needs.

```markdown
## Established result

- Change of control treatment: @Change of Control Treatment

## Task

If Change of Control Treatment is any value other than `Not addressed` or `Unable to determine`, extract the ownership, voting, or control threshold stated in the change of control definition.

If Change of Control Treatment is `Not addressed`, return exactly `Not applicable`.

If Change of Control Treatment is `Unable to determine`, return exactly `Unable to determine`.

## Rules

- Use the established result for routing, but confirm the threshold against the documents in the current unit.
- Report the percentage and what it applies to, for example `50% of voting securities`, `more than 50% of equity interests`, `40% of outstanding shares`.
- Where the definition states multiple independent triggers, report each, separated by semicolons. Report no more than four.
- Where a trigger is qualified rather than numeric, report it as stated, for example `sale of all or substantially all assets`, `change in the composition of a majority of the board`, `power to direct management and policies`.
- Report the threshold as written. Do not state whether this transaction crosses it.

## Fallback rules

- Return `Not stated` where a change of control provision exists but states no threshold and no qualitative trigger.
- Return `Incorporated terms` where the definition is stated to sit in a document not present in the unit.

## Output format

`[threshold]; [threshold]` as needed. Return no more than 45 words. Do not include section numbers, quotations, or citation markers.
```

---

### 25. CoC Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Change of Control Treatment`
- Downstream: none
- Purpose: the exact trigger text. This is the cell the consent request is drafted
  from and the cell a partner checks before the schedule goes to the client.

```markdown
## Established result

- Change of control treatment: @Change of Control Treatment

## Task

If Change of Control Treatment is any value other than `Not addressed` or `Unable to determine`, quote the change of control provision and its definition exactly as written.

If Change of Control Treatment is `Not addressed`, return exactly `Not addressed`.

If Change of Control Treatment is `Unable to determine`, quote whatever change of control language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote both the operative provision and the definition of the defined term it uses, where the definition appears in the documents in the unit. Where they are in different places, quote each and separate them with a line break.
- Where the combined text exceeds 200 words, quote the operative provision in full and the part of the definition that states the trigger and the threshold, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether this transaction triggers the provision.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words. Do not include section numbers or citation markers inside the quotation beyond what the document itself prints.
```

---

### 26. Consent Trigger Profile

- Native type: Free Response
- Upstream: `@Assignment Restriction`, `@Succession Carve-Out`, `@Change of Control Treatment`, `@Execution Status`
- Downstream: none
- Purpose: one filterable cell summarising every transfer-related trigger in the
  family, so the consent schedule is built by filtering this table rather than by
  asking Harvey a fresh question.

**Scope discipline.** This column reports the triggers the documents contain. It
does not decide whether this transaction fires them. That is `Consent Required for
This Structure`, a human column, and it needs the deal structure, which this table
does not have.

```markdown
## Established results

- Assignment restriction: @Assignment Restriction
- Succession carve-out: @Succession Carve-Out
- Change of control treatment: @Change of Control Treatment
- Execution status: @Execution Status

Use these results for routing and consistency. Confirm each reported trigger against the documents in the current unit.

## Task

Summarize every transfer-related trigger this agreement family contains, so a reviewer can assess it against the deal structure.

## Response labels

Begin with exactly one of:

- `Consent trigger`
- `Notice trigger`
- `Termination trigger`
- `No transfer trigger`
- `Not addressed`
- `Unable to determine`

## Routing rules

- Use `Termination trigger` where Change of Control Treatment is `Termination right`, or where the assignment clause gives the counterparty a termination right.
- Use `Consent trigger` where Change of Control Treatment is `Consent required`, or where Assignment Restriction requires consent or prohibits assignment **and** Succession Carve-Out is `Successor expressly captured` or `Silent on succession`.
- Use `Notice trigger` where the only requirement is notice.
- Use `No transfer trigger` where Assignment Restriction is `No restriction`, or where Succession Carve-Out is `Successor permitted without consent` **and** Change of Control Treatment is `Not addressed` or `No consequence stated`.
- Use `Not addressed` where Assignment Restriction and Change of Control Treatment are both `Not addressed`.
- Use `Unable to determine` where either Assignment Restriction or Change of Control Treatment is `Unable to determine`.

Where more than one trigger exists, use the most severe label in this order: `Termination trigger`, `Consent trigger`, `Notice trigger`.

## Rules

- State each trigger, what it attaches to, and whose action it requires, in one clause each.
- Where Succession Carve-Out is `Silent on succession`, append ` [succession silent — legal question]`. This is the flag that routes the row to a lawyer.
- Where Execution Status is `Base unsigned`, `Base executed, later document unsigned`, `Partially executed`, or `Form or template`, append ` [execution: [upstream value]]`. A trigger in an unsigned document is not an obligation.
- Do not state whether this transaction crosses a threshold, whether consent is in fact required, or what the consequence would be for the deal.
- Do not restate the quoted language. It is in the Language columns.

## Output format

`[Response label] — [trigger]; [trigger]` followed by any bracketed flags.

Return no more than 50 words. Do not include section numbers, quotations, or citation markers.
```

---

### 27. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this family refers to that is not in the unit. This
  is the column that feeds the coverage register from every table.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document that the documents in this review unit refer to and that is not present in the unit.

## Scope

- Include exhibits, schedules, annexes, and appendices referenced but not attached.
- Include amendments, restatements, side letters, statements of work, and order forms referenced but not present.
- Include incorporated policies, standard terms, service level documents, codes of conduct, and terms hosted at a URL.
- Include prior agreements referenced as superseded, where the reference indicates they may still govern part of the relationship.
- Exclude documents referenced only as background with no bearing on the parties' obligations, such as a party's certificate of incorporation.
- Exclude statutes, regulations, standards, and published technical specifications.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the applicable order form`, report it as printed and add `(generic reference)`.
- Where a document is referenced by URL, report the document's name and add `(hosted terms)`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every document referenced is present in the unit.

Note: `None identified` is a positive finding for this column, not a fallback state. It means the search was run and found nothing.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"]`

Return no more than 15 lines and no more than 120 words. Do not include section numbers, quotations, or citation markers.
```

---

## Human-review fields

Separate table columns, never populated by Harvey. A cell Harvey filled is a
candidate: not a finding, not in the memo, not told to a client until `Review
Status` says otherwise.

| Column | Values |
| --- | --- |
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Operative version confirmed** | Yes / No, superseded / Chain incomplete |
| **Consent required for this structure** | Yes / No / Ambiguous |
| Revenue significance | Top 10 / Top 50 / Other / Unknown |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: counterparty, dates, assignment, change of
control. Lock cells once `Verified`, and re-run dependents in dependency order
after any upstream change — locking preserves work, it does not refresh it.

Pull 10% of `Verified` cells each matter and open the source. The review columns
are a convention, not a control, and conventions decay silently without sampling.

---

## Test set

Build this before the first full run. An unticked dimension is open risk, not a
pass. Record results in the evaluation log.

- [ ] Base agreement alone, fully executed
- [ ] Base agreement plus two amendments, where the second restates the assignment clause
- [ ] Base agreement plus an amendment that is referenced in a recital but absent
- [ ] Amendment 1 and Amendment 3 present, Amendment 2 absent
- [ ] SOW or order form present with no master agreement
- [ ] Unsigned base agreement
- [ ] Base executed with an unsigned amendment
- [ ] Unpopulated form or template
- [ ] Agreement silent on assignment
- [ ] Assignment clause with an express successor permission
- [ ] Assignment clause expressly capturing operation of law
- [ ] Assignment clause restricting assignment but silent on succession
- [ ] Successors-and-assigns boilerplate as the only assignment language
- [ ] Affiliate-only assignment permission
- [ ] Change of control definition reaching indirect and ultimate parent ownership
- [ ] Change of control triggered by asset sale only
- [ ] Change of control terms incorporated from a document not in the unit
- [ ] Auto-renewing agreement whose stated term ended before the as-of date
- [ ] Agreement continuing until terminated, with no fixed term
- [ ] Terminated agreement with a termination notice in the unit
- [ ] Agreement assigned to a different target entity mid-life
- [ ] Illegible or partially scanned assignment clause
- [ ] Two documents in the unit conflicting on governing law
- [ ] Non-English agreement, to confirm routing rather than analysis

Also test the dependency behaviour directly: change `Assignment Restriction` on a
row from `Consent required` to `No restriction` and confirm that
`Succession Carve-Out`, `Assignment Language`, and `Consent Trigger Profile` all
move to their non-applicable states after re-run, and that a locked
`Consent Trigger Profile` cell does not silently retain the old value.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
| --- | --- | --- | --- | --- | --- | --- |
| | | v1.0 | Initial draft | — | — | — |
