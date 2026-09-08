# Prompt Inventory — Debt: Lien Filings

Table 19 of the POC. Small table, and the only one whose central column is a
match against another table.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - Finance`
- Review unit: **one filing** — the filing itself, together with every amendment,
  continuation, assignment, and termination recorded against it
- Grouping used: **yes**, typically 1–4 documents per unit
- Intended reviewers and downstream use: finance and corporate/M&A teams; feeds
  the lien release checklist, the undisclosed debt analysis, and the coverage
  register
- Inventory version: v1.0

### Why this is a separate table

`review-tables.md` §10 puts facilities and filings in one table, but they have
different row units and different roles: a credit agreement is an Instrument read
for its terms, a financing statement is a Filing read for what it puts on the
public register.

**The reason for having both is the match.** A filing with no corresponding
facility means either undisclosed debt or a stale filing left on the register.
A facility with no filing may mean an unperfected lien. Neither is visible from
one row set, and `Matches a Produced Facility` is the column the whole table
exists to populate.

### Two things this table cannot do

**It cannot tell you what is on the register.** These rows are the filings the
seller produced, or the search results the seller commissioned. A complete picture
requires current searches in every jurisdiction of organisation and operation, run
for the buyer, and that is human work.

**It cannot determine perfection or priority.** It reports the debtor name as
filed, the office, the date, and the collateral description. Whether the filing
perfects anything, and where it ranks, is a legal conclusion.

## Assumptions to confirm before running

1. One row is one original filing with its amendment history. A UCC-1 with two
   UCC-3 amendments and a continuation is one row.
2. **Rows come from two sources: filings produced by the seller, and search
   results.** Where a search report lists filings without producing the filings
   themselves, each listed filing is still a row, and `Documents in Unit` records
   that only the search entry is available.
3. Mortgages recorded against real property are rows here **and** are reported in
   the Real Estate — Owned Property table's `Monetary Liens` column. Note the
   duplication in the production log.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

15 Harvey columns plus 6 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side finance diligence on the target group listed below. This table reviews lien filings and security registrations.

One row is one filing: the filing itself, together with every amendment, continuation, assignment, and termination recorded against it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Review subjects

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the filing or the parties.
- **Report every name, number, and description exactly as it appears on the filing, character for character. Do not correct, normalize, expand, abbreviate, or reformat anything.** A filing is effective or defective by reference to what it actually says, and a corrected name in this table destroys the only evidence of the defect.
- **Do not assess perfection, priority, effectiveness, or enforceability.** All four are legal conclusions and none of them is on the face of a filing.
- **A filing states the position as at its own date, and a search report as at its search date.** Report the date and identify the source.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Filing Type
  Debtor Name as Filed
  Secured Party as Filed
  Filing Office and Jurisdiction
  Filing Number
  Filing Date

Stage 2 — Name test
  Debtor Name as Filed ──→ Debtor Name Match

Stage 3 — Currency
  Filing Type ──→ Lapse or Continuation Due Date
  Documents in Unit ──→ Amendment History
                        Status
                        Referenced but Not Produced

Stage 4 — Substance and match
  Collateral Description as Filed
  Secured Party as Filed ──→ Matches a Produced Facility
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Amendment History; Status; Referenced but Not Produced | v1.0 | draft |
| 2 | Filing Type | Classify | — | Lapse or Continuation Due Date | v1.0 | draft |
| 3 | Debtor Name as Filed | Free Response | — | Debtor Name Match | v1.0 | draft |
| 4 | Debtor Name Match | Classify | @Debtor Name as Filed | — | v1.0 | draft |
| 5 | Secured Party as Filed | Free Response | — | Matches a Produced Facility | v1.0 | draft |
| 6 | Filing Office and Jurisdiction | Free Response | — | — | v1.0 | draft |
| 7 | Filing Number | Free Response | — | — | v1.0 | draft |
| 8 | Filing Date | Date | — | — | v1.0 | draft |
| 9 | Lapse or Continuation Due Date | Date | @Filing Type | — | v1.0 | draft |
| 10 | Collateral Description as Filed | Free Response | — | — | v1.0 | draft |
| 11 | Amendment History | Free Response | @Documents in Unit | — | v1.0 | draft |
| 12 | Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 13 | Matches a Produced Facility | Classify | @Secured Party as Filed | — | v1.0 | draft |
| 14 | Evidence Basis | Classify | — | — | v1.0 | draft |
| 15 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

15 columns. `Evidence Basis` was added during drafting: a row built from a search
report entry and a row built from the filing itself carry very different weight,
and a reviewer must be able to tell them apart at a glance.

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Amendment History`, `Status`, `Referenced but Not Produced`
- Purpose: inventory what is actually available for this filing.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the original filing, every amendment, continuation, assignment, subordination, partial release, and termination recorded against it, and any search report entry that is the only record of the filing.
- Include any acknowledgement or receipt issued by the filing office.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed form title or type. Where none is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own filing or recording date.
- State the function as one of `Original filing`, `Amendment`, `Continuation`, `Assignment`, `Partial release`, `Termination`, `Subordination`, `Office acknowledgement`, or `Search report entry`.
- **Where the only record of this filing is an entry in a search report, state that clearly**, since the filing's own content is then unavailable and several columns will be limited to what the report summarises.
- Where a document relates to a different filing, still list it and append ` [relates to [filing number]]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Type] ([Function])`

Return no more than 8 lines and no more than 70 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Filing Type

- Native type: Classify
- Configured options, in UI order: `UCC-1 financing statement`, `UCC-3 amendment`, `UCC-3 continuation`, `UCC-3 termination`, `UCC-3 assignment`, `Fixture filing`, `Mortgage or deed of trust`, `IP security recordation`, `Judgment lien`, `Tax lien`, `Statutory or mechanics lien`, `Non-US security registration`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: `Lapse or Continuation Due Date`
- Purpose: what kind of filing this is, which determines whether it lapses and
  what has to be done to keep or remove it.

```markdown
## Task

Classify the type of filing this review unit documents. Choose exactly one configured option.

## Rules

- **Classify the original filing, not the amendments recorded against it.** Where the unit contains a UCC-1 with two UCC-3 amendments, classify as `UCC-1 financing statement` and report the amendments in Amendment History. **Only classify as a UCC-3 type where the UCC-3 is the subject of the row in its own right** — for example a standalone termination or assignment produced without the original.
- `IP security recordation`: a security interest recorded with an intellectual property office rather than a UCC filing office. **These are recorded separately and are frequently missed on both sides**, at grant and at release, which is why they have their own option.
- `Judgment lien`, `Tax lien`, `Statutory or mechanics lien`: liens arising by operation of law or by judgment rather than by consensual grant. **Report these prominently in the evidence field** — an involuntary lien is not merely an encumbrance to release, it is evidence of an unpaid obligation or a dispute, and it usually indicates a problem elsewhere in the diligence.
- `Non-US security registration`: a charge, pledge, or security registration in a non-US register. Note the register in the evidence field and route to local counsel for release mechanics.
- `Fixture filing`: a filing against goods that are or will become fixtures on real property. Note the property in the evidence field, since it links to the Real Estate tables.

## Fallback rules

- Use `Other` where the filing is a security or lien record none of the options describes.
- Use `Unable to determine` where the filing type cannot be read.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Debtor Name as Filed

- Native type: Free Response
- Upstream: none
- Downstream: `Debtor Name Match`
- Purpose: the debtor name exactly as it appears. **Reported without correction,
  because the exactness of the name is the point.**

```markdown
## Task

State the debtor's name exactly as it appears on this filing.

## Rules

- **Report the name character for character as filed**, including entity suffix, punctuation, spacing, capitalisation, and any misspelling, abbreviation, or omission. **Do not correct, normalize, expand, or complete it, and do not substitute the name you believe was intended.**
- **Where the filing shows the name in an organisation-name field and an individual-name field separately, report which field was used.** A registered organisation filed under an individual name field is a defect on the face of the filing.
- Where the filing lists more than one debtor, report each on its own line.
- Where an amendment in the unit changed the debtor name, report the current name as amended and append ` (amended from [prior name as filed], [YYYY-MM-DD])`.
- Report any trade name, DBA, or additional name field as filed, labelled.
- Report the debtor's stated address, jurisdiction of organisation, and organisational identification number where the filing includes them. **These fields are how a searcher confirms they have the right entity**, and their absence or error is itself a finding.

## Fallback rules

- Return `Not stated` where the filing shows no debtor name.
- Return `Unable to determine` where the name is illegible.

## Output format

`[Name exactly as filed]` per debtor, with any qualifier appended, then a final line: `Jurisdiction of organisation: [as filed or "not stated"]; org ID: [as filed or "not stated"]`

Return no more than 60 words. Report exactly as filed and correct nothing.
```

---

### 4. Debtor Name Match

- Native type: Classify
- Configured options, in UI order: `Exact match to a target entity`, `Minor variance from a target entity`, `Material variance from a target entity`, `Matches a former name of a target entity`, `Filed against an individual`, `Filed against a third party`, `Filed against a trade name only`, `No debtor name`, `Unable to determine`
- Upstream: `@Debtor Name as Filed`
- Downstream: none
- Purpose: whether the filing names the debtor correctly.

**This is the column that finds perfection problems.** A financing statement filed
against a name that differs from the debtor's registered name may be
seriously misleading and therefore ineffective — which is the lender's problem, not
the buyer's, but it is also how a buyer finds a lien it did not expect: an entity
searched under its correct name will not return a filing made under a wrong one.

The classification separates the two failure modes: a variance in punctuation or
suffix is a different question from a filing against an entirely different name.
Whether either is fatal is a legal conclusion and stays with the reviewer.

```markdown
## Established result

- Debtor name as filed: @Debtor Name as Filed

Use this result and the target group list in the Table Instructions. Compare character by character.

## Task

Classify the relationship between the debtor name as filed and the target group's exact legal names. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No debtor name`: Debtor Name as Filed returned `Not stated`.
2. `Filed against a trade name only`: the filing names a trade name, DBA, or brand with no legal entity name. **A filing against a trade name alone is generally ineffective**, and it is also invisible to a search run under the legal name.
3. `Filed against an individual`: the debtor is a natural person.
4. `Matches a former name of a target entity`: the filed name matches a prior name of a target entity as disclosed in the documents in this unit. **The filing was made before a name change and the register has not caught up.**
5. `Filed against a third party`: the filed name is an entity that is not a target entity and is not a former name of one.
6. `Material variance from a target entity`: the filed name refers to a target entity but differs in a way that changes the searchable name — a misspelling of a distinctive word, a missing or wrong distinctive word, a transposition, or a wholly different suffix such as `Inc.` for `LLC`.
7. `Minor variance from a target entity`: the filed name differs only in punctuation, spacing, capitalisation, the presence or absence of a comma before a suffix, or an abbreviated form of a suffix such as `Incorporated` and `Inc.`.
8. `Exact match to a target entity`: the filed name is character for character identical to a name on the target group list.

**The distinction between minor and material variance is descriptive, not legal.** Report what kind of difference exists. **Do not assess whether the filing is seriously misleading, whether a search under the correct name would find it, or whether the lien is perfected.** Those are legal conclusions for the reviewer.

Where a target entity's former name is not disclosed in this unit, use `Filed against a third party`; the Corporate table's `Prior Names` column resolves it.

## Fallback rules

- Use `Unable to determine` where the name is illegible or Debtor Name as Filed returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 5. Secured Party as Filed

- Native type: Free Response
- Upstream: none
- Downstream: `Matches a Produced Facility`
- Purpose: who holds the security, exactly as filed. **The join key to the
  Facilities table.**

```markdown
## Task

State the secured party's name exactly as it appears on this filing.

## Rules

- **Report the name character for character as filed**, including entity suffix and punctuation. Do not correct or normalize it. **This is the join key to the Debt — Facilities table** and a normalized name breaks the match.
- Where the filing names an agent, trustee, or representative capacity, report it as filed.
- Where more than one secured party is named, report each.
- **Where an assignment in the unit transferred the filing to a different secured party, report the current secured party and append ` (assigned from [prior party], [YYYY-MM-DD])`.** A filing assigned to a party who does not appear in any facility document is a common cause of an apparent orphan, and the assignment is the explanation.
- Report the secured party's stated address where the filing includes it.
- Where the secured party appears to be a filing service, representative, or agent for an unnamed principal, report it as filed and note that in the evidence field.

## Fallback rules

- Return `Not stated` where the filing shows no secured party.
- Return `Unable to determine` where the name is illegible.

## Output format

`[Name exactly as filed][, [capacity as filed]]` per secured party, with any qualifier appended. Return no more than 45 words.
```

---

### 6. Filing Office and Jurisdiction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the filing sits, which determines whether it was filed in the
  right place and where a release must be filed.

```markdown
## Task

State the office and jurisdiction in which this filing was made.

## Rules

- Report the filing office exactly as identified — the Secretary of State of a named state, a county recorder, a named IP office, a named non-US register.
- **Report the county or district as well as the state where the filing is a local one**, since real property and fixture filings are made locally and releases must be filed in the same office.
- **Report whether the filing office corresponds to the debtor's jurisdiction of organisation as stated on the filing.** Where it does not, note the mismatch in the evidence field. A filing made in the wrong jurisdiction is a perfection question for the lender and a discoverability question for the buyer, and the mismatch is a fact on the face of the filing.
- Where the filing is a non-US registration, report the register and the jurisdiction, and note that release mechanics require local counsel.
- Where the unit contains filings in more than one office for the same security, note that in the evidence field — the same collateral is often filed centrally and locally.

## Fallback rules

- Return `Not stated` where the office cannot be identified from the documents.
- Return `Unable to determine` where the office is illegible.

## Output format

`Office: [as identified]; jurisdiction: [as stated][; county or district: [as stated]]`. Return no more than 40 words.
```

---

### 7. Filing Number

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the register identifier, which is what a release or a verification
  search is filed or run against.

```markdown
## Task

State the filing, recording, or registration number for this filing.

## Rules

- **Report the number exactly as printed, including any prefix, year component, hyphens, slashes, and leading zeros. Do not reformat.** A termination filed against a reformatted number will not attach, and a verification search will not find the filing.
- Where the filing is recorded by book and page rather than a single number, report both.
- Where an IP security recordation is identified by reel and frame, report both.
- Where amendments, continuations, or terminations in the unit carry their own numbers, report the original filing's number here and report the others in Amendment History.
- Where a search report gives an abbreviated or truncated number, report it as printed and add `(as shown in search report)`.

## Fallback rules

- Return `Not stated` where no number appears.
- Return `Unable to determine` where the number is illegible.

## Output format

`[Number exactly as printed]`, with any qualifier appended. Return no more than 25 words.
```

---

### 8. Filing Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the filing was made, which fixes its place in time and starts the
  lapse clock.

```markdown
## Task

Identify the date this filing was made or recorded.

## Rules

- Report the filing or recording date stamped by the office on the original filing.
- Where the filing bears both a submission date and a recording date, report the recording date and note the other in the evidence field.
- **Do not report the date of the underlying security agreement**, which is usually earlier and is reported in the Facilities table.
- Do not report the date of an amendment or continuation; those are in Amendment History.
- **Where the filing date is materially later than the date of the security agreement it relates to, note the gap in the evidence field.** A long gap is a fact worth surfacing, and its significance is for the reviewer.
- Where only a search report entry is available, report the filing date it shows and note the source.

## Output format

`YYYY-MM-DD`. Preserve partial precision as printed. Return `Not stated` where no filing date appears.
```

---

### 9. Lapse or Continuation Due Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Filing Type`
- Downstream: none
- Purpose: when the filing lapses if not continued. **A filing that lapses is a
  problem for the lender; a filing that does not lapse and is never terminated is
  a problem for the buyer.**

```markdown
## Established result

- Filing Type: @Filing Type

## Task

Identify the date on which this filing lapses or must be continued, as the documents state it.

## Rules by filing type

- `UCC-1 financing statement`: report the lapse date the filing or a search report states, and where a continuation in the unit has extended it, report the extended date.
- `Mortgage or deed of trust`, `IP security recordation`: report any stated expiry or re-recording requirement, and where the register imposes none return `Not applicable — does not lapse`.
- `Judgment lien`, `Tax lien`, `Statutory or mechanics lien`: report any stated duration or expiry.
- `Non-US security registration`: report any stated renewal or re-registration requirement.
- Where the row is a standalone `UCC-3 termination` or `UCC-3 assignment`, return `Not applicable`.

## Rules

- **Report only a date the documents or a search report state. Do not calculate a lapse date from the filing date and a statutory period, even where the period is standard.** A calculated date is indistinguishable from a stated one in an export and it is not verification.
- Where a continuation in the unit extended the filing, report the extended date and note the continuation.
- Compare the reported date to the diligence as-of date and flag it:
  - already passed: append ` [lapsed on record]`
  - within six months: append ` [lapse within 6 months]`
- **A lapsed filing does not discharge the debt.** Where `[lapsed on record]` applies, note in the evidence field that the underlying obligation and any security agreement remain, and that the lender may refile.

## Fallback rules

- Return `Not stated` where the filing type lapses and no date is stated and none can be reported without calculating. **This is common and the reviewer derives it from the filing date and the applicable period.**

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 10. Collateral Description as Filed

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the filing covers on its face, which is what a searcher sees and
  what the release must address.

```markdown
## Task

Report the collateral description exactly as it appears on this filing.

## Rules

- **Report the description as filed.** Where it is a short all-assets formulation, report it verbatim. Where it is a long enumeration, report the categories as filed and add `(enumerated description, [N] categories as filed)` without reproducing the whole list.
- **Report whether the description is an all-assets formulation, a category enumeration, or a specific-asset identification.** The three have very different scope and a searcher reads them differently.
- Report any specific asset identified by serial number, registration number, address, or schedule reference, exactly as filed.
- **Where the description refers to a schedule or exhibit, report the reference and state whether that schedule is in the unit.** A filing whose collateral is defined by an unproduced schedule cannot be scoped at all.
- Report any express exclusion stated on the filing.
- Report any statement that the filing covers proceeds, products, additions, or accessions.
- Where an amendment in the unit changed the collateral description, report the current description and note the change.
- **Do not assess whether the description is sufficient, whether it covers any particular asset, or whether it matches a security agreement.** All three are legal conclusions.

## Fallback rules

- Return `Not stated` where the filing shows no collateral description.
- Return `Unable to determine` where the description is illegible.

## Output format

`[Description as filed or category summary]; type: [all assets | enumerated | specific]; schedule referenced: [in unit | not in unit | none]; exclusions: [as filed or "none"]`

Return no more than 80 words.
```

---

### 11. Amendment History

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: everything recorded against the original filing, which is the only way
  to know whether it is still live and what it now covers.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify each record against this filing. Confirm the details against the documents.

## Task

List every amendment, continuation, assignment, subordination, release, and termination recorded against this filing.

## Rules

- Report each record in date order with its type, its own filing number, its filing date, and what it changed.
- **State for each amendment what it amended** — the debtor name, the secured party, the collateral description, or an address. An amendment adding collateral and one correcting a typographical error have very different significance.
- **Report each continuation with its filing date and the extended lapse date where stated.**
- **Report any partial release with the collateral released**, since a partial release changes the perimeter without removing the filing.
- Report any assignment with the assignee as filed.
- Report any subordination recorded against the filing.
- Report any termination with its filing date.
- **Where a termination appears in the unit but bears no filing office stamp or acknowledgement, report it and append ` [termination not evidenced as filed]`.** A signed but unfiled termination leaves the filing on the register, and this is one of the most common findings in the table.

## Fallback rules

- Return exactly `None recorded` where no record has been made against the original filing.

Note: this reflects the documents in this unit only. **A current search is what establishes the complete record**, and where the row rests on a search report the report's own date limits it.

- Return `Unable to determine` where records conflict or are illegible.

## Output format

One line per record, earliest first:

`[YYYY-MM-DD] — [type] — [number] — [what it changed]`, with any bracketed flag appended.

Return no more than 8 lines and no more than 85 words.
```

---

### 12. Status

- Native type: Classify
- Configured options, in UI order: `Active`, `Active, continued`, `Terminated and filed`, `Terminated, filing not evidenced`, `Lapsed`, `Partially released`, `Assigned`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether this filing still encumbers the debtor. **Drives the release
  checklist directly.**

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory and the records against this filing. Confirm the status against the documents.

## Task

Classify the status of this filing as shown by the documents in this review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Terminated and filed`: a termination is recorded with a filing office stamp, acknowledgement, or search report entry confirming it was filed. **Only this state removes the filing from the release checklist.**
2. `Terminated, filing not evidenced`: a termination document exists in the unit with no evidence it was filed. **The filing remains on the register**, and this is a release task rather than a completed release.
3. `Lapsed`: the stated lapse date has passed with no continuation recorded. **Note that lapse does not discharge the debt or the security agreement**, and the lender may refile.
4. `Assigned`: the filing has been assigned to a different secured party and remains active. Report the current holder from Secured Party as Filed.
5. `Partially released`: a partial release is recorded and the filing otherwise remains active.
6. `Active, continued`: a continuation has been filed and the filing remains active with an extended lapse date.
7. `Active`: the filing remains on the register with no termination, lapse, or release recorded.

**Do not infer termination from the repayment of a facility, from a payoff letter, or from the passage of time.** A repaid facility very often leaves its filings in place, and that is precisely what the release checklist exists to catch.

## Fallback rules

- Use `Unable to determine` where records conflict about the status, or where the relevant documents are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 13. Matches a Produced Facility

- Native type: Classify
- Configured options, in UI order: `Matches a produced facility`, `Secured party matches, facility not identified`, `No corresponding facility produced`, `Matches a facility shown as repaid`, `Involuntary lien, no facility expected`, `Unable to determine`
- Upstream: `@Secured Party as Filed`
- Downstream: none
- Purpose: **the reason this table exists.**

A filing with no corresponding facility means either undisclosed debt or a stale
filing nobody removed. A filing whose facility was repaid means the release was
never filed. Both are findings, and neither is visible from the Facilities table
alone.

**This column can only go so far.** Harvey sees one filing at a time and cannot
read the Facilities table, so it reports what the filing itself discloses about
the obligation behind it. The definitive match is an Excel join on secured party
name, and that join is human work.

```markdown
## Established result

- Secured party as filed: @Secured Party as Filed

Use this result. Determine what the documents in this unit disclose about the underlying obligation.

## Task

Classify what this filing discloses about the facility or obligation it secures. Choose exactly one configured option.

## Scope

- Consider only what the documents in this review unit state. **You cannot see other rows or the Facilities table.**
- Consider any reference on the filing or in an accompanying document to a credit agreement, note, security agreement, or obligation, with its date or parties.

## Classification rules

Apply the first rule that fits.

1. `Involuntary lien, no facility expected`: the filing is a judgment lien, tax lien, or statutory or mechanics lien. **No consensual facility underlies it**, so the match question does not arise. The obligation is reported in the evidence field and it belongs to the Litigation or Tax workstream.
2. `Matches a facility shown as repaid`: a document in the unit — a payoff letter, a release, or correspondence — indicates the underlying obligation has been repaid or discharged, and the filing has not been terminated and filed. **The clearest possible release task.**
3. `Matches a produced facility`: the filing or an accompanying document identifies the underlying security agreement or credit agreement by name, date, or parties, and that document is present in this unit.
4. `Secured party matches, facility not identified`: the filing names a secured party but identifies no underlying agreement, and none is in the unit. **This is the normal state of a bare financing statement** and it is not a finding by itself — the match must be made in Excel against the Facilities export on the secured party name.
5. `No corresponding facility produced`: the filing or an accompanying document identifies an underlying agreement by name or date and that agreement is not present, **or** the documents affirmatively indicate no facility exists with this secured party.

**Do not conclude that a facility does not exist merely because it is not in this unit.** Each unit contains one filing, and the facility is a different row set. Use option 4 for a bare filing and let the Excel join settle it.

## Fallback rules

- Use `Unable to determine` where the secured party cannot be read or the filing's references are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 14. Evidence Basis

- Native type: Classify
- Configured options, in UI order: `Original filing produced`, `Office-certified copy`, `Search report entry only`, `Unfiled copy or draft`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: how much weight the row can carry. **A row built from a search report
  entry and a row built from a certified copy of the filing are different
  evidence**, and the difference should be visible without opening anything.

```markdown
## Task

Classify the evidentiary basis of the documents in this review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Office-certified copy`: the unit contains a copy of the filing certified by the filing office, or an official register extract. **The strongest evidence available**, and it establishes both content and filing.
2. `Original filing produced`: the unit contains the filing itself bearing an office stamp, acknowledgement, or filing number assigned by the office.
3. `Search report entry only`: the only record is an entry in a lien search report or index. **The filing's own content is unavailable**, so the collateral description and any additional debtor fields are limited to what the report summarises. Report the search company and the report's search date in the evidence field.
4. `Unfiled copy or draft`: the unit contains a copy of a filing form with no office stamp, acknowledgement, or filing number. **Nothing establishes it was ever filed**, which cuts both ways: the lien may be unperfected, or the copy may simply be the borrower's file copy.

## Rules

- **Where the basis is `Search report entry only`, report the search report's own search date in the evidence field.** The row cannot be more current than that date, and a search commissioned by the seller months ago is not a current search.
- Where the unit contains both the filing and a search entry, classify on the filing.

## Fallback rules

- Use `Unable to determine` where the documents cannot be characterised.

## Output format

Return only the exact configured option and no explanation.
```

---

### 15. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this filing refers to that is not present. Feeds
  the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this filing that the documents in this unit refer to and that is not present.

## Scope

- **Include the underlying security agreement, credit agreement, or note the filing identifies.**
- **Include any collateral schedule or exhibit the collateral description refers to.**
- Include any amendment, continuation, assignment, partial release, or termination the documents reference but do not contain.
- Include any office acknowledgement or filing receipt referenced.
- Include any search report referenced as listing this filing.
- Include any subordination or intercreditor agreement referenced.
- Include the original filing itself where only an amendment, termination, or search entry is present.
- Include any payoff letter or release correspondence referenced.
- Exclude statutes and regulations.

## Rules

- Name each document as the referencing document names it, and give its date and number where stated.
- **Where the original filing is absent and only a record against it is present, add `; original filing absent`.** The collateral perimeter and the debtor name as originally filed are then unknown.
- **Where a collateral schedule is referenced and absent, add `; collateral scope unknown`.**
- **Where a termination or release is referenced and absent, add `; release unproven`.** Filter these first, since they are the rows where the register may still be encumbered.
- Where the underlying security agreement is absent, add `; underlying obligation unreadable`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state, and it is common here — **a bare financing statement typically references nothing at all**, which is why the Excel join rather than this column carries the matching work.

## Output format

One line per missing document:

`[Name as referenced] — [date or number as stated][; flag]`

Return no more than 8 lines and no more than 80 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Confirmed against current search** | Yes (date) / No / Search not obtained |
| **Facility identified** | Facility [ref] / Undisclosed debt / Stale filing / Involuntary lien / Unresolved |
| **Release required at closing** | Yes / No / Already released |
| **Release responsibility** | Lender files / Buyer files / Seller files / Unresolved |
| **Name variance action** | None / Confirm with lender / Amend before closing / Unresolved |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Review every row.** This table is small and every active filing is either a
release task or an undisclosed obligation.

### Reconciliation work that never belongs in a column

- **Current searches.** **This table reflects what the seller produced. It is not
  the register.** Commission current searches for every target entity in every
  jurisdiction of organisation and every jurisdiction of material operation, plus
  IP office searches for material assets, plus real property searches for owned
  sites. **Run them against every former name from the Corporate table's
  `Prior Names` column as well** — a filing under a former name will not appear in
  a search under the current one.
- **The facility match.** Join this table's `Secured Party as Filed` against the
  Facilities table's `Lender or Agent` in Excel. Work the exceptions in both
  directions:
  - **A filing with no facility** means undisclosed debt or a stale filing. Both
    need resolving before closing.
  - **A facility with no filing** may mean an unperfected lien, which is the
    lender's problem but changes the negotiation, or a filing the seller did not
    produce.
  - **A filing whose facility is shown as repaid** is a release nobody filed.
- **Name variance resolution.** Every `Material variance` and
  `Matches a former name` row, assessed by counsel. Whether a variance is
  seriously misleading is a legal question, and the answer determines whether the
  lender needs an amendment before closing.
- **Release checklist.** Every row where Status is `Active`, `Active, continued`,
  `Assigned`, `Partially released`, or `Terminated, filing not evidenced`, with a
  named owner and the filing responsibility settled. **The Facilities table's
  `Payoff and Release Mechanics` column tells you whether the lender is obliged to
  file** — where it is not, the terminations are the buyer's task and they are the
  single most commonly missed post-closing item in a financing.
- **Involuntary liens.** Every judgment, tax, or mechanics lien, traced to its
  underlying obligation in the Litigation, Tax, or Real Estate workstreams. **An
  involuntary lien is evidence of an unpaid obligation**, and the lien itself is
  usually the smaller half of the problem.
- **IP recordations.** Every `IP security recordation` row against the IP
  Registrations table's `Encumbrances of Record` column, and against the
  Facilities table's `IP Included in Collateral` column. Mismatches in any
  direction are findings.

---

## Test set

- [ ] UCC-1 with an exact debtor name match and no records against it
- [ ] UCC-1 with a continuation extending the lapse date
- [ ] UCC-1 whose stated lapse date has passed with no continuation
- [ ] UCC-1 filed against a misspelled distinctive word in the debtor name
- [ ] UCC-1 differing only in punctuation before the entity suffix
- [ ] UCC-1 filed with `Inc.` where the entity is an LLC
- [ ] UCC-1 filed against a target entity's former name
- [ ] UCC-1 filed against a trade name only
- [ ] UCC-1 filed against an individual founder
- [ ] UCC-1 filed against a third-party entity with a similar name
- [ ] UCC-1 filed under an individual-name field for a registered organisation
- [ ] UCC-1 filed in a state other than the stated jurisdiction of organisation
- [ ] UCC-1 with an all-assets collateral description
- [ ] UCC-1 with an enumerated collateral description across many categories
- [ ] UCC-1 whose collateral is defined by a schedule not produced
- [ ] UCC-1 with a UCC-3 amendment adding collateral
- [ ] UCC-1 with a UCC-3 amendment correcting the debtor name
- [ ] UCC-1 with a UCC-3 assignment to a credit fund
- [ ] UCC-1 with a partial release recorded
- [ ] UCC-1 with a termination bearing an office stamp
- [ ] UCC-1 with a signed termination and no filing evidence
- [ ] Standalone UCC-3 termination produced without the original filing
- [ ] Fixture filing against a named property
- [ ] Mortgage recorded against an owned property, also in the Real Estate table
- [ ] IP security recordation with a reel and frame reference
- [ ] Judgment lien
- [ ] Tax lien
- [ ] Mechanics lien
- [ ] Non-US charge registration
- [ ] Filing known only from a search report entry
- [ ] Filing produced as an unstamped form copy
- [ ] Office-certified copy of a filing
- [ ] Search report entry whose search date is nine months before the as-of date
- [ ] Filing identifying its underlying security agreement, which is in the unit
- [ ] Filing whose underlying facility is shown as repaid by a payoff letter in the unit
- [ ] Bare financing statement identifying no underlying agreement

Then test the dependencies: change `Debtor Name as Filed` from an exact match to a
misspelled name and confirm `Debtor Name Match` moves to
`Material variance from a target entity`. Change `Filing Type` from
`UCC-1 financing statement` to `Mortgage or deed of trust` and confirm
`Lapse or Continuation Due Date` re-runs and can reach
`Not applicable — does not lapse`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
