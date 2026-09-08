# M&A Diligence POC — Build Plan and Shared Standards

Version 1. Front matter for every Review Table inventory in this set. Read once;
each table inventory refers back here rather than repeating it.

---

## 1. What this POC is

A demonstrable end-to-end legal diligence workflow in Harvey Review Tables:
intake and triage over a whole data room, substantive extraction across every
workstream, and derived artifacts that a deal team actually reads.

**What it is not.** None of these schemas has met a real document. Every table is
a candidate for partner redline, and the numbers in any demo are candidates, not
findings. Say so in the demo — it is the most credible thing you can say about it.

---

## 2. Table register

**25 tables, all drafted. 617 prompts, roughly 590 Harvey columns plus human
review fields.** Every table is v1.0 and none has met a real document.

| # | Table | Row unit | Harvey cols |
|---|---|---|---|
| 01 | Contracts Core | Agreement family | 27 |
| 02 | Corporate and Entity Structure | Entity | 31 |
| 03 | Capitalization and Securities | Instrument | 34 |
| 04 | Equity Plans | Plan | 31 |
| 05 | Intake Classification | File | 20 |
| 06 | Coverage Register | Request item | specification + 2 columns added to 05 |
| 07 | Contracts Commercial | Agreement family | 25 |
| 08 | Employment — Individual Agreements | Person | 38 |
| 09 | Employment — Policies | Policy | 15 |
| 10 | IP — Registrations | Asset | 16 |
| 11 | IP — Chain of Title | Assignment | 16 |
| 12 | IP — Technology and Open Source | Report | 17 |
| 13 | Real Estate — Leasehold | Property | 40 |
| 14 | Real Estate — Owned Property | Property | 21 |
| 15 | Litigation and Disputes | Matter | 30 |
| 16 | Regulatory — Licences | Licence | 26 |
| 17 | Regulatory — Correspondence | Matter | 19 |
| 18 | Debt — Facilities | Facility | 38 |
| 19 | Debt — Lien Filings | Filing | 15 |
| 20 | Insurance | Policy | 31 |
| 21 | Environmental — Assessments | Report | 21 |
| 22 | Environmental — Permits | Permit | 20 |
| 23 | Environmental — Enforcement | Matter | 20 |
| 24 | Tax — Returns and Filings | Filing | 21 |
| 25 | Tax — Agreements and Correspondence | Matter or instrument | 19 |

**The number is the file prefix, and it is the only identifier.** Numbers 01 to 04
reflect the order the tables were drafted in, not the order to build them in — the
build order is in section 12 and it starts with 05. Cite tables by number
throughout: `Table 11` and `11-ip-chain-of-title-prompt-inventory.md` are the same
thing, always.

Front matter carries no table number: `00a` is this document, `00b` is the
extraction schema that produced the set. **`00b` is superseded in substance** by
the 25 inventories and is retained for its rationale — the seven deal outputs and
the reasoning that made each column earn its place against them.

### Known departures from the role rule

One deliberate exception and two justified ones, all documented in the tables
themselves:

- **Tax — Agreements and Correspondence** carries two roles in one table, routed
  on `Matter Category`. Split it into three if the matter is heavy on either side.
- **Real Estate — Owned Property** mixes deed, title report, survey, and tax
  statement because the row is the property. Every substantive column names its
  source document.
- **Corporate** mixes charter, minutes, and good standing certificate for the same
  reason.

### The one structural correction to the source spec

**The Coverage Register is not a Review Table.** Spec §5.3 proposed request-list
rows run against a project; a Review Table column has no review unit in such a
row. The inversion happens in Excel instead, fed by two columns added to Intake.
See `06-`.

### Deliberately excluded

- **Vendor and supplier** — served by Contracts Core filtered on
  `Counterparty Type`. A separate table would duplicate 27 columns to no end.
- **Deal documents** — LOIs, draft SPAs, and structure charts are read directly.
  A grid of them is a grid nobody filters.

### Open scope question for the group

Three taxonomy workstreams are absent from spec §3's scope, so the two source
documents disagree. Decide before batch 3:

- **Privacy and Cybersecurity** — DPAs, incident reports, SOC 2, pen tests,
  subprocessor lists. For a modern target this is the most defensible addition,
  probably 2 tables (~30 cols).
- **Benefits and Pensions** — plan documents, Form 5500s, deferred compensation.
  Feeds transaction payments alongside Employment. 1–2 tables.
- **Compliance** — codes of conduct, hotline logs, sanctions screening,
  investigations. 1 table.

Adding all three takes the POC to 29 tables and ~600 columns.

### Derived artifacts — filter specifications, not prompts

Built by filtering and carrying rows. Only the Coverage Register needs prompts,
and only for its referenced-but-absent pass.

| Artifact | Sources |
|---|---|
| Consent and approval schedule | Contracts Core, Real Estate, Regulatory, Debt, Capitalization, Corporate |
| Closing conditions and calendar | Regulatory, Debt, Corporate |
| Transaction payments schedule | Employment, Capitalization, Equity Plans, Debt |
| Issues list | Every table, filtered on Materiality |
| Disclosure schedule support | Litigation, Regulatory, IP, Contracts, Tax |

**Never re-derive a consent schedule by asking Harvey a fresh question.** Filter
and carry, so the schedule and its sources cannot disagree.

---

## 3. Vault project structure

One project per workstream per matter: `[Matter] - [Workstream]`. Review Tables
run over a project, so project granularity has to match the granularity you want
to re-run at.

| Project | Tables |
|---|---|
| `[Matter] - Intake` | Intake Classification (runs over everything) |
| `[Matter] - Corporate` | Corporate, Capitalization, Equity Plans |
| `[Matter] - Contracts` | Contracts Core, Contracts Commercial |
| `[Matter] - Employment` | Employment ×2 |
| `[Matter] - IP` | IP ×3 |
| `[Matter] - Real Estate` | Real Estate ×2 |
| `[Matter] - Litigation` | Litigation |
| `[Matter] - Regulatory` | Regulatory ×2 |
| `[Matter] - Finance` | Debt ×2, Insurance |
| `[Matter] - Environmental` | Environmental ×3 |
| `[Matter] - Tax` | Tax ×2 |
| `[Matter] - Deal Documents` | none — read directly |

`@Column` references work **within a table only**. Nothing crosses tables or
projects. That is why every substantive table carries its own `Execution Status`
and its own `Referenced but Not Produced` rather than referencing Intake's.

---

## 4. The universal spine

Every substantive table carries these. Defined once; each inventory notes only
its departures.

### Orientation

| Column | Type | Purpose |
|---|---|---|
| Documents in Unit | FR | Inventory of the review unit; the routing input for status columns |
| Subject entity | FR | Which target-group entity is the subject or party |
| Document type | Classify | From the workstream vocabulary |
| Execution / filing status | Classify | What the documents prove about their own completion |
| Document date | Date | With a document-type hierarchy and a stated basis |
| Operative date | Date | Effective date for instruments; as-of date for records |
| Amends or issued under | FR | Base instrument, exact name |
| Chain completeness | Classify | Whether the family reveals a gap |
| **Referenced but not produced** | FR | Feeds the coverage register from every table |
| Governing law | FR | Jurisdiction |

### Human review block

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| Operative version confirmed | Yes / No, superseded / Chain incomplete |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

A cell Harvey filled is a candidate. It is not a finding, it does not go in the
memo, and it is not told to a client until `Review status` says otherwise.

---

## 5. Fallback vocabulary

One controlled set, every table, no synonyms.

| State | Meaning | Reviewer action |
|---|---|---|
| `Not addressed` | The documents are silent on the subject | Check whether another document should cover it |
| `Not stated` | **Date, Number, Currency, Duration columns only.** The value asked for does not appear | Same as above, for typed columns |
| `Not applicable` | No meaningful application to this document or instrument type | None |
| `Incorporated terms` | Another document supplies the terms and is not in the unit | Locate the other document |
| `Unable to determine` | Relevant evidence exists but is conflicting, incomplete, or illegible | Open the source |

Banned: `N/A`, `None`, `Silent`, `Unclear`, `Not determinable`, `Not found`.

**Two rules that are violated most often.** A fallback state never replaces a
value the document states — if an effective date equals the execution date,
return the date. And silence is not uncertainty: a silent document gets
`Not addressed`, never `Unable to determine`.

**Positive findings that look like fallbacks.** `None identified`,
`None referenced`, `None recorded`, `None named`, `None disclosed` mean the search
was run and found nothing. They are answers, not absences, and each is defined in
the column that uses it.

---

## 6. Prompt construction standard

Section order, omitting any that adds no operative instruction:

1. `## Established results` — only for real `@Column` dependencies
2. `## Task`
3. `## Scope` — subject, evidence boundary, inclusions, exclusions
4. `## Options` / `## Response labels`
5. `## Classification rules` / `## Extraction rules`
6. `## Fallback rules`
7. `## Output format` — last, so the final instruction is the output contract

Conventions:

- Classification and detail are separate columns. Harvey cannot return a
  controlled enum plus structured free text in one cell.
- Any classified provision driving a consent, a payment, or a closing condition
  gets a paired **Verbatim** column.
- Exact labels, fallback values, and output templates in backticks.
- Numbered lists only where precedence matters.
- No rule may require counting characters. Apply length limits after export.
- Markdown organises the prompt; it is not authorised in the returned cell.
- Every `@` reference must be consumed by a rule. A reference no rule uses is
  deleted, not kept for context.
- Keep each prompt under 6,000 characters against the ~10,000 limit, leaving room
  for the rules testing will add.

---

## 7. Two rules that carry most of the reliability

**Report, never compute.** No table adds, subtracts, nets, reconciles, or derives
anything. Every figure is reported as stated with its document and date. All
arithmetic — cap table reconciliation, fully diluted counts, vesting, overhang,
exposure totals, accrued interest, payoff amounts — happens in Excel from the
export, against a certified source.

**Filed is not adopted; adopted is not current; signed is not effective.** An
unsigned consent authorises nothing, an unfiled amendment changes nothing, and a
stated effective date proves nothing about signatures. Use `purports to`, `would`,
and `proposed` where the evidence does not support a completed act.

---

## 8. Pre-run verification

Do this **once**, on a two-row test table, before pasting any full suite. Three
unknowns affect every table in the set, and finding out at column 500 is
expensive.

- [ ] **Native type fallbacks.** Test Date, Number, Currency, and Duration with
      `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`,
      and a partial date such as `2024-08`. Record what each accepts:
      - Date: ______
      - Number: ______
      - Currency: ______
      - Duration: ______
      If a type rejects a fallback, switch that column to Free Response with a
      strict format and give up native sorting. **Do not change what the fallback
      means to suit the type.**
- [ ] **Verbatim behaviour.** On three known documents: does it return true
      verbatim text, does it accept `Not addressed`, and how does it handle a
      300-word quotation? The entire spot-check design rests on this, and it has
      been flagged untested since August.
- [ ] **Classify option ceiling.** How many options can one Classify column hold?
      Intake's document-type vocabulary is ~180 values and the answer decides
      whether that column is Classify or Free Response.
- [ ] **Practical column cap.** Contracts Core is 27, Corporate 31, Capitalization
      34. If the cap is lower, the splits noted in each inventory become
      mandatory.
- [ ] **Grouping.** Confirm units of up to 25 documents load, and that a
      provision column reports from the latest document in the unit.
- [ ] **Cell locking across rerun.** Change an upstream value, rerun, and confirm
      a locked dependent cell does not silently retain a stale answer.
- [ ] **Table Instructions propagation.** Confirm they reach every column, and
      whether they count toward a column's query length. Budget as if they do.

Record the answers here, dated. Four of these are load-bearing.

---

## 9. Test-set dimensions

Every table's own inventory lists its specific test rows. All of them should cover
these dimensions; an unticked dimension is open risk, not a pass.

- Each material document type in the row set
- Single-subject and multi-subject files
- Signed, partially signed, unsigned, filed, and government-issued
- Amendments, restatements, compilations, and attachments
- Documents that expressly address the issue, and documents that are silent
- Documents incorporating external terms
- Incomplete, illegible, or internally conflicting records
- Upstream classifications with each fallback state
- Conditional columns with the trigger met and not met
- Grouped units with consistent, complementary, and conflicting evidence
- Locked and unlocked cells during a selective rerun

Keep the evaluation log outside Harvey, one row per failure: test document,
column, prompt version, actual answer, evidence relied on, expected behaviour,
failure class, revision, result after rerun. Record passes too, so a later reader
can tell "tested and correct" from "not tested."

---

## 10. What stays with a human, in every table

Never a Harvey column:

- Which document is operative or controlling
- Whether an authority, entity, or title defect exists
- Whether the transaction requires an approval or consent, and whether one
  obtained is sufficient
- Whether an ownership chain crosses a regulatory threshold
- Enforceability, validity, materiality, or legal risk
- Any arithmetic
- The deal consequence of anything

Grouping documents into one review unit surfaces differences among them. It does
not establish which one controls.

---

## 11. Versioning and maintenance

Harvey holds the current prompts. These inventories hold the history and the
reasons. Neither substitutes for the other.

- One inventory per table, versioned, with a shared change log at the end.
- Every prompt change increments the version and records the failure class it
  addresses, the rerun scope, and any regression — including one-word fixes.
- Table Instructions are **excluded from Harvey exports**, so the copy in each
  inventory is the only one.
- Re-derive each dependency index from the prompts after any edit. The index is
  the rerun plan, so an index that disagrees with the prompts produces a wrong
  rerun.
- Export to a dated file before and after every re-run. There is no grid version
  history; the dated exports are it.
- Name an owner for this set, or it will not survive two matters.

---

## 12. Build order

**Do not build all 25 for a live matter.** Table numbers are identifiers, not a
sequence. Build in this order, and stop when the matter is covered.

| Order | Table | Why here |
|---|---|---|
| 1 | **05** Intake Classification | Everything routes through it |
| 2 | **06** Coverage Register | Gaps drive the supplemental request, which has the longest lead time |
| 3 | **01** Contracts Core | Highest document volume, highest consent yield |
| 4 | **02** Corporate, then **03** Capitalization, then **04** Equity Plans | Closing-critical, and the reconciliation takes time. Build 04 immediately after 03 or the incorporated terms in 03 resolve to nothing |
| 5 | Whichever workstream the deal thesis turns on | **10–12** IP for a technology target, **16–17** Regulatory for financial services, **13–14** Real Estate for retail, **08–09** Employment for a services business |
| 6 | **07** Contracts Commercial | Cheapest remaining once 01 exists |
| 7 | Remaining workstreams as the matter needs them | **15** Litigation, **18–20** Debt and Insurance, **21–23** Environmental, **24–25** Tax |
| 8 | Derived artifacts | Consent schedule, closing conditions calendar, transaction payments, issues list — all filters, no new extraction |

Three pairs must be built together or not at all, because the first returns
`Incorporated terms` that only the second resolves:

- **03 Capitalization → 04 Equity Plans**
- **08 Employment agreements → 09 Employment policies**
- **18 Debt facilities → 19 Debt lien filings** (the facility-to-filing match needs both)

**Before any of it, run the pre-run verification in section 8 once.** Four of its
items are load-bearing across every table in the set, and finding out at column 500
is expensive.
