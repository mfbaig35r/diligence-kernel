# Prompt Inventory — Corporate and Entity Structure

Platform-ready Harvey Review Table. Second reference table, built to the same
standard as Contracts Core.

Keep this file outside Harvey. Exports omit Table Instructions and Harvey does not
version prompts, so this is the authoritative history.

## Table

- Matter: `[Project name]`
- Platform: Harvey Review Tables (UI)
- Review unit: **one entity** — its formation document, charter or operating
  agreement, every amendment and restatement, bylaws, the written consents and
  minutes produced for it, and its good standing certificate
- Grouping used: **yes**, up to 25 documents per unit
- Intended reviewers and downstream use: corporate/M&A team; feeds the approval
  schedule, the closing checklist, the org chart reconciliation, and the coverage
  register
- Inventory version: v1.0
- Last full run: —
- Last evaluated: —

### Why the entity is the row

A document-per-row corporate table cannot answer the question the deal team asks,
which is about an entity, not a document. Authorized capital sits in the charter,
the amendment history sits across four filings, the board is in the bylaws, and
standing is in a certificate from a different office. One row per entity, with the
set grouped, produces the entity table the org chart is reconciled against.

**The limit matters.** Grouping lets Harvey read the set together. It does not
establish which charter version is operative. Every provision column reports the
provision as stated in the most recently dated document in the unit that
addresses it, and names that document. Whether that version governs — especially
where a restatement and a later amendment conflict — is `Operative Version
Confirmed`, a human column.

### Two rules that shape every column

**Report, never compute.** Authorized capital, issued interests, and ownership are
three different facts from three different documents. This table extracts each as
stated. Reconciliation against the certified cap table is arithmetic against an
authoritative source and belongs in Excel. No column here adds, subtracts, or
reconciles anything.

**Filed is not the same as adopted, and adopted is not the same as current.** An
unfiled charter amendment does not change the charter. `Filing Evidence` is the
orientation column that keeps every downstream cell honest about this.

## Assumptions to confirm before running

1. Units are assembled per entity at upload, and each unit contains that entity's
   documents only. A parent's charter in a subsidiary's unit is the single most
   likely source of scope leakage in this table.
2. Buy-side review; the entities in the Table Instructions list are the review
   subjects.
3. This table's job is the entity and governance layer. Securities instruments,
   grants, and holders are in the Capitalization table over the same project.
4. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.
5. Compilations were split before upload. A single PDF containing good standing
   certificates for eight entities cannot be a row.

## Pre-run verification

- [ ] Every Classify column's options configured in the UI, in the order listed in
      each record. **11 Classify columns.**
- [ ] Typed columns tested with one row of each fallback. Test `Formation Date`
      (Date) with `Not stated` and with a partial date such as `1998-06`. Record
      what the type accepts: ______
- [ ] Verbatim column behaviour confirmed on three known documents.
- [ ] Table Instructions pasted from this file, entity list and as-of date set.
- [ ] Dependency index re-derived from the prompts.
- [ ] Grouping tested with a unit containing a restated charter plus a later
      amendment that conflicts with it.
- [ ] Grouping tested with an LLC unit and a corporation unit, to confirm the
      terminology map in Table Instructions routes correctly.
- [ ] Legal choices confirmed by the team: the `Transfer Restrictions` option set,
      and the decision that an incorporator or organizer is not reported as an
      officer or director.

### Column count

31 Harvey columns plus 9 human columns. If your tenant's practical cap is lower,
split into **Corporate Identity and Standing** (columns 1–14) and **Corporate
Governance and Triggers** (columns 15–31) over the same project, joined on entity
name in the export. Do not drop columns to fit.

---

## Table Instructions

- Version: v1.0
- Last changed: —

About 2,600 characters. Longer than the Contracts table's because the terminology
map lives here. That map is a naming convention, which is what Table Instructions
are for — it lets thirty columns say "the governing body" instead of branching on
entity type in every prompt. Decision rules and exclusions stay in the columns
that own them.

```markdown
## Matter

[Project name]. Buyer-side entity and governance diligence on the target group listed below.

One row is one entity: its formation document, charter or operating agreement, every amendment and restatement, its bylaws, the written consents and minutes produced for it, and its good standing certificate. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when an entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Terminology map

Columns refer to governance roles generically. Read them as follows for the entity in the current row:

- **Governing body**: the board of directors of a corporation; the board of managers, managing member, or member acting in a management capacity of an LLC; the general partner of a limited partnership.
- **Owners**: stockholders or shareholders of a corporation; members of an LLC; partners of a partnership.
- **Ownership units**: shares of a corporation; membership interests, units, or percentage interests of an LLC; partnership interests.
- **Constitutional document**: the certificate or articles of incorporation of a corporation; the certificate of formation together with the operating agreement of an LLC; the certificate of limited partnership together with the partnership agreement.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the entities.
- The subject of every answer is the entity that is the subject of the current row. Exclude parents, owners, affiliates, subsidiaries, counterparties, and proposed entities that are merely named in the documents.
- Where two documents in the unit address the same provision, report the provision as stated in the most recently dated document that addresses it, and identify that document by its printed title and date. Do not decide which version legally governs.
- Report only what the documents state. Do not add, subtract, reconcile, or otherwise calculate any number, and do not reconcile one document against another.
- Use entity and individual names exactly as printed; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Governing Documents in Unit
  Entity Name
  Entity Type
  Jurisdiction of Formation
  Entity File Number

Stage 2 — Record status
  Governing Documents in Unit ──→ Filing Evidence
                                  Chain Completeness
                                  Prior Names
                                  Standing Status
                                  Referenced but Not Produced
  Standing Status             ──→ Standing Evidence Detail
  Governing Documents in Unit ──→ Formation Date

Stage 3 — Capital (routed on entity type)
  Entity Type ──→ Authorized Capital
                  Issued and Outstanding

Stage 4 — Governance (routed on entity type)
  Entity Type ──→ Governing Body Composition
                  Quorum
                  Ordinary Governing Body Vote
                  Supermajority and Protective Provisions
                  Owner Approval Threshold for Merger or Sale
                  Amendment Mechanics
  Entity Type + Governing Documents in Unit ──→ Named Officers and Directors
  Supermajority and Protective Provisions   ──→ Protective Provisions Language
  Owner Approval Threshold for Merger or Sale ──→ Approval Threshold Language

Stage 5 — Transfer and transaction triggers
  Transfer Restrictions ──→ Transfer Restriction Detail
  Drag-Along            ──→ Drag-Along Conditions
                            Drag-Along Language
```

`Filing Evidence` is referenced by no substantive column, for the same reason
`Execution Status` was not referenced in Contracts Core: filing evidence changes
what a cell proves, not what the document says, and a reviewer reads the two
side by side. It is the first thing the eye goes to on a suspect row.

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Governing Documents in Unit | Free Response | — | Filing Evidence; Chain Completeness; Prior Names; Standing Status; Formation Date; Named Officers and Directors; Referenced but Not Produced | v1.0 | draft |
| 2 | Entity Name | Free Response | — | — | v1.0 | draft |
| 3 | Entity Type | Classify | — | Authorized Capital; Issued and Outstanding; Governing Body Composition; Named Officers and Directors; Quorum; Ordinary Governing Body Vote; Supermajority and Protective Provisions; Owner Approval Threshold for Merger or Sale; Amendment Mechanics | v1.0 | draft |
| 4 | Jurisdiction of Formation | Free Response | — | — | v1.0 | draft |
| 5 | Entity File Number | Free Response | — | — | v1.0 | draft |
| 6 | Formation Date | Date | @Governing Documents in Unit | — | v1.0 | draft |
| 7 | Prior Names | Free Response | @Governing Documents in Unit | — | v1.0 | draft |
| 8 | Filing Evidence | Classify | @Governing Documents in Unit | — | v1.0 | draft |
| 9 | Chain Completeness | Classify | @Governing Documents in Unit | — | v1.0 | draft |
| 10 | Standing Status | Classify | @Governing Documents in Unit | Standing Evidence Detail | v1.0 | draft |
| 11 | Standing Evidence Detail | Free Response | @Standing Status | — | v1.0 | draft |
| 12 | Foreign Qualifications | Free Response | — | — | v1.0 | draft |
| 13 | Authorized Capital | Free Response | @Entity Type | — | v1.0 | draft |
| 14 | Issued and Outstanding | Free Response | @Entity Type | — | v1.0 | draft |
| 15 | Governing Body Composition | Free Response | @Entity Type | — | v1.0 | draft |
| 16 | Named Officers and Directors | Free Response | @Entity Type; @Governing Documents in Unit | — | v1.0 | draft |
| 17 | Quorum | Free Response | @Entity Type | — | v1.0 | draft |
| 18 | Ordinary Governing Body Vote | Free Response | @Entity Type | — | v1.0 | draft |
| 19 | Supermajority and Protective Provisions | Free Response | @Entity Type | Protective Provisions Language | v1.0 | draft |
| 20 | Protective Provisions Language | Verbatim | @Supermajority and Protective Provisions | — | v1.0 | draft |
| 21 | Owner Approval Threshold for Merger or Sale | Free Response | @Entity Type | Approval Threshold Language | v1.0 | draft |
| 22 | Approval Threshold Language | Verbatim | @Owner Approval Threshold for Merger or Sale | — | v1.0 | draft |
| 23 | Transfer Restrictions | Classify | — | Transfer Restriction Detail | v1.0 | draft |
| 24 | Transfer Restriction Detail | Free Response | @Transfer Restrictions | — | v1.0 | draft |
| 25 | Drag-Along | Classify | — | Drag-Along Conditions; Drag-Along Language | v1.0 | draft |
| 26 | Drag-Along Conditions | Free Response | @Drag-Along | — | v1.0 | draft |
| 27 | Drag-Along Language | Verbatim | @Drag-Along | — | v1.0 | draft |
| 28 | Preemptive Rights | Classify | — | — | v1.0 | draft |
| 29 | Amendment Mechanics | Free Response | @Entity Type | — | v1.0 | draft |
| 30 | Subsidiaries and Affiliates Named | Free Response | — | — | v1.0 | draft |
| 31 | Referenced but Not Produced | Free Response | @Governing Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Governing Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Filing Evidence`, `Chain Completeness`, `Prior Names`, `Standing Status`, `Formation Date`, `Named Officers and Directors`, `Referenced but Not Produced`
- Purpose: inventory the entity's document set, so a reviewer can see what the row
  was built from and later columns can reason about what is present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the formation or organizational document, the charter or constitutional document and every amendment and restatement of it, bylaws and every amendment, the operating or partnership agreement and every amendment, written consents, minutes, good standing certificates, foreign qualification certificates, and merger or conversion certificates.
- Treat exhibits and schedules physically attached to a document as part of that document.
- Do not include documents that are only referenced but not present. Those belong to the Referenced but Not Produced column.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date. Use a filing date where the document is a filed instrument bearing a filing stamp, and state which is which in the function label.
- State the function as one of `Formation`, `Charter`, `Charter amendment`, `Charter restatement`, `Bylaws`, `Bylaws amendment`, `Operating agreement`, `Operating agreement amendment`, `Consent`, `Minutes`, `Good standing`, `Foreign qualification`, `Merger or conversion`, or `Other`.
- Where a document relates to an entity other than the subject of this row, still list it and append ` [relates to [entity name]]`. This is how a misfiled unit surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 25 lines and no more than 160 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Entity Name

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the entity's exact current legal name, which is the join key for the org
  chart, the lien search, and every other workstream.

```markdown
## Task

State the exact current legal name of the entity that is the subject of this review unit.

## Scope

- Take the name from the entity's own constitutional document, or from the most recently dated amendment or restatement in the unit that changes the name.
- Exclude the names of parents, owners, subsidiaries, affiliates, counterparties, merging entities, and proposed entities named in the documents.
- Exclude trade names, assumed names, and DBAs. A trade name is not the legal name.

## Rules

- Report the name exactly as printed, including the entity suffix, punctuation, and capitalization as shown.
- Where the printed name differs from the review-subject list in the Table Instructions, report the printed name and append ` (variant of [listed name])`.
- Where the unit contains a merger or conversion certificate, report the surviving entity's name as stated in that certificate.
- Where the entity operates under a trade name stated in the documents, append ` (t/a [trade name])`.

## Fallback rules

- Return `Unable to determine` where the constitutional document is absent from the unit and no other document states the entity's full legal name, or where the name is illegible.

## Output format

`[Exact legal name]`, with any qualifier appended as described above. Return no more than 25 words. Do not include addresses, jurisdictions, or citation markers.
```

---

### 3. Entity Type

- Native type: Classify
- Configured options, in UI order: `Corporation`, `Limited liability company`, `Limited partnership`, `Limited liability partnership`, `General partnership`, `Statutory trust`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: nine columns — see the index
- Purpose: route every capital and governance column, since the qualifying
  evidence differs by entity form.

```markdown
## Task

Classify the legal form of the entity that is the subject of this review unit. Choose exactly one configured option.

## Scope

- Classify the subject entity only. Exclude parents, owners, subsidiaries, and affiliates named in the documents.

## Classification rules

- Classify on the entity's constitutional document and the statute it is formed under, not on the entity name suffix alone. A suffix is corroborating evidence, not the basis.
- `Corporation`: formed by a certificate or articles of incorporation, governed by bylaws, with stockholders or shareholders and a board of directors. Includes professional corporations and benefit corporations.
- `Limited liability company`: formed by a certificate or articles of organization or formation, governed by an operating or limited liability company agreement, with members.
- `Limited partnership`: formed by a certificate of limited partnership, with a general partner and limited partners.
- `Statutory trust`: formed by a certificate of trust or trust agreement, with trustees and beneficial owners.

Where the unit contains a conversion certificate, classify the entity's form **after** the conversion, and the prior form is reported in Prior Names only if the name also changed.

Where the entity is formed outside the United States, classify to the closest option and append nothing; the specific foreign form is reported in Jurisdiction of Formation.

## Fallback rules

- Use `Other` where the documents state a form none of the options describes.
- Use `Unable to determine` where the constitutional document is absent from the unit and no other document states the form, or where the documents conflict about it.

## Output format

Return only the exact configured option and no explanation.
```

---

### 4. Jurisdiction of Formation

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the governing corporate law, which drives approval mechanics, appraisal
  rights, and local counsel routing.

```markdown
## Task

State the jurisdiction under whose law the subject entity is formed.

## Rules

- Report the state or country of formation, as stated in the constitutional document or in a good standing certificate for the entity.
- Where the entity is formed outside the United States, state the country and, where the documents give it, the specific legal form in that jurisdiction, for example `England and Wales (private limited company)`.
- Do not report jurisdictions where the entity is qualified to do business as a foreign entity. Those belong to the Foreign Qualifications column.
- Do not report the governing law of a contract, or the jurisdiction of a parent or subsidiary.
- Where a conversion or domestication certificate is in the unit, report the current jurisdiction and append ` (converted from [prior jurisdiction], [YYYY-MM-DD])`.

## Fallback rules

- Return `Unable to determine` where no document in the unit states the jurisdiction of formation.

## Output format

`[Jurisdiction]`, with any qualifier appended as described above. Return no more than 20 words.
```

---

### 5. Entity File Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the registry file number, which is the search key for lien and
  litigation searches and for verifying standing independently.

```markdown
## Task

State the registry file number, entity number, or registration number assigned to the subject entity by its jurisdiction of formation.

## Rules

- Report the number exactly as printed, including any letter prefix.
- Take it from a filing stamp, a good standing certificate, or a filed constitutional document for this entity.
- Do not report a federal employer identification number, a tax registration number, a licence number, or a docket number.
- Do not report a file number belonging to a parent, subsidiary, or foreign qualification. Where only a foreign qualification number is available, report it and append ` (foreign qualification number, [jurisdiction])`.

## Fallback rules

- Return `Not stated` where no document in the unit shows a file number for this entity.

## Output format

`[Number]`, with any qualifier appended as described above. Return no more than 15 words.
```

---

### 6. Formation Date

- Native type: Date — **confirm the type accepts `Not stated` and partial precision before use**
- Upstream: `@Governing Documents in Unit`
- Downstream: none
- Purpose: the date the entity came into existence, which is distinct from the date
  of the document being read and is the start of every lookback period.

**The canonical error this column exists to prevent** is reporting the date of a
2019 restated charter as the formation date of an entity formed in 1998.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use the inventory to identify which document is the original formation instrument and which are later amendments or restatements. Confirm the date against the documents in the current unit.

## Task

Identify the date the subject entity was originally formed or incorporated.

## Date-selection hierarchy

1. Use the filing date stamped on the original formation instrument — the certificate or articles of incorporation, organization, formation, or limited partnership.
2. If the original instrument is not in the unit, use a formation or incorporation date expressly recited elsewhere, such as in a good standing certificate or in the recitals of a restated charter.
3. If neither is available, use the date the original formation instrument states for itself, where that instrument is present but unstamped.

## Excluded dates

- The date of an amendment, restatement, or amended and restated charter
- The date of bylaws, an operating agreement, or a partnership agreement
- The date of a conversion, domestication, or merger, unless the documents state that the entity first came into existence on that date
- The date of a good standing certificate, as distinct from a formation date recited within it
- File name and metadata dates, and notarization, transmittal, and scan dates

## Rules

- A restated charter that recites the original date of incorporation supplies the formation date. The restatement's own date is not the formation date, even where the restatement is the only charter document in the unit.
- Where the entity resulted from a conversion, report the original formation date of the predecessor where the documents recite it, and report nothing further; the conversion is reported in Jurisdiction of Formation.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no formation date can be selected under the hierarchy.
```

---

### 7. Prior Names

- Native type: Free Response
- Upstream: `@Governing Documents in Unit`
- Downstream: none
- Purpose: every former legal name of this entity. **An unreported name change
  invalidates a clean lien and litigation search**, because both are run against
  the name.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use the inventory to locate name-change amendments, restatements, and merger or conversion certificates. Confirm each name against the documents in the current unit.

## Task

List every prior legal name of the subject entity that the documents in this unit disclose.

## Scope

- Include names changed by charter amendment, by restatement, by conversion, or by merger where the surviving entity took a different name.
- Include a predecessor entity's name where the documents state that this entity is its successor by merger or conversion.
- Exclude trade names, assumed names, DBAs, and brand names. Those are not prior legal names.
- Exclude the names of merging entities that did not survive, unless this entity is stated to be the survivor of that merger.
- Exclude names of parents, subsidiaries, and affiliates.

## Rules

- Report each prior name exactly as printed, with the date of the change where stated.
- Where the change was effected by a specific instrument, name it in three words or fewer.
- List names in date order, earliest first.

## Fallback rules

- Return exactly `None disclosed` where the documents in the unit disclose no prior name.

Note: `None disclosed` is a positive finding, not a fallback state. It means the documents were searched. It does not mean no prior name exists — only a registry search establishes that.

## Output format

One line per prior name, earliest first:

`[Prior name] — changed [YYYY-MM-DD or "date not stated"] by [instrument]`

Return no more than 6 lines and no more than 60 words.
```

---

### 8. Filing Evidence

- Native type: Classify
- Configured options, in UI order: `Filed and stamped`, `Certified copy`, `Executed but no filing evidence`, `Unsigned draft`, `Mixed`, `Not applicable`, `Unable to determine`
- Upstream: `@Governing Documents in Unit`
- Downstream: none
- Purpose: state what the constitutional documents visibly prove about their own
  effectiveness, so a reviewer never reads an unfiled amendment as having changed
  the charter.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use the inventory to identify the filed instruments in the unit. Confirm filing and signature evidence against the documents themselves.

## Task

Classify the visible filing and execution evidence on the instruments in this unit that require filing to take effect. Choose exactly one configured option.

## Scope

- Evaluate only instruments that require filing with a public office to take effect: the formation instrument, charter amendments, restatements, and merger, conversion, and dissolution certificates.
- Exclude bylaws, operating agreements, partnership agreements, written consents, and minutes. Those take effect on adoption, not filing, and are not evaluated here.
- Exclude good standing and foreign qualification certificates, which are issued by the office rather than filed with it.
- Evaluate only filing stamps, file numbers with filing dates, office certification language, and signature blocks visible on the documents.

## Classification rules

Apply the first rule that fits.

1. `Not applicable`: the unit contains no instrument requiring filing.
2. `Unsigned draft`: any filing instrument in the unit bears no signature marker in the block it provides.
3. `Executed but no filing evidence`: every filing instrument is signed, and at least one bears no filing stamp, file number with filing date, or office certification.
4. `Mixed`: at least one filing instrument is filed and stamped or certified, and at least one is signed without filing evidence.
5. `Certified copy`: every filing instrument bears certification language from the Secretary of State or equivalent office.
6. `Filed and stamped`: every filing instrument bears a filing stamp or a file number with a filing date.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, or a stated effective date is not a signature marker.

A stated effective date does not establish that the instrument was filed.

## Fallback rules

- Use `Unable to determine` where a filing stamp or signature is present but illegible, or where a document conflicts with itself about its filing status.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Chain Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Amendment referenced but absent`, `Constitutional document absent`, `Bylaws or operating agreement absent`, `Sequence gap`, `Unable to determine`
- Upstream: `@Governing Documents in Unit`
- Downstream: none
- Purpose: flag rows where the governance record is incomplete, so a reviewer knows
  before reading any provision cell that the row may not show current terms.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use the inventory to identify what is present. Confirm every reference to a missing document against the text of the documents in the current unit.

## Task

Classify whether the governance record for this entity appears complete. Choose exactly one configured option.

## Scope

- Consider only documents that constitute, govern, or amend the subject entity.
- Exclude documents relating to other entities, securities instruments, commercial contracts, and third-party documents.

## Classification rules

Apply the first rule that fits.

1. `Constitutional document absent`: no certificate or articles of incorporation, organization, or formation, and no restatement of one, is present.
2. `Amendment referenced but absent`: a document in the unit refers to an amendment or restatement of the constitutional document, the bylaws, or the operating agreement that is not present. A restatement's recital of amendment history is the most common source of this evidence.
3. `Sequence gap`: amendments are numbered or dated in a sequence and a member of that sequence is missing.
4. `Bylaws or operating agreement absent`: the constitutional document is present, no amendment is missing, and the entity's bylaws, operating agreement, or partnership agreement is not present. Governance provisions cannot be read without it.
5. `Complete on its face`: the constitutional document and the governing agreement are present, and no document refers to an amending instrument that is absent.

`Complete on its face` states only that nothing in these documents reveals a gap. It does not state that no further amendment exists; only a registry search establishes that.

## Fallback rules

- Use `Unable to determine` where a reference to a prior or further instrument is too vague to tell whether it amends this entity's documents, or where amendment references are illegible.
- Do not use `Unable to determine` for a single unamended charter with bylaws. That is `Complete on its face`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Standing Status

- Native type: Classify
- Configured options, in UI order: `Good standing`, `Active`, `Delinquent`, `Suspended or forfeited`, `Revoked`, `Dissolved`, `No standing evidence in unit`, `Unable to determine`
- Upstream: `@Governing Documents in Unit`
- Downstream: `Standing Evidence Detail`
- Purpose: the entity's status **as stated in an official certificate**, separately
  from the details of the certificate that reports it.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use the inventory to locate any good standing, status, or existence certificate for this entity. Confirm the status against that certificate.

## Task

Classify the standing of the subject entity as stated in an official certificate in this review unit. Choose exactly one configured option.

## Scope

- Rely only on a certificate issued by the entity's jurisdiction of formation or by a jurisdiction of foreign qualification: a certificate of good standing, status, existence, fact, or authorization.
- Exclude a party's own representation in a contract that it is in good standing. That is a representation, not evidence of status.
- Exclude a certificate relating to a different entity, including a parent or subsidiary with a similar name.

## Classification rules

- Report the status the certificate states, mapped to the closest configured option. `Good standing` and `Active` are separate options because some offices certify existence or active status without certifying good standing, and the difference matters where franchise tax is outstanding.
- Where the unit contains certificates from more than one jurisdiction, classify on the certificate from the jurisdiction of formation. Foreign qualification status is reported in Foreign Qualifications.
- Where the unit contains more than one certificate from the jurisdiction of formation, classify on the most recently dated one.
- `No standing evidence in unit`: no official certificate for this entity is present. This is a coverage finding, not an uncertainty.

## Fallback rules

- Use `Unable to determine` only where a certificate is present but its status language is illegible, is qualified in terms that do not map to any option, or conflicts with another certificate of the same date.
- Do not use `Unable to determine` because no certificate is present. That is `No standing evidence in unit`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 11. Standing Evidence Detail

- Native type: Free Response
- Upstream: `@Standing Status`
- Downstream: none
- Purpose: the certificate's own particulars, above all its date. **A good standing
  certificate is only as good as its date**, and one predating the deal timeline is
  not evidence of current standing.

```markdown
## Established result

- Standing status: @Standing Status

## Task

If Standing Status is any value other than `No standing evidence in unit` or `Unable to determine`, report the particulars of the certificate the status was taken from.

If Standing Status is `No standing evidence in unit`, return exactly `Not applicable`.

If Standing Status is `Unable to determine`, return exactly `Unable to determine — upstream standing status is unresolved`.

## Rules

- Use the established result for routing, but confirm every particular against the certificate in the current unit.
- Report the issuing office as printed, the certificate's date, and the entity name as printed on the certificate.
- Report the status language substantively as printed, in ten words or fewer, where it adds anything to the classification — for example a qualification about franchise tax or annual report filings.
- Where the entity name on the certificate differs from the Entity Name for this row, append ` [name mismatch]`.
- Compare the certificate date to the diligence as-of date in the Table Instructions. Where the certificate is dated more than 90 days before that date, append ` [certificate over 90 days old]`.
- Do not state whether the entity is currently in good standing. The certificate speaks as of its own date and nothing else in the unit updates it.

## Output format

`[Issuing office] — [YYYY-MM-DD] — [entity name as printed]` followed by any status qualification and any bracketed flags.

Return no more than 45 words. Do not include section numbers, quotations, or citation markers.
```

---

### 12. Foreign Qualifications

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the jurisdictions where the entity is authorized to do business, matched
  against sites, leases, licences, and payroll to find unqualified operations.

```markdown
## Task

List every jurisdiction in which the subject entity is stated to be qualified or authorized to do business as a foreign entity.

## Scope

- Include jurisdictions evidenced by a foreign qualification or authorization certificate for this entity in the unit.
- Include jurisdictions the entity's own documents state it is qualified in.
- Exclude the jurisdiction of formation, which belongs to Jurisdiction of Formation.
- Exclude jurisdictions where the entity merely operates, holds property, or has customers without stated qualification.
- Exclude qualifications of parents, subsidiaries, and affiliates.

## Rules

- Report each jurisdiction with the qualification date and the certificate date where stated.
- Where a certificate states the qualification has been withdrawn, revoked, or is delinquent, report the jurisdiction and the status.

## Fallback rules

- Return exactly `None evidenced in unit` where no foreign qualification is evidenced or stated.

Note: `None evidenced in unit` is a positive finding, not a fallback state. Whether the entity should be qualified elsewhere is a legal question and is not answered here.

## Output format

One line per jurisdiction:

`[Jurisdiction] — qualified [YYYY-MM-DD or "date not stated"][; status]`

Return no more than 15 lines and no more than 90 words.
```

---

### 13. Authorized Capital

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: what the constitutional document **authorizes**, which is the ceiling
  everything issued must fit inside.

**Authorized, issued, and owned are three different facts.** This column reports
the first only. Conflating them is the most common failure in a corporate grid.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report the ownership units the entity's constitutional document authorizes it to issue.

## Scope

- Report authorized amounts only. Do not report units issued, outstanding, reserved, or held by any owner.
- For a `Corporation`, read the authorized capital clause of the charter, including every class and series.
- For a `Limited liability company`, `Limited partnership`, `Limited liability partnership`, or `General partnership`, read any authorized-units or class provision in the operating or partnership agreement. Many such entities authorize no fixed number; see the fallback rules.
- Where a later amendment or restatement in the unit changes the authorized capital, report the amount in the most recently dated document that addresses it.
- Exclude authorized capital of parents, subsidiaries, and affiliates.

## Rules

- Report each class or series separately, with the number authorized and the par value where stated.
- Report the class name exactly as printed, for example `Series A Preferred Stock`.
- Report numbers exactly as printed. Do not total the classes, and do not calculate anything.
- Where a class is authorized as a blank-check series with terms to be fixed by the governing body, report the number authorized and add `(blank check)`.
- Where units are expressed as percentage interests rather than a number, report the classes and add `(percentage interests, no fixed number)`.

## Fallback rules

- Return `Not applicable` where the entity form does not authorize a fixed number of units and the governing agreement states no class structure — common for a member-managed LLC with percentage interests.
- Return `Not addressed` where the constitutional document is present but states no authorized capital.
- Return `Incorporated terms` where the authorized capital is stated to be set by a document not present in the unit.
- Return `Unable to determine` where the constitutional document is absent, or the clause is illegible or internally inconsistent.

## Output format

One line per class:

`[Class name] — [number] authorized[; par value [amount]]`

Return no more than 8 lines and no more than 70 words. Do not include issued or outstanding amounts, section numbers, or citation markers.
```

---

### 14. Issued and Outstanding

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: units the documents state have actually been **issued**, kept separate
  from what is authorized, so the reviewer can see whether they were reported at
  all and against what date.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report the ownership units the documents in this unit state have been issued and are outstanding, and the date each statement speaks as of.

## Scope

- Report issued or outstanding amounts only. Do not report authorized amounts.
- Read stock ledgers, capitalization statements, written consents authorizing an issuance, and any recital in a governing document stating units outstanding.
- Exclude reserved but unissued units, units subject to unexercised options or warrants, and units authorized but not issued.
- Exclude units of parents, subsidiaries, and affiliates.

## Rules

- Report each class separately, with the number stated and the as-of date of the document stating it.
- Where more than one document states an amount for the same class, report the amount in the most recently dated document and append ` (also stated as [number] at [YYYY-MM-DD])` for the earlier figure.
- **Do not calculate.** Do not total classes, do not add issuances recorded in separate consents, do not net cancellations, and do not derive an amount from a percentage. Report each figure as stated and let the reviewer reconcile.
- Where the only evidence is a consent authorizing an issuance rather than a record of it, report the number and add `(authorized by consent; issuance not separately evidenced)`.

## Fallback rules

- Return `Not addressed` where no document in the unit states an issued or outstanding amount. This is a coverage finding: it means the stock ledger or capitalization record was not produced with this entity's documents.
- Return `Unable to determine` where amounts stated in documents of the same date conflict.

## Output format

One line per class:

`[Class name] — [number] issued and outstanding as of [YYYY-MM-DD or "date not stated"]`

Return no more than 8 lines and no more than 80 words. Do not include authorized amounts, percentages you derived, section numbers, or citation markers.
```

---

### 15. Governing Body Composition

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: the size and structure of the governing body and who has the right to
  appoint it, which determines who must approve the transaction and whether the
  buyer can reconstitute the board at closing.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report how the entity's governing body is constituted: its size, how its members are elected or appointed, and any right of a specific owner or class to designate members.

## Scope

- Read the constitutional document and the bylaws, operating agreement, or partnership agreement.
- Report the structure the documents establish. Do not report the individuals currently holding the positions; those belong to Named Officers and Directors.
- For a `Limited liability company`, state whether the documents make the entity member-managed or manager-managed, since that determines who acts for the entity.
- For a `Limited partnership`, report the general partner's management authority and any limited-partner consent rights over management.
- Exclude committees and their composition, unless a committee holds an approval right over a merger or sale of the business.
- Where a later amendment changes the composition, report the structure in the most recently dated document that addresses it.

## Rules

- Report the authorized size as stated: a fixed number, a range, or a mechanism such as determination by resolution.
- Report designation rights with the designating owner or class exactly as printed and the number of seats each may designate.
- Report the term of office and any staggered or classified structure where stated.
- Do not state whether the body is currently properly constituted, and do not state whether vacancies exist.

## Fallback rules

- Return `Not addressed` where the documents establish no governing body structure.
- Return `Incorporated terms` where composition is stated to be governed by a document not present in the unit, such as a stockholders agreement.
- Return `Unable to determine` where provisions in the unit conflict about composition.

## Output format

`[Management structure]; size: [as stated]; election: [mechanism]; designation rights: [owner or class — seats, or "none stated"]`

Return no more than 70 words. Do not include individual names, section numbers, or citation markers.
```

---

### 16. Named Officers and Directors

- Native type: Free Response
- Upstream: `@Entity Type`, `@Governing Documents in Unit`
- Downstream: none
- Purpose: the individuals the documents name, **each with the date and instrument
  naming them**, so a reviewer can see who was appointed when and whether anything
  in the file shows them still in office.

**The failure this column exists to prevent** is reporting an incorporator named
in a 2011 certificate as a current director. Nothing in a document set establishes
who currently holds office; it establishes who was appointed and when.

```markdown
## Established results

- Entity type: @Entity Type
- Documents in unit: @Governing Documents in Unit

Use the inventory to identify which document names each individual and its date. Confirm every name and title against the documents in the current unit.

## Task

List each individual the documents in this unit name as a member of the governing body or as an officer of the subject entity, with the instrument and date naming them.

## Scope

- Include directors, managers, managing members, general partners acting individually, and officers such as president, chief executive, treasurer, and secretary.
- Include appointments, elections, resignations, and removals recorded in consents or minutes.
- **Exclude incorporators, organizers, and initial or interim directors named solely in a formation instrument, unless a later document in the unit confirms them in office.** An incorporator is not a director.
- Exclude signatories acting as authorized persons, attorneys-in-fact, notaries, and witnesses.
- Exclude officers and directors of parents, subsidiaries, and affiliates.
- Exclude registered agents.

## Rules

- Report each individual's name and title exactly as printed.
- Give the date and the instrument naming them, in four words or fewer.
- Where a document records a resignation or removal, report the individual with `resigned` or `removed` and the date.
- Where the same individual is named in more than one instrument, report the most recent one.
- **Do not state that any individual currently holds office.** Report only what was recorded and when.

## Fallback rules

- Return `Not addressed` where no document in the unit names an officer or governing-body member, after excluding incorporators and organizers.
- Return `Unable to determine` where names are illegible, or where documents of the same date conflict about who holds a position.

## Output format

One line per individual, most recent instrument first:

`[Name] — [Title] — [appointed | resigned | removed] [YYYY-MM-DD] per [instrument]`

Return no more than 12 lines and no more than 110 words. Do not include addresses, section numbers, or citation markers.
```

---

### 17. Quorum

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: the quorum for governing-body and owner action, which is the first thing
  checked when testing whether a past approval was validly given.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report the quorum required for action by the governing body and for action by the owners.

## Scope

- Read the bylaws, operating agreement, or partnership agreement, and any quorum provision in the constitutional document.
- Report quorum only. Voting thresholds belong to the Ordinary Governing Body Vote and Owner Approval Threshold columns.
- Where a later amendment changes a quorum, report the requirement in the most recently dated document that addresses it.

## Rules

- Report the governing-body quorum and the owner quorum separately.
- Report the requirement as stated, for example `majority of directors then in office`, `two managers`, `holders of a majority of outstanding voting stock`.
- Report any class-specific or designated-member quorum requirement, which can allow one holder to block a meeting.
- Report any provision permitting action by written consent in lieu of a meeting, and the consent threshold, since it bypasses quorum entirely and is how most private-company approvals are actually given.

## Fallback rules

- Return `Not addressed` for either element where the documents state no quorum for it.
- Return `Incorporated terms` where quorum is stated to be set by a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict.

## Output format

`Governing body: [requirement]; Owners: [requirement]; Written consent: [threshold or "not permitted" or "Not addressed"]`

Return no more than 60 words. Do not include section numbers, quotations, or citation markers.
```

---

### 18. Ordinary Governing Body Vote

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: the vote required for ordinary action, which is the baseline that
  supermajority and protective provisions depart from.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report the vote required for ordinary action by the governing body.

## Scope

- Report the ordinary or default threshold only. Matters requiring a supermajority, unanimity, or class approval belong to the Supermajority and Protective Provisions column.
- Report action by the governing body, not by the owners.
- Where a later amendment changes the threshold, report the requirement in the most recently dated document that addresses it.

## Rules

- Report the threshold as stated, for example `majority of directors present at a meeting at which a quorum is present`, `majority of the total number of directors`, `unanimous written consent`.
- Distinguish a majority of those present from a majority of the whole body where the documents do. The difference decides whether an absent director defeats an action.
- Report the threshold for action by written consent separately where it differs.
- Report any tie-breaking or casting vote.

## Fallback rules

- Return `Not addressed` where the documents state no ordinary threshold.
- Return `Not applicable` where the entity has no multi-member governing body — for example a single managing member or a sole general partner acting alone.
- Return `Incorporated terms` where the threshold is stated to be set by a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict.

## Output format

`Meeting: [threshold]; Written consent: [threshold or "same"]`

Return no more than 50 words. Do not include section numbers, quotations, or citation markers.
```

---

### 19. Supermajority and Protective Provisions

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: `Protective Provisions Language`
- Purpose: every matter requiring more than an ordinary vote, or the approval of a
  specific class or holder. **Aggregated across entities, this is the approval
  list the closing checklist is built from.**

```markdown
## Established result

- Entity type: @Entity Type

## Task

List every matter the documents state requires a supermajority vote, unanimous approval, or the separate approval of a class, series, or designated owner or governing-body member.

## Scope

- Include class and series protective provisions, veto rights, negative covenants on corporate action, investor consent rights, and any requirement for the approval of a designated director or manager.
- Include matters requiring approval by a percentage above the ordinary threshold.
- Exclude the ordinary threshold itself.
- Exclude approval requirements imposed by statute rather than by the documents.
- Exclude consent rights held under a commercial contract or a debt facility.
- Where a later amendment changes the provisions, report those in the most recently dated document that addresses them.

## Rules

- Report each matter with the approving body or class and the threshold, in one clause each.
- Report the class or holder exactly as printed.
- Consolidate substantially similar matters. Report no more than ten, and where more exist, report the ten most consequential for a change of ownership and append ` and [N] further matters`.
- Give precedence to matters bearing on a sale of the entity: merger, sale of assets, liquidation, recapitalization, charter amendment, issuance of senior securities, incurrence of debt, and related-party transactions.
- Do not state whether this transaction requires any of these approvals, and do not state whether any has been obtained.

## Fallback rules

- Return exactly `None identified` where the documents establish no threshold above the ordinary one.
- Return `Incorporated terms` where protective provisions are stated to sit in a document not present in the unit, such as a stockholders or investor rights agreement.
- Return `Unable to determine` where provisions in the unit conflict, or are illegible.

## Output format

One line per matter:

`[Matter] — [approving class, holder, or body]: [threshold]`

Return no more than 10 lines and no more than 130 words. Do not include quotations, section numbers, or citation markers.
```

---

### 20. Protective Provisions Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Supermajority and Protective Provisions`
- Downstream: none
- Purpose: the exact text, so a partner can confirm the approval list before it
  goes on the closing checklist.

```markdown
## Established result

- Supermajority and protective provisions: @Supermajority and Protective Provisions

## Task

If Supermajority and Protective Provisions identified one or more matters, quote the operative provision text exactly as written.

If it returned `None identified`, return exactly `Not addressed`.

If it returned `Incorporated terms` or `Unable to determine`, quote whatever protective-provision language is legible in the unit and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Prioritize the language governing merger, sale of assets, liquidation, and charter amendment, since those are the provisions the transaction runs into.
- Quote the lead-in establishing whose approval is required, together with the enumerated matters. Where the enumeration exceeds 200 words, quote the lead-in and the matters bearing on a sale of the entity, replacing intervening items with `[...]`.
- Do not add analysis, and do not indicate whether this transaction triggers any provision.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 21. Owner Approval Threshold for Merger or Sale

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: `Approval Threshold Language`
- Purpose: the vote of owners required to approve a merger or a sale of
  substantially all assets. **Closing-critical**, and it decides whether minority
  owners can block the deal.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report the vote of owners the documents state is required to approve a merger, consolidation, or sale of all or substantially all of the entity's assets.

## Scope

- Read the constitutional document and the bylaws, operating agreement, or partnership agreement.
- Report thresholds the documents state. Where the documents are silent and the threshold would come from statute alone, say so under the fallback rules rather than supplying the statutory rule.
- Report separately for merger and for sale of substantially all assets where the documents set different thresholds.
- For a `Limited partnership`, report any limited-partner consent required in addition to general-partner action.
- Exclude governing-body approval, which belongs to the Ordinary Governing Body Vote and Supermajority columns.
- Where a later amendment changes the threshold, report the requirement in the most recently dated document that addresses it.

## Rules

- Report the threshold as stated, for example `holders of a majority of the outstanding shares of Common Stock, voting together as a single class`.
- **Report every separate class or series vote required.** A separate class vote is what allows a small holder to block a transaction, and it is the reason this column exists.
- Report whether the vote is of outstanding units or of units present, where the documents distinguish them.
- Report any requirement for a class vote by a specific series of preferred units or by a designated holder.
- Do not state whether this transaction has obtained or requires the approval, and do not state whether the threshold is achievable.

## Fallback rules

- Return `Not addressed — statutory default applies` where the documents contain no threshold for these actions. This is a real and common answer, and it routes the reviewer to the statute rather than to a missing document.
- Return `Incorporated terms` where the threshold is stated to be set by a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict.

## Output format

`Merger: [threshold]; Asset sale: [threshold or "same"]; Class votes: [each, or "none stated"]`

Return no more than 80 words. Do not include quotations, section numbers, or citation markers.
```

---

### 22. Approval Threshold Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Owner Approval Threshold for Merger or Sale`
- Downstream: none
- Purpose: the exact text of the approval requirement, which a partner reads before
  the approval mechanics are agreed with the seller.

```markdown
## Established result

- Owner approval threshold: @Owner Approval Threshold for Merger or Sale

## Task

If Owner Approval Threshold for Merger or Sale reported a threshold, quote the operative provision exactly as written.

If it returned `Not addressed — statutory default applies`, return exactly `Not addressed`.

If it returned `Incorporated terms` or `Unable to determine`, quote whatever approval language is legible in the unit and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the provision governing merger and asset sale, and every separate class-vote requirement, including the definition of any defined voting group the provision relies on where that definition appears in the unit.
- Where the combined text exceeds 200 words, quote the operative threshold and each class-vote requirement, replacing intervening text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether the threshold is met.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 23. Transfer Restrictions

- Native type: Classify
- Configured options, in UI order: `No restriction`, `Right of first refusal`, `Right of first offer`, `Governing body consent required`, `Owner consent required`, `Transfer prohibited`, `Multiple restrictions`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Transfer Restriction Detail`
- Purpose: whether existing ownership units can be transferred, and on what
  condition — which determines how the sellers can actually deliver the equity.

```markdown
## Task

Classify the restriction the documents impose on a transfer of existing ownership units by an owner. Choose exactly one configured option.

## Scope

- Analyze restrictions on transfers of **existing** units by their holders.
- **Exclude preemptive and participation rights over the issuance of new units.** Those are a different concept with a different consequence and belong to the Preemptive Rights column.
- Exclude drag-along and tag-along rights, which are reported in their own columns.
- Exclude restrictions arising under a securities-law legend alone.
- Exclude restrictions on transfers of assets, and restrictions binding the entity rather than its owners.
- Where a later amendment changes the restriction, classify on the most recently dated document that addresses it.

## Classification rules

- `Right of first refusal`: the entity or other owners may purchase on the terms of a received third-party offer.
- `Right of first offer`: the transferring owner must offer to the entity or other owners before approaching third parties.
- `Governing body consent required`: transfer requires the approval of the board, managers, or general partner.
- `Owner consent required`: transfer requires the approval of some or all other owners.
- `Transfer prohibited`: transfer is prohibited outright, subject only to permitted-transferee carve-outs.
- `Multiple restrictions`: two or more of the above apply cumulatively — for example a refusal right and a consent requirement. Report each in the Detail column.
- `No restriction`: the documents address transfer and impose no restriction.

A permitted-transferee carve-out for estate planning, affiliates, or family members does not change the classification. Report it in the Detail column.

## Fallback rules

- Use `Not addressed` where no document in the unit addresses transfer of units by owners.
- Use `Unable to determine` where provisions conflict, are illegible, or sit in a document not present in the unit. This is a Classify column, so it cannot return `Incorporated terms`; the incorporation is reported in Referenced but Not Produced.

## Output format

Return only the exact configured option and no explanation.
```

---

### 24. Transfer Restriction Detail

- Native type: Free Response
- Upstream: `@Transfer Restrictions`
- Downstream: none
- Purpose: the mechanics — who holds the right, notice periods, and permitted
  transferees — which set the timetable for delivering the equity at closing.

```markdown
## Established result

- Transfer restrictions: @Transfer Restrictions

## Task

If Transfer Restrictions is any value other than `No restriction`, `Not addressed`, or `Unable to determine`, report the mechanics of each restriction.

If Transfer Restrictions is `No restriction` or `Not addressed`, return exactly `Not applicable`.

If Transfer Restrictions is `Unable to determine`, return exactly `Unable to determine — upstream restriction is unresolved`.

## Rules

- Use the established result for routing, but confirm each mechanic against the documents in the current unit.
- For each restriction, report who holds the right, the notice period, and the period within which it must be exercised, as stated.
- Report the permitted transferees the documents exempt, in six words or fewer.
- Report any provision by which the right lapses or is waived, including a deemed waiver on silence.
- Report which classes or series the restriction applies to, where it does not apply to all.
- Do not state whether the restriction applies to this transaction, and do not state whether a waiver has been obtained.

## Output format

One line per restriction:

`[Restriction] — holder: [who]; notice: [period]; exercise window: [period]; permitted transferees: [brief or "none stated"]`

Return no more than 4 lines and no more than 90 words. Do not include quotations, section numbers, or citation markers.
```

---

### 25. Drag-Along

- Native type: Classify
- Configured options, in UI order: `Present`, `Present, in a document not in unit`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Drag-Along Conditions`, `Drag-Along Language`
- Purpose: whether a majority can compel minority owners to sell.

**Often the single most consequential corporate cell.** Without a drag, minority
holders must be persuaded individually, which changes the deal structure, the
timetable, and sometimes the price. Note that in most private companies the drag
sits in a stockholders or investor rights agreement rather than the charter, which
is why this column has a distinct state for it.

```markdown
## Task

Classify whether the documents give any owner or group the right to compel other owners to sell their units in a sale of the entity. Choose exactly one configured option.

## Scope

- Include drag-along rights, bring-along rights, and any obligation on owners to vote for, consent to, or participate in an approved sale.
- Include an obligation to execute transaction documents, give a release, or refrain from exercising appraisal or dissenters' rights in an approved sale, since those are the operative components of a drag.
- **Exclude tag-along and co-sale rights**, which entitle a minority owner to join a sale rather than compel them to sell. The direction is opposite and confusing them inverts the finding.
- Exclude rights of first refusal and first offer.
- Exclude the statutory power of a majority to approve a merger, which is not a drag right.
- Where a later amendment changes the right, classify on the most recently dated document that addresses it.

## Classification rules

- `Present`: a drag right is stated in a document present in this unit.
- `Present, in a document not in unit`: a document in the unit refers to a drag-along, bring-along, or sale-participation obligation in a stockholders, investor rights, voting, or similar agreement that is not present. **This is a coverage finding**, and the agreement is reported in Referenced but Not Produced.
- `Not addressed`: no document in the unit contains or refers to such a right.

## Fallback rules

- Use `Unable to determine` where a provision addresses compelled participation in terms too incomplete or illegible to tell whether a drag right exists, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 26. Drag-Along Conditions

- Native type: Free Response
- Upstream: `@Drag-Along`
- Downstream: none
- Purpose: the conditions on exercise, since a drag that cannot be exercised on
  this deal's terms is no drag at all.

```markdown
## Established result

- Drag-along: @Drag-Along

## Task

If Drag-Along is `Present`, report the conditions on which the right may be exercised.

If Drag-Along is `Present, in a document not in unit`, return `Not applicable — provision sits in [agreement name as referenced]`.

If Drag-Along is `Not addressed`, return exactly `Not applicable`.

If Drag-Along is `Unable to determine`, return exactly `Unable to determine — upstream classification is unresolved`.

## Rules

- Use the established result for routing, but confirm each condition against the documents in the current unit.
- Report who may exercise the right, identifying the class, series, or holder exactly as printed and the percentage required to trigger it.
- Report the conditions the documents attach, which commonly include: a minimum price or valuation; the same form of consideration for all owners; a requirement that the sale be to an unaffiliated third party; a cap on the representations, warranties, or indemnity obligations the dragged owner must give; a limit on escrow or holdback exposure; and a notice period.
- Report the transaction forms the right covers, for example a share sale, merger, or asset sale, since a drag limited to a share sale does not reach a merger.
- Do not state whether this transaction satisfies the conditions, and do not state whether the right is exercisable. That is a human column.

## Output format

`Exercisable by: [holder or class, percentage]; covers: [transaction forms]; conditions: [each, separated by semicolons]; notice: [period or "none stated"]`

Return no more than 100 words. Do not include quotations, section numbers, or citation markers.
```

---

### 27. Drag-Along Language

- Native type: Verbatim — **confirm the type returns true verbatim text and accepts `Not addressed`**
- Upstream: `@Drag-Along`
- Downstream: none
- Purpose: the exact text. A drag is read word by word before the deal is structured
  around it.

```markdown
## Established result

- Drag-along: @Drag-Along

## Task

If Drag-Along is `Present`, quote the drag-along provision exactly as written.

If Drag-Along is `Not addressed` or `Present, in a document not in unit`, return exactly `Not addressed`.

If Drag-Along is `Unable to determine`, quote whatever drag-along language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- Quote the trigger, the obligations imposed on the dragged owners, and the conditions and limits on exercise, including the definition of any defined sale term the provision relies on where that definition appears in the unit.
- Where the provision exceeds 250 words, quote the trigger and the conditions in full and replace subordinate procedural text with `[...]` between sentences.
- Do not add analysis, and do not indicate whether the right applies to this transaction.

## Output format

The quoted text, followed by the source tag. Return no more than 300 words.
```

---

### 28. Preemptive Rights

- Native type: Classify
- Configured options, in UI order: `Present`, `Present, in a document not in unit`, `Expressly denied`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether existing owners must be offered new units before they are issued
  to anyone else — which matters wherever the transaction involves a new issuance,
  a rollover, or a pre-closing reorganisation.

```markdown
## Task

Classify whether existing owners hold a right to participate in the issuance of new ownership units. Choose exactly one configured option.

## Scope

- Include preemptive rights, participation rights, and rights of first offer over **newly issued** units.
- **Exclude restrictions on transfers of existing units**, which belong to the Transfer Restrictions column. The two are routinely conflated and they have different consequences: one constrains the sellers, the other constrains the company.
- Exclude anti-dilution price adjustments, which adjust conversion terms rather than confer a right to buy.
- Exclude drag-along and tag-along rights.
- Where a later amendment changes the position, classify on the most recently dated document that addresses it.

## Classification rules

- `Present`: a document in the unit confers a right to participate in new issuances.
- `Present, in a document not in unit`: a document in the unit refers to preemptive or participation rights in an investor rights, stockholders, or similar agreement that is not present.
- `Expressly denied`: the documents state that owners have no preemptive rights. This is a common and useful charter provision, and it is a different answer from silence.

## Fallback rules

- Use `Not addressed` where the documents neither confer nor deny such rights.
- Use `Unable to determine` where the provision is illegible or incomplete, or where documents in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 29. Amendment Mechanics

- Native type: Free Response
- Upstream: `@Entity Type`
- Downstream: none
- Purpose: who can amend the governing documents and by what vote, which determines
  whether an unhelpful provision can be amended before closing and who has to agree.

```markdown
## Established result

- Entity type: @Entity Type

## Task

Report how the entity's governing documents may be amended.

## Scope

- Report the mechanics for amending the constitutional document and for amending the bylaws, operating agreement, or partnership agreement, separately.
- Include any class or series consent required for an amendment, and any provision requiring a higher threshold to amend specified sections.
- Exclude the procedure for filing an amendment with a public office.
- Where a later amendment changes the mechanics, report those in the most recently dated document that addresses them.

## Rules

- Report who may initiate or adopt each amendment and the vote required.
- Report separately where the governing body may amend one document unilaterally while owner approval is needed for the other. For a corporation, the board amending bylaws while stockholders must approve charter amendments is the common pattern and worth stating explicitly.
- Report any entrenched provision requiring a higher threshold than an ordinary amendment, and name the subject of that provision in six words or fewer.
- Report any class or series whose separate consent is required.
- Do not state whether any provision could or should be amended for this transaction.

## Fallback rules

- Return `Not addressed` for either element where the documents state no amendment mechanics.
- Return `Incorporated terms` where amendment mechanics are stated to sit in a document not present in the unit.
- Return `Unable to determine` where provisions in the unit conflict.

## Output format

`Constitutional document: [who — threshold]; Governing agreement: [who — threshold]; Entrenched provisions: [subject — threshold, or "none stated"]`

Return no more than 70 words. Do not include quotations, section numbers, or citation markers.
```

---

### 30. Subsidiaries and Affiliates Named

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: every related entity these documents name. **Matched against the org
  chart, entities named here but absent from the chart — and entities on the chart
  with no row in this table — are the finding.**

```markdown
## Task

List every other entity the documents in this unit name as a subsidiary, parent, owner, or affiliate of the subject entity.

## Scope

- Include entities named as subsidiaries, parents, holding companies, members, stockholders that are entities, general partners, and predecessors by merger or conversion.
- Include entities named in a schedule of subsidiaries or an organizational chart in the unit.
- Exclude the subject entity itself.
- Exclude individuals, commercial counterparties, lenders, advisers, registered agents, and transfer agents.
- Exclude entities named only as a permitted transferee category rather than by name.

## Rules

- Report each entity's name exactly as printed, with its stated relationship to the subject entity in four words or fewer.
- Report the ownership percentage only where a document states it. Do not derive it.
- Where a document states a jurisdiction for the named entity, include it.
- Do not state whether the group structure is complete, and do not reconcile against any other row.

## Fallback rules

- Return exactly `None named` where the documents name no related entity.

## Output format

One line per entity:

`[Exact legal name] — [relationship][; jurisdiction][; percentage as stated]`

Return no more than 20 lines and no more than 130 words. Do not include addresses, section numbers, or citation markers.
```

---

### 31. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Governing Documents in Unit`
- Downstream: none
- Purpose: name every governance document these documents refer to that is not in
  the unit. Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Governing Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to the subject entity that the documents in this unit refer to and that is not present in the unit.

## Scope

- Include charter amendments, restatements, bylaws amendments, and operating agreement amendments referenced but absent.
- Include stockholders, investor rights, voting, co-sale, and right of first refusal agreements referenced but absent.
- Include board and owner consents or resolutions referenced as authorizing an action, but not produced.
- Include equity incentive plans, schedules of subsidiaries, and exhibits referenced but not attached.
- Include good standing and foreign qualification certificates the documents state exist but that are absent.
- Exclude statutes, regulations, and published standards.
- Exclude documents relating to other entities, and commercial contracts.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the Stockholders Agreement`, report it as printed and add `(no date stated)`.
- Where a consent is referenced as authorizing a specific action, name the action in five words or fewer, because an issuance with no producible approval is the finding.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; authorizes: [action]]`

Return no more than 15 lines and no more than 120 words.
```

---

## Human-review fields

Separate table columns, never populated by Harvey.

| Column | Values |
| --- | --- |
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Operative version confirmed** | Yes / No, superseded / Chain incomplete |
| **Approval required for this transaction** | Governing body / Owners / Class vote / Both / None / Unclear |
| **Approval obtained** | Yes (reference) / No / Not yet required |
| **Drag exercisable on this deal** | Yes / No / Conditions unmet / Unclear |
| **Authority defect** | None / Ratification needed / Unresolved |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: entity name, jurisdiction, authorized
capital, approval thresholds, drag-along, standing.

**Reconciliation work that never belongs in a column.** Charter authorized classes
against the ledger and the certified cap table. Every issuance against a board
approval. The ownership chain against the org chart. Fully diluted counts. All of
it: export and reconcile in Excel against a certified source.

---

## Test set

- [ ] Corporation: charter, bylaws, good standing certificate, complete
- [ ] LLC: certificate of formation and operating agreement, member-managed
- [ ] LLC: manager-managed with an investor-designated manager
- [ ] Single-member LLC with percentage interests and no authorized unit count
- [ ] Limited partnership with GP management and LP consent rights
- [ ] Restated charter reciting an original incorporation date twenty years earlier
- [ ] Restated charter plus a later amendment that conflicts with it
- [ ] Charter amendment signed but bearing no filing stamp
- [ ] Unsigned draft charter amendment
- [ ] Certified copy from the Secretary of State
- [ ] Formation instrument naming an incorporator and initial directors, with no later confirmation
- [ ] Consent recording a director resignation and a replacement appointment
- [ ] Entity with a name change by charter amendment
- [ ] Entity resulting from a conversion from a corporation to an LLC
- [ ] Good standing certificate dated more than 90 days before the as-of date
- [ ] Delinquent or suspended standing certificate
- [ ] Unit with no standing certificate at all
- [ ] Charter expressly denying preemptive rights
- [ ] Charter with blank-check preferred authorized
- [ ] Charter with Series A protective provisions and a separate class vote on merger
- [ ] Documents referring to a stockholders agreement that is not in the unit
- [ ] Unit containing a right of first refusal and a board consent requirement together
- [ ] Unit containing a tag-along but no drag-along, to confirm the direction is not inverted
- [ ] Unit misfiled with a parent entity's charter included
- [ ] Compilation: one PDF of good standing certificates for several entities
- [ ] Bylaws absent, charter present
- [ ] Foreign entity with a non-US legal form

Then test the dependencies directly: change `Entity Type` on a row from
`Corporation` to `Limited liability company` and confirm the nine dependent
columns re-run to the LLC reading. Change `Drag-Along` from `Present` to
`Not addressed` and confirm `Drag-Along Conditions` and `Drag-Along Language` move
to their non-applicable states, and that a locked cell does not silently retain
the old value.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
| --- | --- | --- | --- | --- | --- | --- |
| | | v1.0 | Initial draft | — | — | — |
