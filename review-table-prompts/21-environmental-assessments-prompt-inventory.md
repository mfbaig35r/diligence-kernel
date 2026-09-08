# Prompt Inventory — Environmental: Assessments

Table 21 of the POC. First of three Environmental tables.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Environmental`
- Review unit: **one report** — the report itself, its appendices and figures, any
  addendum or errata, any management or consultant response, and any reliance
  letter produced for it
- Grouping used: **yes**, typically 1–4 documents per unit
- Intended reviewers and downstream use: environmental and corporate/M&A teams;
  feeds the site-level risk assessment, the special indemnity and escrow analysis,
  the reliance negotiation, and the coverage register
- Inventory version: v1.0

### Why environmental sits differently from every other workstream

**Environmental liability in most jurisdictions attaches to the current owner or
operator regardless of fault, retroactively, and without regard to who caused the
contamination.** In a share purchase it does not transfer away — the entity keeps
its liability and the buyer keeps the entity. That makes site-level diligence a
pricing and indemnity exercise rather than a consent exercise, and it is why an
owned industrial site with no assessment is a materially different risk from a
leased office with none.

Two consequences shape this table:

1. **Reliance is not a formality.** A seller-commissioned Phase I addressed to the
   seller, with a no-third-party-reliance clause, gives the buyer no recourse
   against the consultant and may not support a statutory purchaser defence.
   `Reliance Parties` and `Reliance Transferable` exist for that.
2. **Scope and limitations matter as much as findings.** The taxonomy's own
   example: a Phase I that excluded a parcel is a different document from one that
   did not. `Non-Scope Items` and `Data Gaps` are therefore front-loaded, and a
   clean conclusion is read against them rather than on its own.

### The 180-day point

Statutory landowner liability protections in several jurisdictions depend on
completing appropriate inquiry within a stated period before acquisition — 180 days
is the common figure, with certain components requiring update within a year.
**A Phase I older than that may not support the defence even where its findings are
sound.** `Report Date` flags the age; whether the defence is available is a legal
question and stays with the reviewer.

## Assumptions to confirm before running

1. One row is one report for one property. A Phase I covering three sites is one
   row where the report treats them as one assessment, and the properties are
   listed in `Property Assessed`; where it issues separate conclusions per site,
   consider splitting.
2. **Permits and enforcement are separate tables.** A permit is a Filing read for
   status; a notice of violation is Correspondence read for the chronology.
3. Where a target owns or operates industrial, manufacturing, waste, fuel-storage,
   or formerly industrial land and **no assessment exists**, that absence is a
   coverage-register row, not an empty table. Record it.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

21 Harvey columns plus 9 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side environmental diligence on the target group listed below. This table reviews environmental assessments, surveys, and consultant reports.

One row is one report: the report itself, its appendices and figures, any addendum or errata, any management or consultant response, and any reliance letter produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the property or its history.
- **Report the consultant's findings and the consultant's caveats together.** A conclusion reported without its scope and limitations is misleading, and in this workstream it is the most common way a report is misused.
- **Do not perform the assessment the consultant performed.** Do not identify a condition the report did not identify, do not upgrade or downgrade a finding, do not conclude that a condition requires investigation or remediation, and do not estimate a cost the report does not state.
- **Do not opine on liability, on the availability of any statutory defence, or on who bears responsibility for a condition.** All three are legal conclusions.
- Report figures, quantities, and concentrations only as the report states them. Do not calculate, total, or convert units.
- Use entity, property, and consultant names exactly as printed.
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
  Property Assessed
  Preparer and Credentials

Stage 2 — Standing and currency
  Documents in Unit ──→ Report Date
                        Referenced but Not Produced
  Preparer and Credentials ──→ Reliance Parties
  Reliance Parties ──→ Reliance Transferable

Stage 3 — Scope, routed on report type
  Report Type ──→ Standard Applied
                  Scope Inclusions
                  Regulatory Databases Reviewed
  Non-Scope Items
  Data Gaps

Stage 4 — Findings, routed on report type
  Report Type ──→ RECs Identified
                  Controlled and Historical RECs
                  Vapour Encroachment
  Historical Use Findings
  Adjacent Property Concerns
  Sampling Results

Stage 5 — Conclusion
  Recommendation
  Cost Estimate Stated
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Report Date; Referenced but Not Produced | v1.0 | draft |
| 2 | Report Type | Classify | — | Standard Applied; Scope Inclusions; Regulatory Databases Reviewed; RECs Identified; Controlled and Historical RECs; Vapour Encroachment | v1.0 | draft |
| 3 | Property Assessed | Free Response | — | — | v1.0 | draft |
| 4 | Preparer and Credentials | Free Response | — | Reliance Parties | v1.0 | draft |
| 5 | Report Date | Date | @Documents in Unit | — | v1.0 | draft |
| 6 | Reliance Parties | Free Response | @Preparer and Credentials | Reliance Transferable | v1.0 | draft |
| 7 | Reliance Transferable | Classify | @Reliance Parties | — | v1.0 | draft |
| 8 | Standard Applied | Free Response | @Report Type | — | v1.0 | draft |
| 9 | Scope Inclusions | Free Response | @Report Type | — | v1.0 | draft |
| 10 | Non-Scope Items | Free Response | — | — | v1.0 | draft |
| 11 | Data Gaps | Free Response | — | — | v1.0 | draft |
| 12 | Regulatory Databases Reviewed | Free Response | @Report Type | — | v1.0 | draft |
| 13 | Historical Use Findings | Free Response | — | — | v1.0 | draft |
| 14 | Adjacent Property Concerns | Free Response | — | — | v1.0 | draft |
| 15 | RECs Identified | Free Response | @Report Type | — | v1.0 | draft |
| 16 | Controlled and Historical RECs | Free Response | @Report Type | — | v1.0 | draft |
| 17 | Vapour Encroachment | Free Response | @Report Type | — | v1.0 | draft |
| 18 | Sampling Results | Free Response | — | — | v1.0 | draft |
| 19 | Recommendation | Classify | — | — | v1.0 | draft |
| 20 | Cost Estimate Stated | Free Response | — | — | v1.0 | draft |
| 21 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Report Date`, `Referenced but Not Produced`
- Purpose: inventory the report and its supporting material, and record whether
  the appendices are present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the report, its executive summary if separate, its appendices, figures, site plans, boring logs, laboratory analytical reports, chain-of-custody records, historical maps and aerial photographs, interview records, any addendum or errata, any reliance letter, and any management or consultant response.
- Treat appendices bound into the report as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where none is printed, describe it in five words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Report`, `Executive summary`, `Appendix`, `Figures or site plan`, `Laboratory report`, `Boring logs`, `Historical records`, `Interview record`, `Addendum or errata`, `Reliance letter`, `Response`, or `Other`.
- **Where the report's appendices are absent, state that.** In a Phase II or a sampling report the laboratory data is the finding, and a summary without it cannot be verified.
- **Where an addendum or errata is present, note in the evidence field what it changed.** An errata correcting a conclusion is significant and easy to miss.
- Where a document relates to a different property or report, still list it and append ` [relates to [property or report]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 12 lines and no more than 100 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Report Type

- Native type: Classify
- Configured options, in UI order: `Phase I environmental site assessment`, `Limited Phase I or desktop review`, `Transaction screen assessment`, `Phase II investigation`, `Remedial investigation`, `Remediation or closure report`, `Vapour intrusion assessment`, `Asbestos or hazardous materials survey`, `Compliance audit`, `Geotechnical or soils report`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: six columns
- Purpose: route the scope and findings columns, since a Phase I, a Phase II, and
  an asbestos survey answer entirely different questions.

```markdown
## Task

Classify the type of assessment this review unit contains. Choose exactly one configured option.

## Classification rules

- `Phase I environmental site assessment`: a records, interview, and site-reconnaissance assessment conducted to a recognised standard, identifying recognised environmental conditions without sampling. **No sampling is the defining feature** — a Phase I concludes on the likelihood of contamination, not its presence.
- `Limited Phase I or desktop review`: an assessment omitting one or more required Phase I components — commonly the site visit, the interviews, or the historical records review. **Report which components were omitted in the evidence field.** A limited assessment does not support the statutory inquiry standard a full Phase I does.
- `Transaction screen assessment`: a lighter-scope screening to a transaction screen standard rather than a full Phase I. **Materially less than a Phase I** and should never be treated as equivalent.
- `Phase II investigation`: intrusive investigation with sampling and laboratory analysis, undertaken to test conditions a Phase I identified.
- `Remedial investigation`: a broader delineation of contamination extent, usually under regulatory oversight.
- `Remediation or closure report`: documents remedial work performed and any closure, no-further-action, or completion determination obtained.
- `Vapour intrusion assessment`: assesses migration of vapours into structures.
- `Asbestos or hazardous materials survey`: surveys building materials for asbestos, lead paint, PCBs, mercury, or similar. **Often a distinct engagement and frequently the only report on an older building**, and it addresses occupational and demolition risk rather than land contamination.
- `Compliance audit`: reviews the site's compliance with permits and environmental regulation rather than its contamination status.

Classify on what was actually done, not on the report's title. **A document titled Phase I that omits the site visit is `Limited Phase I or desktop review`.**

## Fallback rules

- Use `Other` where the report is environmental but none of the options describes it.
- Use `Unable to determine` where the documents are too fragmentary to identify what was done.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Property Assessed

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what was assessed, and above all **what was excluded**. The join key to
  the Real Estate tables and to the site list.

```markdown
## Task

Report the property or properties this report assesses.

## Include where expressly stated

- The street address of each property, as printed
- The parcel, assessor's, or folio identifier where stated
- The site area, and the acreage or square footage assessed
- **Any parcel, building, area, or portion of the site expressly excluded from the assessment**
- The current use of the site as described
- Any structures on site, and their approximate age or construction date where stated
- Whether the assessment covered the whole of the target's interest in the property, or part

## Rules

- **Report the excluded areas as prominently as the assessed ones.** The taxonomy's own example applies literally here: a Phase I that excluded a parcel is a different document from one that did not, and consultants state exclusions clearly because their liability depends on them. **Where any area is excluded, append ` [partial site coverage]`.**
- Report the address exactly as printed, since it is the join key to the Real Estate tables. **Do not standardize or correct it.**
- Report the parcel identifier where given, since it is the identifier the register and the tax authority use.
- **Where the property is leased rather than owned, report that where the documents state it**, because it changes the liability profile substantially.
- Do not assess whether the coverage was adequate, and do not compare the assessed area to the target's holdings.

## Fallback rules

- Return `Not stated` where the report does not identify the property assessed. **For any assessment this is a fundamental defect** — findings without a stated subject support nothing.
- Return `Unable to determine` where the property description is illegible or internally inconsistent.

## Output format

`[Address as printed][; parcel [identifier]]` per property, then `Area assessed: [as stated]; excluded: [as stated or "none stated"]; interest: [owned | leased | Not addressed]`, with any bracketed flag appended.

Return no more than 70 words.
```

---

### 4. Preparer and Credentials

- Native type: Free Response
- Upstream: none
- Downstream: `Reliance Parties`
- Purpose: who did the work and whether they were qualified to. **The
  environmental professional's qualification is a component of the statutory
  inquiry standard**, not a formality.

```markdown
## Task

State who prepared this report and their stated qualifications.

## Include where expressly stated

- The consulting firm's name, exactly as printed
- The individuals who conducted and reviewed the assessment, with their titles
- **Any statement that the assessment was conducted by or under the supervision of an environmental professional, and any recitation of that person's qualifications** — degree, years of experience, professional licence, or registration
- Any professional certification, licence number, or registration stated
- Any signature or seal on the report
- Whether the preparer is external to the target group, using the review-subject list
- Any statement that the report was prepared for a named engagement or under a named scope of work

## Rules

- **Report any environmental professional qualification statement, and report its absence where none appears.** In several jurisdictions the statutory inquiry standard requires the assessment to be conducted by a qualified environmental professional who declares their qualifications, and **a report with no such declaration may not satisfy the standard however competent the work.**
- **Report whether the report is signed.** An unsigned draft report is not a report, and draft environmental reports circulate widely.
- Report whether the preparer is internal or external. An internally prepared assessment is not third-party assurance.
- **Do not assess whether the preparer was qualified** or whether the statutory standard is met.

## Fallback rules

- Return `Not stated` where the report identifies no preparer. **For an assessment offered as assurance this is a serious defect.**
- Return `Unable to determine` where the preparer is illegible.

## Output format

`[Firm as printed] — [external | internal]; professional: [name and stated qualifications, or "no EP declaration"]; signed: [yes | no]; licence: [as stated or "none"]`

Return no more than 55 words.
```

---

### 5. Report Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: how old the report is. **Age bears directly on whether a statutory
  purchaser defence is available**, and separately on whether conditions have
  changed.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to distinguish the report from any addendum. Confirm the dates against the documents.

## Task

Identify the date of this report and the date the fieldwork was performed.

## Rules

- **Report both the report issue date and the date of the site visit, reconnaissance, or sampling, where the documents state each.** They frequently differ by weeks, and the earlier date is what the currency question turns on.
- Where an addendum or errata is present, report the original report date and note the addendum's date in the evidence field.
- Where the report states a range of fieldwork dates, report the last.
- Do not report the date of a laboratory analysis, the date of an interview, or the date of a records search separately here; note them in the evidence field where they materially predate the report.
- Compare the earlier of the two dates to the diligence as-of date and flag it:
  - more than 180 days: append ` [over 180 days]`
  - more than one year: append ` [over 1 year]`
  - more than five years: append ` [over 5 years]`
- **The 180-day flag is not arbitrary.** Statutory landowner liability protections commonly require appropriate inquiry to have been completed within a stated period before acquisition, with certain components requiring update within a year. **A report carrying this flag may not support the defence even where its findings are sound.** Whether the defence is available, and whether an update would restore it, is a legal question for the reviewer.

## Output format

`Report [YYYY-MM-DD]; fieldwork [YYYY-MM-DD or "not stated"]`, with any bracketed flag appended. Return `Not stated` where no report date appears.
```

---

### 6. Reliance Parties

- Native type: Free Response
- Upstream: `@Preparer and Credentials`
- Downstream: `Reliance Transferable`
- Purpose: **who may rely on this report.**

A seller-commissioned assessment addressed to the seller, with a
no-third-party-reliance clause, gives the buyer no recourse against the consultant
if it is wrong — and in some jurisdictions may not support the buyer's own
statutory inquiry. Reliance is routinely extendable for a fee, which makes this a
negotiation item rather than a dead end.

```markdown
## Established result

- Preparer and credentials: @Preparer and Credentials

## Task

Report what this report states about who may rely on it and how it may be used.

## Include where expressly stated

- The party the report is addressed to or stated to be prepared for
- **Any reliance clause naming the parties entitled to rely, including any lender, investor, or purchaser**
- **Any statement that no third party may rely on the report, or that it is for the addressee's sole use and benefit**
- Any reliance letter present in the unit, and to whom it extends reliance
- Any provision for reliance to be extended, and any fee stated
- Any limitation or cap on the consultant's liability, with the amount
- Any confidentiality restriction on the report itself
- Any restriction on disclosing the report to a purchaser, a lender, or a regulator
- Any disclaimer of warranty as to completeness or accuracy
- Any statement that the report may not be used for a purpose other than the stated engagement

## Rules

- **Report the no-third-party-reliance position explicitly where present.** It is the most consequential item in this column and it is usually in small print at the front.
- **Report the liability cap as stated, with the amount.** A cap at the level of the consultant's fee means the recourse is nominal.
- **Report any restriction preventing disclosure of the report to a buyer or its lenders.** Disclosing a report in breach of its own terms is a real problem and it is easy to overlook.
- Report any reliance letter present and its beneficiaries, since it may already solve the problem.
- Report the terms as stated. **Do not assess whether a reliance exclusion or a liability cap would be effective.**

## Fallback rules

- Return `Not addressed` where the report says nothing about reliance. **Silence is not permission**, and the reviewer should treat an unaddressed reliance position as unresolved rather than open.
- Return `Not applicable` where the report was prepared internally by a target entity, so no third-party reliance question arises. Note that an internal report is also not third-party assurance.
- Return `Unable to determine` where the relevant text is illegible.

## Output format

`Addressed to: [as printed]; reliance: [named parties | sole addressee | expressly excluded | Not addressed]; reliance letter in unit: [to whom, or "none"]; liability cap: [amount or "none stated"]; disclosure restriction: [brief or "none"]`

Return no more than 75 words.
```

---

### 7. Reliance Transferable

- Native type: Classify
- Configured options, in UI order: `Buyer already named or covered`, `Reliance extendable on stated terms`, `Extension contemplated, terms not stated`, `Reliance expressly excluded`, `Not addressed`, `Not applicable`, `Unable to determine`
- Upstream: `@Reliance Parties`
- Downstream: none
- Purpose: a filterable answer to the practical question — can the buyer get the
  benefit of this report, and how.

```markdown
## Established result

- Reliance parties: @Reliance Parties

## Task

Classify whether the benefit of this report is or can be extended to the buyer. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Not applicable`: Reliance Parties returned `Not applicable` because the report was prepared internally.
2. `Buyer already named or covered`: the buyer is a named reliance party, or a reliance letter in the unit extends reliance to a purchaser or to a class including the buyer. Also use this where the report is addressed to a target entity and the target keeps the report in a share purchase, **but note in the evidence field that reliance running to the target entity does not run to the buyer personally**, which matters where the buyer wants its own recourse.
3. `Reliance expressly excluded`: the report states that no party other than the addressee may rely on it, with no extension mechanism.
4. `Reliance extendable on stated terms`: the report or a reliance letter provides a mechanism for extending reliance, with the terms or fee stated.
5. `Extension contemplated, terms not stated`: the report refers to reliance being available to further parties without stating the terms.
6. `Not addressed`: the report is silent on reliance.

**A `Reliance expressly excluded` or `Not addressed` classification does not make the report useless.** It remains a signal about the site, and reliance can usually still be negotiated with the consultant. **What it does mean is that the report cannot on its own support a conclusion or a statutory inquiry**, and the reviewer decides whether to obtain reliance, commission a fresh report, or price the uncertainty.

## Fallback rules

- Use `Unable to determine` where the reliance position cannot be read.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Standard Applied

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: the standard the work was performed to, which determines what the report
  can be used for.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the standard, protocol, or guidance this assessment states it was performed to.

## Rules

- **Report the standard exactly as printed, including its version and year**, for example `ASTM E1527-21`, `ASTM E1528-22`, `ASTM E2600-15`, or a named regulatory guidance document. **The version matters** — standards are revised, and an assessment to a superseded version may not satisfy a current inquiry requirement.
- Report any statement that the assessment was performed to satisfy a named statutory or regulatory requirement, such as an all appropriate inquiries rule.
- Report any statement that the assessment deviated from the standard, and in what respect. **A stated deviation is the consultant telling you the standard was not met.**
- Report any additional standard applied to a component, such as a sampling or analytical protocol.
- For an asbestos or hazardous materials survey, report the survey standard and whether it was a management survey or a pre-demolition or refurbishment survey. **The difference is large**: a management survey does not look inside structures and cannot support demolition or major works.
- **Do not assess whether the standard was correctly applied or whether any statutory requirement is satisfied.**

## Fallback rules

- Return `Not stated` where the report identifies no standard. **For an assessment offered as supporting an inquiry requirement this is a significant defect.**
- Return `Unable to determine` where standards conflict or are illegible.

## Output format

`Standard: [exactly as printed]; statutory purpose stated: [as stated or "none"]; deviations: [brief or "none stated"]`

Return no more than 50 words.
```

---

### 9. Scope Inclusions

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: what the assessment actually did, which determines what its conclusion
  covers.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the components of work this assessment states it performed.

## Rules by report type

- `Phase I environmental site assessment`, `Limited Phase I or desktop review`, `Transaction screen assessment`: state which components were performed — site reconnaissance, regulatory records review, historical records review, interviews with owners, occupants, and local officials, and the environmental professional's own opinion. **Report which of these were omitted**, since the omission determines whether the standard was met.
- `Phase II investigation`, `Remedial investigation`: the media sampled — soil, groundwater, soil vapour, surface water, sediment, or indoor air; the number of sampling locations and depths; the analytes tested; and whether monitoring wells were installed.
- `Remediation or closure report`: the remedial method used, the volume or area treated, the verification sampling performed, and any closure determination obtained.
- `Vapour intrusion assessment`: the media sampled and the buildings assessed.
- `Asbestos or hazardous materials survey`: the materials surveyed, the buildings and areas covered, whether sampling was performed or presumption applied, and the number of samples taken.
- `Compliance audit`: the permits, media, and regulatory areas reviewed, and whether records review, site inspection, or both were performed.

## Rules

- **Report the number of sampling locations and analytes as stated. Do not count them from a table or a figure.**
- **Report where sampling was based on presumption rather than analysis**, particularly in asbestos surveys, since presumed materials are not confirmed materials.
- Report the interview scope where stated, since interviews frequently produce the historical information no record contains.
- Report the components as stated. **Do not assess whether the scope was adequate.**

## Fallback rules

- Return `Not stated` where the report does not describe its scope of work.
- Return `Unable to determine` where the scope description is illegible or inconsistent.

## Output format

`Components performed: [as stated]; omitted: [as stated or "none stated"]; sampling: [media, locations, analytes as stated or "none"]`

Return no more than 85 words.
```

---

### 10. Non-Scope Items

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the conditions the assessment did **not** look for.

**A standard Phase I does not cover asbestos, lead paint, radon, mould, lead in
drinking water, wetlands, or regulatory compliance unless it says so.** These are
non-scope items, consultants list them explicitly, and a clean Phase I says nothing
whatever about any of them. This is the column that stops a clean report being
read as a clean site.

```markdown
## Task

Report the conditions and issues this assessment expressly states were outside its scope.

## Include where expressly stated

- **Asbestos-containing materials, lead-based paint, lead in drinking water, radon, mould, and other building-material or indoor-air conditions**
- **Wetlands, protected habitat, endangered species, and cultural or archaeological resources**
- **Regulatory compliance**, as distinct from contamination status
- Health and safety conditions
- Vapour intrusion, where expressly excluded
- Per- and polyfluoroalkyl substances or other emerging contaminants, where expressly excluded
- Geotechnical, structural, or seismic conditions
- Ecological risk
- Off-site sources beyond a stated radius
- Any specific medium not assessed
- Any non-scope item the report states was assessed as a specifically negotiated addition

## Rules

- **Report every non-scope item the report lists, even where the list appears boilerplate.** It is not boilerplate in effect: a clean Phase I over a 1960s industrial building says nothing about the asbestos in it, and that is frequently the largest liability on the site.
- **Where a non-scope item was assessed as an added service, report it separately and say so**, since that changes what the report covers.
- **Where the report is a Phase I over a building constructed before the relevant asbestos restrictions and asbestos is a non-scope item, note in the evidence field that no asbestos survey is evidenced by this report.** The Referenced but Not Produced column and the coverage register carry the gap.
- Report the items as listed. **Do not assess whether any non-scope item is likely to be present**, and do not recommend further work.

## Fallback rules

- Return exactly `None stated` where the report lists no non-scope items.

Note: for a professionally prepared assessment this is **unusual and worth a look** — consultants list non-scope items to limit their own liability, and their complete absence suggests either an unusual scope or an incomplete document.

- Return `Unable to determine` where the limitations section is illegible.

## Output format

One line per item:

`[Non-scope item as stated][; assessed as added service]`

Return no more than 12 lines and no more than 95 words.
```

---

### 11. Data Gaps

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the consultant could not find out, and whether it said the gap
  mattered.

```markdown
## Task

Report the data gaps, limitations, and deviations the consultant identifies.

## Include where expressly stated

- Any gap in historical records — missing aerial photographs, directories, fire insurance maps, or title records — and the periods not covered
- **Any period of the property's history the assessment could not document, with the years**
- Any area of the site the consultant could not access or observe, and why
- Any interview not obtained, and with whom
- Any regulatory record not obtained or not responded to
- Any physical obstruction to observation — snow cover, vegetation, standing water, occupied space, locked areas
- **The consultant's own statement of whether each gap is significant**, using its words
- Any recommendation to close a gap by further work
- Any assumption the conclusions depend on

## Rules

- **Report the consultant's own characterisation of significance, in its own words.** Recognised standards distinguish a data gap from a significant data gap, and the distinction is the consultant's to make. **Do not assess significance yourself and do not upgrade or downgrade the characterisation.**
- **Report the undocumented historical periods with their years.** A property whose history is undocumented between 1940 and 1975 has an unassessed industrial-era window, and the years are what tell a reviewer whether that matters.
- Report inaccessible areas specifically, since an unobserved area is an unassessed area.
- **Report any recommendation to close a gap**, since it is the consultant saying the assessment is incomplete.
- Report no more than eight gaps. Where more exist, report the eight the consultant identifies as most significant and append ` and [N] further gaps`.

## Fallback rules

- Return exactly `None stated` where the consultant identifies no data gap.
- Return `Unable to determine` where the data gaps section is illegible.

## Output format

One line per gap:

`[Gap as stated] — [consultant's significance characterisation or "not characterised"]`

Return no more than 8 lines and no more than 90 words.
```

---

### 12. Regulatory Databases Reviewed

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: what the records search found, on site and nearby. **The off-site
  listings are frequently the most useful finding**, because a neighbour's plume
  can migrate onto the property.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report the regulatory database findings this assessment states.

## Applicability

- Applies where Report Type is `Phase I environmental site assessment`, `Limited Phase I or desktop review`, `Transaction screen assessment`, `Remedial investigation`, or `Compliance audit`.
- For other report types, report any database findings the report states, and otherwise return `Not applicable`.

## Include where expressly stated

- **Any listing of the subject property itself on a regulatory database, with the database name and the listing details**
- **Any off-site listing within the search radius, with the database, the distance, the direction, and the site name**
- The databases searched, and any search radius applied
- Any storage tank listing — underground or aboveground — on site or adjacent
- Any hazardous waste generator, treatment, storage, or disposal listing
- Any spill, release, or incident listing
- Any listing on a national priorities, contaminated land, or remediation register
- Any dry cleaner, fuel station, or other higher-risk historical use identified nearby
- Any listing the consultant states was unmappable or of unknown location

## Rules

- **Report a listing of the subject property separately and prominently from off-site listings.** An on-site listing is a direct finding; an off-site listing is a potential migration pathway, and the two are read differently.
- **Report the direction and distance of off-site listings where stated.** A contaminated site upgradient of the property matters far more than one downgradient, and the consultant's own gradient assessment should be reported where given.
- **Report any unmappable or orphan listing**, since a listing that could not be located may be on the property.
- Report findings as stated. **Do not assess migration potential, do not judge whether a listing affects the property, and do not count listings from a database report table.**

## Fallback rules

- Return exactly `No listings identified` where the assessment searched databases and identified none, on site or off.
- Return `Not stated` where the report does not describe its database findings.
- Return `Unable to determine` where findings are illegible.

## Output format

`On site: [listings with details, or "none"]` then one line per off-site listing:

`[Site name] — [database] — [distance and direction] — [gradient as stated or "not stated"]`

Return no more than 10 lines and no more than 100 words.
```

---

### 13. Historical Use Findings

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the property was used for before. **Historical use is the single
  best predictor of contamination**, and it is the part of a Phase I that no
  database search replaces.

```markdown
## Task

Report the historical uses of the property this assessment identifies.

## Include where expressly stated

- The chronology of uses identified, with the periods for each
- **Any industrial, manufacturing, fuel storage, dry cleaning, vehicle servicing, printing, metal working, chemical handling, agricultural, or waste-handling use**, with its period
- Any structures formerly on site, and any demolition
- **Any underground or aboveground storage tanks identified, whether in use, removed, or abandoned in place, with dates and removal evidence where stated**
- Any pits, sumps, lagoons, drains, septic systems, or wells identified
- Any fill material placed on site
- Any historical spill, release, or incident recorded
- The sources relied on for the history — aerial photographs, directories, fire insurance maps, title records, interviews — and the earliest year documented
- Any period for which no use could be determined

## Rules

- **Report the earliest year documented and any undocumented period.** The undocumented window is where unknown industrial use hides, and it pairs with the Data Gaps column.
- **Report every storage tank prominently, with its status.** A tank abandoned in place, or removed without documented closure sampling, is among the most common sources of a real finding, and **the absence of removal documentation is itself the point.**
- Report the uses and periods as stated. **Do not infer a use from a business name, do not assume a use was contaminating, and do not conclude that any historical use caused a condition.**
- Report the interview-derived history separately where the documents distinguish it, since it is the least verifiable source and often the most informative.

## Fallback rules

- Return exactly `No use of concern identified` where the assessment identified the history and found nothing of environmental concern.
- Return `Not stated` where the report does not describe the property's history.
- Return `Unable to determine` where the history is illegible or internally inconsistent.

## Output format

One line per use or feature:

`[Period] — [use or feature as stated][; status]`

then a final line: `Earliest year documented: [year]; undocumented periods: [as stated or "none"]`

Return no more than 10 lines and no more than 100 words.
```

---

### 14. Adjacent Property Concerns

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: off-site sources that could affect the property. **Contamination
  migrates**, and a neighbour's condition can create liability and cost without any
  act of the target's.

```markdown
## Task

Report the adjoining and nearby property conditions this assessment identifies as of potential concern.

## Include where expressly stated

- Each adjoining property, its current use, and its historical use where identified
- **Any adjoining or nearby use of environmental concern**, with its direction and distance
- Any known or suspected release on an adjoining property
- The consultant's statement of groundwater flow direction, and whether any off-site source is upgradient
- Any observed evidence of migration onto the property
- Any adjoining property the consultant identifies as warranting further consideration
- Any off-site source the consultant expressly concludes does not affect the property, and why

## Rules

- **Report the groundwater gradient where the consultant states it, and report the direction of each concern relative to it.** An upgradient source is a migration pathway; a downgradient one generally is not, and this is the distinction that determines whether an off-site condition matters.
- **Report the consultant's own conclusion on each off-site concern** — whether it identified the condition as a recognised environmental condition, a de minimis condition, or as not affecting the property. **Do not reach that conclusion yourself.**
- Report distances and directions as stated. Do not estimate either.
- **Note in the evidence field where the consultant states that gradient could not be determined**, since it means off-site sources cannot be ruled out.

## Fallback rules

- Return exactly `None identified` where the assessment considered adjoining properties and identified no concern.
- Return `Not stated` where the report does not address adjoining properties.
- Return `Unable to determine` where the findings are illegible.

## Output format

One line per concern:

`[Property or use] — [direction and distance] — [consultant's conclusion as stated]`

then a final line: `Groundwater gradient: [as stated or "not determined"]`

Return no more than 8 lines and no more than 85 words.
```

---

### 15. RECs Identified

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: the findings that matter. **A recognised environmental condition is the
  consultant's conclusion that a release has occurred, is occurring, or is
  materially threatened**, and each one is a candidate for further investigation,
  remediation, or a special indemnity.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report each recognised environmental condition this assessment identifies.

## Applicability

- Applies where Report Type is `Phase I environmental site assessment`, `Limited Phase I or desktop review`, or `Transaction screen assessment`.
- For `Phase II investigation`, `Remedial investigation`, `Remediation or closure report`, and `Vapour intrusion assessment`, report any condition the report identifies using its own terminology, since these reports test rather than screen.
- For `Asbestos or hazardous materials survey`, `Compliance audit`, and `Geotechnical or soils report`, return `Not applicable`.

## Rules

- **Report each recognised environmental condition using the consultant's own designation.** Recognised standards distinguish a recognised environmental condition from a controlled one, a historical one, and a de minimis condition, and the designations carry defined meanings. **Do not translate between them, do not create a designation the report did not use, and do not upgrade a de minimis condition to a recognised one.**
- For each condition, report what it is, where on the site, the medium affected, and the suspected source, in twelve words or fewer.
- **Report the consultant's recommendation for each condition specifically** — further assessment, sampling, no further action, or monitoring.
- Report any condition the consultant states relates to an off-site source.
- Report each condition separately. **Do not consolidate two conditions into one line and do not count them into a total.**
- **Do not assess severity, estimate cost, conclude that remediation is required, or state whether a condition creates liability.** All of those are for the reviewer and the environmental consultant.

## Fallback rules

- Return exactly `None identified` where the assessment identifies no recognised environmental condition. **This is a meaningful positive finding**, and it should be read together with the Non-Scope Items and Data Gaps columns rather than alone.
- Return `Not applicable` where the report type does not use the concept.
- Return `Unable to determine` where the findings are illegible or the designations cannot be read.

## Output format

One line per condition:

`REC [N] — [condition, location, medium, suspected source] — recommendation: [as stated]`

Return no more than 8 lines and no more than 100 words. Do not include an assessment of your own.
```

---

### 16. Controlled and Historical RECs

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: past conditions and conditions left in place under controls.
  **A controlled condition is a continuing obligation, not a closed matter** — it
  depends on the controls remaining in force, and the buyer inherits the duty to
  maintain them.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report each controlled recognised environmental condition, historical recognised environmental condition, and de minimis condition this assessment identifies.

## Applicability

- Applies where Report Type is `Phase I environmental site assessment`, `Limited Phase I or desktop review`, `Transaction screen assessment`, `Remedial investigation`, or `Remediation or closure report`.
- For other report types, report any such condition the report identifies, and otherwise return `Not applicable`.

## Rules

- **Report controlled conditions separately from historical ones and from de minimis ones, using the consultant's own designations.**
- **For each controlled condition, report the control relied on** — an activity and use limitation, a deed restriction, an environmental covenant, an engineered cap or barrier, a groundwater monitoring programme, or a vapour mitigation system — **and any continuing obligation attached to it, including monitoring, reporting, and maintenance.** These are the obligations that follow the land to the buyer, and they are frequently the largest continuing environmental cost on an otherwise clean site.
- **For each controlled condition, report whether the report states the controls are in place and being complied with**, and whether any regulatory closure or no-further-action determination was obtained, with its date.
- For each historical condition, report what it was, when it was addressed, and the basis on which the consultant concluded it no longer requires action.
- For de minimis conditions, report them briefly. **Do not upgrade a de minimis condition to a recognised one.**
- **Report any recorded land use restriction with its recording reference where stated**, since it also appears in the Real Estate — Owned Property table's restrictive covenants column and the two should agree.
- Do not assess whether any control is adequate or whether any closure remains valid.

## Fallback rules

- Return exactly `None identified` where the assessment identifies no controlled, historical, or de minimis condition.
- Return `Not applicable` where the report type does not use these concepts.
- Return `Unable to determine` where the designations cannot be read.

## Output format

One line per condition:

`[Designation] — [condition] — control: [as stated]; continuing obligation: [as stated or "none"]; closure: [as stated or "none"]`

Return no more than 8 lines and no more than 100 words.
```

---

### 17. Vapour Encroachment

- Native type: Free Response
- Upstream: `@Report Type`
- Downstream: none
- Purpose: vapour migration into buildings. **A distinct pathway assessed under its
  own standard**, frequently excluded from older Phase I work, and the exposure
  route most likely to affect occupants directly.

```markdown
## Established result

- Report Type: @Report Type

## Task

Report what this assessment states about vapour encroachment or vapour intrusion.

## Applicability

- Applies where Report Type is `Phase I environmental site assessment`, `Limited Phase I or desktop review`, `Vapour intrusion assessment`, `Phase II investigation`, or `Remedial investigation`.
- For other report types, report any statement about vapour, and otherwise return `Not applicable`.

## Include where expressly stated

- Whether a vapour encroachment screen or assessment was performed, and to what standard
- **Whether vapour encroachment was expressly excluded from the scope.** Older Phase I work frequently excludes it, and its exclusion means the pathway was not assessed at all
- Any vapour encroachment condition identified, and the source
- Any on-site or nearby source of chlorinated solvents or petroleum vapours identified
- Any sampling performed — soil vapour, sub-slab, or indoor air — and the results as stated
- Any comparison to screening levels the report makes, with the levels as stated
- Any vapour mitigation system present or recommended
- Any occupied building identified as potentially affected
- Any recommendation for further vapour assessment

## Rules

- **Report an express exclusion of vapour from the scope as prominently as a finding.** A Phase I that did not screen for vapour says nothing about it, and on a site with historical dry cleaning or solvent use that is a substantial unassessed pathway.
- **Report any occupied building identified as potentially affected**, since vapour intrusion is the pathway with direct occupant exposure and it can require immediate action rather than long-term monitoring.
- Report concentrations and screening levels exactly as stated. **Do not compare results to any standard yourself and do not calculate an exceedance.**
- Report the consultant's conclusion as stated. Do not reach one.

## Fallback rules

- Return exactly `Screened, no condition identified` where a vapour screen was performed and identified nothing.
- Return `Not addressed` where the report type would normally screen for vapour and says nothing about it.
- Return `Not applicable` where the report type does not address vapour.
- Return `Unable to determine` where the findings are illegible.

## Output format

`Screened: [yes, to [standard] | expressly excluded | Not addressed]; condition: [as stated or "none"]; source: [as stated]; sampling: [media and results as stated or "none"]; mitigation: [as stated or "none"]; buildings affected: [as stated or "none"]`

Return no more than 85 words.
```

---

### 18. Sampling Results

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the analytical data, where any was collected. **This is the only column
  in the workstream that reports measured facts rather than professional
  opinion**, and it is what any remediation estimate is built from.

```markdown
## Task

Report the sampling and analytical results this report states.

## Applicability

- Applies wherever the report states that samples were collected and analysed, whatever its type.
- Where no sampling was performed, return exactly `No sampling performed`. **For a Phase I this is the expected answer**, since a Phase I does not sample.

## Include where expressly stated

- The media sampled, and the number of samples per medium
- **Each analyte or compound detected above a stated screening or regulatory level, with the concentration, the units, the level compared to, and the sample location**
- The screening or regulatory levels applied, named exactly as the report names them
- Any exceedance the report identifies, using the report's own words
- The vertical and lateral extent of any contamination the report delineates
- Whether the extent was fully delineated or remains open
- **Any statement that contamination extends or may extend off site**
- Any groundwater depth, flow direction, and gradient stated
- Any laboratory quality-control issue, holding-time exceedance, or data qualifier the report notes
- Any analyte tested for and not detected, where the report highlights it

## Rules

- **Report concentrations exactly as stated with their units. Do not convert units, do not calculate an exceedance factor, and do not compare a result to a standard the report did not apply.**
- **Report whether the extent of contamination was delineated.** Undelineated contamination cannot be costed, and an open extent is the single most important qualifier on any remediation estimate.
- **Report any statement of off-site migration prominently**, since it converts a site issue into a third-party liability.
- **Report any data qualifier or quality-control issue**, since it bears on whether the results can be relied on.
- Report no more than ten exceedances. Where more exist, report the ten highest as stated and append ` and [N] further exceedances`.
- **Do not assess risk, do not conclude that remediation is required, and do not estimate a volume or a cost.**

## Fallback rules

- Return `No sampling performed` where the report states none.
- Return `Not stated` where the report states sampling was performed but does not give results, **which usually means the laboratory appendix was not produced.**
- Return `Unable to determine` where the results are illegible or internally inconsistent.

## Output format

`Media sampled: [as stated]; levels applied: [as named]` then one line per exceedance:

`[Analyte] — [concentration and units] — [level compared to] — [location]`

then a final line: `Extent delineated: [yes | no | partially]; off-site migration: [as stated or "not addressed"]`

Return no more than 12 lines and no more than 110 words.
```

---

### 19. Recommendation

- Native type: Classify
- Configured options, in UI order: `No further action recommended`, `Further assessment recommended`, `Sampling recommended`, `Remediation recommended`, `Monitoring recommended`, `Regulatory notification recommended`, `Multiple recommendations`, `None stated`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: what the consultant said should happen next, as a filterable value.
  **Every row that is not `No further action recommended` is an open item.**

```markdown
## Task

Classify the consultant's principal recommendation. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits, since the order runs from most to least onerous.

1. `Regulatory notification recommended`: the consultant recommends reporting a condition to a regulator. **The most consequential recommendation**, because notification usually starts a regulatory process that cannot be stopped, and whether and when to notify is a legal decision with a timetable.
2. `Remediation recommended`: the consultant recommends remedial action.
3. `Sampling recommended`: the consultant recommends intrusive sampling to test an identified condition.
4. `Further assessment recommended`: the consultant recommends additional non-intrusive assessment, including closing a data gap or extending scope to a non-scope item.
5. `Monitoring recommended`: the consultant recommends ongoing monitoring without further investigation or remediation.
6. `Multiple recommendations`: two or more of the above apply to different conditions and none clearly predominates. **Report each in the evidence field.**
7. `No further action recommended`: the consultant expressly recommends no further action.

**Report in the evidence field any recommendation attached to a specific condition**, and any recommendation the consultant marks as urgent or time-sensitive.

**Do not infer a recommendation the consultant did not make.** Where a condition is identified with no recommendation attached, use `None stated` and note the condition — a finding with no recommendation is itself something the reviewer needs to see.

## Fallback rules

- Use `None stated` where the report reaches conclusions but makes no recommendation.
- Use `Unable to determine` where the recommendations section is illegible or inconsistent.

## Output format

Return only the exact configured option and no explanation.
```

---

### 20. Cost Estimate Stated

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: any figure the consultant put on the work. **Reported because it
  anchors the discussion, and heavily qualified because it is almost always
  preliminary.**

```markdown
## Task

Report any cost estimate this report states for further assessment, remediation, or monitoring.

## Include where expressly stated

- The estimate, with the currency, and what work it covers
- Whether it is a point estimate, a range, or an order-of-magnitude figure
- **The basis and the assumptions stated**, particularly whether it assumes a remediation standard, an end use, or a delineated extent
- Any express statement that the estimate is preliminary, indicative, or subject to further investigation
- Any exclusion from the estimate — professional fees, regulatory oversight costs, disposal costs, business interruption, or third-party claims
- Any separate estimate for monitoring or long-term operation and maintenance, with its duration
- Any statement of the period over which costs would be incurred
- Any contingency applied, as a percentage

## Rules

- **Report the estimate as stated and report every qualification with it.** An estimate produced before the extent of contamination is delineated is not a cost, and reporting the figure without the qualification is the most misleading thing this table could do.
- **Report any long-term monitoring or operation and maintenance cost separately, with its duration.** A modest annual monitoring cost over thirty years is often larger in total than the remediation itself, and the duration is what makes that visible.
- **Report the exclusions**, since they are frequently where most of the real cost sits.
- Report figures as stated. **Do not total components, do not annualise, do not apply a contingency, do not discount, and do not produce a range from a point estimate.**

## Fallback rules

- Return exactly `None stated` where the report states no cost estimate. **This is the expected answer for a Phase I** and it is not a gap; costing follows delineation.
- Return `Unable to determine` where estimates conflict or are illegible.

## Output format

`Estimate: [figure or range] [currency] for [scope]; basis: [as stated]; qualifications: [as stated]; exclusions: [as stated or "none"]; monitoring: [figure and duration or "none"]`

Return no more than 80 words. Do not include any figure you calculated.
```

---

### 21. Referenced but Not Produced

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

List every document relating to this property or assessment that the documents in this unit refer to and that is not present.

## Scope

- **Include appendices, laboratory analytical reports, boring logs, and figures listed as attached but not present.**
- **Include any prior or subsequent assessment referenced** — an earlier Phase I, a Phase II the report recommends, a remediation report, or a closure determination.
- Include any reliance letter referenced as issued or available.
- Include the engagement letter, proposal, or scope of work referenced, since the reliance and liability terms usually sit there.
- Include any regulatory database report referenced but not attached.
- Include any environmental permit, registration, or notification referenced for the site.
- **Include any recorded land use restriction, environmental covenant, or activity and use limitation referenced.**
- Include any regulatory correspondence, order, or closure letter referenced.
- Include any tank removal or closure report referenced.
- Include any asbestos, lead, or hazardous materials survey referenced.
- Include any operation and maintenance plan or monitoring report referenced for a control in place.
- Exclude published standards, guidance, and screening-level tables.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a laboratory report or analytical appendix is absent, add `; analytical data missing`.** The summary cannot be verified and no remediation estimate can rest on it. Filter these first.
- **Where a recommended further assessment is referenced and no such report is in the unit, add `; recommended work unevidenced`.** Either the work was never done or the report was not produced, and the two have very different consequences.
- **Where a recorded land use restriction is referenced and absent, add `; continuing obligation unreadable`.** The restriction binds the land and its terms are the obligation the buyer inherits.
- Where a tank closure report is absent, add `; tank closure unevidenced`.
- Where an engagement letter or reliance letter is absent, add `; reliance terms missing`.
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
| **Reliance obtained or obtainable** | Obtained / In negotiation / Refused / Not required |
| **Report currency adequate** | Yes / Update required / New assessment required |
| **Statutory defence available** | Likely / Doubtful / Not applicable / Unassessed |
| **Further work required** | None / Scoped (specify) / Commissioned / Unassessed |
| **Cost estimate** | Free text |
| **Special indemnity candidate** | Yes / No / Unassessed |
| **Escrow or holdback candidate** | Yes / No / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** Environmental rows are few and each carries a large,
non-diversifiable, and often uninsurable exposure.

### Reconciliation work that never belongs in a column

- **Site coverage, both directions.** Every property in the Real Estate tables and
  every operating location on the site list against these rows. **An owned or
  formerly owned industrial site with no assessment is the finding**, and it is
  invisible from inside any single row. Include former sites: liability attaches to
  past ownership and operation in many regimes, and the seller may hold sites it no
  longer occupies.
- **The reliance programme.** Every row where reliance is excluded, unaddressed, or
  runs only to the seller. Reliance letters are routinely obtainable for a fee and
  the negotiation should start early, because it also determines whether the
  buyer's own inquiry standard is met.
- **Currency refresh.** Every `[over 180 days]` and `[over 1 year]` flag for
  material sites, with a decision on whether to update or recommission. **The
  180-day question is legal, not technical** — the findings may be perfectly sound
  while the defence is unavailable.
- **Non-scope closure.** Every non-scope item across every row, aggregated by
  property. **Asbestos over a pre-restriction building with no survey is the most
  common material gap in this workstream**, and a clean Phase I does nothing to
  address it.
- **Delineation and costing.** Every row with sampling results where the extent is
  undelineated or open, referred to a consultant for scoping and costing. **No
  figure from this table is a cost estimate**, and the long-term monitoring
  duration frequently dominates the total.
- **Continuing obligations register.** Every controlled condition, recorded land
  use restriction, monitoring programme, and engineered control, with its
  maintenance and reporting duties, a named owner, and cross-references to the Real
  Estate restrictive covenants and the Environmental — Permits table.
- **Off-site sources.** Every upgradient concern, assessed for migration potential
  by a consultant. **A neighbour's plume can create cost and liability without any
  act of the target's**, and it is also a potential recovery route against a third
  party.
- **Insurance.** Every material condition against the Insurance table's
  environmental and pollution legal liability rows, and against the known-conditions
  exclusion. **Known conditions are typically excluded**, which is precisely why
  identified conditions drive indemnity and escrow rather than insurance.

---

## Test set

Where the target holds no property with environmental exposure, record the table
as built and empty. The following assumes assessments exist.

- [ ] Full Phase I to a current standard with no recognised environmental conditions
- [ ] Phase I identifying two recognised environmental conditions with sampling recommended
- [ ] Phase I identifying a controlled condition with an activity and use limitation
- [ ] Phase I identifying a historical condition with a closure letter referenced
- [ ] Phase I identifying a de minimis condition only
- [ ] Phase I to a superseded standard version
- [ ] Phase I omitting the site visit
- [ ] Transaction screen assessment
- [ ] Phase I dated eight months before the as-of date
- [ ] Phase I dated four years before the as-of date
- [ ] Phase I where fieldwork predates the report by two months
- [ ] Phase I expressly excluding one parcel of a multi-parcel site
- [ ] Phase I listing asbestos, lead, radon, and mould as non-scope items
- [ ] Phase I over a 1960s industrial building with asbestos out of scope
- [ ] Phase I with a significant data gap in the 1940 to 1975 history
- [ ] Phase I noting inaccessible areas due to occupied tenancies
- [ ] Phase I with the subject property listed on a regulatory database
- [ ] Phase I with an upgradient dry cleaner within 500 feet
- [ ] Phase I with an unmappable orphan listing
- [ ] Phase I identifying an underground storage tank abandoned in place
- [ ] Phase I identifying a tank removed with no closure sampling documented
- [ ] Phase I expressly excluding vapour encroachment
- [ ] Phase I with a vapour encroachment condition identified
- [ ] Phase II with exceedances above screening levels and delineated extent
- [ ] Phase II with exceedances and undelineated extent
- [ ] Phase II with laboratory appendix not produced
- [ ] Phase II with data qualifiers and holding-time exceedances noted
- [ ] Phase II stating contamination extends off site
- [ ] Remediation report with a no-further-action determination
- [ ] Remediation report with an engineered cap and an operation and maintenance plan
- [ ] Vapour intrusion assessment with sub-slab sampling and a mitigation system
- [ ] Asbestos management survey over an occupied building
- [ ] Asbestos pre-demolition survey
- [ ] Compliance audit reviewing permits rather than contamination
- [ ] Report addressed to the seller with reliance expressly excluded
- [ ] Report with a reliance letter extending reliance to a purchaser
- [ ] Report with a liability cap at the fee level
- [ ] Report with a confidentiality restriction preventing disclosure to a lender
- [ ] Internally prepared environmental review
- [ ] Unsigned draft Phase I
- [ ] Report with no environmental professional declaration
- [ ] Report with a remediation cost range and stated exclusions
- [ ] Report with a thirty-year monitoring cost stated separately
- [ ] Report recommending regulatory notification
- [ ] Report identifying a condition with no recommendation attached
- [ ] Report with an errata correcting a conclusion
- [ ] Unit mistakenly containing two reports for different sites

Then test the dependencies: change `Report Type` from
`Phase I environmental site assessment` to `Asbestos or hazardous materials
survey` and confirm `RECs Identified`, `Controlled and Historical RECs`, and
`Vapour Encroachment` move to `Not applicable` while `Standard Applied` and
`Scope Inclusions` re-run against the survey rules. Change
`Preparer and Credentials` from external to internal and confirm
`Reliance Parties` returns `Not applicable` and `Reliance Transferable` follows.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
