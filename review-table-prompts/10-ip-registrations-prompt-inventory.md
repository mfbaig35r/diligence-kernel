# Prompt Inventory — IP: Registrations

Table 10 of the POC. First of three IP tables.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - IP`
- Review unit: **one registered or applied-for IP asset** — its registration
  certificate or application, any office correspondence, renewal and maintenance
  receipts, and any recordation confirmation produced for it
- Grouping used: **yes**, typically 1–5 documents per unit
- Intended reviewers and downstream use: IP and corporate/M&A teams; feeds the
  schedule of registered IP, the chain-of-title analysis, the lien cross-check,
  and the coverage register
- Inventory version: v1.0

### Why IP is three tables

`review-tables.md` §5 collapsed registrations, chain of title, and technology into
one table, which is why `N/A` was doing so much work there. They have three
different row units and three different roles:

| Table | Row | Role | Read for |
|---|---|---|---|
| Registrations | One asset | Filing | Status, ownership of record, effectiveness |
| Chain of Title | One assignment | Instrument | What the operative words transfer |
| Technology and Open Source | One report | Analysis | Scope, limitation, and findings |

A registration certificate and an assignment cannot share a schema. Neither can an
assignment and a penetration test report.

### What this table is for

Two questions, and the second is the important one:

1. **What is registered, where, and is it live?** Status, jurisdiction, and the
   next maintenance date.
2. **Does the target own it?** `Owner Matches Target Entity` is the finding —
   a mismatch means either an unrecorded assignment, which is a chain-of-title
   problem, or an asset the target does not own, which is a very different
   problem.

## Assumptions to confirm before running

1. One row is one asset in one jurisdiction. A trademark registered in six
   countries is six rows, because status, dates, and maintenance differ by
   jurisdiction. A single file covering six jurisdictions is a compilation and
   must be split.
2. Licences in and out are **not** rows here. Inbound and outbound licences are
   agreements, reviewed in Contracts Core and Commercial with
   `Counterparty Type` and the IP grant columns.
3. Unregistered rights — trade secrets, know-how, unregistered marks — are not
   rows here. They have no registry record, and they are addressed in the
   Technology table and in the employment IP assignment coverage check.
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

[Project name]. Buyer-side intellectual property diligence on the target group listed below. This table reviews registered and applied-for IP assets.

One row is one IP asset in one jurisdiction: its registration certificate or application, any office correspondence, renewal and maintenance receipts, and any recordation confirmation produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Target group

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the asset or its owner.
- **Report what the registry documents state. Do not assess validity, enforceability, infringement, or freedom to operate.** Those are legal conclusions and none of them is in a registration certificate.
- Where two documents in the unit address the same fact, report the fact as stated in the most recently dated document that addresses it, and identify that document by its printed title and date.
- Report names, numbers, and dates exactly as printed. Do not normalize, reformat, or correct a registration number, and do not expand or shorten an owner name.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Asset Type
  Title or Mark
  Office and Jurisdiction
  Record Owner

Stage 2 — Ownership test
  Record Owner ──→ Owner Matches Target Entity

Stage 3 — Registry facts, routed on asset type
  Asset Type ──→ Registration or Application Number
                 Filing Date
                 Registration or Grant Date
                 Status
                 Scope
                 Next Maintenance or Renewal Date

Stage 4 — Encumbrance and family
  Encumbrances of Record
  Licensees of Record
  Related Applications or Family

Stage 5 — Coverage
  Documents in Unit ──→ Referenced but Not Produced
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Referenced but Not Produced | v1.0 | draft |
| 2 | Asset Type | Classify | — | Registration or Application Number; Filing Date; Registration or Grant Date; Status; Scope; Next Maintenance or Renewal Date | v1.0 | draft |
| 3 | Title or Mark | Free Response | — | — | v1.0 | draft |
| 4 | Registration or Application Number | Free Response | @Asset Type | — | v1.0 | draft |
| 5 | Office and Jurisdiction | Free Response | — | — | v1.0 | draft |
| 6 | Record Owner | Free Response | — | Owner Matches Target Entity | v1.0 | draft |
| 7 | Owner Matches Target Entity | Classify | @Record Owner | — | v1.0 | draft |
| 8 | Filing Date | Date | @Asset Type | — | v1.0 | draft |
| 9 | Registration or Grant Date | Date | @Asset Type | — | v1.0 | draft |
| 10 | Status | Classify | @Asset Type | — | v1.0 | draft |
| 11 | Next Maintenance or Renewal Date | Date | @Asset Type | — | v1.0 | draft |
| 12 | Scope | Free Response | @Asset Type | — | v1.0 | draft |
| 13 | Encumbrances of Record | Free Response | — | — | v1.0 | draft |
| 14 | Licensees of Record | Free Response | — | — | v1.0 | draft |
| 15 | Related Applications or Family | Free Response | — | — | v1.0 | draft |
| 16 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Referenced but Not Produced`
- Purpose: inventory the registry documents for the asset.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the registration certificate, the application, office actions and responses, notices of allowance or publication, renewal and maintenance receipts, assignment recordation confirmations, and registry extracts or status printouts.
- Treat exhibits and drawings attached to a document as part of that document.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated or filing-stamped date.
- State the function as one of `Certificate`, `Application`, `Office action`, `Response`, `Allowance or publication`, `Renewal or maintenance`, `Recordation`, `Registry extract`, or `Other`.
- **Where a document relates to a different asset or jurisdiction than the subject of this row, still list it and append ` [relates to [asset or jurisdiction]]`.** A unit covering several jurisdictions produces a merged row, and this is how that surfaces.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 10 lines and no more than 90 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Asset Type

- Native type: Classify
- Configured options, in UI order: `Patent`, `Patent application`, `Trademark`, `Trademark application`, `Copyright registration`, `Design or design patent`, `Domain name`, `Plant variety or other sui generis`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: six columns
- Purpose: route every registry column, since a granted patent, a pending
  trademark, and a domain name carry different fields entirely.

```markdown
## Task

Classify the type of intellectual property right this review unit documents. Choose exactly one configured option.

## Scope

- Classify the right the documents record. Exclude rights merely mentioned, such as a mark referenced in a patent specification.

## Classification rules

- **Distinguish granted rights from pending ones.** `Patent` and `Patent application`, and `Trademark` and `Trademark application`, are separate options because the dates, the status, and the maintenance obligations differ. A pending application has no grant date and no renewal date.
- `Patent`: a granted or issued patent, evidenced by a patent number and a grant or issue date.
- `Patent application`: a filed application not yet granted, whether published or unpublished, including provisional, PCT, continuation, and divisional applications.
- `Trademark`: a registered mark, evidenced by a registration number and a registration date.
- `Trademark application`: a filed application not yet registered, whether published, opposed, or allowed.
- `Design or design patent`: a registered design, design patent, or industrial design right.
- `Domain name`: a domain registration, evidenced by registrar records rather than an IP office.
- `Copyright registration`: a copyright registered with a national office. Unregistered copyright is not a row in this table.

Classify on the current state of the right at the most recently dated document in the unit. **Where an application in the unit has since been granted per a later document, classify as granted.**

## Fallback rules

- Use `Other` where the documents record a right none of the options describes.
- Use `Unable to determine` where the documents are too fragmentary to identify the right.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Title or Mark

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what the right actually covers, in the form the registry records it.

```markdown
## Task

State the title, mark, or name of the asset as recorded.

## Rules

- For a patent or application, report the invention title exactly as printed.
- **For a trademark, report the mark exactly as printed, and state its form**: word mark, device or logo, stylised, combined, sound, or colour. A word mark and a device mark for the same words are different rights with different scope, and reporting only the words loses that.
- For a design, report the design title and the article it applies to.
- For a domain name, report the full domain including the extension.
- For a copyright registration, report the work title and the class of work.
- Report the mark or title exactly as printed, including capitalization, punctuation, and any stylisation note. **Do not normalize or correct it.**
- Where the documents record a transliteration or translation of a non-Latin mark, report both.
- Do not describe the goods or services here; those belong to the Scope column.

## Fallback rules

- Return `Unable to determine` where no document in the unit states the title or mark, or it is illegible.

## Output format

`[Title or mark as printed][ — [form]]`. Return no more than 30 words.
```

---

### 4. Registration or Application Number

- Native type: Free Response
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: the registry identifier, which is the key for verifying status
  independently and for matching against lien filings and assignment records.

```markdown
## Established result

- Asset Type: @Asset Type

## Task

State the registry numbers recorded for this asset.

## Rules by asset type

- `Patent`: the patent or grant number, **and** the application number, since both appear and both are needed to trace the file.
- `Patent application`: the application number, and the publication number where published.
- `Trademark`: the registration number and the application or serial number.
- `Trademark application`: the application or serial number.
- `Design or design patent`: the registration or patent number and the application number.
- `Copyright registration`: the registration number.
- `Domain name`: return `Not applicable — domain registration`, and report the registrar and any registry identifier in the evidence field. Domains have no office number.

## Rules

- **Report each number exactly as printed, including any country prefix, slashes, spaces, and check digits. Do not reformat.** Registry searches fail on reformatted numbers, and this cell is what a verification search is run from.
- Label each number, for example `Reg. 5,412,889; App. 87/234,110`.
- Where a PCT or international registration number appears alongside a national number, report both and label them.

## Fallback rules

- Return `Not stated` where the documents state no number for the asset.
- Return `Unable to determine` where numbers in the unit conflict, or are illegible.

## Output format

`[Label] [number]` per number, separated by semicolons. Return no more than 25 words.
```

---

### 5. Office and Jurisdiction

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: where the right subsists, which determines its territorial reach and
  whether the row needs local counsel.

```markdown
## Task

State the office that granted or received the filing, and the jurisdiction the right covers.

## Rules

- Report the office as printed, for example `United States Patent and Trademark Office`, `EUIPO`, `WIPO`, `UK Intellectual Property Office`.
- **Report the jurisdiction the right covers, which is not always the office.** A European Union trade mark filed at EUIPO covers all member states; an international registration at WIPO covers only the designated countries. Report the designated countries where the documents list them.
- For an international registration, report the designations as stated, and where more than eight are listed report the first eight and append ` and [N] further designations`.
- For a domain name, report the registrar and the top-level domain, and state that the right is contractual rather than territorial.
- Where the right arises from a regional system, name the system.

## Fallback rules

- Return `Unable to determine` where the documents identify no office or jurisdiction.

## Output format

`Office: [as printed]; covers: [jurisdiction or designations]`. Return no more than 45 words.
```

---

### 6. Record Owner

- Native type: Free Response
- Upstream: none
- Downstream: `Owner Matches Target Entity`
- Purpose: who the registry says owns the asset, exactly as recorded.

**Report the record owner, not the owner you expect.** The whole value of the next
column depends on this one reporting what the registry actually says, including
misspellings and outdated names.

```markdown
## Task

State the owner, applicant, registrant, or proprietor of record for this asset.

## Rules

- Report the name **exactly as printed on the registry document**, including entity suffix, punctuation, misspellings, and any outdated form. Do not correct, normalize, expand, or update it. An error in the register is a finding, and correcting it here hides it.
- Where the documents record a change of owner, report the current record owner and append ` (recorded change from [prior owner], [YYYY-MM-DD])`.
- Where more than one owner is recorded, list each on its own line and append ` [co-owned]` to the first line. **Co-ownership is a material finding**, because a co-owner's consent is usually needed to license or enforce.
- Where the recorded owner is an individual, report the name as printed.
- Report the recorded owner's address country only where it appears, since it helps distinguish similarly named entities.
- Do not report an inventor, author, or designer as the owner. Report them in the evidence field.

## Fallback rules

- Return `Not stated` where no document in the unit records an owner.
- Return `Unable to determine` where owners recorded in documents of the same date conflict, or where the name is illegible.

## Output format

`[Owner name exactly as printed][, [country]]` per line, with any qualifier appended. Return no more than 40 words.
```

---

### 7. Owner Matches Target Entity

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Recorded to a former name`, `Recorded to an individual`, `Recorded to a third party`, `Co-owned with a third party`, `No owner recorded`, `Unable to determine`
- Upstream: `@Record Owner`
- Downstream: none
- Purpose: the finding this table exists to produce.

**A mismatch is one of three very different problems** and the option set separates
them. Recorded to a former name is a recordation housekeeping item. Recorded to an
individual — usually a founder — is a chain-of-title gap requiring an assignment
before closing. Recorded to a third party may mean the target does not own the
asset at all. Filter this column and you have the IP remediation list.

```markdown
## Established result

- Record owner: @Record Owner

Use this result and the target group list in the Table Instructions. Confirm the recorded name against the documents in the current unit.

## Task

Classify the relationship between the record owner and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `No owner recorded`: Record Owner returned `Not stated`.
2. `Co-owned with a third party`: more than one owner is recorded and at least one is not a target entity. **Use this in preference to the options below**, because co-ownership constrains licensing and enforcement regardless of who else holds it.
3. `Recorded to an individual`: the record owner is a natural person. This is the founder-holds-the-patent case and it is a chain-of-title gap.
4. `Recorded to a former name`: the recorded name matches a prior name of a target entity as disclosed in the documents, rather than its current name.
5. `Recorded to a third party`: the recorded owner is an entity that is not a target entity and is not a former name of one.
6. `Matches with name variance`: the recorded name is the same entity as a listed target entity but differs in form — a misspelling, a missing or different suffix, an abbreviation, a different punctuation, or a divisional or trading name.
7. `Matches a target entity exactly`: the recorded name is character-for-character a name on the target group list.

**Do not resolve a variance by assuming.** Where the recorded name is similar to a target entity but could be a different entity — a similarly named affiliate, a parent, or an unrelated company — use `Recorded to a third party` and note the similarity in the evidence field. Overstating a match hides the finding; overstating a mismatch merely creates work.

Where a target entity's former name is not disclosed in the documents in this unit, you cannot use `Recorded to a former name`. Use `Recorded to a third party`, and the Corporate table's `Prior Names` column is where the reviewer resolves it.

## Fallback rules

- Use `Unable to determine` where the recorded name is illegible, or where Record Owner returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 8. Filing Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: the filing or priority date, which fixes the right's place in time and
  drives every deadline that follows.

```markdown
## Established result

- Asset Type: @Asset Type

## Task

Identify the filing date of this asset, and the earliest priority date claimed.

## Rules by asset type

- `Patent`, `Patent application`, `Design or design patent`: the filing date, **and** the earliest priority date claimed where the documents state one. Report both, labelled.
- `Trademark`, `Trademark application`: the filing or application date, and any priority date claimed.
- `Copyright registration`: the date of the registration application, and the date of creation or first publication where stated.
- `Domain name`: the creation or registration date recorded by the registrar.

## Excluded dates

- The registration, grant, or issue date, which has its own column
- The publication date
- The date of an office action or response
- The date of a renewal or maintenance payment
- File name and metadata dates, and printing, download, and scan dates

## Rules

- **Report the earliest priority date separately where one is claimed.** The priority date, not the filing date, determines what prior art applies and what the right is measured against, and a patent claiming priority to a much earlier application is a materially different asset.
- Report dates as printed. Do not calculate any deadline from them.

## Output format

`Filed [YYYY-MM-DD][; priority [YYYY-MM-DD]]`. Preserve partial precision as printed. Return `Not stated` where no filing date appears.
```

---

### 9. Registration or Grant Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: when the right came into force, which starts the term and the
  maintenance cycle.

```markdown
## Established result

- Asset Type: @Asset Type

## Task

Identify the date this right was granted, registered, or issued.

## Rules by asset type

- `Patent`, `Design or design patent`: the grant or issue date.
- `Trademark`: the registration date.
- `Copyright registration`: the effective date of registration.
- `Domain name`: return `Not applicable — domain has no grant date`, and the expiry is reported in the maintenance column.
- `Patent application`, `Trademark application`: return `Not applicable — not yet granted`. **Where a later document in the unit shows the application has been granted, the Asset Type column should have classified it as granted**, so a granted date here with a pending asset type is a routing inconsistency worth flagging in the evidence field.

## Excluded dates

- The filing or priority date
- The publication or allowance date. **An allowance is not a grant** — allowed applications still require an issue fee and can lapse
- The date of a certificate reprint or a corrected certificate, unless it is the only date available
- File name and metadata dates

## Rules

- Report the date as printed. Do not calculate the expiry from it.
- Where a corrected or reissued certificate is in the unit, report the original grant or registration date and note the correction in the evidence field.

## Output format

`YYYY-MM-DD`, or one of the exact fallback values above. Preserve partial precision as printed. Return `Not stated` where the right is granted but no date appears.
```

---

### 10. Status

- Native type: Classify
- Configured options, in UI order: `Registered or granted`, `Pending`, `Published`, `Allowed`, `Opposed or contested`, `Office action outstanding`, `Abandoned`, `Expired or lapsed`, `Cancelled or invalidated`, `Not stated`, `Unable to determine`
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: whether the right is live. **The status as at the most recent document
  in the unit**, which is not the same as the status today.

**Scope discipline.** A registry document speaks as of its own date. Nothing in a
data room updates it, and a certificate from 2021 does not establish that the mark
is registered now. This column reports what the documents show and the reviewer
verifies live status against the register.

```markdown
## Established result

- Asset Type: @Asset Type

## Task

Classify the status of this right as shown by the most recently dated document in the review unit. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Cancelled or invalidated`: the documents record cancellation, invalidation, revocation, or a successful challenge.
2. `Expired or lapsed`: the documents record expiry, lapse for non-payment, or a term that the documents state has ended.
3. `Abandoned`: the documents record abandonment, withdrawal, or a final refusal not appealed.
4. `Opposed or contested`: an opposition, cancellation action, inter partes proceeding, or third-party challenge is recorded as pending.
5. `Office action outstanding`: an office action, examination report, or refusal is recorded with no response evidenced in the unit. **This is a live deadline** and it is why the state is separate from `Pending`.
6. `Allowed`: the application is allowed or accepted, with grant or registration not yet recorded. Note in the evidence field any issue-fee or publication deadline stated.
7. `Published`: the application is published with examination not concluded.
8. `Pending`: the application is filed and none of the above applies.
9. `Registered or granted`: the right is granted or registered and none of the adverse states above applies.

**Report the status as at the most recent document, and give that document's date in the evidence field.** Compare it to the diligence as-of date in the Table Instructions, and where the most recent document is more than twelve months older than the as-of date, note that in the evidence field.

## Fallback rules

- Use `Not stated` where the documents record the asset without stating any status.
- Use `Unable to determine` where statuses recorded in documents of the same date conflict, or where the relevant text is illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 11. Next Maintenance or Renewal Date

- Native type: Date — confirm the type accepts `Not applicable` and `Not stated`
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: the next deadline. **An annuity or renewal lapsing during the deal is
  avoidable, embarrassing, and irreversible for a patent.**

```markdown
## Established result

- Asset Type: @Asset Type

## Task

Identify the next renewal, maintenance, annuity, or affidavit deadline for this asset.

## Rules by asset type

- `Patent`: the next maintenance fee or annuity due date the documents state.
- `Trademark`: the next renewal date, and separately any declaration of use or affidavit deadline, since missing the affidavit cancels the registration even where the renewal is not yet due.
- `Design or design patent`: the next renewal date where the right is renewable.
- `Patent application`, `Trademark application`: any response, issue-fee, or national-phase deadline the documents state. **A national-phase entry deadline is the highest-consequence date in this table**, because missing it forfeits the right in every country not yet entered.
- `Domain name`: the registration expiry date.
- `Copyright registration`: return `Not applicable` unless the documents state a renewal requirement.

## Rules

- **Report only a date the documents state. Do not calculate a deadline from the grant date, the filing date, or a statutory schedule**, even where the schedule is well known. A calculated annuity date looks identical to a stated one in an export and it is not verification.
- Where more than one deadline is stated, report the earliest and append ` (next of [N] stated deadlines)`.
- Compare the reported date to the diligence as-of date in the Table Instructions. Where it falls before that date, append ` [deadline passed on record]`. Where it falls within six months after it, append ` [deadline within 6 months]`.
- Report any grace period the documents state in the evidence field.

## Fallback rules

- Return `Not stated` where the documents state no forward deadline. **This is common and it is a coverage finding**: the renewal schedule or docket report was not produced.
- Return `Unable to determine` where stated deadlines conflict, or are illegible.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended, or one of the exact fallback values above.
```

---

### 12. Scope

- Native type: Free Response
- Upstream: `@Asset Type`
- Downstream: none
- Purpose: what the right actually covers, which determines whether it protects
  the business the buyer is acquiring.

```markdown
## Established result

- Asset Type: @Asset Type

## Task

Report the scope of protection recorded for this asset.

## Rules by asset type

- `Trademark`, `Trademark application`: the classes with their numbers, and the goods and services as recorded. **Where the specification exceeds 40 words, report each class number with the goods summarised in six words or fewer.** Note any class that has been deleted, restricted, or refused.
- `Patent`, `Patent application`: the subject matter of claim 1 in fifteen words or fewer, the total number of claims, and the number of independent claims. **Do not summarise the whole claim set and do not construe any claim.**
- `Design or design patent`: the article the design applies to, and the number of embodiments or figures.
- `Copyright registration`: the class of work and any statement of the material deposited.
- `Domain name`: return `Not applicable — no scope of protection`.

## Rules

- Report the scope as recorded. **Do not assess breadth, strength, validity, or whether the scope covers any particular product.** Whether a claim covers the target's product is an infringement or clearance opinion and it is not in a certificate.
- Report any recorded limitation, disclaimer, or partial refusal, since a restricted specification is a materially narrower right.
- Where a class or claim set was amended during prosecution and the documents show it, report the final recorded scope and note the amendment in the evidence field.

## Fallback rules

- Return `Not stated` where the documents record the asset without stating its scope.
- Return `Unable to determine` where the scope statement is illegible or internally inconsistent.

## Output format

For a mark: `Class [N]: [goods, brief]` per line. For a patent: `Claim 1: [subject]; [N] claims, [N] independent`. Otherwise as the rules above provide.

Return no more than 8 lines and no more than 90 words.
```

---

### 13. Encumbrances of Record

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: security interests and liens recorded against the asset. **Matched
  against the Debt lien-filing table, this is where a security interest in core IP
  surfaces.**

```markdown
## Task

Report any security interest, lien, charge, or other encumbrance recorded against this asset.

## Scope

- Include security interests, mortgages, charges, pledges, and liens recorded with the office.
- Include any recorded assignment for security purposes.
- Include any court order, injunction, or restraint recorded against the asset.
- Include any recorded judgment lien.
- Exclude licences, which have their own column.
- Exclude co-ownership, which is reported in Record Owner.

## Rules

- For each encumbrance, report the secured party exactly as recorded, the recordation date, the reel and frame or recordation number, and whether a release or termination is also recorded.
- **Where a security interest is recorded with no release, append ` [no release recorded]`.** A live security interest over a core asset has to be released at closing, and this is the flag the payoff and lien-release checklist is built from.
- Report a recorded release with its date, since a stale unreleased filing is a different problem from a live one.
- Do not assess perfection, priority, or enforceability.

## Fallback rules

- Return exactly `None of record` where the documents record no encumbrance.

Note: `None of record` is a positive finding, not a fallback state. **It means these documents record none. It does not mean none exists** — only a current search of the register and the relevant UCC or companies registry establishes that, and that search belongs in the Debt workstream.

- Return `Unable to determine` where recorded encumbrances are illegible or conflicting.

## Output format

One line per encumbrance:

`[Secured party] — recorded [YYYY-MM-DD] — [recordation reference] — [released [YYYY-MM-DD] | no release recorded]`

Return no more than 6 lines and no more than 75 words.
```

---

### 14. Licensees of Record

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: licences recorded with the office, which can bind a purchaser of the
  asset and constrain what the buyer can do with it.

```markdown
## Task

Report any licence recorded with the office against this asset.

## Scope

- Include exclusive and non-exclusive licences recorded with the office or registrar.
- Include any recorded consent, coexistence, or settlement agreement affecting use of the asset. **A coexistence agreement is a permanent constraint on a trademark** and it is frequently the most consequential thing recorded against a mark.
- Include any recorded franchise or distribution right.
- Exclude unrecorded licences, which are agreements reviewed in the Contracts tables.
- Exclude security assignments, which belong to Encumbrances of Record.

## Rules

- For each entry, report the licensee or counterparty exactly as recorded, the recordation date, whether the licence is recorded as exclusive or non-exclusive, and any recorded territory or field limitation.
- **Where an exclusive licence is recorded, append ` [exclusive — may bind purchaser]`.** An exclusive licence of record can exclude the owner itself and it survives a transfer of the asset.
- Where a coexistence or consent agreement is recorded, append ` [use constraint]`.
- Report any recorded termination with its date.
- Do not assess enforceability or whether the licence binds a transferee.

## Fallback rules

- Return exactly `None of record` where the documents record no licence or consent.

Note: this is a positive finding, not a fallback state. Most licences are never recorded, so an empty cell here says very little about whether licences exist.

- Return `Unable to determine` where recorded entries are illegible or conflicting.

## Output format

One line per entry:

`[Counterparty] — recorded [YYYY-MM-DD] — [exclusive | non-exclusive | consent or coexistence] — [territory or field, or "no limitation recorded"]`

Return no more than 6 lines and no more than 75 words.
```

---

### 15. Related Applications or Family

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the asset's family, so a reviewer can tell whether the schedule of
  registered IP is complete. **Family members named here and absent from the table
  are the gap.**

```markdown
## Task

Report every related application or registration this asset's documents identify.

## Scope

- Include parent, continuation, continuation-in-part, divisional, and reissue applications, and any application from which priority is claimed.
- Include national-phase and regional filings derived from the same international application.
- Include corresponding foreign filings the documents identify.
- Include related marks in other classes or jurisdictions where the documents identify them.
- Include any application the documents identify as a successor or replacement for this one.
- Exclude prior art references cited during examination. **Cited prior art is not family**, and reporting it here would swamp the cell.
- Exclude the target's unrelated assets mentioned incidentally.

## Rules

- Report each family member with its relationship, its number as printed, and its jurisdiction.
- **Where a related filing in another jurisdiction is identified, append ` [check schedule]`.** These are the rows that should exist in this table and may not, and this flag is what the completeness check filters on.
- Where an international application designates countries with no corresponding national filing identified, note that in the evidence field.
- Report relationships as the documents state them. Do not infer a family relationship from a similar title or a shared priority date alone.

## Fallback rules

- Return exactly `None identified` where the documents identify no related filing.
- Return `Unable to determine` where family references are illegible or inconsistent.

## Output format

One line per family member:

`[Relationship] — [number] — [jurisdiction][ [check schedule]]`

Return no more than 10 lines and no more than 90 words.
```

---

### 16. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this asset's file refers to that is not present.
  Feeds the coverage register.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document relating to this asset that the documents in this unit refer to and that is not present.

## Scope

- Include assignments and recordation confirmations referenced but absent. **These are the highest-value gaps this column finds**, because an assignment referenced and not produced is a chain-of-title hole.
- Include office actions, responses, and examination reports referenced but absent.
- Include renewal, maintenance, and annuity receipts referenced but absent.
- Include declarations of use, affidavits, and specimens referenced but absent.
- Include powers of attorney and agent appointment documents referenced but absent.
- Include licences, consents, coexistence agreements, and settlement agreements referenced but absent.
- Include related applications and priority documents referenced but absent, where the documents indicate they belong to this asset's file.
- Include any docket, portfolio schedule, or status report referenced as recording this asset.
- Exclude cited prior art.
- Exclude statutes, regulations, treaties, and office practice manuals.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- Where a reference is generic, for example `the assignment recorded at reel 4412`, report it as printed and add the recordation reference.
- **Where an assignment or recordation document is referenced but absent, add `; chain of title gap`.** This flag lets the population be filtered against the Chain of Title table across the whole portfolio.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; chain of title gap]`

Return no more than 12 lines and no more than 110 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Live status verified against register** | Yes (date) / No / Not required |
| **Chain complete** | Yes / Gap identified / Unresolved |
| **Critical to product or brand** | Yes / No / Unknown |
| **Transferable in this deal** | Yes / Consent required / No / Unclear |
| **Remediation required before closing** | None / Recordation / Assignment / Renewal / Release / Multiple |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

Critical fields do not ship unreviewed: record owner, owner match, status,
maintenance date, encumbrances.

### Reconciliation work that never belongs in a column

- **Live status verification.** Every material asset's status checked against the
  live register, not against the certificate in the data room. A certificate
  proves the position on its own date and nothing more.
- **Portfolio completeness.** Assets the target claims to own, from its own
  schedule and its marketing, against the rows in this table. Also every
  `[check schedule]` flag from `Related Applications or Family`. **An asset the
  business relies on with no row here is the finding.**
- **Ownership remediation list.** Filter `Owner Matches Target Entity` to anything
  other than `Matches a target entity exactly`, and work each against the Chain of
  Title table. Recorded to an individual and recorded to a third party are the two
  to escalate.
- **Name-variance resolution.** Filter to `Matches with name variance` and
  `Recorded to a former name`, and check against the Corporate table's
  `Prior Names`. Recordation of a name change is cheap; discovering at closing
  that it was never done is not.
- **Lien cross-check.** Every `[no release recorded]` encumbrance against the Debt
  lien-filing table and the payoff schedule.
- **Maintenance calendar.** Every `[deadline within 6 months]` and
  `[deadline passed on record]` flag, sequenced against the deal timetable, with a
  named owner. **A lapsed patent annuity is usually irrecoverable.**

---

## Test set

- [ ] Granted US patent with a certificate, recorded to a target entity exactly
- [ ] Pending patent application with an outstanding office action
- [ ] Patent application allowed but not yet issued
- [ ] Patent claiming priority to a much earlier provisional
- [ ] PCT application with designations and no national filings identified
- [ ] Patent recorded to a founder individually
- [ ] Patent recorded to a third-party entity with a similar name to a target entity
- [ ] Trademark recorded to a target entity's former name
- [ ] Trademark recorded with a misspelled owner name
- [ ] Word mark and a device mark for the same words, as two rows
- [ ] Trademark with a declaration of use deadline before the renewal date
- [ ] Trademark under opposition
- [ ] Trademark with a class deleted during prosecution
- [ ] EU trade mark, and a WIPO international registration with designations
- [ ] Co-owned patent with a university or third party
- [ ] Asset with a recorded security interest and no release
- [ ] Asset with a recorded security interest and a recorded release
- [ ] Trademark with a recorded coexistence agreement
- [ ] Asset with a recorded exclusive licence
- [ ] Domain name registration
- [ ] Copyright registration
- [ ] Design registration
- [ ] Asset whose most recent document is four years old
- [ ] Asset with a maintenance deadline that has passed on record
- [ ] Asset with a maintenance deadline within six months of the as-of date
- [ ] Asset with no forward deadline stated anywhere
- [ ] Asset file referencing an assignment recorded at a reel and frame, not produced
- [ ] Abandoned application
- [ ] Expired patent
- [ ] Single file covering the same mark in six jurisdictions

Then test the dependencies: change `Asset Type` from `Patent` to
`Patent application` and confirm `Registration or Grant Date` moves to
`Not applicable — not yet granted` and `Next Maintenance or Renewal Date` re-runs
against the application rules. Change `Record Owner` from a target entity to an
individual and confirm `Owner Matches Target Entity` moves to
`Recorded to an individual`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
