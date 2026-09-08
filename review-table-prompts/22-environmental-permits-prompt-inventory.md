# Prompt Inventory — Environmental: Permits

Table 22 of the POC. Second of three Environmental tables.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Environmental`
- Review unit: **one permit, authorisation, or registration** — the instrument
  itself, any renewal, modification, or variation, the conditions schedule, and any
  transfer approval produced for it
- Grouping used: **yes**, typically 1–5 documents per unit
- Intended reviewers and downstream use: environmental and corporate/M&A teams;
  feeds the closing conditions and regulatory calendar, the compliance obligations
  register, and the coverage register
- Inventory version: v1.0

### Why environmental permits are not Regulatory permits

They sit in their own table for two reasons:

1. **Transferability behaves differently.** Many environmental permits attach to a
   **site or an installation** rather than to a legal entity, and several regimes
   require a formal transfer application even in a share purchase where the holder
   does not change. Others transfer automatically. The variation is wide enough
   that the question needs its own column with its own option set.
2. **Financial assurance.** Waste, landfill, extraction, and storage permits
   commonly require a bond, letter of credit, or trust to cover closure and
   post-closure obligations. **These are long-tail liabilities with a funding
   requirement that can survive for decades**, and no other permit table in the set
   needs to ask about them.

### The relationship to Assessments and Enforcement

- A permit condition breached is an **Enforcement** row.
- A permit governing a site with contamination is read alongside the
  **Assessments** row for that site.
- A monitoring obligation imposed by a permit and a monitoring obligation imposed
  by a controlled environmental condition are different obligations on the same
  site, and both belong in the continuing obligations register.

## Assumptions to confirm before running

1. One row is one permit for one site held by one entity. The same permit type at
   three facilities is three rows.
2. **Operating without a required permit is not a row here** — there is no permit
   to be the subject. It is an Enforcement row where a regulator has raised it, and
   a coverage-register row where the reviewer identifies the gap.
3. Non-environmental licences are in the Regulatory workstream.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

18 Harvey columns plus 8 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side environmental diligence on the target group listed below. This table reviews environmental permits, authorisations, and registrations.

One row is one permit, authorisation, or registration: the instrument itself, any renewal, modification, or variation, the conditions schedule, and any transfer approval produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the permit or the regulator.
- **Report what the documents state. Do not supply a requirement, a limit, a transfer rule, or a review period from the governing legislation, even where it is well known.** A requirement not in the documents is `Not addressed` here, and the reviewer establishes it from the law.
- **A permit states the position as at its own date.** Nothing in a data room updates it. Report the status the documents show and identify the document.
- **Do not determine whether this transaction requires a transfer application, whether the permit is adequate for the site's operations, or whether any condition is being complied with.** All three are for the reviewer.
- Report limits, quantities, and figures exactly as stated, with their units. Do not calculate, total, or convert.
- Use entity, facility, and authority names exactly as printed.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Permit Type
  Permittee Entity
  Issuing Authority
  Facility or Site
  Permit Number

Stage 2 — Validity
  Documents in Unit ──→ Status
                        Modification History
                        Referenced but Not Produced
  Permittee Entity ──→ Permittee Match
  Issue Date, Expiry Date
  Expiry Date ──→ Renewal Requirements

Stage 3 — Substance
  Permit Type ──→ Permitted Activity and Limits
                  Financial Assurance
  Monitoring and Reporting Obligations
  Conditions and Compliance Schedule

Stage 4 — Transaction
  Transferability on Change of Control ──→ Transfer Requirements
  Prior Transfer Approvals
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Status; Modification History; Referenced but Not Produced | v1.0 | draft |
| 2 | Permit Type | Free Response | — | Permitted Activity and Limits; Financial Assurance | v1.0 | draft |
| 3 | Permittee Entity | Free Response | — | Permittee Match | v1.0 | draft |
| 4 | Permittee Match | Classify | @Permittee Entity | — | v1.0 | draft |
| 5 | Issuing Authority | Free Response | — | — | v1.0 | draft |
| 6 | Facility or Site | Free Response | — | — | v1.0 | draft |
| 7 | Permit Number | Free Response | — | — | v1.0 | draft |
| 8 | Issue Date | Date | — | — | v1.0 | draft |
| 9 | Expiry Date | Date | — | Renewal Requirements | v1.0 | draft |
| 10 | Renewal Requirements | Free Response | @Expiry Date | — | v1.0 | draft |
| 11 | Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 12 | Modification History | Free Response | @Documents in Unit | — | v1.0 | draft |
| 13 | Permitted Activity and Limits | Free Response | @Permit Type | — | v1.0 | draft |
| 14 | Conditions and Compliance Schedule | Free Response | — | — | v1.0 | draft |
| 15 | Monitoring and Reporting Obligations | Free Response | — | — | v1.0 | draft |
| 16 | Financial Assurance | Free Response | @Permit Type | — | v1.0 | draft |
| 17 | Transferability on Change of Control | Classify | — | Transfer Requirements | v1.0 | draft |
| 18 | Transfer Requirements | Free Response | @Transferability on Change of Control | — | v1.0 | draft |
| 19 | Prior Transfer Approvals | Free Response | — | — | v1.0 | draft |
| 20 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

20 columns — two more than estimated. `Modification History` and
`Prior Transfer Approvals` earned their place: a permit varied three times is not
the permit as originally issued, and a prior transfer file is the best available
evidence of what the regulator will actually require this time.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Status`, `Modification History`, `Referenced but Not Produced`
- Purpose: inventory the permit file, and record whether the conditions schedule
  is present.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the permit or authorisation instrument, the original application and any supporting submission, renewal certificates, modifications, variations, and endorsements, the conditions schedule, any transfer or change-of-control approval, any financial assurance instrument, and any regulator confirmation of status.
- Treat schedules and conditions annexed to the instrument as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where none is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated or issue date.
- State the function as one of `Permit`, `Application`, `Renewal`, `Modification or variation`, `Conditions schedule`, `Transfer approval`, `Financial assurance`, `Status confirmation`, or `Other`.
- **Where the conditions schedule is absent, state that.** The conditions are the obligations the buyer inherits and they cannot be read from the face of a permit certificate.
- **Where a modification is present, note in the evidence field what it changed.** A varied limit or condition supersedes the original and the row must report the current position.
- Where a document relates to a different permit, facility, or entity, still list it and append ` [relates to [permit, facility, or entity]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 10 lines and no more than 90 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Permit Type

- Native type: Free Response
- Upstream: none
- Downstream: `Permitted Activity and Limits`, `Financial Assurance`
- Purpose: what the authorisation is, named as the regulator names it.

Free Response rather than Classify because environmental permit nomenclature is
jurisdiction-specific and unbounded: a controlled vocabulary would either be
enormous or force most rows into `Other`.

```markdown
## Task

State the type of environmental permit, authorisation, or registration this review unit documents.

## Rules

- **Report the type exactly as the regulator names it**, for example `NPDES Individual Permit`, `Title V Operating Permit`, `RCRA Part B Hazardous Waste Permit`, `Environmental Permit (Installations)`, `Waste Carrier Registration`, `Air Quality Minor Source Permit`. Do not translate it into a generic category and do not normalize across jurisdictions.
- **Report the environmental medium or media the permit regulates** — air, water discharge, stormwater, wastewater, drinking water, hazardous waste, solid waste, storage tanks, extraction or abstraction, emissions trading, noise, or contaminated land.
- Report any class, category, tier, or schedule designation, since it usually determines both the conditions and the transfer requirements.
- **Report whether the instrument is a permit, a registration, a notification, an exemption, or a general permit or permit-by-rule.** The distinction matters: **a general permit or registration is commonly obtained by simple notification and transfers easily, while an individual permit is negotiated, site-specific, and frequently requires a formal transfer application.**
- Report any endorsement or additional authorisation added by a later document.

## Fallback rules

- Return `Unable to determine` where the documents do not identify what the authorisation is.

## Output format

`[Type as named]; medium: [as stated]; class: [as stated or "none"]; instrument: [individual permit | general permit | registration | notification | exemption]`

Return no more than 45 words.
```

---

### 3. Permittee Entity

- Native type: Free Response
- Upstream: none
- Downstream: `Permittee Match`
- Purpose: who holds the permit, exactly as recorded.

```markdown
## Task

State the entity or person named as the permittee, operator, or holder.

## Rules

- Report the name **exactly as printed**, including entity suffix, punctuation, and any misspelling or outdated form. **Do not correct, normalize, or update it.** An error in the permit register is a finding, and correcting it here hides it.
- **Report the capacity in which the holder is named** — owner, operator, or both. **The distinction is central in environmental regulation**, because obligations and liability commonly attach to the operator, and a permit naming the target as operator of a site it does not own creates obligations without control.
- Where a later document records a change of permittee or a name change, report the current holder and append ` (changed from [prior name], [YYYY-MM-DD])`.
- **Where the permit names a facility, installation, or site rather than a legal entity, report it as printed and add `(site-based permit)`.** Site-based permits behave differently on a transaction and the Transferability column depends on knowing this.
- Where the permit is held by an individual, report the name and add `(individual holder)`.
- Where more than one holder is named, list each with its capacity.

## Fallback rules

- Return `Not stated` where the documents name no permittee.
- Return `Unable to determine` where the name is illegible.

## Output format

`[Name exactly as printed] — [capacity as stated]` per holder, with any qualifier appended. Return no more than 40 words.
```

---

### 4. Permittee Match

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Held under a former name`, `Held by an individual`, `Held by a third party`, `Site-based, no entity named`, `Held by seller or an affiliate outside the group`, `No permittee named`, `Unable to determine`
- Upstream: `@Permittee Entity`
- Downstream: none
- Purpose: whether the permit sits inside the acquired group.

**The `Held by seller or an affiliate outside the group` state is the one to look
for.** In a carve-out, a permit held by the seller's group covering a site being
sold has to be transferred or reapplied for, and until it is the site may not be
lawfully operable by the buyer.

```markdown
## Established result

- Permittee entity: @Permittee Entity

Use this result and the target group list in the Table Instructions. Confirm the name against the documents.

## Task

Classify the relationship between the named permittee and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No permittee named`: Permittee Entity returned `Not stated`.
2. `Site-based, no entity named`: the permit attaches to a facility, installation, or site without naming a legal entity as holder. Report the site in the evidence field.
3. `Held by an individual`: the permittee is a natural person. **A personally held permit does not pass with a share sale**, and where that individual is not remaining the authorisation may be lost.
4. `Held by seller or an affiliate outside the group`: the permittee is the selling shareholder, its parent, or an affiliate that is not being acquired. **The most consequential state in this column** — the permit does not come with the business and must be transferred or reapplied for.
5. `Held under a former name`: the named permittee matches a prior name of a target entity as disclosed in the documents in this unit.
6. `Held by a third party`: the permittee is an entity that is neither a target entity, nor a former name of one, nor the seller's group. **This may mean the site operates under a contractor's or a landlord's permit**, which is a distinct arrangement the reviewer must understand.
7. `Matches with name variance`: the named permittee is the same entity as one on the target group list but differs in form.
8. `Matches a target entity exactly`: the name is character for character a name on the target group list.

**Do not resolve a variance by assuming.** Where the name is similar but could be a different entity, use `Held by a third party` and note the similarity in the evidence field.

## Fallback rules

- Use `Unable to determine` where the name is illegible or Permittee Entity returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Issuing Authority

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: who issued it and who must be applied to. The join key to the
  Environmental — Enforcement table.

```markdown
## Task

State the authority that issued this permit.

## Rules

- Report the authority exactly as printed, including the region, district, or programme office where stated.
- **Report the level — federal or national, state or provincial, regional, or local — since it determines whose approval a transfer needs**, and environmental permitting is commonly delegated to a state or regional body operating a federal programme.
- Where the permit is issued under a delegated programme, report both the issuing body and the programme it operates under.
- Report any named permit writer, case officer, or programme contact by role rather than by name.
- Report any filing address, portal, or system identified for applications and reports, in the evidence field, since it is the practical route for the transfer application and the periodic returns.
- **Where more than one authority regulates the same activity at the site — a state agency and a local air district, for example — report each and label its role.** Two authorities means two transfer processes.

## Fallback rules

- Return `Unable to determine` where the documents do not identify the issuing authority.

## Output format

`[Authority as printed][ — [office or region]]; level: [as stated]`, with any additional authority labelled.

Return no more than 45 words.
```

---

### 6. Facility or Site

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the permit covers. **The join key to the Real Estate tables, the
  Assessments table, and the site list.**

```markdown
## Task

State the facility, installation, or site this permit covers.

## Include where expressly stated

- The facility name and the street address, as printed
- Any facility, installation, or site identifier the regulator assigns
- **Any specific unit, process, stack, outfall, tank, or activity the permit covers**
- Any part of the site expressly excluded
- The coordinates, parcel identifier, or legal description where stated
- Any statement that the permit covers multiple locations

## Rules

- Report the address exactly as printed. **Do not standardize or correct it**, since it is the join key to the Real Estate and Assessments tables.
- **Report the regulator's facility identifier where given.** Environmental regulators maintain facility registries and the identifier is what a compliance history search is run against.
- **Report the specific permitted units, outfalls, or emission points where the permit enumerates them.** A permit covering three of five process lines is a partial authorisation, and the enumeration is the only place that shows.
- Report any excluded area or activity.
- **Where the permit covers a site the target leases rather than owns, report that where stated**, since the permit obligations and the landlord's interest then interact.
- Do not compare the permitted units to the site's actual operations.

## Fallback rules

- Return `Not stated` where the permit does not identify a facility or site.
- Return `Unable to determine` where the description is illegible or inconsistent.

## Output format

`[Facility name], [address as printed][; regulator ID: [as stated]]; units covered: [as stated]; excluded: [as stated or "none"]`

Return no more than 60 words.
```

---

### 7. Permit Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the register identifier, which is what a status check and a transfer
  application are run against.

```markdown
## Task

State the permit, authorisation, or registration number.

## Rules

- **Report the number exactly as printed, including any prefix, suffix, slashes, spaces, and revision or version suffix. Do not reformat.** Status checks and transfer applications fail on reformatted numbers.
- Where the permit carries more than one identifier — a permit number and a facility registry identifier, or a state number and a federal programme number — report each and label it.
- **Where a modification or renewal issued a revised number or a version suffix, report the current identifier and append ` (previously [number])`.** Environmental permits are commonly renumbered on modification and the old number will not find the current permit.
- Where the permit is a general permit or registration under a numbered rule, report both the registration number and the rule or general permit reference.

## Fallback rules

- Return `Not stated` where no number appears.
- Return `Unable to determine` where numbers conflict or are illegible.

## Output format

`[Label] [number]` per identifier, separated by semicolons, with any qualifier appended. Return no more than 30 words.
```

---

### 8. Issue Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the authorisation began, which bears on the permit cycle and on
  how long the site has been regulated.

```markdown
## Task

Identify the date this permit was originally issued.

## Date-selection hierarchy

1. Use an original issue or effective date the documents state for the permit.
2. If none, use the issue date printed on the earliest permit document in the unit.
3. If neither, use the effective date of the earliest authorisation document in the unit.

## Excluded dates

- The date of a renewal or a modification, where an original issue date is stated. **Report the most recent renewal or modification date in the evidence field**
- The date of the application
- The date of a conditions schedule issued separately
- The date of a status confirmation or register extract
- File name and metadata dates, and printing and scan dates

## Rules

- **Report the original issue date, not the current certificate's date.** Where only the current permit is present with a recent issue date and no original, report that date and note in the evidence field that no original is available.
- Where the permit was first issued as a different instrument type — a registration later replaced by an individual permit — report the date of the current instrument and note the earlier one.
- **Note in the evidence field the date of the most recent modification**, since it is the date from which the current conditions run and it is what the Modification History column develops.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no issue date can be selected.
```

---

### 9. Expiry Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: none
- Downstream: `Renewal Requirements`
- Purpose: when the permit lapses. **Operating on a lapsed environmental permit is
  usually an offence**, not an irregularity.

```markdown
## Task

Identify the date this permit expires.

## Rules

- Report the expiry, valid-until, or review date stated on the most recent permit or renewal in the unit.
- **Where the permit continues indefinitely subject to periodic review, fees, or returns, return `Not applicable — continuous`** and report the review, fee, or return obligation in Renewal Requirements. **Many environmental permits do not expire but do lapse for non-payment or non-submission**, and that is a different mechanism with the same consequence.
- Where the documents state a term rather than a date, report the resulting date only if a document states it. Do not calculate.
- Compare the reported date to the diligence as-of date and flag it:
  - already passed: append ` [expired on record]`
  - within three months: append ` [expires within 3 months]`
  - within twelve months: append ` [expires within 12 months]`
- **Where `[expired on record]` applies and no renewal appears in the unit, this is a live compliance finding.** Note in the evidence field any administrative continuance or timely-renewal provision the documents state, under which a permit continues in force where a renewal application was filed on time — **that provision is frequently the difference between an expired permit and an unlawful operation**, and its existence should be reported rather than assumed.

## Fallback rules

- Return `Not stated` where the permit is of a kind that expires and no date appears.
- Return `Unable to determine` where dates conflict.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or `Not applicable — continuous`.
```

---

### 10. Renewal Requirements

- Native type: Free Response
- Upstream: `@Expiry Date`
- Downstream: none
- Purpose: what has to be done to keep the permit, and how far ahead. **A renewal
  falling in the deal period may have to be filed by the seller and may itself
  disclose the transaction.**

```markdown
## Established result

- Expiry date: @Expiry Date

## Task

Report what is required to renew or maintain this permit.

## Include where expressly stated

- **The renewal application deadline, and how far before expiry it falls.** Environmental renewal deadlines are commonly six months or more ahead, which means a permit expiring after closing may need its renewal filed before it
- **Any timely-renewal, administrative continuance, or deemed-continuation provision** permitting operation while a renewal is pending
- The regulator's stated processing time for a renewal
- Any requirement to submit monitoring data, emissions inventories, or compliance certifications with the renewal
- Any requirement to update site, process, or ownership information on renewal. **This is where a renewal can itself disclose the transaction**
- Any public notice, consultation, or comment period the renewal triggers
- Any renewal fee
- Any requirement to demonstrate continued compliance, or to address outstanding enforcement, as a condition of renewal
- Any annual fee, annual return, or periodic report required to prevent lapse where the permit does not expire
- Any opportunity the regulator has on renewal to impose new or stricter conditions

## Rules

- **Report the possibility of new conditions on renewal prominently.** A renewal is frequently the regulator's opportunity to tighten limits to current standards, and **an old permit with generous legacy limits may not be renewable on the same terms** — which is a forward cost the buyer inherits.
- **Report any public notice or comment requirement**, since it makes the renewal visible and can attract objections.
- **Report any requirement to resolve outstanding enforcement before renewal**, since it links this row to the Enforcement table and can convert a minor breach into a permit risk.
- Report deadlines and periods as stated. Do not calculate a filing date.

## Fallback rules

- Return `Not addressed` where the documents state no renewal or maintenance requirement.
- Return `Not applicable` where the permit is one-off and requires no maintenance.
- Return `Unable to determine` where provisions conflict or are illegible.

## Output format

`Deadline: [as stated]; continuance while pending: [as stated or "Not addressed"]; processing time: [as stated or "Not addressed"]; submissions required: [brief]; ownership update: [required | Not addressed]; public notice: [as stated or "none"]; new conditions possible: [as stated or "Not addressed"]`

Return no more than 85 words.
```

---

### 11. Status

- Native type: Classify
- Configured options, in UI order: `Active`, `Active with compliance schedule`, `Administratively continued`, `Pending or in application`, `Suspended`, `Modified or varied`, `Revoked`, `Expired`, `Surrendered`, `Under review`, `Not stated`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the permit is live, as at the most recent document.

**Scope discipline.** A permit certificate speaks as of its own date. Most
environmental regulators maintain public facility and permit registries, so
verification is usually quick and the reviewer should do it.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify the most recent document bearing on status. Confirm the status against it.

## Task

Classify the status of this permit as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Revoked`: the documents record revocation, cancellation, or refusal to renew.
2. `Surrendered`: the holder surrendered the permit or withdrew an application. **Note in the evidence field whether the documents evidence that closure or surrender obligations were discharged** — surrendering a waste or storage permit usually triggers closure requirements, and an undischarged surrender is a liability rather than a resolution.
3. `Suspended`: the documents record suspension, whether temporary or pending an investigation.
4. `Expired`: the stated expiry has passed and neither a renewal nor an administrative continuance appears.
5. `Administratively continued`: the stated expiry has passed and the documents evidence a timely renewal application with the permit continuing in force pending determination. **Distinguished from `Expired` because the operation remains lawful**, and the distinction is the whole difference between a finding and a diary entry.
6. `Under review`: the documents record a pending review, investigation, or enforcement process affecting the permit.
7. `Pending or in application`: an application is filed and not yet determined. Report in the evidence field whether activity is permitted meanwhile.
8. `Modified or varied`: a modification or variation is the most recent record and the permit continues as varied. **Use this rather than `Active` where the current terms differ from those originally issued**, so the reviewer knows to read the Modification History column.
9. `Active with compliance schedule`: in force subject to a compliance schedule, consent order, or agreed programme of works. **This means the permit itself records that the site is not currently in full compliance**, which is a substantive finding and not merely a status.
10. `Active`: in force with none of the above applying.

Give the date of the document the status comes from in the evidence field, and note where it is more than twelve months older than the diligence as-of date.

## Fallback rules

- Use `Not stated` where the documents evidence the permit without stating a status.
- Use `Unable to determine` where statuses conflict or the relevant text is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 12. Modification History

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: how the permit has changed since issue. **A permit varied three times
  is not the permit as issued**, and the modifications are where limits get
  tightened and conditions get added.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify each modification. Confirm the details against the documents.

## Task

List every modification, variation, amendment, or endorsement to this permit that the documents disclose.

## Rules

- Report each modification in date order with its reference, its date, and what it changed in eight words or fewer.
- **Report specifically any modification that changed a permitted limit, added or removed a permitted activity or unit, changed a monitoring requirement, added a condition, changed the permittee, or imposed a compliance schedule.** These are the changes that alter the answers elsewhere in the row.
- **Report whether each modification was applied for by the holder or initiated by the regulator.** A regulator-initiated variation usually follows a compliance problem or a change in standards, and it reads very differently from a holder's application to expand capacity.
- **Report any modification that tightened a limit**, since it may indicate the site was struggling to meet the previous one, or that standards have moved.
- **Where a modification is referenced but not present, note it**; the Referenced but Not Produced column carries it.
- **Where modifications are numbered or lettered in a sequence and one is missing, note the gap.**
- Report the modifications as recorded. Do not assess why any was made.

## Fallback rules

- Return exactly `None recorded` where the documents disclose no modification.

Note: this reflects the documents in this unit only. **A permit issued fifteen years ago with no modifications recorded is unusual** and may mean the modification record was not produced.

- Return `Unable to determine` where records conflict or are illegible.

## Output format

One line per modification, earliest first:

`[YYYY-MM-DD] — [reference] — [what it changed] — [holder application | regulator initiated]`

Return no more than 8 lines and no more than 85 words.
```

---

### 13. Permitted Activity and Limits

- Native type: Free Response
- Upstream: `@Permit Type`
- Downstream: none
- Purpose: what the permit allows, and the numbers the site must stay inside.
  **A limit the site has outgrown is a live compliance problem**, and it is also a
  constraint on the buyer's growth plans.

```markdown
## Established result

- Permit Type: @Permit Type

## Task

Report the activities this permit authorises and the limits it imposes.

## Include where expressly stated

- The activities, processes, or operations authorised, as described
- **Every numerical limit, with its parameter, value, unit, and averaging period** — emission concentrations and mass rates, discharge concentrations and loads, abstraction or extraction volumes, waste throughput and storage capacity, tank capacity, or operating hours
- Any capacity or throughput limit on the installation as a whole
- Any technology, control equipment, or best-available-technique requirement
- Any feedstock, waste type, or input restriction, including permitted waste codes
- Any restriction on the source or destination of waste
- Any limit expressed as a rolling or annual total
- Any limit that steps down on a stated date

## Rules

- **Report each limit with its averaging period.** A daily maximum and an annual average of the same parameter are different obligations, and a value reported without its averaging basis is not usable.
- **Report any limit that tightens on a future date**, since it is a forward compliance obligation the buyer inherits and the site may not currently meet it.
- **Report any throughput or capacity limit prominently**, since it caps the site's output regardless of demand and is a direct constraint on the buyer's growth plans. Expanding it means a permit variation with its own timetable.
- Report values and units exactly as stated. **Do not convert units, do not total limits, and do not compare a limit to any monitoring result.**
- **Do not assess whether the permitted activity matches the site's actual operations.** That comparison is human work against the operational data, and it is where the highest-value finding in this workstream comes from.

## Fallback rules

- Return `Not stated` where the permit does not describe the authorised activity.
- Return `Incorporated terms` where the limits are stated to be set out in a schedule or conditions document not present in the unit. **Common, and it is a substantial gap.**
- Return `Unable to determine` where limits conflict or are illegible.

## Output format

`Activities: [as described]; capacity: [as stated]` then one line per limit:

`[Parameter] — [value] [unit] — [averaging period]`

Return no more than 12 lines and no more than 110 words. Do not include converted or totalled figures.
```

---

### 14. Conditions and Compliance Schedule

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the obligations attached to holding the permit, and any programme of
  works the site is already committed to.

```markdown
## Task

Report the conditions attached to this permit and any compliance schedule or programme of works.

## Include where expressly stated

- Operating conditions, and any requirement to maintain equipment, controls, or abatement
- Any management system, plan, or procedure required — a waste management plan, a spill prevention plan, an environmental management system, an emergency response plan
- Any training or competence requirement
- Any requirement to maintain records, and for how long
- **Any compliance schedule, agreed programme of works, or improvement condition, with each milestone and its deadline**
- Any closure, decommissioning, or post-closure requirement
- Any site restoration or aftercare obligation, and its duration
- Any groundwater or soil monitoring requirement imposed by the permit
- Any notification condition, and its trigger and period
- Any condition imposed following enforcement, with the action identified

## Rules

- **Report each compliance schedule milestone with its deadline, and compare each to the diligence as-of date.** Where a milestone has passed with no evidence of completion, append ` [milestone deadline passed]` to that line. **A compliance schedule is the regulator recording that the site is not yet compliant**, and a missed milestone is a breach on top of the original one.
- **Report closure, decommissioning, and aftercare obligations prominently, with their duration.** These are long-tail liabilities — landfill aftercare can run for decades — and they pair directly with the Financial Assurance column.
- **Distinguish conditions attached at issue from conditions imposed following enforcement**, and label each. A condition imposed after an investigation tells the reviewer there was one, and it belongs alongside the Enforcement rows.
- Report each condition in eight words or fewer, with its source document.
- Report no more than twelve conditions. Where more exist, report the twelve with the greatest operational or financial effect and append ` and [N] further conditions`.
- Do not assess compliance.

## Fallback rules

- Return exactly `None attached` where the permit is unconditional. **Rare for an environmental permit** and worth checking against Chain Completeness.
- Return `Incorporated terms` where conditions are stated to be set out in a schedule not present in the unit.
- Return `Unable to determine` where conditions conflict or are illegible.

## Output format

One line per condition or milestone:

`[Condition or milestone] — [deadline or "ongoing"] — [at issue | imposed [YYYY-MM-DD]]`, with any bracketed flag appended.

Return no more than 12 lines and no more than 110 words.
```

---

### 15. Monitoring and Reporting Obligations

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the recurring obligations the buyer inherits, and the notifications the
  transaction itself triggers.

```markdown
## Task

Report the monitoring and reporting obligations this permit imposes.

## Include where expressly stated

- Each monitoring requirement, with the parameter, the medium, the frequency, and the method or standard where stated
- Any continuous monitoring requirement, and any availability or uptime requirement for the monitoring system
- Any requirement for third-party or accredited laboratory analysis
- Each periodic report or return, with its frequency and due date
- Any annual compliance certification, and who must sign it. **Where an officer or a named responsible person must certify, report that** — it is a personal obligation that survives to whoever holds the role after closing
- Any requirement to report exceedances or incidents, and the period for doing so
- **Any event-driven notification obligation, and the period for each**: an exceedance, a spill or release, a breakdown of abatement equipment, a change in operations, a change of operator, a change of ownership, or cessation of activity
- Any record-retention obligation, with the period
- Any requirement to permit inspection or to provide information on demand
- Any requirement to publish or make information publicly available

## Rules

- **Report the event-driven notifications separately from the periodic ones, with the period for each.** A change-of-operator or change-of-ownership notification with a short period is triggered by the transaction and it is easy to miss.
- **Report any requirement for a named individual or officer to certify reports**, since it is a personal exposure and it needs a designated person after closing.
- **Report any exceedance-reporting obligation with its period.** Self-reporting an exceedance is generally mandatory, and a failure to report is usually treated more seriously than the exceedance itself.
- Report frequencies and periods as stated. Do not calculate due dates.

## Fallback rules

- Return exactly `None stated` where the permit imposes no monitoring or reporting obligation.
- Return `Incorporated terms` where the obligations are stated to be set out in a schedule not present in the unit.
- Return `Unable to determine` where obligations conflict or are illegible.

## Output format

`Monitoring: [parameter, medium, frequency]` per line, then `Reporting: [report — frequency and due date]` per line, then `Event-driven: [event — period]` per line.

Return no more than 12 lines and no more than 110 words.
```

---

### 16. Financial Assurance

- Native type: Free Response
- Upstream: `@Permit Type`
- Downstream: none
- Purpose: the security the permit requires for closure and long-term
  obligations. **A liability with a funding requirement that can outlive the
  transaction by decades**, and one no other permit table in the set needs to ask
  about.

```markdown
## Established result

- Permit Type: @Permit Type

## Task

Report any financial assurance, bonding, or security requirement attached to this permit.

## Include where expressly stated

- **The amount of financial assurance required, and what it covers** — closure, post-closure care, corrective action, third-party liability, or restoration
- The instrument required or in place: surety bond, letter of credit, trust fund, insurance policy, corporate guarantee, or financial test
- **The provider or issuer of any instrument in place, and its expiry or renewal date**
- **Whether the assurance is provided by the permittee, a parent, or an affiliate**, and any parent or corporate guarantee given to the regulator
- Any financial test or net worth requirement the holder must satisfy to self-assure
- Any requirement to increase the assurance on a stated event, on inflation, or on a periodic review
- **Any requirement triggered by a change of control, a change of operator, or a deterioration in the holder's financial position**
- Any cost estimate for closure, post-closure, or corrective action stated, and its basis and date
- The duration of any post-closure care obligation
- Any statement that the assurance is currently inadequate or under review

## Rules

- **Report any corporate or parent guarantee given to the regulator prominently.** Where the guarantor is the seller or an entity outside the acquired group, it must be replaced at closing, **and the regulator's agreement to the replacement is itself an approval with a timetable.** This is among the most commonly missed items in environmental diligence.
- **Report any self-assurance based on a financial test.** A holder that self-assures on its own balance sheet may fail the test after the transaction — particularly in a leveraged acquisition — and would then have to post an instrument, which is a cash cost triggered by the deal structure.
- **Report the closure cost estimate with its date and basis.** An estimate several years old, or based on a superseded standard, understates the liability, and the regulator will usually require it to be updated.
- **Report the post-closure care duration**, since a long aftercare obligation is a decades-long funding commitment.
- Report amounts as stated. **Do not calculate whether the assurance is adequate**, and do not compare it to any cost estimate.

## Fallback rules

- Return exactly `None required` where the documents impose no financial assurance requirement. **This is the expected answer for most air and discharge permits** and it is not a gap.
- Return `Incorporated terms` where the requirement is stated to be set out in rules or a schedule not present in the unit.
- Return `Unable to determine` where requirements conflict or are illegible.

## Output format

`Amount: [as stated]; covers: [as stated]; instrument: [type and provider]; expiry: [date or "n/a"]; provided by: [permittee | parent | affiliate]; financial test: [as stated or "none"]; closure estimate: [amount and date]; post-closure duration: [as stated]; change of control trigger: [as stated or "Not addressed"]`

Return no more than 90 words.
```

---

### 17. Transferability on Change of Control

- Native type: Classify
- Configured options, in UI order: `Transfers with the entity, no filing`, `Notification required`, `Prior approval required`, `Formal transfer application required`, `New application required, not transferable`, `Site-based, transfers with the site`, `Not addressed`, `Unable to determine`
- Upstream: none
- Downstream: `Transfer Requirements`
- Purpose: whether the permit survives the transaction. **The column that puts
  environmental permits on the closing calendar.**

Environmental permits vary more widely than any other authorisation in this set.
Some attach to the entity and are unaffected by a share sale. Some attach to the
site and pass with it. Some require a formal transfer application naming the new
operator **even in a share purchase where the holder does not change** — because
the regime regulates the operator's identity and control rather than the corporate
shell.

```markdown
## Task

Classify what the documents state is required on a change of ownership or control of the permittee, or on a transfer of the site. Choose exactly one configured option.

## Scope

- Consider requirements stated in the permit, its conditions, the applicable rules where the documents reproduce them, or any prior transfer approval in the unit.
- Consider requirements triggered by a change of control of the permittee, a change of operator, and a transfer of the site or installation.

## Classification rules

Apply the first rule that fits.

1. `New application required, not transferable`: the permit cannot be transferred and a new application must be made. **The most severe outcome** — the site may not be lawfully operable by a new operator until a new permit issues, and interim arrangements may be needed.
2. `Formal transfer application required`: a transfer or variation application naming the new holder or operator must be made and determined. **Note in the evidence field whether the documents state this applies to a share transfer as well as an asset transfer** — in several regimes it does, and that is the point most often missed.
3. `Prior approval required`: the regulator's affirmative approval must be obtained before the change takes effect. **A closing condition.**
4. `Notification required`: notification is required, before or after the change, with no approval needed.
5. `Site-based, transfers with the site`: the permit attaches to the installation or site and passes with it, without regard to the holder's ownership.
6. `Transfers with the entity, no filing`: the permit is held by the entity and is unaffected by a change in that entity's ownership, with no filing required.

**Do not supply a transfer requirement from the governing legislation.** Where the documents state none, use `Not addressed` — and note in the evidence field that the position must be established from the law, since **environmental transfer rules are rarely recited on the face of a permit and `Not addressed` is the common answer rather than evidence that nothing is required.**

## Fallback rules

- Use `Not addressed` where the documents do not address transfer or change of control.
- Use `Unable to determine` where requirements conflict or are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 18. Transfer Requirements

- Native type: Free Response
- Upstream: `@Transferability on Change of Control`
- Downstream: none
- Purpose: the mechanics and the timetable. **What the closing calendar entry is
  built from.**

```markdown
## Established result

- Transferability on change of control: @Transferability on Change of Control

## Task

If Transferability on Change of Control is `Notification required`, `Prior approval required`, `Formal transfer application required`, or `New application required, not transferable`, report the requirements and mechanics.

If it is `Transfers with the entity, no filing` or `Site-based, transfers with the site`, return exactly `Not applicable`.

If it is `Not addressed` or `Unable to determine`, return exactly `Not addressed`.

## Include where expressly stated

- **The period for making the filing, whether before or after the change**
- **The regulator's stated determination period**
- Any fee payable
- **What the incoming holder or operator must demonstrate** — technical competence, management systems, a named technically competent person, financial standing, or a compliance history
- Any requirement to provide the incoming holder's ultimate ownership details
- **Any requirement to provide or replace financial assurance as part of the transfer**, and whether the outgoing holder's assurance is released only on the new one being accepted
- Any requirement for the outgoing and incoming holders to sign jointly
- Any public notice, consultation, or objection period
- Any interim or temporary operating permission available pending determination
- Any requirement to resolve outstanding enforcement or compliance issues before transfer
- Any statement that liability for pre-transfer matters remains with the outgoing holder, or passes

## Rules

- **Report the determination period as stated and do not supply one from the legislation.** A wrong period produces a wrong closing date.
- **Report the technical competence requirement prominently.** Several regimes require the operator to demonstrate technical competence through a named individual holding a specific qualification — **and where that individual is not staying, the transfer cannot complete until a replacement is in place.** It links directly to the Employment key-person analysis.
- **Report any requirement to resolve outstanding enforcement before transfer**, since it converts an Enforcement row into a closing condition.
- **Report the financial assurance replacement mechanics**, since the outgoing holder will not release its bond before the incoming one is accepted and the sequencing has to be planned.
- **Report any interim operating permission**, since it can decouple the approval from the closing timetable.
- Report periods and requirements as stated. Do not estimate a timetable.

## Output format

`Filing deadline: [as stated]; determination period: [as stated or "Not addressed"]; fee: [as stated]; incoming holder must demonstrate: [brief]; financial assurance: [as stated or "Not addressed"]; joint signature: [yes | Not addressed]; public notice: [as stated or "none"]; interim permission: [as stated or "Not addressed"]; enforcement must be resolved: [yes | Not addressed]`

Return no more than 95 words. Do not include any period not stated in the documents.
```

---

### 19. Prior Transfer Approvals

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: **how this regulator has actually handled a transfer before.** The
  single most useful document in the unit, because it shows the real process and
  the real timetable rather than the stated one.

```markdown
## Task

Report any prior transfer, change of operator, or change of control approval in this review unit.

## Include where expressly stated

- The date of the application and the date of the approval, **and the elapsed period between them**
- The transaction it related to, in six words or fewer
- The outgoing and incoming holders as named
- **Any condition the regulator imposed as part of the approval**
- What the regulator required from the incoming holder, and any information request in the file
- Any financial assurance change required, and how it was sequenced
- Any interim permission granted pending determination
- Any objection, public representation, or consultation response received
- Any refusal, withdrawal, or resubmission in the history
- Any post-approval review or reporting the regulator required

## Rules

- **Report the actual elapsed period from application to approval.** It is better evidence of the timetable than any stated determination period, and it is the figure to plan against.
- **Report every condition the regulator imposed**, since it indicates what it will require this time and conditions imposed on a prior transfer frequently continue to bind.
- **Report any information request the file shows**, since it tells the buyer what to prepare before filing rather than after.
- **Report how the financial assurance was sequenced**, since it is the most common source of delay in an environmental permit transfer.
- Report what the documents state. **Do not predict what the regulator will do on this transaction**, and do not assume the prior process will repeat.

## Fallback rules

- Return exactly `None in unit` where no prior transfer approval appears.

Note: this is a positive finding, not a fallback state. **Where the site or the target has changed hands before and no transfer approval file was produced, that is a coverage gap worth pursuing** — the file is usually the most useful document available for planning.

- Return `Unable to determine` where approval documents are illegible.

## Output format

One line per approval:

`[Transaction] — applied [YYYY-MM-DD], approved [YYYY-MM-DD] ([elapsed period]) — from [holder] to [holder] — conditions: [brief or "none"]`

Return no more than 4 lines and no more than 80 words.
```

---

### 20. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this permit file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this permit that the documents in this unit refer to and that is not present.

## Scope

- **Include the conditions schedule where it is absent.** The conditions are the obligations the buyer inherits.
- **Include any rulebook, regulation, code of practice, or guidance the permit states its conditions or limits are set by**, where a specific document is identified.
- Include the original application and supporting submissions referenced.
- Include renewal certificates and confirmations referenced but absent.
- Include modifications, variations, and endorsements referenced but absent.
- **Include any prior transfer or change-of-control approval referenced but absent.**
- **Include any management plan, procedure, or system the permit requires** — waste management plan, spill prevention plan, environmental management system, closure plan, monitoring plan.
- **Include any financial assurance instrument, bond, guarantee, or trust document referenced.**
- Include any closure or post-closure cost estimate referenced.
- Include monitoring reports, returns, and compliance certifications required by the permit.
- Include any inspection report, enforcement notice, or compliance correspondence referenced.
- Include any technical competence certificate for a named individual referenced.
- Exclude general statutes and regulations not specifically identified as containing the permit's conditions.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where the conditions schedule is absent, add `; conditions unreadable`.** Filter these first: the obligations cannot be assessed at all.
- **Where a financial assurance instrument is referenced and absent, add `; assurance unproven`.**
- **Where a required management or closure plan is absent, add `; required plan not produced`.** A permit condition requiring a plan means the plan exists or the condition is breached.
- **Where a prior transfer approval is referenced and absent, add `; transfer precedent`.**
- Where a monitoring return or compliance certification is absent, add `; compliance record incomplete`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is uncommon here — **environmental permits routinely incorporate schedules, plans, and rules by reference.**

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
| **Status verified against register** | Yes (date) / No / Not available |
| **Transfer or filing required** | Prior approval / Transfer application / Notification / None / Unassessed |
| **Closing condition** | Yes / No / Unresolved |
| **Estimated timetable** | Free text |
| **Permit adequate for operations** | Yes / Gap identified / Unassessed |
| **Financial assurance action required** | None / Replace guarantee / Post instrument / Update estimate / Unresolved |
| **Technical competence person critical** | Yes / No / Unassessed |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: permittee, facility, status, expiry,
limits, transferability, financial assurance.

### Reconciliation work that never belongs in a column

- **Permits against operations.** Every row against the site list, the process
  descriptions, and the jurisdictions of operation. **An activity requiring a
  permit at a site where none is produced is the highest-value finding this
  workstream generates**, and it is invisible from inside any row. Check emissions
  sources, discharge points, waste streams, storage tanks, and abstraction against
  the permits held.
- **Limits against actual operations.** Every permitted limit against actual
  throughput, emissions, and discharge data from the operational and monitoring
  records. **A site operating above a permitted limit is in breach**, and a site
  near its limit cannot grow without a variation.
- **The transfer calendar.** Every row requiring an approval, notification, or
  transfer application, sequenced with its determination period against the deal
  timetable. **The longest period sets the earliest closing date** for the site,
  and where a new application is required the site may need interim arrangements.
- **Financial assurance.** Every row with a bond, guarantee, or self-assurance
  test, against the financing plan and the transaction structure. **Guarantees from
  entities outside the acquired group must be replaced, and a leveraged structure
  may fail a financial test the target currently passes.** Also check every closure
  cost estimate's date, since a stale estimate understates the liability and the
  regulator will require an update.
- **Technical competence.** Every row requiring a named competent person, matched
  to the Employment table. **Where that person is not staying, the transfer cannot
  complete until a qualified replacement is appointed and, in some regimes,
  approved.**
- **Continuing obligations register.** Every compliance schedule milestone,
  monitoring obligation, closure duty, and aftercare requirement, consolidated with
  the controlled conditions from the Assessments table and the Real Estate recorded
  restrictions, with named owners.
- **Enforcement interaction.** Every row where a transfer requires outstanding
  enforcement to be resolved, matched to the Enforcement table. **This converts a
  compliance matter into a closing condition.**
- **Status verification.** Every material row against the regulator's public
  facility or permit registry. Most environmental regulators publish these and
  verification is quick.

---

## Test set

- [ ] Air operating permit with numerical emission limits and averaging periods
- [ ] Water discharge permit with concentration and load limits per outfall
- [ ] Stormwater general permit obtained by notification
- [ ] Hazardous waste permit with closure and post-closure requirements
- [ ] Waste carrier registration
- [ ] Storage tank registration
- [ ] Abstraction or extraction licence with a volume limit
- [ ] Permit expired on record with no renewal produced
- [ ] Permit expired on record with a timely renewal application and administrative continuance
- [ ] Permit expiring within three months of the as-of date
- [ ] Permit with a renewal deadline nine months before expiry
- [ ] Permit continuing indefinitely subject to annual fees and returns
- [ ] Permit with a compliance schedule and a passed milestone
- [ ] Permit with a compliance schedule fully performed
- [ ] Permit varied three times, with limits tightened by the latest variation
- [ ] Permit with a regulator-initiated variation
- [ ] Permit with a modification sequence gap
- [ ] Permit held under a target entity's former name
- [ ] Permit held by the seller's parent covering a site being sold
- [ ] Permit held by an individual
- [ ] Site-based permit naming no legal entity
- [ ] Permit naming the target as operator of a site it leases
- [ ] Permit requiring a formal transfer application on a share transfer
- [ ] Permit requiring prior approval with a stated determination period
- [ ] Permit requiring post-change notification only
- [ ] Permit stated to transfer with the entity with no filing
- [ ] Permit not transferable, requiring a new application
- [ ] Permit with a prior transfer approval showing a five-month elapsed period
- [ ] Permit with a prior transfer approval imposing continuing conditions
- [ ] Permit with a surety bond expiring within the deal period
- [ ] Permit with a corporate guarantee given to the regulator by the seller
- [ ] Permit with self-assurance based on a financial test
- [ ] Permit with a closure cost estimate six years old
- [ ] Permit with a thirty-year post-closure care obligation
- [ ] Permit requiring a named technically competent person
- [ ] Permit requiring an officer to certify annual compliance
- [ ] Permit with continuous monitoring and an uptime requirement
- [ ] Permit with an exceedance-reporting obligation of 24 hours
- [ ] Permit with conditions stated to be in a schedule not produced
- [ ] Permit requiring a waste management plan not produced
- [ ] Permit with a limit that steps down on a future date
- [ ] Permit covering three of five process lines at a site
- [ ] Permit surrendered with no evidence closure obligations were discharged
- [ ] Permit suspended by the regulator
- [ ] Unit covering the same permit type at three facilities

Then test the dependencies: change `Expiry Date` from a future date to
`Not applicable — continuous` and confirm `Renewal Requirements` re-runs against
the maintenance rules. Change `Transferability on Change of Control` from
`Prior approval required` to `Transfers with the entity, no filing` and confirm
`Transfer Requirements` moves to `Not applicable`. Change `Permittee Entity` from
a target entity to the seller's parent and confirm `Permittee Match` moves to
`Held by seller or an affiliate outside the group`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
