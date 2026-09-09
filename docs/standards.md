# Standards

`00a-build-plan-and-standards.md` states rules the prompts are meant to follow. The kernel
**enforces** the ones that can be checked mechanically, because a prompt instruction is a
request and a check is a check.

## The fallback vocabulary (§5)

Five states, and only five:

| State | Meaning |
|---|---|
| `Not addressed` | The documents are silent on the subject |
| `Not stated` | The value asked for does not appear |
| `Not applicable` | No meaningful application to this document type |
| `Incorporated terms` | Another document supplies the terms and is not in the unit |
| `Unable to determine` | Evidence exists but is conflicting, incomplete, or illegible |

Banned: `N/A`, `None`, `Silent`, `Unclear`, `Not determinable`, `Not found`.

Two rules `00a` says are violated most often, both checked:

- **A fallback never replaces a value the document states.** If an effective date equals the
  execution date, return the date.
- **Silence is not uncertainty.** A silent document is `Not addressed`, never
  `Unable to determine`.

**Positive findings that look like fallbacks** — `None identified`, `None referenced`,
`None recorded`, `None named`, `None disclosed` — mean the search was run and found nothing.
They are answers, and are not treated as absences.

## Where each rule is enforced

| `00a` rule | Check | Code |
|---|---|---|
| §5 banned synonyms | Cell value against the banned list | `BANNED_FALLBACK` |
| §5 `Not stated` is for typed columns | Cell value against native type | `NOT_STATED_ON_UNTYPED_COLUMN` |
| Classify returns a configured option | Cell against the option list | `OPTION_NOT_CONFIGURED` |
| Classify is one line | Cell shape | `CLASSIFY_MULTILINE` |
| ISO dates, partial precision preserved | Cell format | `DATE_FORMAT` |
| §6 markdown is not authorised in a cell | Cell text | `MARKDOWN_IN_CELL` |
| §6 citations belong in evidence | Cell text | `CITATION_IN_CELL` |
| §7 report, never compute | Cell text | `ARITHMETIC_IN_CELL` |
| Verbatim reproduces source text | Quote against the unit's documents | `VERBATIM_NOT_IN_SOURCE` |
| Verbatim checked against a transcription | Unit provenance | `VERBATIM_FROM_OCR` |

## Two places the check is deliberately narrower than the rule

**A configured option is the column's declared vocabulary.** Where a column explicitly
configures a value `00a` bans, the cell is not flagged — the defect is the prompt, and
flagging the cell produces one identical violation per row. A check that fires on correct
answers stops being read.

**A truncated option list is not a vocabulary.** Where the parser could not read the whole
list, it is neither presented to the model as complete nor enforced against.

## The Verbatim comparison form

`00a` says the entire spot-check design rests on Verbatim returning true source text, so the
comparison absorbs what extraction does to text without absorbing paraphrase. Each of these
was observed on a real PDF and each rejected a correct quotation before it was handled:

ligatures (`oﬃce`), soft hyphens, hyphenated line breaks (`non-\nexclusive`), line wrapping,
smart quotes, en and em dashes, non-breaking spaces.

Hyphens are dropped entirely, so `non-compete` and `noncompete` compare equal. That is a
deliberate loosening — the check exists to catch paraphrase, and paraphrase differs by words,
not punctuation. Tests assert three plausible paraphrases of the fixture lease's assignment
clause are still rejected.

## What stays with a human (§10)

Never a filled column: which document is operative or controlling; whether an authority,
entity or title defect exists; whether the transaction requires a consent and whether one
obtained is sufficient; enforceability, validity, materiality or legal risk; any arithmetic;
the deal consequence of anything.

## Two contradictions inside `00a` worth resolving

Found by linting the corpus against its own standard:

**§5 versus §8.** §5 restricts `Not stated` to Date, Number, Currency and Duration columns.
§8 says that where a type rejects a fallback, the column becomes Free Response and *"do not
change what the fallback means to suit the type"*. 84 Free Response columns follow §8 and
therefore breach §5's parenthetical. The prompts are right; §5 needs a sentence acknowledging
§8's escape hatch.

**§6's "consumed by a rule".** §6 says every `@` reference must be consumed by a rule. The
corpus consistently consumes one either in the preamble (`Use this inventory to identify what
is present`) or by branching on the upstream's values (`For a \`Corporation\`, read…`) rather
than by naming the column. Of 253 columns declaring a reference, 88 consume it in the
preamble, 130 by name, 25 by value, and roughly 10 are candidates for a genuine dangling
reference. Whether the first and third count is a drafting decision, not a mechanical fact.
