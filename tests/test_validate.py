"""00a is enforced, not requested. These are the checks that make that true."""

from __future__ import annotations

import pytest

from diligence_kernel.engine.validate import (
    is_fallback,
    is_positive_null,
    validate_cell,
    validate_verbatim,
)

OPTIONS = ["Complete on its face", "Sequence gap", "Unable to determine"]


def codes(*args, **kwargs) -> set[str]:
    return {v.code for v in validate_cell(*args, **kwargs)}


@pytest.mark.parametrize("value", ["N/A", "None", "Silent", "Unclear", "Not found"])
def test_banned_synonyms_are_rejected(value):
    assert "BANNED_FALLBACK" in codes(value, native_type="Free Response")


@pytest.mark.parametrize("value", ["Not addressed", "Not applicable", "Incorporated terms"])
def test_permitted_fallbacks_pass(value):
    assert codes(value, native_type="Free Response") == set()
    assert is_fallback(value)


def test_not_stated_is_reserved_for_typed_columns():
    assert "NOT_STATED_ON_UNTYPED_COLUMN" in codes("Not stated", native_type="Free Response")
    assert codes("Not stated", native_type="Date") == set()
    assert codes("Not stated", native_type="Duration") == set()


def test_positive_null_findings_are_answers_not_absences():
    assert is_positive_null("None identified")
    assert not is_fallback("None identified")
    assert codes("None identified", native_type="Free Response") == set()


def test_classify_must_return_a_configured_option():
    assert (
        codes("Complete on its face", native_type="Classify", configured_options=OPTIONS) == set()
    )
    assert "OPTION_NOT_CONFIGURED" in codes(
        "Looks complete", native_type="Classify", configured_options=OPTIONS
    )
    # A permitted fallback is always acceptable, configured or not.
    assert "OPTION_NOT_CONFIGURED" not in codes(
        "Not addressed", native_type="Classify", configured_options=OPTIONS
    )


def test_classify_must_be_one_line():
    assert "CLASSIFY_MULTILINE" in codes(
        "Sequence gap\nbecause amendment 2 is missing",
        native_type="Classify",
        configured_options=OPTIONS,
    )


@pytest.mark.parametrize(
    "value,ok",
    [
        ("2024-08-14", True),
        ("2024-08", True),
        ("2024", True),
        ("14 August 2024", False),
        ("08/14/2024", False),
    ],
)
def test_dates_are_iso_with_partial_precision_preserved(value, ok):
    assert ("DATE_FORMAT" in codes(value, native_type="Date")) is not ok


def test_markdown_is_not_authorised_in_a_cell():
    assert "MARKDOWN_IN_CELL" in codes("**Acme Corp**", native_type="Free Response")
    assert "MARKDOWN_IN_CELL" in codes("- one\n- two", native_type="Free Response")
    # A Verbatim column reproduces source text, which may legitimately look like markup.
    assert "MARKDOWN_IN_CELL" not in codes("- one\n- two", native_type="Verbatim")


def test_computed_figures_are_refused():
    assert "ARITHMETIC_IN_CELL" in codes(
        "4,500,000 shares for a total of $9,000,000", native_type="Free Response"
    )
    assert codes("4,500,000 shares as stated", native_type="Free Response") == set()


def test_citations_belong_in_evidence_not_the_cell():
    assert "CITATION_IN_CELL" in codes("2024-08-14 per Section 4.2", native_type="Date")


def test_empty_cell_is_a_violation():
    assert "CELL_EMPTY" in codes("   ", native_type="Free Response")


SOURCE = [
    "Neither party may assign this Agreement without the prior written consent of the other party."
]


def test_verbatim_tolerates_wrapping_but_not_paraphrase():
    wrapped = "Neither party may assign this Agreement\nwithout the prior written consent of the\nother party."
    assert validate_verbatim(wrapped, SOURCE) == []
    assert (
        validate_verbatim("The agreement cannot be assigned.", SOURCE)[0].code
        == "VERBATIM_NOT_IN_SOURCE"
    )


def test_verbatim_tolerates_smart_quotes_and_dashes():
    source = ["The Company's obligations — including payment — survive termination."]
    assert (
        validate_verbatim(
            "The Company's obligations - including payment - survive termination.", source
        )
        == []
    )


def test_verbatim_accepts_a_fallback():
    assert validate_verbatim("Not addressed", SOURCE) == []


# --- a column's declared vocabulary ------------------------------------------------


def test_a_configured_option_is_not_flagged_on_the_cell(loaded):
    """`None` is Secondary Workstream's declared vocabulary; the defect is the prompt."""
    assert (
        validate_cell(
            "None", native_type="Classify", configured_options=["None", "Unable to determine"]
        )
        == []
    )
    # Where it is not configured, it is still a banned synonym.
    violations = validate_cell("None", native_type="Free Response")
    assert [v.code for v in violations] == ["BANNED_FALLBACK"]


def test_a_truncated_option_list_is_not_enforced_as_a_vocabulary():
    """Where the parser could not read the whole list, it is not a vocabulary to enforce.

    Asserting a partial list rejects correct answers: `Employment and HR` was off-vocabulary
    against the two options a truncated Secondary Workstream bullet produced.
    """
    assert validate_cell("Employment and HR", native_type="Classify", configured_options=[]) == []
    violations = validate_cell(
        "Employment and HR",
        native_type="Classify",
        configured_options=["None", "Unable to determine"],
    )
    assert [v.code for v in violations] == ["OPTION_NOT_CONFIGURED"]


# --- the source tag every Verbatim column is told to append ---------------------------


def test_a_verbatim_quote_may_carry_the_source_tag_it_was_asked_for():
    """Every Verbatim column's output contract says "the quoted text, followed by the source
    tag" — and the corpus never defines the tag's shape, so a model invents one. Rejecting a
    correct quotation for carrying it is a false positive on the check 00a says the whole
    spot-check design rests on.
    """
    source = [
        "Neither party may assign this Agreement without the prior written consent of the "
        "other party; provided, however, that either party may assign this Agreement without "
        "consent to a successor in connection with a merger, consolidation, or sale of all or "
        "substantially all of its assets."
    ]
    quote = source[0]
    for tag in (
        " [source: msa-amendment-1.txt, 2024-01-09]",
        " (Amendment No. 1, 2024-01-09)",
        " — source: Amendment No. 1",
        "",
    ):
        assert validate_verbatim(quote + tag, source) == [], tag or "bare quote"


@pytest.mark.parametrize(
    "value",
    [
        "The agreement may not be transferred without permission.",
        "Tenant shall pay base rent of $61,250.00 per month. [source: lease.pdf]",
        "[source: msa-amendment-1.txt]",
        "the other party [source: x]",
    ],
)
def test_the_tag_allowance_does_not_let_paraphrase_through(value):
    """Including a cell that is only a tag: an empty needle is `in` every source."""
    source = ["Neither party may assign this Agreement without the prior written consent."]
    assert [v.code for v in validate_verbatim(value, source)] == ["VERBATIM_NOT_IN_SOURCE"]


def test_strip_source_tag_leaves_ordinary_text_alone():
    from diligence_kernel.engine.validate import strip_source_tag

    assert strip_source_tag("no tag here") == "no tag here"
    assert strip_source_tag("quoted text [source: a.pdf]") == "quoted text"
    # Parentheses that are part of the quotation are not a tag when text follows them.
    assert strip_source_tag("fifty percent (50%) of the voting securities").endswith("securities")
