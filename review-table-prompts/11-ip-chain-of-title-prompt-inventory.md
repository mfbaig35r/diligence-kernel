# Prompt Inventory — IP: Chain of Title

Table 11 of the POC. Second of three IP tables, and the one that decides whether
the target owns what it says it owns.

Shared conventions, fallback vocabulary, pre-run verification, and testing
standards are in `00-build-plan-and-standards.md`.

## Table

- Matter: `[Project name]`
- Project: `[Matter] - IP`
- Review unit: **one transfer document** — the assignment, transfer, or
  contribution instrument, any amendment or confirmatory assignment of it, and any
  recordation confirmation produced for it
- Grouping used: **yes**, typically 1–3 documents per unit
- Intended reviewers and downstream use: IP and corporate/M&A teams; feeds the
  chain-of-title analysis, the pre-closing remediation list, and the coverage
  register
- Inventory version: v1.0

### What this table is for

One question, asked one document at a time: **does this instrument actually
transfer anything, and from whom to whom?**

`Present Assignment or Promise` is the column the table exists for. "Agrees to
assign" transfers nothing. It is a contractual promise requiring a further
instrument, and until that instrument exists the assignor still owns the asset.
Across a portfolio this is the single most common IP defect in a private-company
diligence, and it is invisible in a registrations table — the register shows an
owner, not whether the paper behind it works.

### What this table cannot do

**It cannot trace a chain.** Each row is one link. Tracing creator to current owner
through four assignments across two jurisdictions is a multi-hop problem, it does
not automate in a Review Table, and it is human work performed in Excel from this
table's export plus the Registrations export.

Budget real time for it. On a technology target it is usually the single longest
task in the IP workstream.

## Assumptions to confirm before running

1. One row is one transfer instrument. An assignment covering forty patents is
   still one row; the assets are reported in `Assigned Asset or Scope`.
2. Employee and contractor invention assignments are **not** rows here. They are
   reviewed in the Employment tables, where the population is the workforce rather
   than the asset. This table covers asset-level transfers: acquisitions,
   founder-to-company assignments, inter-company transfers, and assignments from
   development partners.
3. Licences are not transfers. An exclusive licence, however broad, is reviewed in
   the Contracts tables.
4. Buy-side review; the entities in the Table Instructions list are the target
   group.
5. `[Project name]`, the entity list, and the diligence as-of date are real matter
   parameters.

## Column count

16 Harvey columns plus 6 human columns.

---

## Table Instructions

- Version: v1.0

```markdown
## Matter

[Project name]. Buyer-side intellectual property diligence on the target group listed below. This table reviews instruments transferring ownership of intellectual property.

One row is one transfer document: the assignment, transfer, or contribution instrument, any amendment or confirmatory assignment of it, and any recordation confirmation produced for it. Analyze all documents in the current review unit together.

Diligence as-of date: `[YYYY-MM-DD]`. When a column compares a date to the present, use this date and not the date of processing.

## Target group

Use these names exactly as written when a target entity is the subject of an answer:

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer and [Seller or parent legal name] is the selling shareholder. Neither is a review subject unless a column expressly asks about them.

## Shared rules

- Analyze only the documents in the current review unit. Do not use other rows, file names, or outside knowledge of the parties or the assets.
- **Report what the instrument's operative words do. Do not assess whether the transfer was effective, whether the assignor had title to give, or whether the chain is complete.** Effectiveness depends on the assignor's own title, on formalities in each jurisdiction, and on documents that are not in this unit. Those are legal conclusions for the reviewer.
- Report names exactly as printed, including entity suffix, punctuation, and any misspelling. Do not correct, normalize, or update a party name.
- Where two documents in the unit address the same term, report the term as stated in the most recently dated document that addresses it, and identify that document by its printed title and date.
- Write dates as `YYYY-MM-DD`. Preserve partial dates as written.
- Use only these fallback states, with the meaning each column defines: `Not addressed`, `Not stated`, `Not applicable`, `Incorporated terms`, `Unable to determine`.
- Return the normalized answer only. Reasoning, quotations, section numbers, and citations belong in Harvey's evidence fields, not in the cell.
```

---

## Dependency map

```
Stage 1 — Orientation (no upstream)
  Documents in Unit
  Instrument Type
  Assignor
  Assignee
  Assigned Asset or Scope
  Assignment Date

Stage 2 — Record status
  Documents in Unit ──→ Execution Status
                        Recordation Evidence
                        Referenced but Not Produced
  Assignor ──→ Assignor Authority
  Assignee ──→ Assignee Is Target Entity

Stage 3 — The operative test
  Present Assignment or Promise ──→ Operative Assignment Language

Stage 4 — Supporting provisions
  Further Assurances and Power of Attorney
  Work Made for Hire and Moral Rights
  Consideration
```

## Column index

| # | Column | Native type | Upstream | Downstream | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Documents in Unit | Free Response | — | Execution Status; Recordation Evidence; Referenced but Not Produced | v1.0 | draft |
| 2 | Instrument Type | Classify | — | — | v1.0 | draft |
| 3 | Assignor | Free Response | — | Assignor Authority | v1.0 | draft |
| 4 | Assignor Authority | Free Response | @Assignor | — | v1.0 | draft |
| 5 | Assignee | Free Response | — | Assignee Is Target Entity | v1.0 | draft |
| 6 | Assignee Is Target Entity | Classify | @Assignee | — | v1.0 | draft |
| 7 | Assigned Asset or Scope | Free Response | — | — | v1.0 | draft |
| 8 | Assignment Date | Date | — | — | v1.0 | draft |
| 9 | Present Assignment or Promise | Classify | — | Operative Assignment Language | v1.0 | draft |
| 10 | Operative Assignment Language | Verbatim | @Present Assignment or Promise | — | v1.0 | draft |
| 11 | Consideration | Free Response | — | — | v1.0 | draft |
| 12 | Further Assurances and Power of Attorney | Classify | — | — | v1.0 | draft |
| 13 | Work Made for Hire and Moral Rights | Free Response | — | — | v1.0 | draft |
| 14 | Execution Status | Classify | @Documents in Unit | — | v1.0 | draft |
| 15 | Recordation Evidence | Free Response | @Documents in Unit | — | v1.0 | draft |
| 16 | Referenced but Not Produced | Free Response | @Documents in Unit | — | v1.0 | draft |

---

## Column records

### 1. Documents in Unit

- Native type: Free Response
- Upstream: none
- Downstream: `Execution Status`, `Recordation Evidence`, `Referenced but Not Produced`
- Purpose: inventory the instrument and anything supporting it.

```markdown
## Task

List every document in the current review unit, in date order, identifying each one and its function.

## Scope

- Include the transfer instrument, any amendment or restatement of it, any confirmatory or corrective assignment, any schedule of assigned assets, and any recordation confirmation or registry acknowledgement.
- Treat schedules and exhibits physically attached to the instrument as part of it.
- Do not include documents that are only referenced but not present.

## Rules

- Identify each document by its printed title. Where no title is printed, describe it in four words or fewer and add `(untitled)`.
- Give each document's own stated date.
- State the function as one of `Assignment`, `Confirmatory assignment`, `Corrective assignment`, `Amendment`, `Schedule of assets`, `Recordation confirmation`, or `Other`.
- **Where a document is a confirmatory or corrective assignment, note in the evidence field what it was correcting.** A corrective assignment is usually evidence that the original instrument had a defect, which is itself worth knowing.
- Where a document relates to a different transfer than the subject of this row, still list it and append ` [different transfer]`.

## Output format

One line per document, earliest first:

`[YYYY-MM-DD or "date not stated"] — [Title] ([Function])`

Return no more than 8 lines and no more than 80 words. Do not include page counts, file names, quotations, or citation markers.
```

---

### 2. Instrument Type

- Native type: Classify
- Configured options, in UI order: `Standalone IP assignment`, `Assignment within an asset purchase`, `Contribution or capital transfer`, `Inter-company transfer`, `Founder assignment`, `Development partner assignment`, `Security assignment`, `Confirmatory assignment`, `Other`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: what kind of transfer this is, which tells a reviewer where in the chain
  it sits and what supporting documents should exist alongside it.

```markdown
## Task

Classify the kind of transfer instrument this review unit documents. Choose exactly one configured option.

## Classification rules

- `Founder assignment`: an individual founder, inventor, or author assigns to a target entity. **Frequently the first link in the chain and frequently the weakest**, because these are often signed late, without consideration recited, or as a promise rather than a present assignment.
- `Standalone IP assignment`: an assignment whose sole subject is intellectual property, between entities.
- `Assignment within an asset purchase`: an IP assignment executed as part of, or under, a broader asset or business acquisition. The acquisition agreement itself is a Contracts row; this is the IP transfer instrument delivered under it.
- `Contribution or capital transfer`: IP transferred as a capital contribution, in exchange for equity, or on a formation or reorganisation.
- `Inter-company transfer`: a transfer between two entities within the target group. Note in the evidence field whether both are on the Table Instructions list.
- `Development partner assignment`: an assignment from a development contractor, agency, joint development partner, or university.
- `Security assignment`: an assignment by way of security rather than outright. **This does not transfer beneficial ownership** and it is reported here rather than being mistaken for an acquisition.
- `Confirmatory assignment`: an instrument whose stated purpose is to confirm or perfect an earlier transfer.

Classify on the instrument's stated purpose and its parties, not its title. A document titled Assignment that transfers IP as part of an asset sale is `Assignment within an asset purchase`.

## Fallback rules

- Use `Other` where the instrument transfers IP in a way none of the options describes.
- Use `Unable to determine` where the document is too fragmentary to identify the kind of transfer.

## Output format

Return only the exact configured option and no explanation.
```

---

### 3. Assignor

- Native type: Free Response
- Upstream: none
- Downstream: `Assignor Authority`
- Purpose: who is transferring, exactly as named. **The chain is traced on these
  names**, so a normalized name breaks the trace.

```markdown
## Task

State the assignor or transferor under this instrument.

## Rules

- Report the name **exactly as printed**, including entity suffix, punctuation, and any misspelling or outdated form. Do not correct, normalize, expand, or update it. **The chain is traced by matching this name against the assignee name in the previous link and the record owner in the register**, and a corrected name breaks the match silently.
- Where the assignor is an individual, report the name as printed and add `(individual)`.
- Where there are several assignors, list each on its own line. Where more than six, list the first six and end with `and [N] further assignors`.
- Where the instrument recites that the assignor holds by a prior assignment, note that prior instrument in the evidence field, since it identifies the previous link.
- Where the assignor's name differs from the record owner shown in the Registrations table for the same asset, that mismatch is for the reviewer; report what this instrument says.
- Do not report a signatory acting for an entity assignor as the assignor. Signatories are reported in Assignor Authority.

## Fallback rules

- Return `Unable to determine` where the instrument names no assignor, or the name is illegible.

## Output format

`[Name exactly as printed][ (individual)]` per line. Return no more than 50 words.
```

---

### 4. Assignor Authority

- Native type: Free Response
- Upstream: `@Assignor`
- Downstream: none
- Purpose: who signed for the assignor and in what stated capacity. **An
  assignment signed by someone without authority transfers nothing**, and the
  capacity recited is the only evidence in the document.

```markdown
## Established result

- Assignor: @Assignor

Use this to identify whose signature block to read. Confirm the signatory and capacity against the instrument.

## Task

Report who executed this instrument for the assignor, and in what stated capacity.

## Rules

- Report the signatory's name and the title or capacity printed beneath the signature line, exactly as printed. Write `capacity not stated` where none is printed.
- Where the assignor is an individual signing personally, report `assignor signed personally`.
- **Where an individual signs for an entity in its capacity as manager, member, general partner, or attorney of another entity, report the chain as printed.** A layered signature block is where authority problems hide.
- Report any recital of authority, such as a statement that the signatory is duly authorised, and note whether a board or member resolution is referenced.
- **Where the instrument recites that a resolution or power of attorney authorises the signature, report it and append ` [authority document referenced]`.** That document should be produced, and it is reported in Referenced but Not Produced.
- Report any notarisation or witnessing, since some jurisdictions require it for an IP assignment to be recordable.
- **Do not assess whether the signatory had authority, and do not state whether the assignment is valid.** Report the capacity recited and stop.

## Fallback rules

- Return `Not stated` where the instrument bears a signature with no name or capacity printed.
- Return `Not applicable` where the instrument is unsigned by the assignor. The Execution Status column carries that.
- Return `Unable to determine` where the signature block is illegible.

## Output format

`[Signatory name] — [capacity as printed][; notarised]` per assignor, with any bracketed flag appended.

Return no more than 50 words.
```

---

### 5. Assignee

- Native type: Free Response
- Upstream: none
- Downstream: `Assignee Is Target Entity`
- Purpose: who is receiving, exactly as named.

```markdown
## Task

State the assignee or transferee under this instrument.

## Rules

- Report the name **exactly as printed**, including entity suffix, punctuation, and any misspelling. Do not correct, normalize, expand, or update it.
- Where the assignee is an individual, report the name as printed and add `(individual)`.
- Where there are several assignees, list each on its own line and append ` [co-assignment]` to the first line. **A transfer to two or more assignees creates co-ownership**, which constrains licensing and enforcement permanently and is easy to miss.
- Report any address or jurisdiction printed for the assignee, since it helps distinguish similarly named entities.
- Where the instrument names a successor, nominee, or designee as assignee rather than a specific entity, report the wording as printed.
- Do not report a signatory acting for the assignee as the assignee.

## Fallback rules

- Return `Unable to determine` where the instrument names no assignee, or the name is illegible.

## Output format

`[Name exactly as printed][, [jurisdiction]][ (individual)]` per line, with any qualifier appended. Return no more than 50 words.
```

---

### 6. Assignee Is Target Entity

- Native type: Classify
- Configured options, in UI order: `Matches a target entity exactly`, `Matches with name variance`, `Matches a former name of a target entity`, `An individual`, `A third party`, `Co-assignment including a non-target party`, `Unable to determine`
- Upstream: `@Assignee`
- Downstream: none
- Purpose: whether this link actually lands inside the target group.

**A chain of perfectly drafted assignments that ends at the wrong entity is not a
chain.** This is the column that catches IP assigned to a founder's holding
company, to a predecessor entity that was later dissolved, or to an affiliate that
is not being acquired.

```markdown
## Established result

- Assignee: @Assignee

Use this result and the target group list in the Table Instructions. Confirm the name against the instrument.

## Task

Classify the relationship between the assignee and the target group. Choose exactly one configured option.

## Classification rules

Apply the first rule that fits.

1. `Co-assignment including a non-target party`: more than one assignee is named and at least one is not a target entity.
2. `An individual`: the assignee is a natural person. **This is an assignment running the wrong way for diligence purposes** — IP held personally by a founder or employee is outside the business being bought.
3. `Matches a former name of a target entity`: the assignee name matches a prior name of a target entity as disclosed in the documents in this unit.
4. `A third party`: the assignee is an entity that is not a target entity and is not a former name of one.
5. `Matches with name variance`: the assignee is the same entity as one on the target group list but differs in form — a misspelling, a different or missing suffix, an abbreviation, or a trading name.
6. `Matches a target entity exactly`: the name is character-for-character a name on the target group list.

**Do not resolve a variance by assuming.** Where the name is similar to a target entity but could be a different entity — an affiliate, a parent, or an unrelated company — use `A third party` and note the similarity in the evidence field.

Where a target entity's former name is not disclosed in this unit, you cannot use `Matches a former name of a target entity`. Use `A third party`; the Corporate table's `Prior Names` column is where the reviewer resolves it.

## Fallback rules

- Use `Unable to determine` where the assignee name is illegible, or where Assignee returned `Unable to determine`.

## Output format

Return only the exact configured option and no explanation.
```

---

### 7. Assigned Asset or Scope

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what is actually transferred. **A schedule listing forty patents and a
  clause assigning "all intellectual property relating to the Business" are
  completely different facts**, and only one of them can be matched to a
  registration.

```markdown
## Task

Report the intellectual property this instrument transfers, as described.

## Rules

- Where the instrument identifies assets specifically — by registration number, application number, title, or mark — report the identifiers. Where more than eight are identified, report the count, the asset types, and the first four identifiers, then append ` and [N] further identified assets`.
- **Where the instrument transfers assets by general description rather than by identifier** — for example all intellectual property relating to a named business, all inventions conceived during a period, or all rights in a named product — report the description as printed and append ` [general description, no identifiers]`. That flag is what separates assets you can match to the register from assets you cannot.
- Report the categories of right transferred: patents, trademarks, copyrights, designs, domains, trade secrets, know-how, or software.
- **Report whether the transfer includes the right to sue for past infringement**, which is a distinct right and does not pass automatically. Its absence limits what the buyer can enforce for pre-closing conduct.
- Report any express exclusion or reservation, and any retained licence back to the assignor. **A retained licence back means the assignor keeps using the asset**, which materially changes what the buyer acquired.
- Report any geographic limitation on the transfer.
- Where a schedule is referenced but not attached, report that and append ` [schedule not in unit]`. The transfer's actual scope is then unknown.

## Fallback rules

- Return `Unable to determine` where the instrument's description of the transferred assets is illegible or absent.

## Output format

`Categories: [list]; identified assets: [identifiers or count]; past infringement: [included | Not addressed]; exclusions: [brief or "none"]; licence back: [brief or "none"]`, with any bracketed flags appended.

Return no more than 90 words.
```

---

### 8. Assignment Date

- Native type: Date — confirm the type accepts `Not stated`
- Upstream: none
- Downstream: none
- Purpose: when the transfer took effect, which orders the chain and reveals gaps.

```markdown
## Task

Identify the date this transfer took effect.

## Date-selection hierarchy

1. Use the effective date the instrument states for itself.
2. If none, use the date of the last party signature.
3. If neither, use the date printed in the preamble.

## Excluded dates

- The recordation date, which has its own column and is usually later
- The notarisation date
- The date of any prior instrument recited in the recitals
- The date of a schedule prepared separately
- File name and metadata dates, and transmittal and scan dates

## Rules

- Report the stated effective date even where it precedes the signature dates. **A retroactive effective date is common in founder and confirmatory assignments and it is worth seeing**, because it may not be effective against a third party who took an interest in between.
- Where the effective date precedes the signature date by more than thirty days, append ` [retroactive effective date]`.
- Where the instrument states no date at all, return `Not stated`. **An undated assignment is a real problem** — it cannot be placed in the chain — and the reviewer needs to see it as a finding rather than as a blank.
- Do not calculate anything from the date.

## Output format

`YYYY-MM-DD`, with any bracketed flag appended. Preserve partial precision as printed. Return `Not stated` where no date can be selected under the hierarchy.
```

---

### 9. Present Assignment or Promise

- Native type: Classify
- Configured options, in UI order: `Present assignment`, `Present assignment with future-rights clause`, `Agreement to assign in future`, `Conditional assignment`, `Assignment by way of security`, `Not an assignment`, `Unable to determine`
- Upstream: none
- Downstream: `Operative Assignment Language`
- Purpose: **the reason this table exists.**

A promise to assign transfers nothing. It requires a further instrument, and until
that instrument exists the assignor still owns the asset. Filtered across a
portfolio, this column produces the pre-closing remediation list, and it is the
most common IP defect in a private-company diligence.

```markdown
## Task

Classify what the operative words of this instrument do. Choose exactly one configured option.

## Scope

- Read the operative granting or transferring words, not the clause heading, the document title, or the recitals.
- Where the instrument contains several granting provisions covering different asset categories, classify on the weakest of them and report the others in the Language column. **A single promise-to-assign limb defeats the certainty of the rest.**

## Classification rules

Apply the first rule that fits.

1. `Not an assignment`: the operative words grant a licence, a covenant not to sue, or a right of use, without transferring ownership. **A document titled Assignment that grants only a licence belongs here**, and it is a finding.
2. `Assignment by way of security`: the transfer is expressed as security for an obligation, with a reassignment or redemption on discharge. Beneficial ownership does not pass.
3. `Agreement to assign in future`: the operative words are **agrees to assign, will assign, shall assign, undertakes to assign, or covenants to assign**. This is a promise, not a transfer. It requires a further instrument.
4. `Conditional assignment`: the transfer is expressed to take effect only on a stated condition — payment of consideration, completion of a transaction, or an approval. **Report in the evidence field whether the documents evidence the condition being satisfied.** Until it is, nothing has passed.
5. `Present assignment with future-rights clause`: the operative words assign presently, **and** a further limb purports to assign rights arising in the future. The present limb works; the future limb has the same weakness as a promise in most jurisdictions, and the split is worth recording.
6. `Present assignment`: the operative words assign presently — **assigns, hereby assigns, does hereby assign, hereby transfers, hereby sells and assigns** — with no material qualification.

**Classify on the verb.** Tense and mood are the finding. A clause reading "Assignor hereby agrees to assign" is `Agreement to assign in future` notwithstanding the word hereby.

A further-assurances covenant alongside a present assignment does not weaken it. Classify as `Present assignment` and report the covenant in its own column.

## Fallback rules

- Use `Unable to determine` where the operative words are illegible, or where two granting provisions of equal prominence conflict irreconcilably.
- Do not use `Unable to determine` because a jurisdiction's formalities are unclear. That is a legal question, not an extraction problem.

## Output format

Return only the exact configured option and no explanation.
```

---

### 10. Operative Assignment Language

- Native type: Verbatim
- Upstream: `@Present Assignment or Promise`
- Downstream: none
- Purpose: the exact granting words. The finding is a verb, and a reviewer has to
  see it rather than take a classification on trust.

```markdown
## Established result

- Present assignment or promise: @Present Assignment or Promise

## Task

If Present Assignment or Promise is any value other than `Unable to determine`, quote the operative granting or transferring words exactly as written.

If it is `Unable to determine`, quote whatever granting language is legible and begin the answer with `Partial —`.

## Rules

- Quote verbatim, without paraphrase, correction, or ellipsis inside a sentence.
- Quote from the most recently dated document in the unit that states the provision, and end the quotation with ` [Source: [document title], [YYYY-MM-DD]]`.
- **Quote the granting words in full, including the verb.** The verb is the finding. A quotation that begins after the verb is useless.
- Quote the description of the transferred subject matter within the granting provision, and any condition attached to the transfer.
- Where the instrument contains several granting provisions covering different categories, quote each and label it, so the reviewer can see which limbs work and which do not.
- Where the instrument includes a future-rights limb, quote it separately and label it.
- Where the granting provision exceeds 200 words, quote the granting words and the subject-matter description in full, replacing subordinate enumerations with `[...]` between sentences.
- Do not add analysis, and do not state whether the transfer was effective.

## Output format

The quoted text, followed by the source tag. Return no more than 250 words.
```

---

### 11. Consideration

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: what was given for the transfer. **In several jurisdictions an
  assignment without consideration is vulnerable**, and a nominal recital with no
  evidence of payment is a common weakness in founder assignments.

```markdown
## Task

Report the consideration recited for this transfer.

## Rules

- Report the consideration as recited, with the currency where an amount is stated.
- **Report a nominal recital as printed rather than describing it as nominal** — for example `$1.00 and other good and valuable consideration`. The precise wording matters because it is what a challenge would be argued on.
- Where the consideration is non-cash, report it as described in six words or fewer: shares issued, employment, cancellation of indebtedness, mutual covenants, or contribution to capital.
- Where the consideration is stated to be the consideration under another agreement, name that agreement as printed and add `(consideration under referenced agreement)`.
- **Report whether the instrument recites that consideration has been received**, for example an acknowledgement of receipt, as distinct from an obligation to pay it.
- Where the transfer is conditional on payment, note it here and confirm the condition is also reported in `Present Assignment or Promise`.
- Do not calculate, allocate, or value anything, and do not assess adequacy.

## Fallback rules

- Return `Not stated` where the instrument recites no consideration at all. **This is a finding in its own right**, particularly for a founder assignment, and the reviewer will treat it as one.
- Return `Unable to determine` where the recital is illegible.

## Output format

`[Consideration as recited]; receipt acknowledged: [yes | Not addressed]`. Return no more than 45 words.
```

---

### 12. Further Assurances and Power of Attorney

- Native type: Classify
- Configured options, in UI order: `Both further assurances and power of attorney`, `Further assurances only`, `Power of attorney only`, `Neither`, `Unable to determine`
- Upstream: none
- Downstream: none
- Purpose: whether the assignee can perfect the transfer **without the assignor's
  cooperation.**

This is the practical question. A present assignment from a founder who has since
left on bad terms is only recordable if someone can execute the recordation
papers. A power of attorney means the assignee can. Without one, perfecting
requires finding and persuading the assignor, and that is a remediation task with
a real chance of failure.

```markdown
## Task

Classify whether the instrument contains a further-assurances covenant and a power of attorney. Choose exactly one configured option.

## Scope

- A further-assurances covenant obliges the assignor to execute further documents, provide information, or cooperate in recording, prosecuting, or enforcing the transferred rights.
- A power of attorney appoints the assignee, or someone on its behalf, to execute documents in the assignor's name. **It may be labelled as an appointment of attorney-in-fact, an irrevocable proxy, or a limited power of attorney.**
- Exclude a general cooperation clause about the wider transaction that does not extend to the IP.
- Exclude an obligation on the assignee rather than the assignor.

## Classification rules

- `Both further assurances and power of attorney`: the strongest position, and the one to expect in a well-drafted assignment.
- `Power of attorney only`: unusual, and sufficient for perfection in practice.
- `Further assurances only`: the assignee has a contractual right to cooperation but no self-help. **This is the common case and it is adequate only while the assignor is available and willing.**
- `Neither`: the assignee has no stated route to perfection if the assignor will not cooperate.

Report in the evidence field whether the power of attorney is stated to be irrevocable and whether it is stated to be coupled with an interest, since a revocable power is worth much less. Report also whether the further-assurances covenant is stated to be at the assignee's expense.

## Fallback rules

- Use `Unable to determine` where the relevant provisions are illegible.

## Output format

Return only the exact configured option and no explanation.
```

---

### 13. Work Made for Hire and Moral Rights

- Native type: Free Response
- Upstream: none
- Downstream: none
- Purpose: the copyright-specific provisions, which are separate from assignment
  and can be the operative mechanism or a fallback to it.

```markdown
## Task

Report any work-made-for-hire, first-ownership, or moral rights provision in this instrument.

## Include where expressly stated

- Any statement that the works are, or are intended to be, works made for hire
- Any statement that copyright vests in the assignee on creation, or belongs to it as a matter of law
- **Any assignment expressed as a fallback where a work-made-for-hire characterisation fails.** This is the standard belt-and-braces drafting and its presence is reassuring; its absence, in an instrument relying only on work-made-for-hire, is a gap
- Any waiver of moral rights, and the jurisdictions or rights it covers
- Any consent to acts that would otherwise infringe moral rights, used where waiver is not permitted
- Any waiver or assignment of rights of attribution and integrity
- Any assignment of rights in performances

## Rules

- **Report whether a work-made-for-hire statement stands alone or is backed by an assignment.** A work-made-for-hire characterisation only works for defined categories of work and defined relationships; where it fails and there is no assignment fallback, nothing transferred.
- Report the moral rights provision as waiver, consent, or assignment, since the three have different effects and only some are available in some jurisdictions.
- Report the terms as stated. **Do not assess whether the work-made-for-hire characterisation is available, or whether a moral rights waiver is effective in any jurisdiction.** Both are jurisdiction-specific legal questions.

## Fallback rules

- Return `Not addressed` where the instrument contains no such provision. **For an instrument transferring software, designs, or content, this is a gap** and the reviewer should see it.
- Return `Not applicable` where the instrument transfers only patents, trademarks, or domains, so no copyright question arises.
- Return `Unable to determine` where the provisions are illegible or inconsistent.

## Output format

`Work made for hire: [as stated or "Not addressed"]; assignment fallback: [present | absent]; moral rights: [waiver | consent | assignment | Not addressed]; scope: [brief]`

Return no more than 60 words.
```

---

### 14. Execution Status

- Native type: Classify
- Configured options, in UI order: `Fully executed`, `Assignor signed only`, `Assignee signed only`, `Unsigned`, `Form or template`, `Notarised`, `Unable to determine`
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the instrument was signed. **An unsigned assignment transfers
  nothing, however well drafted**, and unsigned assignments in a data room are
  common.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to know which documents to check. Confirm signature evidence against the signature blocks.

## Task

Classify the visible execution status of the transfer instrument in this review unit. Choose exactly one configured option.

## Scope

- Evaluate the transfer instrument itself. Where an amendment or confirmatory assignment is also present, classify on the least complete.
- Exclude witness and notary blocks from the party count, but see the `Notarised` option below.
- Where the instrument provides only an assignor signature block — which is normal for a short-form recordable assignment — treat the assignor's block as the only party block.

## Classification rules

Apply the first rule that fits.

1. `Form or template`: the document is an unpopulated form, with bracketed placeholders, blank party names, or a blank schedule.
2. `Unsigned`: party signature blocks are provided and none bears a signature marker.
3. `Assignee signed only`: the assignee's block bears a signature marker and the assignor's does not. **This is the worst common case**: the party who needed to sign has not.
4. `Assignor signed only`: the assignor's block bears a signature marker and the assignee's does not. Where the instrument provides no assignee block, use `Fully executed` instead.
5. `Notarised`: every party block required is signed **and** a notarial certificate or apostille is present. Use this in preference to `Fully executed`, because some jurisdictions require notarisation for recordation.
6. `Fully executed`: every signature block the document provides bears a signature marker.

A signature marker is a handwritten signature, an electronic-signature block from a signing platform, or a conformed signature shown as `/s/` followed by a name. A typed name, a blank signature line, a `DRAFT` watermark, or a stated effective date is not a signature marker.

## Fallback rules

- Use `Unable to determine` where a signature is present but illegible, where a signature page is referenced but missing, or where documents in the unit conflict.
- Do not treat a recordation confirmation as evidence that the underlying instrument was signed, unless the confirmation reproduces the signed instrument.

## Output format

Return only the exact configured option and no explanation.
```

---

### 15. Recordation Evidence

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: whether the transfer was recorded with the office. **Recordation is not
  what makes an assignment effective, but an unrecorded assignment leaves the
  register showing the wrong owner** — and in several jurisdictions it can be
  defeated by a later purchaser who does record.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use the inventory to identify any recordation document. Confirm the details against it.

## Task

Report whether and where this transfer has been recorded with an intellectual property office or registrar.

## Rules

- For each recordation, report the office, the recordation date, and the recordation reference — a reel and frame, a recordation number, or an equivalent identifier — exactly as printed.
- **Where the instrument covers assets in several jurisdictions, report which jurisdictions have recordation evidence and which do not.** Partial recordation is common and it is the actionable finding, because the unrecorded jurisdictions are the remediation list.
- Where a recordation is evidenced only by a filing receipt rather than a confirmation of recordation, say which.
- Report any recorded correction or re-recordation and its date.
- Compare the recordation date to the assignment date. **Where the gap exceeds twelve months, append ` [recorded over 12 months after assignment]`.** A long gap is where an intervening third-party interest could have arisen.
- **Do not assess the effect of recordation or non-recordation.** It differs by jurisdiction and by right, and it is a legal question.

## Fallback rules

- Return exactly `No recordation evidence in unit` where the documents contain none.

Note: this is a positive finding, not a fallback state. It means the recordation confirmation was not produced. **It does not establish that the assignment is unrecorded** — a register search does that, and it belongs in the reviewer's verification work.

- Return `Not applicable` where the transferred rights are of a kind not recordable in any relevant register, such as trade secrets or know-how only.
- Return `Unable to determine` where recordation documents are illegible or inconsistent.

## Output format

One line per recordation:

`[Office] — recorded [YYYY-MM-DD] — [reference]`, with any bracketed flag appended, and a final line naming any jurisdictions with no recordation evidence.

Return no more than 6 lines and no more than 75 words.
```

---

### 16. Referenced but Not Produced

- Native type: Free Response
- Upstream: `@Documents in Unit`
- Downstream: none
- Purpose: name every document this instrument refers to that is not present.
  **In this table the referenced documents are usually the missing links in the
  chain**, which makes it the highest-value coverage column in the set.

```markdown
## Established results

- Documents in unit: @Documents in Unit

Use this inventory to determine what is present. Identify references by reading the documents in the current unit.

## Task

List every document this instrument refers to that is not present in the review unit.

## Scope

- **Include any prior assignment, transfer, or instrument recited as the source of the assignor's title.** These are the previous links in the chain and they are what the chain analysis needs.
- Include schedules, exhibits, and annexes of assigned assets listed as attached but not present.
- Include the acquisition, contribution, development, or employment agreement the assignment is stated to be executed under.
- Include board or member resolutions, powers of attorney, and authority documents referenced as authorising execution.
- Include confirmatory or corrective assignments referenced but absent.
- Include recordation confirmations referenced but absent.
- Include any licence back, escrow, or side agreement referenced as affecting the transfer.
- Include any consent required from a co-owner, licensor, or lender that the instrument references.
- Exclude statutes, regulations, treaties, and office practice manuals.

## Rules

- Name each document as the referencing document names it, and give its date where stated.
- **Where a prior instrument is recited as the source of the assignor's title and is not produced, add `; prior link in chain`.** This is the flag the chain analysis is built from, and it should be filtered first.
- **Where a schedule of assigned assets is referenced and absent, add `; scope unknown without schedule`.** Without it, what the instrument transferred cannot be determined at all.
- Where an authority document is referenced, add `; execution authority`.
- Do not report a document as absent where it is attached to a document in the unit.
- Consolidate repeated references to the same document into one line.

## Fallback rules

- Return exactly `None identified` where every referenced document is present.

Note: `None identified` is a positive finding for this column, not a fallback state.

## Output format

One line per missing document:

`[Name as referenced] — [YYYY-MM-DD or "date not stated"][; prior link in chain | ; scope unknown without schedule | ; execution authority]`

Return no more than 12 lines and no more than 120 words.
```

---

## Human-review fields

| Column | Values |
|---|---|
| Review status | Unreviewed / Verified / Corrected / Disputed |
| Reviewed by | Initials |
| **Link effective** | Yes / Defective / Unresolved |
| **Chain complete to target** | Yes / Gap identified / Not traced |
| **Remediation required** | None / Confirmatory assignment / Recordation / Both / Third-party consent |
| **Assignor available** | Yes / Departed / Dissolved / Unknown |
| Materiality | Critical / Material / Monitor / Immaterial |
| Deal consequence | Free text |

**Assignor available** is the column that turns a defect into a plan. A promise to
assign from a current employee is a form to sign. The same promise from a founder
who left four years ago, or from a dissolved development agency, is a problem that
may not be fixable before closing.

### The chain analysis, which is human work

**This is the canonical multi-hop problem and it does not automate in a Review
Table.** Perform it in Excel from this table's export plus the Registrations
export.

1. For each critical asset, list every instrument in this table whose
   `Assigned Asset or Scope` covers it, in `Assignment Date` order.
2. Confirm each link's `Assignee` matches the next link's `Assignor`
   character-for-character. **Every mismatch is a gap or a name-variance question.**
3. Confirm the last link's assignee matches the `Record Owner` in the
   Registrations table.
4. Confirm the first link's assignor is the creator, inventor, or original owner.
   For assets created by employees or contractors, this is where the Employment
   tables' IP assignment coverage check joins the chain.
5. Flag every asset whose chain contains a row where
   `Present Assignment or Promise` is anything other than `Present assignment` or
   `Present assignment with future-rights clause`.
6. Flag every asset covered only by rows with
   `[general description, no identifiers]`, since those cannot be matched to the
   register with confidence.

Then work the exceptions. The output is the pre-closing IP remediation list, and it
is the deliverable the IP workstream is judged on.

### Other reconciliation work

- **Employee and contractor coverage.** Everyone who contributed to critical IP
  needs an assignment. Match the Employment tables against this one; anyone in the
  first without a corresponding present assignment is a gap.
- **Present-versus-future filter.** Filter `Present Assignment or Promise` to
  `Agreement to assign in future` and `Conditional assignment`. **These are
  defects, not assignments**, and each needs a confirmatory instrument before
  closing.
- **Recordation remediation.** Every row with `No recordation evidence in unit`
  or a partial-recordation note, for material assets.
- **Co-ownership.** Every row classified
  `Co-assignment including a non-target party`, against the licensing and
  enforcement plan.

---

## Test set

- [ ] Standalone assignment with present-tense granting words, fully executed and recorded
- [ ] Assignment using "agrees to assign"
- [ ] Assignment using "hereby agrees to assign", to confirm the verb governs over "hereby"
- [ ] Assignment with a present limb and a separate future-rights limb
- [ ] Assignment conditional on payment, with no evidence the condition was met
- [ ] Document titled Assignment that grants only a licence
- [ ] Assignment by way of security
- [ ] Confirmatory assignment correcting an earlier defective instrument
- [ ] Founder assignment with no consideration recited
- [ ] Founder assignment with a nominal consideration recital
- [ ] Assignment signed by the assignee only
- [ ] Unsigned assignment
- [ ] Assignment with a layered signature block, an individual signing for an LLC as manager of another entity
- [ ] Assignment reciting a board resolution not produced
- [ ] Notarised assignment with an apostille
- [ ] Assignment with further assurances and no power of attorney
- [ ] Assignment with an irrevocable power of attorney coupled with an interest
- [ ] Assignment with neither further assurances nor a power of attorney
- [ ] Assignment with a schedule of forty patents attached
- [ ] Assignment referencing a schedule that is not attached
- [ ] Assignment by general description of a business, with no identifiers
- [ ] Assignment silent on the right to sue for past infringement
- [ ] Assignment with a licence back to the assignor
- [ ] Assignment to two assignees, one outside the target group
- [ ] Assignment to an individual
- [ ] Assignment to a target entity's former name
- [ ] Assignment to an entity with a name close to but not matching a target entity
- [ ] Assignment relying on work made for hire with no assignment fallback
- [ ] Assignment with a moral rights waiver covering named jurisdictions
- [ ] Patent-only assignment, to confirm the moral rights column returns `Not applicable`
- [ ] Assignment with an effective date eighteen months before signature
- [ ] Assignment recorded three years after its date
- [ ] Assignment covering five jurisdictions with recordation evidence for two
- [ ] Undated assignment
- [ ] Assignment reciting a prior assignment not produced

Then test the dependencies: change `Present Assignment or Promise` from
`Present assignment` to `Unable to determine` and confirm
`Operative Assignment Language` switches to the `Partial —` behaviour. Change
`Assignee` from a target entity to an individual and confirm
`Assignee Is Target Entity` moves to `An individual`.

---

## Shared change log

| Date | Column | From → To | Change | Failure class | Rerun scope | Regressions |
|---|---|---|---|---|---|---|
| | | v1.0 | Initial draft | — | — | — |
