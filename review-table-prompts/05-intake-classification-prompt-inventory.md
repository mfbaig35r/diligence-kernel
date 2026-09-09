# Prompt Inventory — Intake Classification

Platform-ready Harvey Review Table. **Build this first.** It runs over the whole
data room before any workstream table exists, and everything downstream depends on
it.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`. This file records only what is
specific to this table.

## Table

- Matter: `[Project name]`
- Platform: Harvey Review Tables (UI)
- Project: `[Matter] - Intake` — a single project holding every produced document
- Review unit: **one file**
- Grouping used: **no.** Intake is deliberately per-file, because its job includes
  finding the files that should not be single rows at all
- Intended reviewers and downstream use: whoever owns intake; routes every
  document to a Vault project and a workstream table, and seeds the coverage
  register
- Inventory version: v1.0

### What this table is for

It extracts almost no substance. Its job is to decide what every other table
sees, and classification is the only step in the whole workflow where an error is
cheap to fix and expensive to inherit. A misfiled document costs a minute at
intake and can cost the whole finding at synthesis.

Three of its columns exist purely to catch problems that would otherwise
propagate silently: `Compilation Flag` finds files that are twenty instruments in
one PDF and cannot be a row anywhere; `Completeness` separates a genuine
`Unable to determine` downstream from a prompt defect; and `Routing Disposition`
keeps administrative clutter out of the substantive tables.

### One design decision to make before building

**`Document Type` may not fit in a Classify column.** The taxonomy vocabulary is
roughly 180 values across 18 workstreams, and a Classify column's options are
configured per column, not per row — so routing on `@Workstream` narrows what the
prompt tells Harvey to choose from, but every option still has to be configured.

This inventory drafts `Document Type` as **Free Response** with the vocabulary
supplied in the prompt. That trades native validation for feasibility. Post-export
validation in Excel against the vocabulary list catches drift, and it is a
one-formula check.

If the Classify option ceiling in your tenant turns out to be comfortably above
180, switch the column to Classify and keep the prompt as drafted. That test is in
the shared pre-run verification.

### On the Workstream / Document Type sequence

The taxonomy wants Workstream derived independently of Document Type so that
mismatches surface as a signal. This build routes `Document Type` on
`@Workstream` instead, because a 180-value open choice is materially less reliable
than a 15-value one.

**The mismatch signal is preserved by a different mechanism.** `Document Type`
returns `Unclassified` when no value in the assigned workstream's vocabulary fits,
and names what the document appears to be. A document routed to the wrong
workstream therefore comes back `Unclassified` rather than being force-fitted to
the nearest available label. Filter on `Unclassified` and you have the mismatch
list — the same signal, from a more reliable column.

`Document Role` runs before both, because a document's function is readable
independently of its type and it is the most robust of the three.

## Assumptions to confirm before running

1. Every produced file is in the intake project, including files you expect to
   discard. A file excluded before intake is invisible to the coverage register.
2. Files were renamed on ingest per the naming convention, and the production log
   is being maintained. Neither is enforced by the product.
3. Compilations have **not** necessarily been split yet. This table finds them.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

20 Harvey columns plus 4 human columns. Comfortably within any plausible cap.

---

## Table Instructions

- Version: v1.0

About 2,400 characters. Note the departure from every other table: the review unit
is a single file, so the shared rule about reporting from the latest document in
the unit does not apply and is absent.

```markdown
## Matter

[Project name]. Buyer-side legal diligence on the target group listed below. This table classifies and routes every document in the data room.

One row is one file. Analyze each file as a standalone document. Do not use other rows, file names, or outside knowledge of the parties.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Target group

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer, [Seller or parent legal name] is the selling shareholder, and [Adviser names] are advisers. None is a target entity unless a column expressly asks about them.

## Shared rules

- Classify what the document is. Do not analyze what it says beyond what a column expressly asks for.
- Use entity and individual names exactly as printed in the document; do not shorten, expand, or correct them.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written when the document gives less precision.
- Report only what the document states. Do not infer from a file name, a folder name, or a document's position in a set.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Function and form (no upstream)
  Document Role
  Workstream
  Compilation Flag
  Completeness
  Language
  Execution Status
  Signature Evidence
  Governing Law

Stage 2 — Type, routed on workstream
  Workstream ──→ Document Type
                 Secondary Workstream

Stage 3 — Parties and dates, routed on role and type
  Document Type ──→ Subject Entity
                    Counterparty
                    Document Date
                    Amends or Issued Under
  Document Role ──→ Operative Date
  Counterparty  ──→ Counterparty Type

Stage 4 — Triage and coverage
  Document Type + Compilation Flag + Completeness ──→ Routing Disposition
  Document Type ──→ Referenced but Not Produced
  Document Type ──→ Duplicate Indicators
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Document Role | Classify | — | Operative Date | v1.0 | draft |
| 2 | Workstream | Classify | — | Document Type; Secondary Workstream | v1.0 | draft |
| 3 | Document Type | Free Response | @Workstream | Subject Entity; Counterparty; Document Date; Amends or Issued Under; Routing Disposition; Referenced but Not Produced; Duplicate Indicators | v1.0 | draft |
| 4 | Secondary Workstream | Classify | @Workstream | — | v1.1 | draft |
| 5 | Subject Entity | Free Response | @Document Type | — | v1.0 | draft |
| 6 | Counterparty | Free Response | @Document Type | Counterparty Type | v1.0 | draft |
| 7 | Counterparty Type | Classify | @Counterparty | — | v1.0 | draft |
| 8 | Execution Status | Classify | — | — | v1.0 | draft |
| 9 | Signature Evidence | Classify | — | — | v1.0 | draft |
| 10 | Document Date | Date | @Document Type | — | v1.0 | draft |
| 11 | Operative Date | Date | @Document Role | — | v1.0 | draft |
| 12 | Amends or Issued Under | Free Response | @Document Type | — | v1.0 | draft |
| 13 | Compilation Flag | Classify | — | Routing Disposition | v1.0 | draft |
| 14 | Completeness | Classify | — | Routing Disposition | v1.0 | draft |
| 15 | Language | Classify | — | — | v1.0 | draft |
| 16 | Governing Law | Free Response | — | — | v1.0 | draft |
| 17 | Duplicate Indicators | Free Response | @Document Type | — | v1.0 | draft |
| 18 | Referenced but Not Produced | Free Response | @Document Type | — | v1.0 | draft |
| 19 | Routing Disposition | Classify | @Document Type; @Compilation Flag; @Completeness | — | v1.0 | draft |
| 20 | Confidentiality Markings | Free Response | — | — | v1.0 | draft |

---

## Column records

### 1. Document Role

- Native type: Classify
- Configured options, in UI order: `Instrument`, `Record`, `Correspondence`, `Analysis`, `Filing`, `Administrative`, `Unable to determine`
- Upstream: none
- Downstream: `Operative Date`
- Purpose: state what kind of thing the document is, which decides what should be
  extracted from it and which table it can share a row set with.

**This is the axis people skip and it is the one that decides everything
downstream.** Mixing roles in one Review Table is the most common reason a grid
comes back useless. An instrument is read for what it obligates; a record for what
it asserts and as of when; correspondence for the chronology; analysis for scope
and limitation as much as conclusion; a filing for status and effectiveness.

```markdown
## Task

Classify the function this document performs. Choose exactly one configured option.

## Options

- `Instrument` — creates or transfers rights and obligations
- `Record` — evidences a state of affairs at a point in time
- `Correspondence` — communicates something between parties
- `Analysis` — a third party's opinion or assessment
- `Filing` — a submission to, or a certificate issued by, a public body
- `Administrative` — a document with no diligence content of its own
- `Unable to determine`

## Classification rules

Classify on function, not on subject matter or title.

- `Instrument`: the document's operative effect is to bind parties or move rights. Agreements, leases, security agreements, assignments, charters, plans, policies of insurance, and settlement agreements.
- `Record`: the document reports facts as at a date. Cap tables, stock ledgers, employee censuses, loss runs, organizational charts, schedules of subsidiaries, tax returns, and compliance certificates. **An as-of date is what makes a record usable**, which is why the Operative Date column treats records differently.
- `Correspondence`: the document's purpose is to communicate. Demand letters, breach notices, regulator inquiries, audit correspondence, and transmittal letters with substantive content.
- `Analysis`: a third party assesses or opines. Phase I and II environmental assessments, 409A valuations, penetration test reports, audit opinions, tax opinions, actuarial reports, and title reports.
- `Filing`: submitted to or issued by a public body. UCC-1 financing statements, Form 5500s, trademark and patent registrations, good standing certificates, and filed charter amendments.
- `Administrative`: no diligence content. Blank pages, folder cover sheets, index or file listings, transmittal emails with nothing substantive, and data room download receipts.

Where a document performs two functions, classify on its operative effect. A filed charter amendment is a `Filing` because its effectiveness depends on filing. A signed but unfiled amendment is an `Instrument`.

A board consent is an `Instrument`: it takes an action rather than reporting one. Minutes of a meeting are a `Record`: they report what happened.

An internal policy that binds employees is an `Instrument`. A policy adopted purely as a compliance artifact with no binding effect is a `Record`.

## Fallback rules

- Use `Unable to determine` where the document is too fragmentary, illegible, or truncated to tell what it does. Do not use it for a document whose function is clear but whose subject matter is unfamiliar.

## Output format

Return only the exact configured option and no explanation.
```

---

### 2. Workstream

- Native type: Classify
- Configured options, in UI order: `Corporate and Entity Structure`, `Capitalization and Securities`, `Commercial Contracts`, `Vendor and Supplier`, `IP and Technology`, `Privacy and Cybersecurity`, `Employment and HR`, `Benefits and Pensions`, `Real Estate`, `Environmental`, `Litigation and Disputes`, `Regulatory and Licenses`, `Compliance`, `Tax`, `Insurance`, `Debt and Financing`, `Related-Party`, `Deal Documents`, `Unable to determine`
- Upstream: none
- Downstream: `Document Type`, `Secondary Workstream`
- Purpose: decide which reviewer owns the document and therefore which Vault
  project it goes into.

```markdown
## Task

Classify which diligence workstream owns this document. Choose exactly one configured option.

## Scope

- Assign the **primary** workstream, meaning the one whose reviewer needs the document most. A secondary assignment is reported in the next column.
- Classify on the document's subject matter, not on which party produced it or where in the data room it sat.

## Classification rules

- `Corporate and Entity Structure`: formation, charter, bylaws, operating agreements, board and owner consents and minutes, good standing, org charts, mergers and conversions.
- `Capitalization and Securities`: securities instruments, grants, warrants, SAFEs, notes, cap tables, stock ledgers, equity plans, valuations.
- `Commercial Contracts`: agreements under which the target sells or delivers to customers, resellers, distributors, and partners.
- `Vendor and Supplier`: agreements under which the target buys goods or services.
- `IP and Technology`: registrations, applications, assignments, licences in and out, open source and software reports, joint development.
- `Privacy and Cybersecurity`: data processing agreements, privacy policies, subprocessor lists, incident and breach records, security assessments and certifications.
- `Employment and HR`: employment, consulting, and contractor agreements, restrictive covenants, separation agreements, handbooks and HR policies, censuses, collective agreements.
- `Benefits and Pensions`: benefit plan documents, summary plan descriptions, Form 5500s, bonus and deferred compensation plans, pension valuations.
- `Real Estate`: leases, subleases, deeds, title reports, surveys, easements, mortgages on real property, estoppels, property tax.
- `Environmental`: permits, environmental site assessments, remediation, notices of violation, waste and emissions records.
- `Litigation and Disputes`: pleadings, orders, judgments, settlements, demand letters, arbitration, subpoenas, litigation holds, investigations.
- `Regulatory and Licenses`: licences, permits, registrations, regulatory filings, regulator correspondence, examination reports, consent orders.
- `Compliance`: codes of conduct, compliance policies, risk assessments, internal investigations, hotline logs, sanctions screening, third-party diligence.
- `Tax`: returns, provisions, audit correspondence, tax sharing agreements, elections, transfer pricing, tax opinions.
- `Insurance`: policies, binders, certificates of insurance, loss runs, claim notices, coverage correspondence.
- `Debt and Financing`: credit agreements, notes, guaranties, security agreements, UCC filings, intercreditor and subordination, payoff letters, lien releases.
- `Related-Party`: arrangements between the target and an affiliate, founder, officer, director, or a person or entity they control.
- `Deal Documents`: letters of intent, term sheets, draft purchase agreements, disclosure schedules, structure charts, exclusivity and deal confidentiality agreements.

Apply these precedence rules where more than one fits:

1. `Related-Party` takes precedence over the subject-matter workstream whenever the documents state that a party is an affiliate, founder, officer, director, or an entity one of them controls. An affiliate lease is `Related-Party`, not `Real Estate`.
2. `Deal Documents` takes precedence for anything generated by this transaction.
3. A mortgage or security interest over real property granted to a lender is `Debt and Financing`. A mortgage produced as evidence of title to a property is `Real Estate`.
4. A data processing agreement is `Privacy and Cybersecurity`, with the commercial workstream secondary.
5. Where the target sells to the counterparty, use `Commercial Contracts`. Where it buys, use `Vendor and Supplier`. A mutual NDA with no direction is `Commercial Contracts`.

## Fallback rules

- Use `Unable to determine` where the subject matter cannot be identified from the document, or where it spans workstreams so evenly that no primary owner can be chosen. Both need a human, and this cell is how they get one.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Document Type

- Native type: **Free Response** — see the design note above; switch to Classify only if the option ceiling permits ~180 values
- Upstream: `@Workstream`
- Downstream: seven columns — see the index
- Purpose: identify the instrument, which decides which Review Table the document
  belongs to and which extraction schema applies.

About 6,450 characters — the longest prompt in the set, because the controlled
vocabulary is the column's option list and has to be stated somewhere. That is
comfortably under the ~10,000 limit but above the 6,000 working target, so it has
less headroom than any other column for the rules testing will add. If it needs to
grow, drop the vocabulary blocks for workstreams this matter has no documents in.

```markdown
## Established result

- Workstream: @Workstream

Choose a value from that workstream's vocabulary below. Confirm the type against the document itself; do not select on the workstream alone.

## Task

Classify this document using exactly one value from the vocabulary for its assigned workstream.

## Vocabulary by workstream

- **Corporate and Entity Structure**: `Certificate of Incorporation` `Articles of Organization` `Bylaws` `LLC Operating Agreement` `Partnership Agreement` `Board Minutes` `Board Written Consent` `Stockholder Minutes` `Stockholder Written Consent` `Stock Ledger` `Subsidiary Register` `Organizational Chart` `Good Standing Certificate` `Foreign Qualification` `Merger Certificate` `Charter Amendment`
- **Capitalization and Securities**: `Capitalization Table` `Stock Purchase Agreement` `Subscription Agreement` `Equity Incentive Plan` `Option Grant Agreement` `Warrant` `SAFE` `Convertible Note` `Shareholders Agreement` `Investor Rights Agreement` `Right of First Refusal Agreement` `Voting Agreement` `409A Valuation` `Restricted Stock Agreement`
- **Commercial Contracts**: `Master Services Agreement` `Statement of Work` `Order Form` `Customer Agreement` `Reseller Agreement` `Distributor Agreement` `Partnership Agreement (Commercial)` `Amendment` `Side Letter` `Non-Disclosure Agreement` `Data Processing Agreement` `Service Level Agreement` `Letter of Intent (Commercial)`
- **Vendor and Supplier**: `Supply Agreement` `SaaS Agreement` `Cloud Services Agreement` `Outsourcing Agreement` `Purchase Order Terms` `Manufacturing Agreement` `Logistics Agreement` `Professional Services Agreement`
- **IP and Technology**: `Patent Registration` `Patent Application` `Trademark Registration` `Trademark Application` `Copyright Registration` `Domain Registration` `IP Assignment` `Inbound License` `Outbound License` `Employee Invention Assignment` `Contractor IP Assignment` `Open Source Report` `Software Bill of Materials` `Joint Development Agreement` `Trade Secret Policy`
- **Privacy and Cybersecurity**: `Privacy Policy` `Data Processing Agreement` `Subprocessor List` `Incident Report` `Breach Notification` `Security Assessment` `Penetration Test Report` `SOC 2 Report` `ISO Certification` `Information Security Policy` `Data Map`
- **Employment and HR**: `Employment Agreement` `Offer Letter` `Consulting Agreement` `Contractor Agreement` `Employee Census` `Restrictive Covenant Agreement` `Separation Agreement` `Employee Handbook` `HR Policy` `Collective Bargaining Agreement` `Works Council Agreement` `Retention Agreement` `Change in Control Agreement`
- **Benefits and Pensions**: `Plan Document` `Summary Plan Description` `Form 5500` `Bonus Plan` `Deferred Compensation Plan` `Pension Valuation` `Benefits Broker Report` `COBRA Notice`
- **Real Estate**: `Lease` `Sublease` `Lease Amendment` `Lease Guaranty` `Estoppel Certificate` `Subordination Non-Disturbance Agreement` `Deed` `Title Report` `Survey` `Easement` `Mortgage` `Deed of Trust` `Property Tax Bill`
- **Environmental**: `Environmental Permit` `Phase I Environmental Site Assessment` `Phase II Environmental Site Assessment` `Remediation Agreement` `Notice of Violation` `Waste Manifest` `Emissions Report`
- **Litigation and Disputes**: `Complaint` `Answer` `Motion` `Court Order` `Judgment` `Settlement Agreement` `Demand Letter` `Arbitration Award` `Subpoena` `Litigation Hold Notice` `Investigation Notice` `Tolling Agreement`
- **Regulatory and Licenses**: `License` `Permit` `Registration` `Regulatory Filing` `Regulator Correspondence` `Examination Report` `Consent Order` `No-Action Letter` `Change of Control Application`
- **Compliance**: `Compliance Policy` `Code of Conduct` `Risk Assessment` `Internal Investigation File` `Hotline Log` `Third-Party Diligence File` `Training Record` `Sanctions Screening Report` `Audit Report`
- **Tax**: `Tax Return` `Tax Provision` `Tax Audit Correspondence` `Tax Sharing Agreement` `Tax Election` `Transfer Pricing Study` `Sales Tax Filing` `Payroll Tax Filing` `Tax Opinion`
- **Insurance**: `Insurance Policy` `Insurance Binder` `Certificate of Insurance` `Loss Run` `Claim Notice` `Coverage Denial Letter`
- **Debt and Financing**: `Credit Agreement` `Promissory Note` `Security Agreement` `Guaranty` `UCC-1 Financing Statement` `Intercreditor Agreement` `Subordination Agreement` `Payoff Letter` `Lien Release` `Mortgage (Financing)` `Pledge Agreement` `Compliance Certificate`
- **Related-Party**: `Intercompany Agreement` `Affiliate Services Agreement` `Affiliate Lease` `Founder Loan` `Related-Party Note` `Management Services Agreement`
- **Deal Documents**: `Letter of Intent` `Term Sheet` `Purchase Agreement Draft` `Disclosure Schedule` `Structure Chart` `Exclusivity Agreement` `Confidentiality Agreement (Deal)`

## Classification rules

- Return the value **exactly as written above**, including capitalization and any parenthetical. Downstream tables filter on these strings.
- Classify on the operative document, not the title. A document titled a services agreement that sets framework terms for future orders is a `Master Services Agreement`.
- **An amendment classifies as `Amendment`, not as the type of the document it amends.** The base agreement is named in the Amends or Issued Under column. `Charter Amendment` and `Lease Amendment` are the two exceptions, because those vocabularies provide a specific value.
- Classify a draft or unsigned document by what it is. An unsigned MSA is a `Master Services Agreement`; its status is reported in Execution Status.
- Where two workstreams share a value, such as `Data Processing Agreement`, use the value from the assigned workstream's block.

## Fallback rules

- Return `Unclassified` where no value in the assigned workstream's vocabulary fits, followed by an em dash and what the document appears to be in eight words or fewer. **Do not force-fit to the nearest available label.**

An `Unclassified` result usually means one of three things, all of which need a human: the workstream assignment is wrong, the vocabulary needs extending for this matter, or the document is something nobody anticipated. Filter on `Unclassified` and work those rows by hand.

- Return `Unable to determine` where the document is too fragmentary or illegible to identify at all.

## Output format

Return the exact vocabulary value and nothing else, or `Unclassified — [description]`. Do not add the workstream, explanation, or citation markers.
```

---

### 4. Secondary Workstream

- Native type: Classify
- Configured options, in UI order: `Corporate and Entity Structure`, `Capitalization and Securities`, `Commercial Contracts`, `Vendor and Supplier`, `IP and Technology`, `Privacy and Cybersecurity`, `Employment and HR`, `Benefits and Pensions`, `Real Estate`, `Environmental`, `Litigation and Disputes`, `Regulatory and Licenses`, `Compliance`, `Tax`, `Insurance`, `Debt and Financing`, `Related-Party`, `Deal Documents`, `None`, `Unable to determine`
- Upstream: `@Workstream`
- Downstream: none
- Purpose: identify a genuinely dual document, which under one-project-per-workstream
  must be uploaded to both projects.

**Duplication in Vault is cheaper than a document invisible to the reviewer who
needs it.** Record the duplicate in the production log so it is not later mistaken
for a second instrument.

```markdown
## Established result

- Primary workstream: @Workstream

## Task

Identify a second workstream whose reviewer genuinely needs this document. Choose exactly one configured option, or `None`.

## Scope

- Report a second workstream only where a reviewer in that workstream would reach a wrong conclusion without this document. The test is need, not topical overlap.
- Do not report the primary workstream again.

## Classification rules

Use a secondary workstream in cases of this kind:

- A data processing agreement: primary `Privacy and Cybersecurity`, secondary `Commercial Contracts` or `Vendor and Supplier`.
- An affiliate lease: primary `Related-Party`, secondary `Real Estate`.
- An intercompany services agreement: primary `Related-Party`, secondary `Commercial Contracts`.
- A mortgage or deed of trust securing a facility: primary `Debt and Financing`, secondary `Real Estate`.
- An employee invention assignment: primary `IP and Technology`, secondary `Employment and HR`.
- A change in control agreement with an executive: primary `Employment and HR`, secondary `Capitalization and Securities` where it addresses equity acceleration.
- A settlement agreement with ongoing commercial obligations: primary `Litigation and Disputes`, secondary `Commercial Contracts`.
- An insurance certificate produced to satisfy a contract requirement: primary `Insurance`, secondary the workstream of the contract.
- A tax sharing agreement: primary `Tax`, secondary `Corporate and Entity Structure`.

Return `None` where the document belongs to one workstream only. **Most documents do**, and over-assigning secondaries defeats the purpose by duplicating half the data room.

## Fallback rules

- Use `Unable to determine` where the document plainly spans workstreams but the second cannot be identified from its face.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Subject Entity

- Native type: Free Response
- Upstream: `@Document Type`
- Downstream: none
- Purpose: which target-group entity the document relates to. **Critical in a
  multi-entity group**, and the join key for reconciling every workstream table to
  the corporate chart.

```markdown
## Established result

- Document type: @Document Type

## Task

Identify the target-group entity that is the subject of, or a party to, this document.

## Scope

- Use the target group list in the Table Instructions to determine which named entity is a target entity.
- Use the document type to locate the subject: for a formation or governance document, the entity formed or governed; for an agreement, the contracting entity; for a record, the entity whose affairs it reports; for a filing, the entity whose status is filed or certified; for correspondence, the entity addressed or discussed; for analysis, the entity or asset assessed.
- Exclude parents, owners, affiliates, and subsidiaries merely mentioned, named as beneficiaries, or listed as permitted affiliate users.
- Exclude counterparties, advisers, the buyer, and the selling shareholder.

## Rules

- Report the entity name exactly as printed in the document, including the entity suffix, even where it differs from the Table Instructions list.
- Where the printed name differs from a listed name, append ` (variant of [listed name])`.
- Where more than one target entity is a subject or party, list each on its own line. Where more than four are, list the first four and end with `and [N] further target entities`.
- Where a document relates to a property, asset, or individual rather than an entity, report the target entity that holds or employs it.
- Where no target entity is a subject or party, return `Not applicable — no target entity` and name the parties in six words or fewer. **This surfaces documents produced by mistake or belonging to another matter.**

## Fallback rules

- Return `Unable to determine` where the document names no entity, or the names are illegible.

## Output format

`[Exact entity name]` per line, with any qualifier appended. Return no more than 40 words. Do not include addresses or citation markers.
```

---

### 6. Counterparty

- Native type: Free Response
- Upstream: `@Document Type`
- Downstream: `Counterparty Type`
- Purpose: the non-target party by exact legal name, which is the join key for
  revenue concentration, consent requests, and conflict checks.

```markdown
## Established result

- Document type: @Document Type

## Task

Identify the non-target party or parties to this document.

## Scope

- Report every party other than a target-group entity listed in the Table Instructions.
- For correspondence, report the sender where the target is the recipient, and the recipient where the target is the sender.
- For a filing or an official certificate, report the issuing body.
- For analysis, report the preparer.
- Exclude affiliates of the counterparty merely permitted to receive services, guarantors, third-party beneficiaries, and named individuals signing on behalf of a party.

## Rules

- Report each name exactly as printed, including the entity suffix. Do not correct spelling or expand abbreviations.
- Where a party is described by a trade name and the legal name appears elsewhere in the document, report the legal name and append ` (t/a [trade name])`.
- Where there are more than four non-target parties, list the first four and end with `and [N] further parties`.
- Return `Not applicable` where the document is internal to the target group with no external party, such as a board consent, an internal policy, or a cap table.

## Fallback rules

- Return `Unable to determine` where the document has an evident external party whose name cannot be read.

## Output format

`[Exact legal name]` per line, with any qualifier appended. Return no more than 40 words. Do not include addresses, roles, or citation markers.
```

---

### 7. Counterparty Type

- Native type: Classify
- Configured options, in UI order: `Customer`, `Vendor or supplier`, `Reseller or distributor`, `Partner or collaborator`, `Employee or contractor`, `Investor`, `Lender`, `Landlord`, `Insurer`, `Regulator or court`, `Adviser or professional`, `Affiliate or related party`, `Other`, `Not applicable`, `Unable to determine`
- Upstream: `@Counterparty`
- Downstream: none
- Purpose: filter the whole data room by relationship, which is what turns intake
  into a usable map before any workstream table exists.

```markdown
## Established result

- Counterparty: @Counterparty

Use this to identify the party being classified. Determine its role from the document itself.

## Task

Classify the counterparty's relationship to the target group. Choose exactly one configured option.

## Classification rules

- `Customer`: pays the target for goods, services, or a licence.
- `Vendor or supplier`: is paid by the target for goods, services, or a licence.
- `Reseller or distributor`: resells, distributes, or sublicenses the target's offering.
- `Partner or collaborator`: joint development, marketing, or delivery without one party simply paying the other.
- `Employee or contractor`: an individual providing services to the target.
- `Investor`: holds or is subscribing for securities of a target entity.
- `Lender`: provides debt, or holds a security interest or guarantee.
- `Landlord`: grants the target an interest in real property.
- `Insurer`: an insurance carrier, underwriter, or broker.
- `Regulator or court`: a public body, agency, court, or tribunal.
- `Adviser or professional`: accountants, valuers, environmental consultants, counsel, and other assessors.
- `Affiliate or related party`: stated to be under common ownership or control with a target entity, or a founder, officer, director, or an entity one of them controls.

Classify on the payment and delivery direction in the operative terms, not on the document's title.

`Affiliate or related party` takes precedence over every other option where the relationship is stated in the document.

Return `Not applicable` where the Counterparty column returned `Not applicable`.

## Fallback rules

- Use `Unable to determine` where the document does not show the relationship, or where the direction conflicts within the document.
- Do not default an unidentified entity to `Other`. Use `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Execution Status

- Native type: Classify
- Configured options, in UI order: `Executed`, `Partially executed`, `Unsigned draft`, `Form or template`, `Filed or issued`, `Certified copy`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: what the document proves about its own completion.

**This field alone justifies the intake pass.** Data rooms are full of unsigned
drafts, and a finding built on one is a finding built on nothing. Every workstream
table must be filtered on it before conclusions are drawn — a standing
instruction, not a one-time check.

```markdown
## Task

Classify the visible completion status of this document. Choose exactly one configured option.

## Scope

- Evaluate only signature blocks, electronic-signature markers, conformed signatures, filing stamps, file numbers, and certification language visible in this document.
- Include signature pages and counterpart pages belonging to this document.
- Exclude signature and filing evidence appearing on exhibits, attachments, or referenced documents; that evidence describes those documents, not this one.
- Exclude notary, witness, and attestation blocks from the party count.

## Classification rules

Apply the first rule that fits.

1. `Certified copy`: the document bears certification language from a public office or a corporate secretary certifying it as a true copy.
2. `Filed or issued`: the document bears a government filing stamp, a file number with a filing date, or is a certificate issued by a public office. Use this even where the document also carries signatures.
3. `Form or template`: the document is an unpopulated form, containing bracketed placeholders, blank party names, or blank commercial terms.
4. `Unsigned draft`: the document provides party signature blocks and none bears a signature marker. This includes drafts with typed names, blank signature lines, and a "signature page follows" reference with no signed page attached.
5. `Partially executed`: at least one party signature block bears a signature marker and at least one does not.
6. `Executed`: every party signature block the document provides bears a signature marker.
7. `Not applicable`: the document provides no signature block and bears no filing or certification evidence — a cap table, an organizational chart, a report, a census, or correspondence.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated effective date is not a signature marker.

## Fallback rules

- Use `Unable to determine` only where signature or filing evidence exists but cannot be read, where a signature page is referenced but missing, or where the document conflicts with itself about execution.
- Do not treat a `duly executed` recital, a stated effective date, or a transmittal email describing the document as signed as evidence that signatures were completed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 9. Signature Evidence

- Native type: Classify
- Configured options, in UI order: `Wet ink`, `Electronic signature platform`, `Conformed signature`, `Typed name only`, `Signature block blank`, `Mixed`, `Not applicable`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: how the document was signed, which bears on authenticity and on
  whether a purported signature is a signature at all.

Kept separate from `Execution Status` because they answer different questions:
whether it was signed, and how. A conformed closing set and a wet-ink original are
both `Executed`, but only one is evidence of anything if authenticity is disputed.

```markdown
## Task

Classify the form of signature evidence on this document. Choose exactly one configured option.

## Scope

- Evaluate party signature blocks only. Exclude notary, witness, and attestation blocks.
- Exclude signature evidence on exhibits and attachments.

## Classification rules

Apply the first rule that fits.

1. `Not applicable`: the document provides no party signature block.
2. `Signature block blank`: every party block is provided and empty.
3. `Mixed`: different party blocks bear different forms of signature evidence.
4. `Typed name only`: a name is typed in the signature block with no handwritten signature, platform block, or `/s/` marker. **This is not a signature**, and the cell exists to make that visible.
5. `Conformed signature`: signatures are shown as `/s/` followed by a name, as in a conformed closing set.
6. `Electronic signature platform`: the document bears a signing-platform certificate, envelope identifier, audit stamp, or platform-applied signature block.
7. `Wet ink`: the document bears a handwritten signature image.

## Fallback rules

- Use `Unable to determine` where the signature area is present but too poorly scanned or too illegible to tell which form it takes.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Document Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Document Type`
- Downstream: none
- Purpose: the date the document bears for itself, which orders the data room
  chronologically and is the first input to every amendment chain.

```markdown
## Established result

- Document type: @Document Type

Use the document type to select the applicable rule below. Confirm the date against the document itself.

## Task

Identify the date this document bears for itself.

## Date-selection hierarchy

### Agreements, instruments, plans, and policies

1. Use the date stated in the preamble or on the cover.
2. If none, use the date of the last party signature.
3. If neither, use a date the document states for itself elsewhere.

### Filings and official certificates

1. Use the filing stamp date, or the issue date printed by the office.
2. If none, use the date the instrument states for itself.

### Records

1. Use the as-of date the record states.
2. If none, use the date the record was prepared or printed, where stated.

### Correspondence

Use the date of the letter, notice, or message.

### Analysis and reports

Use the report date on the cover or signature page, not the date of the site visit or fieldwork.

## Excluded dates

- File name and document metadata dates
- Notarization, transmittal, download, retrieval, and scan dates
- Dates belonging only to a referenced document
- The effective or commencement date where it differs from the document's own date; that belongs to Operative Date
- A period covered by a return or report, as distinct from the document's date

## Rules

- Report the date even where it equals a date in another column. A value the document states is never replaced by a fallback state.
- Where the document bears two dates for itself and neither is a signature date, report the earlier and append nothing; the discrepancy is visible against Operative Date.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 11. Operative Date

- Native type: Date — confirm the type accepts `Not stated` and `Not applicable`
- Upstream: `@Document Role`
- Downstream: none
- Purpose: the date that determines what the document is evidence of — the
  effective date for an instrument, the as-of date for a record.

**A record without an as-of date is unusable**, and the taxonomy's own universal
metadata list included as-of date while its intake table dropped it. This column
restores it, routed on role so that one column serves both concepts.

```markdown
## Established result

- Document role: @Document Role

Use the role to select which date concept applies. Confirm the date against the document itself.

## Task

Identify the date that determines what this document is evidence of.

## Rules by role

### Instrument

Report the effective, commencement, or operative date the document states. Where the document states no effective date separately from its own date, report the document's own date. **Do not return a fallback state because the two dates are the same** — a value the document states is always reported.

### Record

Report the as-of date the record speaks as of: the balance date of a cap table, the census date, the period end of a ledger, the certificate date of a good standing certificate. Where the record states no as-of date, return `Not stated`. **That is a finding**, not a gap in the extraction.

### Filing

Report the effective date of the filing where the document states one distinct from the filing date. Otherwise report the filing date.

### Correspondence

Report any date by which action is required, or on which a stated event took effect. Where the letter merely communicates, return `Not applicable`.

### Analysis

Report the date as of which the assessment speaks, where distinct from the report date — for example a valuation date or a site inspection date. Otherwise return `Not applicable`.

### Administrative

Return `Not applicable`.

## Excluded dates

- Expiry, maturity, and termination dates
- Renewal notice deadlines
- File name and metadata dates
- Dates belonging only to a referenced document

## Output format

`YYYY-MM-DD`, or one of the exact fallback values above. Preserve partial precision as printed.
```

---

### 12. Amends or Issued Under

- Native type: Free Response
- Upstream: `@Document Type`
- Downstream: none
- Purpose: name the base instrument, which is how a document family is assembled
  without a document-family feature.

```markdown
## Established result

- Document type: @Document Type

## Task

Identify the document this one amends, restates, supplements, or is issued under.

## Scope

- Include the base agreement of an amendment, restatement, side letter, statement of work, or order form.
- Include the master agreement, plan, charter, or facility a document is issued or granted under.
- Include a prior agreement this document expressly supersedes or replaces.
- Exclude documents referenced only as background, definitions sources, or for context.
- Exclude statutes, regulations, and published standards.

## Rules

- Name the base document **exactly as this document names it**, including its date where stated. Downstream matching depends on the string, so do not normalize or correct it.
- Where this document is an amendment, state its number as the document numbers itself, for example `Amendment No. 2 to [name]`. Do not infer a number.
- Where this document is issued under more than one instrument — a statement of work under an MSA that is itself governed by a framework agreement — name the immediate parent and append ` (under [further parent])`.
- Return `Standalone` where the document is a base instrument, or is not issued under and does not amend anything.

## Fallback rules

- Return `Unable to determine` where the document plainly amends or is issued under something that it does not name identifiably.

## Output format

`[Base document name] — [YYYY-MM-DD or "date not stated"]`, or `Standalone`. Return no more than 30 words. Do not include section numbers or citation markers.
```

---

### 13. Compilation Flag

- Native type: Classify
- Configured options, in UI order: `Single document`, `Multiple instruments — same type`, `Multiple instruments — mixed types`, `Multiple entities or subjects`, `Unable to determine`
- Upstream: none
- Downstream: `Routing Disposition`
- Purpose: find files that cannot be a single row anywhere.

**A single PDF holding twenty executed agreements is one file and twenty
instruments.** A Review Table cannot return twenty rows from one file, and one row
averaging twenty contracts is worse than nothing. Splitting is manual, tedious,
and not optional — this column is what tells you where to do it.

```markdown
## Task

Classify whether this file contains one document or several. Choose exactly one configured option.

## Scope

- Count separately titled, separately dated, or separately executed documents.
- Treat exhibits, schedules, annexes, and attachments to a document as part of that document, not as separate documents.
- Treat a counterpart signature page as part of the document it belongs to.
- Treat an amendment bound together with its base agreement as **two** documents.

## Classification rules

- `Multiple entities or subjects`: the file contains records or certificates for more than one entity, property, or individual — for example good standing certificates for eight entities, or a bundle of employment agreements. Use this option in preference to the others where it applies, because the split has to be by subject.
- `Multiple instruments — mixed types`: two or more documents of different types, for example a lease bound with an estoppel certificate and an SNDA.
- `Multiple instruments — same type`: two or more documents of the same type relating to one subject, for example a base agreement with three amendments.
- `Single document`: one document, with or without attachments.

Where the file contains multiple documents, state the count in the evidence field rather than in the cell.

## Fallback rules

- Use `Unable to determine` where the file is too fragmentary or poorly scanned to tell whether it holds one document or several.

## Output format

Return only the exact configured option and no explanation.
```

---

### 14. Completeness

- Native type: Classify
- Configured options, in UI order: `Complete on its face`, `Pages missing`, `Exhibits or schedules missing`, `Signature page missing`, `Illegible in part`, `Fragment only`, `Unable to determine`
- Upstream: none
- Downstream: `Routing Disposition`
- Purpose: distinguish a document that genuinely cannot be read from a prompt that
  is failing.

Without this column, every downstream `Unable to determine` is ambiguous between
"the document is damaged" and "the prompt is wrong," and the difference decides
whether you re-request the document or fix the prompt.

```markdown
## Task

Classify the physical completeness and legibility of this file. Choose exactly one configured option.

## Scope

- Assess the document as produced. Do not assess whether its terms are commercially complete.
- Exclude the absence of a referenced separate document, which belongs to Referenced but Not Produced. This column is about pages missing from **this** file.

## Classification rules

Apply the first rule that fits.

1. `Fragment only`: the file contains a portion of a document with no beginning or no end, such as pages 14 to 22 of an agreement.
2. `Pages missing`: internal pages are absent, evidenced by a break in page numbering, a broken sentence across a page boundary, or a reference to a section that is not present.
3. `Signature page missing`: the document is complete except that a referenced signature or counterpart page is absent.
4. `Exhibits or schedules missing`: exhibits, schedules, or annexes are listed or referenced as attached and are not present in the file.
5. `Illegible in part`: pages are present but partly unreadable through poor scanning, redaction, handwriting, skew, or truncation.
6. `Complete on its face`: page numbering is continuous where present, every referenced attachment is present, and the text is legible throughout.

Where more than one condition applies, use the earliest applicable rule above, and note the others in the evidence field.

Redaction counts as `Illegible in part`. Note in the evidence field that the illegibility is redaction rather than scan quality, because the remedy differs.

## Fallback rules

- Use `Unable to determine` where the file cannot be opened or rendered enough to assess it.

## Output format

Return only the exact configured option and no explanation.
```

---

### 15. Language

- Native type: Classify
- Configured options, in UI order: `English`, `English with non-English portions`, `Non-English`, `Non-English with English translation`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: route to local counsel rather than analysing non-US documents by
  US-law analogue.

```markdown
## Task

Classify the language of this document. Choose exactly one configured option.

## Rules

- Where the document is not wholly in English, state the language or languages in the evidence field.
- `English with non-English portions`: the operative document is in English with a non-English exhibit, schedule, or annex.
- `Non-English with English translation`: both a non-English original and an English translation are present in this file. Note in the evidence field whether the translation is certified, since an uncertified translation is not evidence of the original's terms.
- Do not attempt to analyze or translate a non-English document. Identify the language and stop.

## Fallback rules

- Use `Unable to determine` where the text cannot be read well enough to identify the language.

## Output format

Return only the exact configured option and no explanation.
```

---

### 16. Governing Law

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the choice-of-law jurisdiction, which routes local counsel and flags
  foreign-law documents early.

```markdown
## Task

Identify the governing law stated in this document.

## Rules

- Report the jurisdiction chosen to govern, as stated.
- Report the jurisdiction only. Do not report the forum, venue, arbitral seat, or service-of-process provisions.
- Where the document chooses different law for different subject matter, report each with the subject in three words or fewer.
- For a filing or official certificate, report the jurisdiction of the issuing office.
- For a court or tribunal document, report the jurisdiction of the court.

## Fallback rules

- Return `Not addressed` where the document contains no choice of law.
- Return `Not applicable` where the document type could not carry one, such as a cap table, an organizational chart, or a report.
- Return `Incorporated terms` where governing law is stated to be set by a document not present in this file.

## Output format

`[Jurisdiction]`, for example `Delaware` or `England and Wales`. Return no more than 20 words.
```

---

### 17. Duplicate Indicators

- Native type: Free Response
- Upstream: `@Document Type`
- Downstream: none
- Purpose: surface probable duplicates, so the same instrument is not reviewed
  three times and counted three times.

**Scope discipline.** Harvey analyses one file at a time and cannot compare this
row to other rows. This column therefore reports the **identifying facts** a
reviewer sorts on to find duplicates. It does not identify duplicates itself.

```markdown
## Established result

- Document type: @Document Type

## Task

Report the identifying facts that would allow this document to be matched against another copy of the same instrument.

## Rules

- Report, in order: the document's own date, the parties in the order printed, the principal commercial figure or subject where the document states one, and the total page count.
- For the principal figure, use whatever the document type makes distinctive: the contract value, the premises address, the principal amount, the number of units, the case number, the licence number, or the policy number. Report it as printed.
- Report any version, draft, or revision marking printed on the document, including a `DRAFT`, `EXECUTION VERSION`, or `CONFORMED COPY` legend, and any version number in a footer.
- Report any indication that this file is a copy of another, such as a stamp reading `COPY`, a certification that it is a true copy, or a duplicate Bates or production number.
- **Do not state whether this document is a duplicate of anything.** You cannot see other rows. Report the facts and let the reviewer sort.

## Output format

`[YYYY-MM-DD] | [parties] | [principal figure or subject] | [N] pages | [version markings or "none"]`

Return no more than 40 words. Do not include file names or citation markers.
```

---

### 18. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Document Type`
- Downstream: none
- Purpose: name every document this one refers to that is not in this file.

This is the column the whole coverage register is built from. Run across the entire
data room, it produces **the gaps nobody asked for because nobody knew they
existed**, which is where the real exposure hides.

```markdown
## Established result

- Document type: @Document Type

## Task

List every document this document refers to that is not present in this file.

## Scope

- Include exhibits, schedules, annexes, and appendices referenced but not attached.
- Include amendments, restatements, side letters, statements of work, and order forms referenced but absent.
- Include base agreements, master agreements, plans, charters, and facilities the document is issued under.
- Include board and owner consents or resolutions referenced as authorizing an action.
- Include policies, standard terms, service level documents, codes of conduct, and terms hosted at a URL that the document incorporates.
- Include certificates, valuations, opinions, and reports the document states exist or relies on.
- Exclude documents referenced only as background with no bearing on the parties' obligations or on the document's effect.
- Exclude statutes, regulations, published standards, and case citations.

## Rules

- Name each document **as this document names it**, with its date where stated. The reviewer will request it using this name.
- Where a reference is generic, for example `the applicable order form` or `the Plan`, report it as printed and add `(generic reference)`.
- Where a document is incorporated by URL, report its name and add `(hosted terms)`.
- Where a consent is referenced as authorizing a specific action, name the action in five words or fewer. **An action with no producible approval is the finding.**
- Do not report a document as absent where it is attached to this file.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every document referenced is present in this file.

Note: `None identified` is a positive finding for this column, not a fallback state. It means the search was run.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; authorizes: [action]]`

Return no more than 15 lines and no more than 130 words.
```

---

### 19. Routing Disposition

- Native type: Classify
- Configured options, in UI order: `Route to workstream table`, `Route to two projects`, `Split before review`, `Re-request from seller`, `Route to local counsel`, `No substantive content`, `Human triage required`
- Upstream: `@Document Type`, `@Compilation Flag`, `@Completeness`
- Downstream: none
- Purpose: one filterable cell saying what happens to this file next. This is the
  column that turns intake from a classification exercise into a work queue.

```markdown
## Established results

- Document type: @Document Type
- Compilation flag: @Compilation Flag
- Completeness: @Completeness

Use these results for routing. Confirm the disposition against the document itself.

## Task

Classify what must happen to this file before it can be reviewed. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits. The order is deliberate: a file needing several actions is routed to the one that must happen first.

1. `Split before review`: Compilation Flag is `Multiple instruments — same type`, `Multiple instruments — mixed types`, or `Multiple entities or subjects`. The file cannot be a row anywhere until it is split, and no other action can precede that.
2. `Human triage required`: Document Type is `Unclassified` or `Unable to determine`, or Compilation Flag is `Unable to determine`. Nothing can be routed until a person decides what the document is.
3. `Re-request from seller`: Completeness is `Fragment only`, `Pages missing`, `Signature page missing`, or `Exhibits or schedules missing`. The document as produced cannot support a conclusion, so it goes on the supplemental request list.
4. `No substantive content`: the document is administrative — a blank page, a folder cover sheet, an index or file listing, a transmittal with no substantive content, or a download receipt. **Keep these rows.** They are logged as produced and excluded from review, which is a different thing from being missing.
5. `Route to local counsel`: the document is governed by non-US law, or the Language column indicates it is not in English. Route rather than analyze by US-law analogue.
6. `Route to two projects`: the Secondary Workstream column identifies a second workstream whose reviewer needs the document.
7. `Route to workstream table`: none of the above applies. The document is complete, single, classified, and belongs to one workstream.

`Illegible in part` under Completeness does not by itself force a re-request. Where the illegible portion is not the operative text, route normally and note it in the evidence field. Where it is, use `Re-request from seller`.

## Fallback rules

- Where two dispositions genuinely compete and the order above does not resolve it, use `Human triage required` rather than guessing.

## Output format

Return only the exact configured option and no explanation.
```

---

### 20. Confidentiality Markings

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: flag documents whose handling is restricted, including privilege and
  clean-team markings. Handling errors on these are the kind that end engagements.

```markdown
## Task

Report any confidentiality, privilege, or handling marking printed on this document.

## Scope

- Include privilege markings such as `Privileged and Confidential`, `Attorney-Client Privileged`, `Attorney Work Product`, and `Prepared at the Direction of Counsel`.
- Include competitively sensitive handling markings such as `Clean Team Only`, `Outside Counsel Only`, or `Antitrust Sensitive`.
- Include confidentiality legends, protective order legends, and `Subject to FRE 408` or settlement-privilege markings.
- Include any marking restricting the document to named recipients.
- Include Bates numbers and production stamps, reporting the range as printed.
- Exclude ordinary contractual confidentiality clauses in the body of an agreement. This column is about markings on the face of the document governing how the file itself may be handled.

## Rules

- Report each marking exactly as printed.
- Report where it appears — cover page, header, footer, or watermark — in three words or fewer.
- **Do not assess whether privilege applies, whether it has been waived, or whether the marking is correct.** Report the marking and stop; a privileged document reaching the wrong reviewer is a handling problem, and this cell exists to prevent it.

## Fallback rules

- Return exactly `None marked` where the document bears no such marking.

## Output format

One line per marking:

`[Marking as printed] — [location]`

Return no more than 5 lines and no more than 50 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| **Classification confirmed** | Blank / Confirmed / Reclassified |
| Reviewed by | Initials |
| **Disposition actioned** | Blank / Done / In progress / Blocked |
| Notes | Free text |

**Do not skip the classification column.** Classification is where an error is
cheapest to catch and most expensive to inherit.

### The four filters to work first

Intake is not read row by row. It is filtered, in this order:

1. `Routing Disposition` = `Split before review` — nothing downstream can start
   on these files, and splitting has the longest lead time
2. `Routing Disposition` = `Human triage required`, and `Document Type` =
   `Unclassified` — the misclassification list
3. `Routing Disposition` = `Re-request from seller` — straight onto the
   supplemental request list
4. `Classification confirmed` blank, for the high-value document types — the
   rows nobody has checked

Then `Referenced but Not Produced`, across every row, which seeds the coverage
register.

---

## Test set

- [ ] Executed agreement, complete, single workstream
- [ ] Unsigned draft agreement with typed names in the signature blocks
- [ ] Conformed closing-set copy with `/s/` signatures
- [ ] Unpopulated template with bracketed placeholders
- [ ] Filed charter amendment bearing a filing stamp
- [ ] Signed but unfiled charter amendment
- [ ] Good standing certificate for one entity
- [ ] One PDF containing good standing certificates for eight entities
- [ ] One PDF containing a base agreement and three amendments
- [ ] One PDF containing a lease, an estoppel, and an SNDA
- [ ] Amendment produced alone, naming its base agreement
- [ ] Statement of work naming its master agreement
- [ ] Agreement with exhibits listed as attached and not present
- [ ] Fragment: pages 14 to 22 of an agreement, no beginning or end
- [ ] Heavily redacted agreement
- [ ] Poorly scanned, skewed document
- [ ] Cap table with an as-of date
- [ ] Cap table with no as-of date
- [ ] Board written consent
- [ ] Minutes of a board meeting
- [ ] Affiliate lease between a target entity and a founder-controlled entity
- [ ] Data processing agreement as an exhibit to an MSA
- [ ] Standalone data processing agreement
- [ ] Mortgage granted to a lender over target real property
- [ ] Document with no target entity as a party
- [ ] Non-English agreement with no translation
- [ ] Non-English agreement with an uncertified English translation
- [ ] Document marked `Privileged and Confidential`
- [ ] Document marked `Clean Team Only`
- [ ] Blank page, and a data room index listing
- [ ] Phase I environmental assessment
- [ ] A document type not in any vocabulary block, to confirm `Unclassified` fires

Then test the dependencies: change `Workstream` on a row from `Real Estate` to
`Related-Party` and confirm `Document Type` re-runs against the new vocabulary
rather than retaining `Lease`. Set `Compilation Flag` to
`Multiple entities or subjects` and confirm `Routing Disposition` moves to
`Split before review` ahead of every other disposition.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
| 2026-09-08 | Secondary Workstream | v1.0 → v1.1 | Enumerated the configured options in full. The bullet previously read "the same 18 workstream values, plus `None`, plus `Unable to determine`", which names a vocabulary without spelling it out. Any reader taking it literally — including a parser — sees two options, and a run then presents that truncated list to the model as the complete set. Observed: the column returned `None` on 9 of 10 documents on two different models, because it could not return anything else. | Truncated controlled vocabulary | Secondary Workstream on every row of Table 05; nothing downstream, the column has no dependents | None; no prompt text changed |
