# Prompt Inventory — IP: Technology and Open Source

Table 12 of the POC. Third of three IP tables. Rows are third-party reports, so
the role is Analysis and the reading is different from the other two.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - IP`
- Review unit: **one report or assessment** — the report itself, its appendices
  and component inventories, any management response, and any remediation
  confirmation produced with it
- Grouping used: **yes**, typically 1–4 documents per unit
- Row count: usually 3 to 15 per matter
- Intended reviewers and downstream use: IP, technology, and corporate/M&A teams;
  feeds the open source remediation list, the technology risk section of the
  issues list, and the coverage register
- Inventory version: v1.0

### Reading an Analysis document

The taxonomy's own rule: **analysis is read for scope and limitation as much as
for conclusion.** A Phase I that excluded a parcel is a different document from one
that did not, and an open source scan that covered one repository out of nine is a
different document from one that covered all nine.

So this table front-loads scope and limitations, and treats the conclusion as one
column among several rather than the point. `Scope and Method`,
`Product or Codebase Covered`, and `Limitations and Data Gaps` are the columns that
tell a reviewer whether the findings mean anything.

The second question, and the one that catches people: **can the buyer rely on this
report at all?** A seller-commissioned assessment addressed to the seller, with a
no-third-party-reliance clause, has very little diligence value. `Reliance and
Confidentiality` is where that surfaces.

## Assumptions to confirm before running

1. One row is one report. A bundle containing a pen test and an open source scan
   is two rows, and a single file containing both is a compilation to be split.
2. Software licence agreements are **not** rows here. Inbound licences of
   third-party components are agreements, reviewed in the Contracts tables.
3. This table reports what the reports say. **It does not itself analyse a
   codebase, an SBOM's component list, or a licence's terms.** Where an SBOM lists
   4,000 components, this table reports what the report concludes about them, not
   a component-by-component review. Reading an SBOM is a specialist task performed
   directly and, per `review-tables.md` §5, is not attempted as a column.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

16 Harvey columns plus 7 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side technology and intellectual property diligence on the target group listed below. This table reviews third-party and internal reports about the target's technology.

One row is one report or assessment: the report itself, its appendices and component inventories, any management response, and any remediation confirmation produced with it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Target group

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the target's technology.
- **Report what the report states, and report its scope and limitations alongside its conclusions.** A conclusion reported without its scope is misleading.
- **Do not perform the analysis the report performs.** Do not assess licence compatibility, evaluate a vulnerability, judge architecture, or reach a conclusion the report did not reach. Report the preparer's findings and the preparer's caveats.
- Report figures and counts only as the report states them. Do not total, recount, or estimate.
- Use entity, product, and component names exactly as printed. Do not correct or normalize a component or licence name.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Report Type
  Preparer
  Product or Codebase Covered

Stage 2 — Status and standing
  Documents in Unit ──→ Assessment Date
                        Referenced but Not Produced
  Preparer          ──→ Reliance and Confidentiality

Stage 3 — Scope, routed on report type
  Report Type ──→ Scope and Method
                  Copyleft Components Identified
                  Licence Obligations Stated
                  Open Findings and Severity
                  AI and Model Rights

Stage 4 — Findings and caveats
  Distribution Status
  Third-Party Components Critical to Product
  Escrow and Continuity Arrangements
  Remediation Status
  Limitations and Data Gaps
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Assessment Date; Referenced but Not Produced | v1.0 | draft |
| 2 | Report Type | Classify | — | Scope and Method; Copyleft Components Identified; Licence Obligations Stated; Open Findings and Severity; AI and Model Rights | v1.0 | draft |
| 3 | Preparer | Free Response | — | Reliance and Confidentiality | v1.0 | draft |
| 4 | Assessment Date | Date | @Documents in Unit | — | v1.0 | draft |
| 5 | Reliance and Confidentiality | Free Response | @Preparer | — | v1.0 | draft |
| 6 | Product or Codebase Covered | Free Response | — | — | v1.0 | draft |
| 7 | Scope and Method | Free Response | @Report Type | — | v1.0 | draft |
| 8 | Limitations and Data Gaps | Free Response | — | — | v1.0 | draft |
| 9 | Copyleft Components Identified | Free Response | @Report Type | — | v1.0 | draft |
| 10 | Distribution Status | Classify | — | — | v1.0 | draft |
| 11 | Licence Obligations Stated | Free Response | @Report Type | — | v1.0 | draft |
| 12 | Third-Party Components Critical to Product | Free Response | — | — | v1.0 | draft |
| 13 | AI and Model Rights | Free Response | @Report Type | — | v1.0 | draft |
| 14 | Open Findings and Severity | Free Response | @Report Type | — | v1.0 | draft |
| 15 | Escrow and Continuity Arrangements | Free Response | — | — | v1.0 | draft |
| 16 | Remediation Status | Free Response | — | — | v1.0 | draft |
| 17 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

17 columns — one more than estimated, because `Remediation Status` and
`Open Findings and Severity` had to be separated. A finding and whether it was
fixed are different facts with different review consequences.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Assessment Date`, `Referenced but Not Produced`
- Purpose: inventory the report and its supporting material.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the report, its executive summary if separate, its appendices and component inventories, any management or engineering response, any remediation or retest confirmation, and the engagement letter or statement of work if produced.
- Treat appendices bound into the report as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Report`, `Executive summary`, `Component inventory`, `Appendix`, `Management response`, `Remediation confirmation`, `Retest report`, `Engagement letter`, or `Other`.
- **Where a component inventory or SBOM is present, state its stated component count in the evidence field** rather than counting it yourself.
- Where a document is a different report than the subject of this row, still list it and append ` [different report: [name]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 8 lines and no more than 80 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Report Type

- Native type: Classify
- Configured options, in UI order: `Open source composition analysis`, `Software bill of materials`, `Penetration test`, `Security assessment or audit`, `Code quality or technical debt review`, `Architecture description`, `AI or model documentation`, `Vulnerability scan`, `Third-party certification report`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: five columns
- Purpose: route the substantive columns, since an open source scan and a
  penetration test have nothing in common beyond both being reports about
  software.

```markdown
## Task

Classify the kind of report this review unit contains. Choose exactly one configured option.

## Classification rules

- `Open source composition analysis`: identifies third-party and open source components in a codebase and their licences. **The licence analysis is what distinguishes it** from a vulnerability scan over the same components.
- `Software bill of materials`: a structured inventory of components, typically without an analytical conclusion. Where a document is an inventory with licence analysis attached, classify as `Open source composition analysis`.
- `Penetration test`: active testing for exploitable weaknesses, reporting findings by severity.
- `Vulnerability scan`: automated scanning against known vulnerability databases, without active exploitation. Distinguished from a penetration test because the assurance is much weaker.
- `Security assessment or audit`: a controls or process review against a framework or standard, rather than technical testing.
- `Third-party certification report`: SOC 2, ISO 27001, or an equivalent attestation issued by an auditor. Note in the evidence field whether it is Type 1 or Type 2, since Type 1 tests design only and not operation.
- `Code quality or technical debt review`: an assessment of maintainability, test coverage, or engineering practice.
- `Architecture description`: a description of the system, its dependencies, and its hosting, whether prepared internally or externally.
- `AI or model documentation`: documentation of a model, its training data, its provenance, or its evaluation.

Classify on the operative content, not the title. A document titled Security Report that lists open source components and their licences is `Open source composition analysis`.

## Fallback rules

- Use `Other` where the document is a report about the technology that none of the options describes.
- Use `Unable to determine` where the document is too fragmentary to identify what it assessed.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Preparer

- Native type: Free Response
- Upstream: none
- Downstream: `Reliance and Confidentiality`
- Purpose: who prepared the report and for whom, which is the first input to
  whether it can be relied on.

```markdown
## Task

State the preparer of this report and the party it was prepared for.

## Rules

- Report the preparing firm or organisation exactly as printed, and any named individual with their stated credentials or certifications.
- **State whether the preparer is external or internal to the target group**, using the entity list in the Table Instructions. An internally prepared assessment is not third-party assurance, and it is common for architecture descriptions and code reviews.
- **Report the addressee as printed** — the party the report is addressed to or stated to be prepared for. Where it is the seller, a target entity, an investor, a lender, or the buyer, say which.
- Report any engagement reference, statement of work, or scope letter identified.
- Where the report is a certification or attestation, report the auditor and any accreditation stated.
- Where the report is stated to have been commissioned for an earlier transaction or financing, report that, since it bears on both currency and reliance.

## Fallback rules

- Return `Not stated` where the report identifies no preparer. **For an external assurance document this is a serious gap** — an unattributed report is not assurance at all.
- Return `Unable to determine` where the preparer is illegible.

## Output format

`[Preparer as printed] — [external | internal]; prepared for: [addressee as printed or "not stated"]`

Return no more than 45 words.
```

---

### 4. Assessment Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: when the work was done, which determines whether the report describes
  the product the buyer is acquiring.

**A twelve-month-old open source scan describes a codebase that no longer exists.**
Currency matters more here than in almost any other table, because the subject
changes weekly.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to distinguish the report from any retest or remediation document. Confirm the date against the documents.

## Task

Identify the date as of which this report describes the technology.

## Date-selection hierarchy

1. Use the date of the assessment, scan, or testing window the report states, taking the end of the window where a range is given.
2. If none, use the date of the codebase snapshot, commit, or version the report states it examined.
3. If neither, use the report's own issue or publication date.

## Excluded dates

- The date of a retest or remediation confirmation, which is reported in Remediation Status
- The date of the engagement letter
- The date of a management response
- File name and metadata dates, and printing, download, and scan dates
- A copyright year in a footer

## Rules

- **Report the assessment date, not the report date, where they differ.** A report issued in March describing a January scan speaks as of January.
- Where the report states the specific version, release, or commit examined, report it in the evidence field. That is the most precise statement of what was assessed.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where the gap exceeds six months, append ` [over 6 months old]`. Where it exceeds twelve, append ` [over 12 months old]`.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 5. Reliance and Confidentiality

- Native type: Free Response
- Upstream: `@Preparer`
- Downstream: none
- Purpose: whether the buyer can rely on this report.

**A seller-commissioned report the buyer cannot rely on has almost no diligence
value.** It may still be useful as a signal, but it cannot support a conclusion,
and the buyer has no recourse against the preparer if it is wrong. Reliance is
frequently obtainable for a fee, which makes this a live negotiation item rather
than a dead end.

```markdown
## Established result

- Preparer: @Preparer

## Task

Report what the report says about who may rely on it and how it may be used.

## Include where expressly stated

- Any reliance clause naming who may rely on the report
- **Any statement that no third party may rely on it**, or that it is for the addressee's sole use and benefit
- Any provision for reliance to be extended, and any reliance letter referenced
- Any limitation or exclusion of the preparer's liability, and any cap on it
- Any confidentiality or non-disclosure restriction on the report itself
- Any restriction on disclosing the report to a purchaser, lender, or regulator
- Any statement that the report may not be quoted or referred to
- Any disclaimer of warranty as to completeness or accuracy

## Rules

- **Report the no-third-party-reliance position explicitly where present.** It is the single most consequential thing in this column and it is usually in small print at the front or back.
- Report any liability cap as stated, with the amount. A cap at the fee level means the preparer's exposure is nominal.
- Report whether a reliance letter is referenced as available or already issued, and to whom.
- **Report any restriction that would prevent the report being shared with the buyer or its lenders.** Disclosing a report in breach of its own confidentiality terms is a real problem and it is easy to overlook.
- Report the terms as stated. **Do not assess whether a reliance exclusion or liability cap would be effective.**

## Fallback rules

- Return `Not addressed` where the report says nothing about reliance or use restrictions. **Silence is not permission**, and the reviewer should treat an unaddressed reliance position as unresolved rather than open.
- Return `Not applicable` where the report was prepared internally by a target entity, so no third-party reliance question arises. Note that an internal report is also not third-party assurance.
- Return `Unable to determine` where the relevant text is illegible.

## Output format

`Reliance: [named parties | sole addressee | expressly excluded | Not addressed]; liability cap: [amount or "none stated"]; reliance letter: [available | issued to [party] | not referenced]; disclosure restriction: [brief or "none stated"]`

Return no more than 70 words.
```

---

### 6. Product or Codebase Covered

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what was assessed. **The gap between what was assessed and what the
  business actually sells is the most common way a clean report misleads.**

```markdown
## Task

Report the products, systems, repositories, or environments this report covers.

## Include where expressly stated

- The named products, applications, or services assessed
- The repositories, modules, or codebases assessed, and their stated version, release, branch, or commit
- The environments assessed: production, staging, development, or a specific cloud account
- The stated proportion or count of the estate covered, for example three of nine repositories
- Any product, system, or repository expressly excluded
- The hosting or infrastructure covered, where the report identifies it
- Whether third-party or vendor-hosted components were included

## Rules

- **Report the excluded items as prominently as the included ones.** An exclusion is what turns a clean report into a partial one, and preparers usually state exclusions clearly because their own liability depends on it.
- Report the version or commit assessed where stated, since it is the only precise statement of what the findings apply to.
- **Where the report covers part of the estate, report the covered and total counts as stated** and append ` [partial coverage]`. Do not calculate a percentage.
- Report product names exactly as printed, since they are the join key to the commercial and revenue analysis.
- Do not assess whether the coverage is adequate, and do not compare it to the target's product range. That comparison is human work against the commercial workstream.

## Fallback rules

- Return `Not stated` where the report does not identify what it covered. **For any assessment this is a fundamental defect** — findings without a stated subject cannot be relied on for anything.
- Return `Unable to determine` where the coverage statement is illegible or internally inconsistent.

## Output format

`Covered: [products or repositories, with versions]; environments: [as stated]; excluded: [as stated or "none stated"]`, with any bracketed flag appended.

Return no more than 80 words.
```

---

### 7. Scope and Method

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: how the work was done, which determines how much the conclusion is
  worth.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the scope of work and the method the preparer states it used.

## Rules by report type

- `Open source composition analysis`, `Software bill of materials`: the scanning tool named, whether the scan was of source code or of binaries, whether it covered transitive dependencies, whether snippet or partial-match detection was used, and any stated confidence or match threshold. **Whether transitive dependencies were scanned is the key scope question**, since most copyleft exposure arrives indirectly.
- `Penetration test`: whether testing was black box, grey box, or white box; whether it was authenticated or unauthenticated; whether it covered network, application, API, mobile, or social engineering; the testing window; and whether exploitation was attempted or only identified.
- `Vulnerability scan`: the tool and the vulnerability database used, and whether findings were manually validated. **Unvalidated scan output contains false positives** and the report usually says so.
- `Security assessment or audit`, `Third-party certification report`: the framework or standard applied, the trust services criteria or control domains covered, the observation period, and whether design only or design and operating effectiveness were tested.
- `Code quality or technical debt review`: the metrics and tools used, and whether review was automated, manual, or both.
- `Architecture description`, `AI or model documentation`: the basis of the description — interviews, documentation review, or inspection — and whether any of it was independently verified.

## Rules

- Report the method as stated. **Do not assess whether the method was appropriate or sufficient.**
- **Report any statement that the assessment was point-in-time**, which almost all are.
- Report the standard or framework by its printed name and version.

## Fallback rules

- Return `Not stated` where the report describes no method. This is a significant weakness for any report offered as assurance.
- Return `Unable to determine` where the method description is illegible or inconsistent.

## Output format

`Method: [as stated]; tools or standard: [as printed]; depth: [as stated]; point in time: [yes | Not addressed]`

Return no more than 80 words.
```

---

### 8. Limitations and Data Gaps

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the preparer said it could not do or did not check.

**The taxonomy's rule applied literally: a report that excluded something is a
different document from one that did not.** Preparers state their limitations
carefully because their own liability turns on them, which makes this one of the
most reliable columns in the table.

```markdown
## Task

Report the limitations, caveats, exclusions, and data gaps the preparer states.

## Include where expressly stated

- Any system, component, environment, or repository the preparer could not access
- Any test, check, or analysis not performed, and why
- Any reliance on information provided by management without independent verification
- Any time or resource constraint the preparer states affected the work
- Any statement that findings are not exhaustive, or that absence of a finding is not assurance of absence
- Any stated false-positive or false-negative limitation
- Any area flagged as requiring further work or a follow-up assessment
- Any assumption the conclusions depend on

## Rules

- **Report each limitation as stated, in eight words or fewer.** Do not paraphrase into something milder, and do not omit a limitation because it appears boilerplate. A standard caveat about non-exhaustiveness is still the reason a clean report is not a clean bill of health.
- **Report any recommendation for further work prominently**, since it is the preparer telling you the assessment is incomplete.
- Report any statement that management information was accepted without verification, since it identifies which findings rest on the seller's own account.
- Report no more than eight limitations. Where more exist, report the eight bearing most on the conclusions and append ` and [N] further limitations`.
- Do not assess whether a limitation is material, and do not resolve any gap.

## Fallback rules

- Return exactly `None stated` where the preparer states no limitation at all.

Note: `None stated` is a positive finding, not a fallback state. **For a professionally prepared report it is also unusual and slightly suspicious** — most preparers state limitations to protect themselves, and their complete absence is worth a look.

- Return `Unable to determine` where the limitations section is illegible.

## Output format

One line per limitation:

`[Limitation as stated]`

Return no more than 8 lines and no more than 90 words.
```

---

### 9. Copyleft Components Identified

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: the components whose licences may require source disclosure or
  reciprocal licensing. **The core open source risk**, and it only bites where the
  product is distributed.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the components the report identifies as subject to copyleft or reciprocal licence terms.

## Applicability

- Applies where Report Type is `Open source composition analysis` or `Software bill of materials`.
- For `Architecture description` and `Code quality or technical debt review`, report any copyleft component the document identifies, and otherwise return `Not applicable`.
- For all other report types, return `Not applicable`.

## Include where expressly stated

- Each component the report identifies under a strong copyleft licence — the GPL family, AGPL, and equivalents — with its name, version, and licence as printed
- Each component under a weak or file-level copyleft licence — LGPL, MPL, EPL, CDDL — with the same detail
- The component's stated role: direct dependency, transitive dependency, or embedded or modified code
- Any component the report flags as licence-unknown, licence-conflicting, or dual-licensed
- Any snippet or partial match the report identifies as copied code
- The counts by licence category where the report states them

## Rules

- Report licence names **exactly as the report prints them**, including version — `GPL-2.0-only` and `GPL-3.0-or-later` are different licences with different consequences, and normalizing them destroys the distinction.
- **Report `AGPL` components separately and prominently where identified.** AGPL's network-use provision can trigger disclosure obligations for a hosted service that never distributes anything, which is the case most often missed.
- **Report whether each component is a direct or transitive dependency where stated**, since transitive copyleft is both the most common and the least known to the target's engineers.
- Report the report's stated counts. **Do not count components yourself and do not total across categories.**
- Report no more than ten components. Where more exist, report the strong-copyleft components first, up to ten, and append ` and [N] further components identified`.
- **Do not assess licence compatibility, do not evaluate whether an obligation is triggered, and do not conclude that any component creates exposure.** That is the licence analysis, it depends on how the software is distributed and modified, and it is specialist legal work.

## Fallback rules

- Return exactly `None identified` where the report scanned for licences and identified no copyleft component.
- Return `Not stated` where the report inventories components without identifying their licences. **An SBOM without licence data does not answer this question at all**, and that is worth surfacing.
- Return `Unable to determine` where the licence findings are illegible or internally inconsistent.

## Output format

One line per component:

`[Component] [version] — [licence as printed] — [direct | transitive | embedded | not stated]`

Return no more than 10 lines and no more than 110 words. Do not include counts you calculated or a compatibility assessment.
```

---

### 10. Distribution Status

- Native type: Classify
- Configured options, in UI order: `Distributed to customers`, `Hosted service only`, `Both distributed and hosted`, `Internal use only`, `Embedded in hardware`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether copyleft obligations are triggered at all.

**This is the column that turns an open source finding into a risk or a
non-issue.** Most copyleft obligations attach on distribution. A GPL component in
a purely hosted service may create no obligation; the same component in
downloadable software does. AGPL is the exception, which is why it is called out
separately in the previous column.

```markdown
## Task

Classify how the software covered by this report reaches users, as the documents in this unit state it. Choose exactly one configured option.

## Scope

- Consider statements in this report about how the product is delivered: downloaded, installed on customer premises, provided as a hosted or cloud service, embedded in a device, or used only internally.
- Include statements in an architecture description or management response in the unit.
- Exclude your own inference from the product name, the company's business, or general knowledge.

## Classification rules

- `Distributed to customers`: the software is delivered to customers as an installable, downloadable, on-premises, or client-side artifact, including a mobile application, a desktop client, an SDK, or a browser-side bundle. **A JavaScript bundle served to a browser is distribution** in most analyses, and it is the case most often overlooked in a service that considers itself hosted-only.
- `Hosted service only`: the software runs on infrastructure controlled by the target and customers access it over a network, with no artifact delivered.
- `Both distributed and hosted`: both models apply to the covered software.
- `Embedded in hardware`: the software ships inside a device.
- `Internal use only`: the software is used by the target and not made available to customers in any form.

## Fallback rules

- Use `Not addressed` where the documents in this unit do not state how the software is delivered. **This is common, because a composition scan often says nothing about the delivery model** — and it means the open source conclusion cannot be reached from this report alone. The reviewer establishes delivery from the commercial and architecture material.
- Use `Unable to determine` where statements in the unit conflict.

## Output format

Return only the exact configured option and no explanation.
```

---

### 11. Licence Obligations Stated

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: the obligations the report says attach, reported as the preparer stated
  them rather than as the reviewer might assess them.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the licence obligations, conflicts, or policy breaches this report identifies.

## Applicability

- Applies where Report Type is `Open source composition analysis` or `Software bill of materials`.
- For all other report types, return `Not applicable` unless the document identifies licence obligations, in which case report them.

## Include where expressly stated

- Attribution or notice obligations, and whether the report found them satisfied
- Source disclosure or source availability obligations
- Reciprocal or same-licence obligations on derivative works
- Patent grant, patent retaliation, or patent termination provisions the report flags
- Any obligation the report states is unsatisfied or at risk
- Any licence conflict or incompatibility the report identifies
- Any breach of the target's own open source policy the report identifies
- Any component the report states requires removal, replacement, or re-architecture

## Rules

- **Report the obligations the report identifies, and whether the report states each is satisfied.** An identified but satisfied attribution obligation is housekeeping; an unsatisfied source disclosure obligation is a finding.
- **Report any recommendation to remove or replace a component prominently**, since it is the preparer stating that the current position is not sustainable, and it usually carries engineering cost.
- Report the report's own risk ratings or severity labels exactly as printed, and do not translate them into a different scale.
- **Do not perform the licence analysis.** Do not conclude that an obligation is triggered, assess compatibility, or judge whether a use is a derivative work. Report the preparer's conclusions and stop.

## Fallback rules

- Return exactly `None identified` where the report analysed licences and identified no obligation of concern.
- Return `Not stated` where the report inventories components without analysing obligations.
- Return `Unable to determine` where the obligation findings are illegible or inconsistent.

## Output format

One line per obligation or conflict:

`[Obligation or conflict] — [component or "portfolio-wide"] — [satisfied | unsatisfied | not stated] — [preparer's severity as printed]`

Return no more than 8 lines and no more than 100 words. Do not include an assessment of your own.
```

---

### 12. Third-Party Components Critical to Product

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the dependencies the product cannot function without. **A core
  dependency under a non-transferable licence, or on an unmaintained project, is a
  continuity risk independent of any licence question.**

```markdown
## Task

Report the third-party or open source components this report identifies as critical, core, or otherwise essential to the product.

## Scope

- Include components the report identifies as core, critical, foundational, or as presenting concentration or continuity risk.
- Include commercial third-party software, libraries, APIs, and hosted services the report identifies as essential.
- Include any model, dataset, or API the report identifies as essential to a product feature.
- Exclude the full component inventory. **This column is about the components the report singles out**, not the 4,000 in an SBOM.

## Include where expressly stated

- The component or service name and version, exactly as printed
- The role it plays, in six words or fewer
- Whether it is commercially licensed, open source, or a hosted third-party service
- Any statement that the component is unmaintained, deprecated, end-of-life, or has no active upstream project
- Any single-vendor or single-source dependency the report flags
- Any statement that replacing it would require significant work

## Rules

- **Report end-of-life and unmaintained flags prominently.** An unmaintained dependency in a core path is a security and continuity issue that no licence remediation addresses, and it often carries a larger engineering cost than any copyleft finding.
- Report commercial components separately from open source ones, since a commercial licence raises a transferability question that goes to the Contracts tables.
- Report the component's role as stated. Do not assess criticality yourself, and do not judge whether a dependency is replaceable.

## Fallback rules

- Return exactly `None identified` where the report identifies no component as critical.
- Return `Not applicable` where the report type could not address this, such as a certification report.
- Return `Unable to determine` where the relevant findings are illegible.

## Output format

One line per component:

`[Component] [version] — [role] — [commercial | open source | hosted service][; end of life | unmaintained | single source]`

Return no more than 8 lines and no more than 90 words.
```

---

### 13. AI and Model Rights

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: rights in models, training data, and outputs. **Increasingly the core
  asset question for a technology target, and absent from most diligence
  schemas.**

```markdown
## Established result

- Report Type: @Report Type

## Task

Report what this report states about artificial intelligence or machine learning components, their training data, and rights in their outputs.

## Applicability

- Applies where Report Type is `AI or model documentation`, `Architecture description`, `Open source composition analysis`, or `Software bill of materials`.
- For other report types, report any statement the document makes on these subjects, and otherwise return `Not applicable`.

## Include where expressly stated

- Each model identified, with its name, version, and provider, and whether it is proprietary to the target, open weight, or accessed through a third-party API
- **The licence or terms the model is used under**, exactly as printed. Model licences frequently carry field-of-use, acceptable-use, and scale restrictions that ordinary software licences do not
- Any restriction on commercial use, on use to train a competing model, or on redistribution of weights or outputs
- **The provenance of training or fine-tuning data**: proprietary, licensed, publicly scraped, customer data, or synthetic
- Any statement about rights to use customer data for training, and any consent or contractual basis identified
- Any statement about ownership of, or rights in, model outputs
- Any attribution, disclosure, or watermarking obligation
- Any evaluation, bias, or safety testing referenced, and any regulatory classification stated
- Any dependency on a third-party API whose terms could change

## Rules

- **Report the training data provenance where stated, and report its absence where the documents do not address it.** Whether the target had the right to use what it trained on is the question with the longest tail, and silence is the most common answer.
- Report any use of customer data for training separately, since it engages the privacy workstream and the customer contracts simultaneously.
- Report model and licence names exactly as printed.
- **Do not assess whether any use is permitted, whether outputs are protectable, or whether any regulation applies.** All three are unsettled legal questions.

## Fallback rules

- Return exactly `None identified` where the report addresses AI or model components and identifies none.
- Return `Not addressed` where the report covers software that may include such components and says nothing about them. **For a product marketed as AI-enabled, that silence is itself a coverage finding.**
- Return `Unable to determine` where the relevant statements are illegible or inconsistent.

## Output format

One line per model or component:

`[Model] [version] — [proprietary | open weight | third-party API] — licence: [as printed]; training data: [provenance or "Not addressed"]; output rights: [as stated or "Not addressed"]`

Return no more than 6 lines and no more than 100 words.
```

---

### 14. Open Findings and Severity

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: what the report found, using the preparer's own severity scale.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the findings this report identifies, with the preparer's own severity rating for each.

## Rules by report type

- `Penetration test`, `Vulnerability scan`: findings by severity as the preparer rated them, with the stated counts per severity band. Note any finding the preparer describes as actively exploitable or as having been exploited during testing.
- `Security assessment or audit`, `Third-party certification report`: control deficiencies, exceptions, or qualifications. **For a certification report, report whether the opinion is unqualified or qualified, and report every exception noted**, since an unqualified opinion with exceptions is not a clean report.
- `Open source composition analysis`, `Software bill of materials`: security vulnerabilities identified in components, distinct from licence obligations which have their own column.
- `Code quality or technical debt review`: the significant deficiencies identified, with any rating.
- `Architecture description`, `AI or model documentation`: any risk or weakness the document identifies.

## Rules

- **Use the preparer's severity labels exactly as printed** — critical, high, medium, low, informational, or a numeric scale. Do not translate between scales, and do not assign a severity the report did not.
- Report the counts by severity as the report states them. **Do not count or total findings yourself.**
- Report the highest-severity findings individually, in eight words or fewer each, up to six. Report lower severities by count only.
- **Report any finding the preparer states is unremediated at the report date**, separately from the overall list, since those are the live items.
- Report any finding the preparer describes as systemic or as affecting multiple systems.
- **Do not assess a finding's exploitability, likelihood, or business impact, and do not re-rate anything.** The preparer tested; you are reporting.

## Fallback rules

- Return exactly `None identified` where the report states it identified no findings.
- Return `Not applicable` where the report type produces no findings, such as a plain SBOM.
- Return `Unable to determine` where the findings section is illegible or the severity scale cannot be identified.

## Output format

`Counts as stated: [severity: N; severity: N]` followed by one line per high-severity finding:

`[Severity as printed] — [finding] — [remediated | open | not stated]`

Return no more than 8 lines and no more than 100 words. Do not include counts or ratings of your own.
```

---

### 15. Escrow and Continuity Arrangements

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: arrangements protecting continuity of the technology — source escrow,
  backup, disaster recovery, and key-person dependency.

```markdown
## Task

Report any escrow, backup, disaster recovery, or continuity arrangement this report identifies.

## Include where expressly stated

- Any source code escrow arrangement, the agent, the beneficiaries, and the stated release triggers
- Whether the escrow deposit is stated to be current, and the date of the last deposit
- Backup arrangements, their frequency, and whether restoration has been tested
- Disaster recovery or business continuity provisions, and any stated recovery objectives
- Any single point of failure the report identifies in infrastructure or process
- **Any key-person dependency the report identifies**, described by role rather than by name
- Any statement that documentation is insufficient for another engineer to maintain the system
- Any dependency on infrastructure or accounts controlled by an individual rather than by the entity

## Rules

- **Report whether an escrow deposit is stated to be current.** An escrow arrangement with a deposit three years stale protects nothing, and it is a common finding.
- **Report key-person dependencies by role, not by name**, so the finding can be matched to the Employment table without carrying personal data into this row.
- **Report any infrastructure or account controlled by an individual rather than the entity** — a domain registered to a founder's personal account, a cloud account on a personal card, a repository in a personal namespace. These are cheap to fix before closing and painful afterwards.
- Report the arrangements as stated. Do not assess adequacy or test any claim.

## Fallback rules

- Return exactly `None identified` where the report addresses continuity and identifies no arrangement or risk.
- Return `Not addressed` where the report does not address continuity at all.
- Return `Unable to determine` where the relevant statements are illegible.

## Output format

One line per arrangement or risk:

`[Arrangement or risk] — [detail as stated]`

Return no more than 6 lines and no more than 85 words. Do not name individuals.
```

---

### 16. Remediation Status

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what has actually been fixed. **A finding and its remediation are
  different facts**, and the report itself is usually silent on the second because
  it predates the work.

```markdown
## Task

Report what the documents in this unit state about remediation of the findings.

## Scope

- Consider the report's own statements about remediation status, any management or engineering response in the unit, and any retest or remediation confirmation.
- Exclude your own inference about what is likely to have been fixed since.

## Include where expressly stated

- Any finding the documents state has been remediated, and the date
- Any retest confirming remediation, with its date and what it covered
- Any management response accepting, disputing, or deferring a finding
- **Any finding the management response states is accepted as a risk rather than fixed**
- Any remediation plan with target dates, and whether those dates have passed
- Any statement that remediation requires re-architecture, a version upgrade, or third-party action
- Any stated cost or effort estimate for remediation

## Rules

- **Distinguish remediation confirmed by a retest from remediation asserted by management.** The first is evidence and the second is a claim, and the difference matters when the buyer is deciding what to price.
- **Report any accepted risk explicitly.** A finding the target decided not to fix is a deliberate position the buyer is inheriting, and it is more informative than an open finding nobody has looked at.
- Compare any stated remediation target date to the diligence as-of date in the Table Instructions. Where a target date has passed with no confirmation of completion, append ` [target date passed]`.
- Report cost and effort estimates as stated. **Do not estimate anything yourself.**
- Do not assess whether remediation was adequate.

## Fallback rules

- Return exactly `Not addressed` where the documents in this unit say nothing about remediation. **This is the expected answer for a standalone report**, and it is a coverage finding rather than a defect: the remediation evidence exists elsewhere or not at all, and it belongs in the coverage register.
- Return `Unable to determine` where remediation statements conflict or are illegible.

## Output format

`Confirmed by retest: [findings or "none"]; asserted by management: [findings or "none"]; accepted as risk: [findings or "none"]; plan: [target dates or "none stated"]`, with any bracketed flag appended.

Return no more than 85 words.
```

---

### 17. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this report refers to that is not present. Feeds
  the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document this report refers to that is not present in the review unit.

## Scope

- Include appendices, component inventories, and finding registers listed as attached but not present. **Where the detailed findings appendix is missing, the report's summary is all there is**, and that should be visible.
- Include earlier or later reports, retests, and scans referenced but absent.
- Include the engagement letter, statement of work, or scope document referenced but absent, since the reliance and liability terms usually live there.
- Include any reliance letter referenced as issued or available.
- Include management responses and remediation plans referenced but absent.
- Include the target's own open source policy, security policy, or coding standards referenced as the benchmark applied.
- Include escrow agreements and deposit confirmations referenced but absent.
- Include third-party licences or model terms referenced as governing an identified component.
- Include any certification, attestation, or bridge letter referenced but absent.
- Exclude published standards, frameworks, and vulnerability databases.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the detailed findings appendix`, report it as printed and add `(no date stated)`.
- **Where a findings appendix or component inventory is referenced and absent, add `; findings detail missing`.** The summary alone cannot support a conclusion, and this flag identifies the reports that need to be re-requested in full.
- **Where an engagement letter or reliance letter is referenced and absent, add `; reliance terms missing`.** Whether the buyer can rely on the report may be undeterminable without it.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; findings detail missing | ; reliance terms missing]`

Return no more than 12 lines and no more than 115 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Report currency adequate** | Yes / Refresh required / Unassessed |
| **Buyer reliance obtainable** | Yes / No / In negotiation / Not required |
| **Coverage adequate for the estate** | Yes / Partial, gap identified / Unassessed |
| **Licence exposure assessed** | No exposure / Remediation required / Specialist review needed / Unassessed |
| **Remediation cost estimate** | Free text |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** This table has a handful of rows and each one either supports
or fails to support a conclusion about the target's core asset.

### Work that never belongs in a column

- **The licence analysis itself.** Take `Copyleft Components Identified` together
  with `Distribution Status`, and have specialist counsel assess which obligations
  are actually triggered. **Whether a GPL component in a hosted service creates
  exposure depends on facts no column can settle**, and AGPL behaves differently
  from the rest of the family.
- **Reading the SBOM.** Where a component inventory lists thousands of entries,
  read it directly with the right tooling, or ask Assistant over the project.
  Per `review-tables.md` §5, do not attempt it as a column.
- **Estate coverage.** Compare `Product or Codebase Covered` across every row
  against the target's actual product range from the commercial workstream. **A
  product with no assessment covering it is the finding**, and it is invisible
  inside any single row.
- **Currency refresh.** Every row flagged `[over 6 months old]` or
  `[over 12 months old]`, for material products. On a fast-moving codebase a
  refreshed scan is usually cheaper than arguing about a stale one.
- **Reliance negotiation.** Every row where reliance is excluded or unaddressed.
  Reliance letters are routinely obtainable for a fee, so this is a live item
  rather than a dead end.
- **Key-person and personal-account remediation.** Every item from
  `Escrow and Continuity Arrangements`, matched to the Employment table for the
  people and actioned before closing for the accounts. Domains and cloud accounts
  in personal names are cheap to move now and painful to chase later.
- **AI provenance.** Every row where `AI and Model Rights` returns
  `Not addressed` for a product marketed as AI-enabled, and every row where
  training data provenance is unstated or includes customer data. The second joins
  the privacy workstream and the customer contracts at once.

---

## Test set

- [ ] Open source composition analysis with licence data, covering all repositories
- [ ] Open source composition analysis covering three of nine repositories
- [ ] SBOM with component names and no licence data
- [ ] Composition analysis identifying an AGPL component
- [ ] Composition analysis identifying GPL-2.0-only and GPL-3.0-or-later separately
- [ ] Composition analysis identifying only transitive copyleft
- [ ] Composition analysis flagging licence-unknown components
- [ ] Composition analysis recommending removal of a component
- [ ] Report covering software delivered as a browser bundle
- [ ] Report covering a hosted service only
- [ ] Report saying nothing about how the software is delivered
- [ ] Penetration test with critical findings and stated counts by severity
- [ ] Penetration test with a finding actively exploited during testing
- [ ] Unvalidated vulnerability scan output
- [ ] SOC 2 Type 1 report
- [ ] SOC 2 Type 2 report with exceptions noted
- [ ] Certification report with a qualified opinion
- [ ] Report with a retest confirming remediation
- [ ] Report with a management response accepting a finding as a risk
- [ ] Report with a remediation plan whose target dates have passed
- [ ] Report expressly excluding third-party reliance
- [ ] Report with a reliance letter referenced as available
- [ ] Report with a liability cap at the fee level
- [ ] Report commissioned for an earlier financing round
- [ ] Internally prepared architecture description
- [ ] Report with no preparer identified
- [ ] Report describing a scan eighteen months before the as-of date
- [ ] Report stating the commit or release examined
- [ ] Report with an extensive limitations section
- [ ] Report with no limitations stated at all
- [ ] AI model documentation with training data provenance stated
- [ ] AI model documentation silent on training data
- [ ] Architecture description identifying use of customer data for model training
- [ ] Report identifying a third-party API dependency with changeable terms
- [ ] Report identifying an unmaintained core dependency
- [ ] Report identifying a domain registered to a founder's personal account
- [ ] Report identifying a stale source code escrow deposit
- [ ] Report referencing a findings appendix that is not attached
- [ ] Single file containing both a pen test and a composition analysis

Then test the dependencies: change `Report Type` from
`Open source composition analysis` to `Penetration test` and confirm
`Copyleft Components Identified` and `Licence Obligations Stated` move to
`Not applicable` while `Open Findings and Severity` re-runs against the
penetration-test rules. Change `Preparer` from external to internal and confirm
`Reliance and Confidentiality` moves to `Not applicable`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
