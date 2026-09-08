# M&A Diligence Extraction Schema

Draft for redline. Twelve categories, designed from the deal outputs backwards.

**Assumptions.** Buy-side. Private US target, multi-entity group. Stock purchase or
merger. Mid-market. Harvey Review Tables, UI only, with `@Column` references,
Table Instructions, native column types, cell locking, and document grouping
available.

If this is an **asset deal or a carve-out**, assignment analysis changes
materially throughout (every contract needs assignment consent, not just those
with anti-assignment clauses) and a shared-asset / TSA layer has to be added to
Contracts, IP, Real Estate, and Related-Party.

---

## 0. How columns were selected

A column belongs in the grid only if it feeds one of seven deal outputs:

| # | Output | What it decides |
|---|---|---|
| 1 | Consent and approval schedule | Whether you can close, and who has to sign |
| 2 | Closing conditions and regulatory calendar | The deal timetable |
| 3 | Purchase price and transaction payments | Payoffs, severance, acceleration, 280G, bonuses |
| 4 | Disclosure schedule and reps support | What the SPA has to say |
| 5 | Indemnity, escrow, special indemnity | Risk allocation |
| 6 | Integration, TSA, run-off | Day-one operability |
| 7 | Coverage register | What should exist and does not |

Columns are typed for Harvey: **C** = Classify, **FR** = Free Response,
**V** = Verbatim, **D** = Date, **$** = Currency, **N** = Number,
**Dur** = Duration, **H** = human-only.

Three rules applied throughout:

- **Classification and detail are separate columns.** Harvey cannot return a
  controlled enum plus structured free text in one cell.
- **A classified provision that drives a consent, a payment, or a closing
  condition gets a paired Verbatim column.** That is the spot-check mechanism and
  the drafting basis for the consent request.
- **Harvey reports what the document says. A human decides what it means.**
  Operative version, enforceability, materiality, approval sufficiency, and deal
  consequence are never Harvey columns.

### Fallback vocabulary

One controlled set, table-wide, in Table Instructions:

`Not addressed` (silent) · `Not stated` (typed columns only: no such value in the
document) · `Not applicable` (no meaningful application to this document type) ·
`Incorporated terms` (another document supplies the terms) · `Unable to
determine` (evidence exists but is conflicting, incomplete, or illegible)

No synonyms. No `N/A`, `None`, `Silent`, `Unclear`, `Not determinable`.

---

## 1. The universal spine

Every table carries these. Defined once here, not repeated per section. Put the
shared rules in Table Instructions; keep the routing logic in the columns.

### Orientation

| Column | Type | Purpose |
|---|---|---|
| Subject entity | FR | Which target-group entity is the subject or the contracting party, exact legal name. Without this a multi-entity group cannot be reconciled to the corporate chart |
| Document type | C | From the workstream vocabulary. Drives every downstream route |
| Document role | C | Instrument / Record / Correspondence / Analysis / Filing. Decides evidence standard and which columns apply |
| Execution status | C | Executed / Partially executed / Unsigned draft / Form or template / Certified copy / Filed and stamped. **Every substantive column depends on this.** A finding built on an unsigned draft is a finding built on nothing |
| Document date | D | With a document-type hierarchy and a stated basis. Excludes filename, notarization, and scan dates |
| Operative date | D | Effective / commencement date for instruments; as-of date for records. A record without an as-of date is unusable |
| Amends or issued under | FR | Base instrument, exact name as written. Assembles families without a family feature |
| **Referenced but not produced** | FR | Exhibits, schedules, side letters, amendments, and annexes named inside the document. **Seeds every coverage-register row.** The gaps nobody asked for because nobody knew they existed |
| Completeness | C | Complete / Pages missing / Exhibits missing / Signature page missing / Illegible in part. Separates a genuine `Unable to determine` from a prompt defect |
| Governing law | FR | Jurisdiction, or `Not addressed` |

### Human review block

| Column | Type | Values |
|---|---|---|
| Review status | H | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | H | Initials |
| Materiality | H | Critical / Material / Monitor / Immaterial |
| Deal consequence | H | Free text. The lawyer's conclusion |

Lock cells once `Verified`. Re-run in dependency order after any upstream change;
locking does not refresh dependents.

---

## 2. Intake Classification

**Rows:** one per file, over the whole data room.
**Feeds:** routing, and outputs 7.
**Purpose:** this table does not extract substance. It decides what everything
else sees.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Workstream | C | Eighteen values. Derive independently of Document type so mismatches surface as a signal |
| Secondary workstream | C | A DPA is privacy and commercial. An affiliate lease is related-party and real estate. Dual documents go to both projects |
| Counterparty | FR | The non-target party, exact name. `Not applicable` for internal records |
| Counterparty type | C | Customer / Vendor / Employee / Lender / Landlord / Regulator / Affiliate / Advisor / Other |
| **Compilation flag** | C | Single instrument / Multiple instruments in one file (state how many). A twenty-agreement PDF is one row and twenty instruments; it must be split before it can be reviewed |
| Signature evidence | C | Wet ink / E-signature platform / Typed name only / Signature block blank / Conformed copy. A typed name is not a signature |
| Language | C | English / Other (state which). Routes to local counsel rather than to a US-law analogue |
| Duplicate of | FR | Exact file name of an apparent duplicate or near-duplicate, or `Not applicable` |
| Classification confirmed | H | Blank / Confirmed / Reclassified |

**Do not skip the human column.** Classification is where an error is cheapest to
catch and most expensive to inherit.

---

## 3. Contracts

**Rows:** one per agreement family (base agreement grouped with its amendments,
SOWs, and order forms — up to 25 per unit).
**Feeds:** outputs 1, 3, 4, 5, 6, 7.
**Split:** two tables over the same project, joined on file name. ~30 columns
will not fit in one grid.

The two change-of-control columns and the assignment carve-out are the
highest-value cells in the matter.

### 3A. Contracts Core

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Counterparty | FR | Exact legal name |
| Counterparty type | C | Customer / Vendor / Reseller / Distributor / Partner / Other |
| Agreement type | C | MSA / SOW / Order form / Customer agreement / Reseller / Distributor / NDA / DPA / SLA / Side letter / Other |
| Initial term | Dur | Length of the initial term |
| Expiry of current term | D | The date that matters for the term sheet |
| Renewal mechanism | C | Automatic / On notice / None / `Not addressed` |
| Renewal length | Dur | Length of each renewal period |
| Notice to prevent renewal | Dur | The date you have to diarise |
| **Current term status** | C | In initial term / Renewed / Expired but performing / Terminated / `Unable to determine`. **An expired agreement still being performed is a finding**, and it is invisible in a plain expiry column |
| Termination for convenience — holder | C | Target only / Counterparty only / Either / Neither |
| Termination for convenience — notice | Dur | Notice required |
| Termination for convenience — language | V | Quoted |
| Termination for cause — grounds | FR | Grounds, summarised |
| Cure period | Dur | Cure period, if any |
| Termination on insolvency | C | Present / `Not addressed`. Interacts with financing and with any pre-closing restructuring |
| **Assignment restriction** | C | No restriction / Consent required / Consent, not to be unreasonably withheld / Prohibited / Permitted to affiliate or successor |
| **Succession carve-out** | C | Merger or successor expressly carved out / Expressly captured / Silent / `Unable to determine`. **This single cell decides whether a merger trips the clause.** A consent-required contract with a successor carve-out needs no consent |
| Assignment language | V | Quoted |
| **Change of control** | C | Consent required / Notice required / Termination right / Deemed assignment / `Not addressed` |
| **CoC — indirect changes captured** | C | Direct transfer only / Indirect or upstream change captured / `Unable to determine`. Decides whether a parent-level deal triggers it |
| CoC — threshold | FR | Any stated ownership or voting percentage, or `Not addressed` |
| **CoC language** | V | Quoted, verbatim |
| Amendments and orders referenced | FR | Every amendment, SOW, order, or side letter named, with dates. Compared against the intake table, **the difference is the gap** |
| Consent required for this structure | H | Yes / No / Ambiguous |
| Operative version confirmed | H | Yes / No, superseded / Chain incomplete |

### 3B. Contracts Commercial

| Column | Type | Purpose |
|---|---|---|
| Contract value stated | $ | Committed or stated value, if any |
| Pricing terms | FR | Fees or rates as written |
| Price increase mechanism | FR | Uplift, index, or benchmarking right, or `Not addressed` |
| Minimum commitment | $ | Take-or-pay, minimum purchase, or spend commitment |
| Commitment period | Dur | Period over which it applies |
| Exclusivity | C | Binds target / Binds counterparty / Mutual / `Not addressed` |
| Exclusivity language | V | Quoted |
| MFN | C | Present / `Not addressed`. Separate from exclusivity: different obligation, different consequence |
| Non-compete binding target | FR | Scope and duration, or `Not addressed` |
| Liability cap | FR | Amount or formula, `Uncapped`, or `Not addressed` |
| Cap carve-outs | FR | Which liabilities sit outside the cap. Uncapped indemnities are the real exposure |
| Indemnity — direction | C | Target indemnifies / Counterparty indemnifies / Mutual / `Not addressed` |
| Indemnity — scope | FR | What is indemnified, one sentence per direction |
| IP granted to counterparty | C | Licence / Assignment / Joint ownership / None / `Not addressed`. A customer contract that assigns deliverable IP away is an IP finding, not a contracts finding |
| Source code escrow | C | Present / `Not addressed` |
| Data protection terms | C | DPA in place / Terms in body / `Incorporated terms` / `Not addressed` |
| Insurance required of target | FR | Coverage types and limits imposed. Cross-checked against the insurance table |
| SLA and service credits | FR | Commitments and remedies, or `Not addressed` |
| Audit rights | C | Counterparty may audit target / Target may audit / Mutual / `Not addressed` |
| Dispute resolution | C | Courts / Arbitration (state seat and rules) / `Not addressed` |
| Revenue significance | H | Top 10 / Top 50 / Other / Unknown |

**Cross-document work, not columns.** Revenue concentration matching against
financial data; defined-term drift on `Affiliate` and `Change of Control` across a
family; which version is operative.

---

## 4. Corporate and Entity Structure

**Rows:** one per **entity**, with its charter, bylaws, amendments, and good
standing certificate grouped into the review unit. This is a different artifact
from a document grid and it is the one the deal team needs.
**Feeds:** outputs 1, 2, 4, 7.

Spine, plus:

### Identity and standing

| Column | Type | Purpose |
|---|---|---|
| Exact legal name | FR | As stated in the organisational documents |
| **Former or prior names** | FR | Every prior name referenced, or `Not addressed`. **Name changes break UCC and litigation searches**, and an unreported one invalidates a clean lien search |
| Entity type | C | Corporation / LLC / LP / LLP / General partnership / Other |
| Jurisdiction of formation | FR | State or country |
| Formation date | D | Distinct from the date of the principal document |
| State file or entity number | FR | The search key |
| Standing status | C | Active / Good standing / Delinquent / Suspended / Revoked / Dissolved / `Unable to determine` |
| Standing certificate as-of date | D | A good standing certificate is only as good as its date |
| Foreign qualifications | FR | Every jurisdiction of qualification listed |
| Registered agent | FR | Agent and address |
| Fiscal year end | FR | Feeds the tax and financial workstreams |

### Capital and governance

| Column | Type | Purpose |
|---|---|---|
| Authorized capital by class | FR | Classes, number authorized, par value. **Authorized only** |
| Issued and outstanding by class | FR | Separate concept, separate review consequence, separate column |
| Board size | N | Number of directors or managers |
| Board appointment rights | FR | Who appoints or elects whom, including investor designation rights |
| Officers named | FR | With titles, and whether stated as current or as at a past date |
| Quorum | FR | Board quorum requirement |
| Ordinary board vote | FR | Vote required for ordinary board action |
| **Supermajority and protective provisions** | FR | Every matter requiring supermajority, unanimous, or class approval |
| Protective provisions language | V | Quoted |
| **Stockholder approval threshold for merger or asset sale** | FR | The vote of holders required, by class. **Closing-critical, and absent from the current schema** |
| Approval threshold language | V | Quoted |

### Transfer and transaction triggers

| Column | Type | Purpose |
|---|---|---|
| **Drag-along** | C | Present / `Not addressed`. **Decides whether minority holders can be forced into the deal** — often the single most important corporate cell |
| Drag-along conditions | FR | Thresholds and conditions to exercise |
| Drag-along language | V | Quoted |
| Tag-along | C | Present / `Not addressed` |
| ROFR or ROFO | C | Present / `Not addressed` |
| Preemptive rights | C | Present / `Not addressed`. Distinct from restrictions on transfers of existing equity |
| Transfer restrictions | FR | Restrictions on transfer of existing equity |
| Transfer restriction language | V | Quoted |
| Deemed liquidation or CoC provision | FR | Including any deemed-liquidation definition, or `Not addressed` |
| Appraisal or dissenters' rights waiver | C | Present / `Not addressed` |
| D&O indemnification and advancement | FR | Scope, and whether advancement is mandatory. Survives closing and interacts with the D&O tail |
| Exculpation | C | Present / `Not addressed` |
| Charter amendment mechanics | FR | Who may amend, and by what vote |
| Bylaw amendment mechanics | FR | Board or stockholder, and by what vote |
| Subsidiaries named | FR | Every subsidiary referenced. Matched against the org chart; entities in one and not the other are the finding |
| Amendment and restatement history | FR | Every amendment or restatement referenced, with dates |

| Human column | Values |
|---|---|
| Approval required for this transaction | Board / Stockholder / Class vote / Both / None / Unclear |
| Approval obtained | Yes (reference) / No / Not yet required |
| Drag exercisable | Yes / No / Conditions unmet / Unclear |
| Authority defect | None / Ratification needed / Unresolved |

**Never a column:** which charter version is operative where a restatement and a
later amendment conflict.

---

## 5. Capitalization and Securities

**Missing entirely from the current set.** Rows: one per instrument, grant, or
holder.
**Feeds:** outputs 1, 3, 4.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Instrument type | C | Common / Preferred (state series) / Option / Warrant / SAFE / Convertible note / RSU / Restricted stock / Phantom |
| Holder | FR | Exact name |
| Holder type | C | Founder / Employee / Investor / Former employee / Advisor / Entity |
| Issuer | FR | Issuing entity |
| Quantity | N | Shares, units, or principal. State the unit |
| Grant or issue date | D | |
| Exercise or conversion price | $ | Or the formula as written |
| Conversion mechanics | FR | Discount, cap, maturity conversion, MFN — for SAFEs and notes |
| Vesting schedule | FR | Including cliff, or `Fully vested` |
| Vested to date | FR | As stated in the document only. **Never computed** |
| **Acceleration on CoC** | C | Single trigger / Double trigger / None / `Not addressed` |
| Acceleration language | V | Quoted. Feeds the transaction payments schedule |
| Liquidation preference | FR | Multiple, and participating or not. `Not applicable` for common and derivatives |
| Anti-dilution | C | Broad-based weighted average / Narrow-based / Full ratchet / `Not addressed` |
| Dividend rights | FR | Cumulative or not, rate |
| Redemption rights | C | Present / `Not addressed`. A redeemable instrument is debt-like in the price model |
| **Holder consent or veto right** | FR | Any consent right over a merger, sale, or financing. Aggregated, this is the approval list |
| Consent right language | V | Quoted |
| Transfer restrictions | FR | Including ROFR and market stand-off |
| Board approval referenced | FR | The consent or resolution authorising this issuance, named and dated, or `Not addressed` |
| 409A referenced | FR | The valuation relied on for the strike price, and its date |
| Securities law exemption | FR | Reg D, 701, or other exemption recited, or `Not addressed` |

| Human column | Values |
|---|---|
| Reconciles to certified cap table | Yes / No / Not on cap table |
| Holder consent required | Yes / No / Unclear |
| Transaction treatment | Cash out / Assume / Accelerate / Cancel / Unresolved |
| 280G implicated | Yes / No / Unassessed |

**Never Harvey:** fully diluted count, waterfall, acceleration cost, or any
reconciliation to the certified cap table. Export and do the arithmetic in Excel
against a certified source.

---

## 6. Employment and HR

**Rows:** one per individual agreement. Policies and the census are separate row
sets — different role, different schema.
**Feeds:** outputs 3, 4, 5, 6, 7.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Individual | FR | Name |
| **Employing entity** | FR | Which group entity employs them. Critical in a multi-entity group and in a carve-out |
| Role or title | FR | As stated |
| **Classification** | C | Employee / Independent contractor / Consultant, as characterised in the document. Feeds the misclassification review |
| Jurisdiction of employment | FR | Governs covenant enforceability and statutory entitlements |
| Start date | D | |
| Employment basis | C | At will / Fixed term / Indefinite with notice |
| Fixed term expiry | D | |
| Notice — by employer | Dur | |
| Notice — by employee | Dur | |
| Base compensation | $ | With period |
| Variable compensation | FR | Bonus, commission, or incentive terms, or `Not addressed` |
| Equity referenced | FR | Any grant referenced. Matched against the cap table; equity on the cap table with no agreement is a gap |
| **Severance entitlement** | FR | Amount and trigger, or `Not addressed`. Absent from the current schema and it is a purchase-price item |
| Severance language | V | Quoted |
| **Qualifying termination definition** | FR | What triggers severance |
| **Good reason definition** | FR | Or `Not addressed`. **This is what makes a double trigger real** — without a good-reason clause, a double trigger rarely fires |
| **CoC payment or benefit** | C | Single trigger / Double trigger / None / `Not addressed` |
| CoC benefit amount | FR | As stated |
| CoC language | V | Quoted |
| Retention or transaction bonus | FR | Or `Not addressed` |
| Non-compete | FR | Duration and geography |
| Non-compete language | V | Quoted |
| Non-solicit — employees | FR | Duration and scope |
| Non-solicit — customers | FR | Duration and scope |
| Garden leave | C | Present / `Not addressed` |
| **IP assignment** | C | Present assignment / Promise to assign / `Not addressed`. A promise to assign is a defect, not an assignment |
| IP assignment language | V | Quoted |
| Statutory IP carve-out | C | Referenced / `Not addressed`. State-mandated carve-outs affect scope |
| Confidentiality survival | Dur | Or `Perpetual` |
| Arbitration and class waiver | C | Both / Arbitration only / `Not addressed` |
| Immigration dependency | C | Sponsored visa referenced / `Not addressed`. A key person whose status is employer-dependent is an integration risk |
| Union or works council coverage | C | Covered / `Not addressed`. Triggers information and consultation obligations, which are timetable items |

| Human column | Values |
|---|---|
| Key person | Yes / No |
| Retention risk | High / Medium / Low |
| Covenant enforceable | Likely / Doubtful / Jurisdiction-dependent |
| Transaction payment triggered | Yes (amount) / No / Unclear |
| 280G analysis needed | Yes / No |

---

## 7. IP and Technology

**Three row sets.** Registrations (one per asset), chain of title (one per
assignment), and technology and open source (one per report). Currently collapsed
into one table, which is why `N/A` is doing so much work.
**Feeds:** outputs 1, 4, 5, 6, 7.

### 7A. Registrations

| Column | Type | Purpose |
|---|---|---|
| Asset type | C | Patent / Patent application / Trademark / Trademark application / Copyright / Domain |
| Title or mark | FR | As registered |
| Registration or application number | FR | |
| Office and jurisdiction | FR | |
| **Record owner** | FR | Owner of record, exactly as written |
| **Owner matches a target entity** | C | Matches / Differs / `Unable to determine`. **A mismatch is the finding** — it means an unrecorded assignment or an asset the target does not own |
| Filing date | D | |
| Registration or grant date | D | Or `Not stated` where pending |
| Status | C | Registered / Pending / Published / Allowed / Abandoned / Expired / Cancelled |
| Next maintenance or renewal date | D | An annuity lapsing during the deal is avoidable and embarrassing |
| Scope | FR | Classes and goods for marks; claim subject for patents |
| Encumbrances of record | FR | Security interests, liens, or recorded licences, or `Not addressed` |
| Licensee of record | FR | Or `Not addressed` |

### 7B. Chain of title

| Column | Type | Purpose |
|---|---|---|
| Assignor | FR | Exact name |
| Assignee | FR | Exact name |
| Assigned asset or scope | FR | As described |
| Assignment date | D | |
| Consideration | FR | As recited, or `Nominal`, or `Not stated` |
| **Present assignment or promise** | C | Present assignment / Agreement to assign in future / `Unable to determine`. **The defect detector.** "Agrees to assign" transfers nothing |
| Operative assignment language | V | Quoted |
| Further assurances | C | Present / `Not addressed` |
| Power of attorney | C | Present / `Not addressed`. Determines whether you can perfect without the assignor |
| Work made for hire language | C | Present / `Not addressed` |
| Moral rights waiver | C | Present / `Not applicable` / `Not addressed` |
| Recordation evidence | FR | Registry and date, or `Not addressed` |

### 7C. Technology and open source

| Column | Type | Purpose |
|---|---|---|
| Report type | C | Open source report / SBOM / Penetration test / Security assessment / Architecture description |
| Preparer | FR | And whether internal or third party |
| Scan or assessment date | D | A twelve-month-old SBOM describes a product you are not buying |
| Copyleft components identified | FR | Components under GPL-family licences, or `None identified` |
| Distributed in product | C | Yes / No / `Unable to determine`. Copyleft matters where the product is distributed |
| Licence obligations stated | FR | Attribution, source disclosure, or reciprocal licensing |
| Third-party components critical to product | FR | |
| **AI or model training data rights** | FR | Any statement of rights in training data, model weights, or outputs, or `Not addressed`. Increasingly the core asset question and absent from most schemas |
| Escrow arrangements | FR | Or `Not addressed` |
| Open findings | FR | Unremediated vulnerabilities or defects noted |

| Human column | Values |
|---|---|
| Chain complete | Yes / Gap identified / Unresolved |
| Critical to product | Yes / No / Unknown |
| Transferable in this deal | Yes / Consent required / No / Unclear |

**Never a column:** the multi-hop chain of title from creator to current owner.
Build it by hand from 7A and 7B.

---

## 8. Real Estate

**Rows:** one per property, with the lease and its amendments grouped.
**Feeds:** outputs 1, 3, 6, 7.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Property address | FR | Full address of the premises |
| Interest type | C | Lease / Sublease / Owned / Easement / Licence |
| Tenant entity | FR | Which group entity, exact name |
| Landlord | FR | Exact name |
| Lease structure | C | Triple net / Gross / Modified gross / `Not addressed` |
| Rentable area | N | Square feet as stated |
| Commencement date | D | |
| Rent commencement date | D | Often later, and it is the one the model needs |
| Expiry of current term | D | |
| Renewal options | FR | Number, length, and notice to exercise |
| Renewal rent determination | C | Fixed / Fair market / Index / `Not addressed` |
| Base rent | $ | Current, with period |
| Escalation | FR | Fixed uplift, index, or stepped schedule |
| Additional rent | FR | Opex, CAM, taxes, insurance |
| Percentage rent | FR | Or `Not addressed` |
| Security deposit | $ | Amount |
| Security deposit form | C | Cash / Letter of credit / Guaranty / None. **An LC is a financing item** and its issuer needs consent |
| Guaranty | FR | Guarantor and scope, or `Not addressed`. Confirm the guarantor survives the structure |
| **Assignment and subletting** | C | Freely permitted / Consent required / Consent, not unreasonably withheld / Prohibited / Permitted to affiliate |
| Assignment language | V | Quoted |
| **Landlord recapture right** | C | Present / `Not addressed`. **Worse than a consent requirement** — the landlord takes the space back instead of consenting |
| Consent conditions | FR | Fees, profit sharing, or financial tests attached to consent |
| **CoC treated as assignment** | C | Yes / No / `Not addressed` |
| CoC threshold | FR | Any stated ownership percentage |
| CoC language | V | Quoted |
| Permitted use | FR | As written |
| Exclusive use right | C | Present / `Not addressed` |
| Early termination right | FR | Holder, notice, and any fee, or `Not addressed` |
| Holdover rent | FR | Multiple or rate |
| Restoration or removal obligation | FR | Quoted where present. An end-of-term liability that belongs in the price |
| Casualty or condemnation termination | C | Present / `Not addressed` |
| Expansion, ROFR, or ROFO | C | Present / `Not addressed` |
| SNDA or estoppel referenced | C | Present / `Not addressed` |
| Mortgagee named | FR | Or `Not addressed` |

| Human column | Values |
|---|---|
| Consent required for this structure | Yes / No / Ambiguous |
| Site criticality | Critical / Important / Replaceable |
| Estoppel required | Yes / No |

---

## 9. Environmental

**Split by role.** Analysis, Filing, and Correspondence cannot share a schema —
this is the clearest case in the set.
**Feeds:** outputs 2, 4, 5, 7.

### 9A. Assessments and reports (Analysis)

| Column | Type | Purpose |
|---|---|---|
| Report type | C | Phase I ESA / Phase II ESA / Compliance audit / Vapour assessment / Other |
| Property assessed | FR | Address, and any parcels expressly excluded |
| Preparer | FR | Firm and credentials |
| Report date | D | A Phase I older than 180 days no longer supports the defence |
| Standard applied | FR | ASTM E1527-21 or other, as stated |
| **Reliance parties** | FR | Who may rely on the report, or `Not addressed`. **A seller-commissioned report the buyer cannot rely on has almost no diligence value** |
| Reliance transferable | C | Yes / No / `Not addressed` |
| Scope inclusions | FR | What was assessed |
| **Non-scope items** | FR | Asbestos, lead, radon, mould, wetlands — expressly outside scope |
| RECs identified | FR | Each, or `None identified` |
| CRECs identified | FR | Each, or `None identified` |
| HRECs identified | FR | Each, or `None identified` |
| De minimis conditions | FR | Or `None identified` |
| **Data gaps** | FR | Gaps noted and whether the preparer called them significant |
| Historical use findings | FR | Prior uses of concern |
| Adjacent property concerns | FR | Or `None identified` |
| Recommendation | C | No further action / Further assessment recommended / Remediation recommended / `Not addressed` |
| Cost estimate stated | $ | Or `Not stated`. Harvey reports it; nobody relies on it |

### 9B. Permits (Filing)

| Column | Type | Purpose |
|---|---|---|
| Permit type | FR | As named |
| Permittee entity | FR | Exact name |
| Issuing authority | FR | |
| Permit number | FR | |
| Issue date | D | |
| Expiry or renewal date | D | |
| Permitted activity and limits | FR | Emission, discharge, or waste limits as stated |
| **Transferability on change of control** | C | Transfers automatically / Notice required / New application required / Non-transferable / `Not addressed`. A permit that must be reapplied for is a closing condition |
| Monitoring and reporting obligations | FR | |
| Financial assurance or bonding | $ | Or `Not addressed` |

### 9C. Enforcement and correspondence

| Column | Type | Purpose |
|---|---|---|
| Document type | C | Notice of violation / Consent order / Information request / Inspection report |
| Issuing authority | FR | |
| Date | D | |
| Alleged violation | FR | As stated |
| Penalty demanded or assessed | $ | Or `Not stated` |
| Required corrective action | FR | |
| Deadline | D | |
| Resolution status stated | C | Open / Resolved / Under appeal / `Unable to determine` |

| Human column | Values |
|---|---|
| Materiality | Critical / Material / Monitor / Immaterial |
| Remediation cost estimate | Free text |
| Special indemnity candidate | Yes / No |
| Reliance obtainable | Yes / No / In negotiation |

---

## 10. Litigation and Disputes

**Rows:** one per **matter**, with all pleadings, correspondence, and orders for
that matter grouped. Currently one row per document, which cannot answer the
questions the deal team asks.
**Feeds:** outputs 4, 5, 7.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Matter name | FR | Caption as written |
| Target entity party | FR | Which group entity is party |
| **Target's role** | C | Plaintiff / Defendant / Third party / Claimant / Respondent / Non-party. Absent from the current schema, and it inverts the entire risk reading |
| Adverse party | FR | Exact name |
| Adverse party type | C | Customer / Supplier / Employee / Former employee / Competitor / Regulator / Shareholder / Class |
| Forum | FR | Court, tribunal, or agency, and jurisdiction |
| Case or docket number | FR | |
| Commenced date | D | |
| Claims asserted | FR | Causes of action |
| Factual subject | FR | What the dispute is about, one or two sentences |
| Amount claimed | $ | Or `Not stated` |
| Unquantified relief | FR | Injunctive, declaratory, or equitable relief sought, or `Not addressed`. Separate from the money |
| Counterclaims | FR | Or `Not addressed` |
| **Class or representative** | C | Individual / Putative class / Certified class / Collective / Representative. Changes the exposure by orders of magnitude |
| Procedural stage | FR | Stage as of the most recent document in the unit |
| Stage as-of date | D | Which document the stage statement comes from |
| Next deadline or hearing | D | Or `Not stated` |
| Trial or hearing date | D | Or `Not stated` |
| **Settlement terms** | FR | Payment, ongoing obligations, and release scope, or `Not applicable` |
| Release scope | FR | Who is released and for what. A narrow release leaves live exposure |
| **Insurance tendered** | C | Tendered and accepted / Tendered, coverage disputed / Tendered, denied / Not referenced |
| Carrier referenced | FR | Matched against the insurance table |
| Reserve or accrual referenced | $ | Or `Not stated` |
| Related contract, asset, or property | FR | What the dispute concerns. Links to Contracts, IP, or Real Estate |
| Litigation hold referenced | C | Present / `Not addressed` |

| Human column | Values |
|---|---|
| Exposure estimate | Free text |
| Outcome likelihood | Free text |
| Disclosure schedule item | Yes / No |
| Special indemnity candidate | Yes / No |
| Escrow candidate | Yes / No |

**Never a column:** pattern detection across matters, and the chronology of a
material dispute. Ask Assistant over the project for the first; build the second
by hand.

---

## 11. Regulatory and Licenses

**Rows:** one per licence, permit, or registration. Regulator correspondence and
examination reports are separate row sets.
**Feeds:** outputs 1, 2, 6, 7. This workstream sets the deal calendar more often
than any other.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Licence type | FR | As named in the document |
| Holder entity | FR | Exact name |
| Regulator | FR | Authority, and the specific division |
| Jurisdiction | FR | Separate from the regulator's name |
| Licence number | FR | |
| Issue date | D | |
| Expiry or renewal date | D | Or `No expiry stated` |
| Renewal lead time | Dur | How far ahead renewal must be filed |
| Status | C | Active / Pending / Conditional / Suspended / Expired / Revoked / `Unable to determine` |
| Permitted scope | FR | What the entity may do |
| Conditions and undertakings | FR | Or `Not addressed` |
| **Ownership or control threshold** | FR | The percentage of ownership or voting power that triggers a filing. **This is the entire point of the workstream** and the current schema does not ask for the number |
| Threshold language | V | Quoted |
| **Indirect control captured** | C | Direct ownership only / Indirect or ultimate control captured / `Unable to determine`. Decides whether an upstream acquirer triggers it |
| **Filing type required** | C | Prior approval / Post-closing notice / No filing / `Not addressed` |
| Statutory review period | Dur | As stated. Any period longer than the deal timetable becomes a closing condition |
| Transferability | C | Transfers with the entity / New application required / Non-transferable / `Not addressed` |
| **Qualifying individual requirement** | FR | Any named responsible or qualified person the licence depends on, or `Not addressed`. If that person leaves at closing, the licence is at risk |
| Fitness or probity requirements | FR | Requirements applying to new controllers, or `Not addressed` |
| Ongoing reporting obligations | FR | |
| Open findings or conditions | FR | From examinations or consent orders, or `None identified` |

| Human column | Values |
|---|---|
| Threshold crossed by this deal | Yes / No / Requires local counsel |
| Filing required | Prior approval / Post-closing notice / None |
| Closing condition | Yes / No |
| Estimated timeline | Free text |

**Never a column:** whether the buyer's resulting direct and indirect ownership
crosses the threshold. Harvey supplies the threshold; a lawyer supplies the
ownership chain and the conclusion.

---

## 12. Debt and Financing

**Two row sets.** One per facility, and one per lien filing. The
facility-to-UCC match is where undisclosed debt surfaces, and it needs both.
**Feeds:** outputs 1, 2, 3, 6, 7.

### 12A. Facilities

| Column | Type | Purpose |
|---|---|---|
| Facility type | C | Term loan / Revolver / Note / Equipment finance / Capital lease / Mezzanine / Other |
| Borrower | FR | Exact name |
| Co-borrowers | FR | Or `Not addressed` |
| **Guarantors** | FR | Every guarantor named, or `Not addressed`. Absent from the current schema; needed to confirm the structure does not orphan a guaranty |
| Lender or agent | FR | Exact name |
| Original commitment | $ | |
| **Outstanding balance stated** | $ | With the as-of date. This is the payoff number |
| Balance as-of date | D | |
| Interest rate | FR | Rate or formula as written |
| Default rate | FR | Or `Not addressed` |
| Maturity date | D | |
| Amortization | FR | Schedule as written, or `Not addressed` |
| Financial covenants | FR | Each covenant and its level |
| Most recent tested compliance | FR | As stated in a compliance certificate in the unit, or `Not addressed` |
| Equity cure | C | Present / `Not addressed` |
| Negative covenants | FR | Restrictions on debt, liens, asset sales, dividends, investments, and affiliate transactions |
| Permitted lien basket | FR | Or `Not addressed` |
| **Change of control consequence** | C | Event of default / Mandatory prepayment / Consent required / Notice required / `Not addressed` |
| CoC definition and threshold | FR | The definition as written, including any percentage |
| CoC language | V | Quoted |
| Assignment by borrower | C | Prohibited / Consent required / Permitted / `Not addressed` |
| Cross-default or cross-acceleration | FR | Quoted where present. One tripped facility can cascade |
| Prepayment permitted | C | Yes / Yes with premium / No / `Not addressed` |
| Prepayment premium or make-whole | FR | The cost of retiring the debt at closing |
| Breakage costs | FR | Or `Not addressed` |
| MAC or MAE clause | C | Present / `Not addressed` |
| Springing maturity | C | Present / `Not addressed` |
| Collateral description | FR | As written, or `Unsecured` |
| Excluded assets | FR | Or `Not addressed` |
| **IP included in collateral** | C | Yes / No / `Unable to determine`. A security interest in core IP interacts with the IP workstream |
| Deposit account control | C | Present / `Not addressed` |
| Intercreditor or subordination | FR | Or `Not addressed` |

### 12B. Lien filings

| Column | Type | Purpose |
|---|---|---|
| Debtor name as filed | FR | **Exactly as filed.** A mismatch against the exact legal name can mean an unperfected lien |
| Secured party | FR | |
| Filing jurisdiction | FR | |
| Filing number | FR | |
| Filing date | D | |
| Continuation due date | D | |
| Collateral description | FR | As filed |
| Status | C | Active / Terminated / Amended / Assigned / Lapsed |
| Matches a produced facility | C | Matches / No corresponding facility / `Unable to determine`. **A UCC with no facility means undisclosed debt or a stale filing.** Both need resolving |

| Human column | Values |
|---|---|
| Payoff required at closing | Yes / No / Under negotiation |
| Payoff amount confirmed | Yes / No |
| Lien release required | Yes / No |
| Lender consent required | Yes / No / Ambiguous |
| Treatment | Repay / Assume / Refinance / Unresolved |

---

## 13. Insurance

**Rows:** one per policy.
**Feeds:** outputs 5, 6, 7. The central question is not what is covered today but
what survives closing.

Spine, plus:

| Column | Type | Purpose |
|---|---|---|
| Insurer | FR | Exact name |
| Broker | FR | Or `Not addressed` |
| Policy number | FR | |
| Coverage type | C | General liability / Product liability / Property / Business interruption / Workers compensation / D&O / E&O / Cyber / Employment practices / Environmental / Auto / Umbrella / Excess / Other |
| Named insured | FR | Exactly as written |
| Additional insureds | FR | Or `Not addressed` |
| **All target entities covered** | C | All covered / Some entities not named / `Unable to determine`. **A subsidiary not named is an uninsured subsidiary** |
| Policy period | FR | Inception to expiry |
| **Claims made or occurrence** | C | Claims made / Occurrence / `Not stated`. **Decides whether the tail transfers with the business.** Absent from the current schema and it is the M&A question |
| Retroactive date | D | For claims-made policies. Anything before it is uncovered |
| Per occurrence limit | $ | |
| Aggregate limit | $ | |
| Sublimits | FR | Or `Not addressed` |
| Retention or deductible | $ | |
| Defense inside or outside limits | C | Inside / Outside / `Not addressed`. Defense inside limits can consume the coverage |
| Material exclusions | FR | Exclusions material to this business, or `None identified` |
| Prior acts coverage | C | Present / Excluded / `Not addressed` |
| **Extended reporting period available** | C | Available (state period and cost) / Not available / `Not addressed`. Whether a D&O tail can be bought, and at what price |
| **CoC or assignment provision** | C | Terminates on CoC / Consent required / Notice required / Continues / `Not addressed` |
| CoC language | V | Quoted |
| Cancellation provisions | FR | Notice and grounds |
| Premium | $ | Annual |
| Retro or audit premium | C | Subject to audit / Fixed / `Not addressed`. An audit premium is an unbooked liability |
| Open claims referenced | FR | Or `Not addressed` |
| Loss run referenced | C | Present / `Not addressed` |

| Human column | Values |
|---|---|
| Coverage adequate | Yes / Gap identified / Unassessed |
| Tail or run-off required | Yes / No / Unassessed |
| Gap against contract requirements | Yes / No / Unassessed |

---

## 14. Tax

**Split by role.** Returns and filings, agreements, and correspondence have almost
nothing in common.
**Feeds:** outputs 3, 4, 5. Legal diligence extracts the documents and the
positions; quantification sits with tax advisers.

### 14A. Returns and filings (Record)

| Column | Type | Purpose |
|---|---|---|
| Taxpayer entity | FR | Exact name |
| Tax type | C | Federal income / State income / Franchise / Sales and use / Payroll / Property / Excise / International / Other |
| Jurisdiction | FR | |
| Period covered | FR | |
| Filing date | D | Or `Not stated` |
| Extension filed | C | Yes / No / `Not addressed` |
| Filing status | C | Filed / Pending / Extended / Amended / Not filed / `Unable to determine` |
| Taxable income or loss | $ | As shown |
| Tax liability | $ | Separate sign convention from a refund |
| Refund claimed | $ | Separate column, not merged with liability |
| NOL carryforward | $ | Balance as shown. Survival through the deal is a Section 382 question |
| Credits carried forward | $ | |
| Consolidated group members | FR | Every member listed |
| **Elections made** | FR | Check-the-box, S corporation, QSub, 338, 754, or other, as stated |
| **Statute of limitations expiry** | D | Or as computed from the filing date in the document only. **Sets the tax indemnity tail** |
| Uncertain positions or reserves | FR | Or `None identified` |
| Transfer pricing method | FR | Or `Not applicable` |
| Related-party transactions disclosed | FR | Or `None identified` |
| Preparer | FR | Internal or named firm |
| **States registered** | FR | Jurisdictions where the entity is registered or filing |

### 14B. Agreements

| Column | Type | Purpose |
|---|---|---|
| Agreement type | C | Tax sharing / Tax indemnity / Closing agreement / Tax opinion / Other |
| Parties | FR | Exact names |
| Allocation method | FR | How liability is allocated among group members |
| **Survival after a change of control** | C | Survives / Terminates / `Not addressed`. A tax sharing agreement that survives can follow the target out of the seller's group |
| Indemnity provisions | FR | Who indemnifies whom, and for what |
| Opinion scope and reliance | FR | For opinions: what was opined on, subject to what assumptions, and who may rely |

### 14C. Correspondence and audits

| Column | Type | Purpose |
|---|---|---|
| Document type | C | Audit notice / Information request / Proposed adjustment / Assessment / Appeal / Closing letter |
| Authority | FR | |
| Date | D | |
| Periods under examination | FR | |
| Issues raised | FR | |
| Proposed or assessed amount | $ | Or `Not stated` |
| Interest and penalties | $ | Or `Not stated` |
| Deadline to respond | D | |
| Status stated | C | Open / Resolved / Under appeal / `Unable to determine` |

| Human column | Values |
|---|---|
| Exposure quantified | Free text |
| Indemnity or escrow candidate | Yes / No |
| Rep required | Yes / No |
| Pre-closing period allocation | Free text |

---

## 15. Derived artifacts

None of these is a new extraction. Each is a filter over the tables above, which
is what keeps them from disagreeing with their sources.

| Artifact | Built from | Rows |
|---|---|---|
| **Consent and approval schedule** | Contracts, Real Estate, Regulatory, Debt, Capitalization, Corporate | Every row with a CoC, assignment, consent, or approval trigger |
| **Closing conditions and calendar** | Regulatory, Debt, Corporate | Every prior approval, stockholder vote, and lender consent, sequenced against the statutory review periods |
| **Transaction payments schedule** | Employment, Capitalization, Debt | Severance, CoC benefits, acceleration, retention bonuses, payoffs, prepayment premiums |
| **Coverage register** | Every table's "Referenced but not produced" column, plus the request list | One per request item and per referenced-but-absent document |
| **Issues list** | Every table where Materiality is Critical or Material | The deliverable the deal team actually reads |
| **Disclosure schedule support** | Litigation, Regulatory, IP, Contracts, Tax | Organised by SPA rep |

---

## 16. What stays with a human

Never a Harvey column, in any table:

- Which document in a family is operative or controlling
- Whether an authority or entity defect exists
- Whether the transaction requires an approval, and whether one obtained is
  sufficient
- Whether an ownership chain crosses a regulatory threshold
- Enforceability, validity, materiality, or legal risk
- Any arithmetic: cap table reconciliation, fully diluted counts, waterfalls,
  acceleration cost, exposure totals
- The deal consequence of anything

Grouping documents into one review unit surfaces differences among them. It does
not establish which one controls.

---

## 17. Column counts and build order

| Table | Substantive columns | Note |
|---|---|---|
| Intake | ~19 | Runs over the whole room |
| Contracts | ~48 | **Split into Core and Commercial** |
| Corporate | ~40 | Consider splitting identity/standing from governance/triggers |
| Capitalization | ~24 | |
| Employment | ~37 | Consider splitting economics from covenants and IP |
| IP | ~35 | Three separate tables |
| Real Estate | ~37 | Consider splitting economics from transfer provisions |
| Environmental | ~37 | Three separate tables by role |
| Litigation | ~26 | |
| Regulatory | ~22 | |
| Debt | ~43 | Two tables: facilities and lien filings |
| Insurance | ~26 | |
| Tax | ~37 | Three tables by role |

Verify the practical column cap in your tenant before building. Where a table
exceeds it, split by theme over the same project and join on file name in the
export — do not drop columns to fit.

Build order, and do not build all of it:

1. Intake classification
2. Coverage register — gaps drive the supplemental request, which has the longest
   lead time
3. Contracts Core
4. Corporate, then Capitalization
5. Whichever workstream the deal thesis turns on
6. Contracts Commercial and the remaining workstreams as the matter needs them
7. Consent schedule, transaction payments, issues list — derived, once the sources
   exist

A schema that has never met a real document is a guess. Every table here is a
guess until a partner redlines it against one closed matter.
