"""Auditing the corpus against the standards it sets for itself."""

from __future__ import annotations

from collections import Counter

from diligence_kernel import server
from diligence_kernel.corpus.lint import lint_corpus
from diligence_kernel.engine.validate import validate_cell


def codes(findings) -> Counter:
    return Counter(f.code for f in findings)


def test_the_corpus_lints_with_only_known_defects(loaded):
    """A regression guard: these counts should fall as prompts are corrected, never rise."""
    found = codes(lint_corpus(loaded))
    assert found["BANNED_VALUE_IN_PROMPT"] == 33
    assert found["RETURN_VALUE_NOT_CONFIGURED"] == 3
    assert found["PROMPT_OVER_BUDGET"] == 1
    assert found["PROMPT_SECTIONS_OUT_OF_ORDER"] == 0, "section order is clean corpus-wide"


def test_banned_values_name_the_column_and_the_remedy(loaded):
    findings = [f for f in lint_corpus(loaded) if f.code == "BANNED_VALUE_IN_PROMPT"]
    secondary = next(f for f in findings if f.subject_name == "05 Secondary Workstream")
    assert "'None'" in secondary.observation
    assert "None identified" in secondary.observation, "the remedy 00a already provides"
    assert secondary.evidence["options"] == ["None"]


def test_a_classify_column_told_to_return_an_unoffered_option(loaded):
    findings = [f for f in lint_corpus(loaded) if f.code == "RETURN_VALUE_NOT_CONFIGURED"]
    names = {f.subject_name for f in findings}
    assert "01 Assignment Restriction" in names
    one = next(f for f in findings if f.subject_name == "01 Assignment Restriction")
    assert one.evidence["instructed"] == ["Incorporated terms"]
    assert "Incorporated terms" not in one.evidence["options"]


def test_a_reference_to_another_column_is_not_an_instruction(loaded):
    """`If Assignment Restriction is `Not addressed`` is about the upstream column."""
    findings = [f for f in lint_corpus(loaded) if f.code == "RETURN_VALUE_NOT_CONFIGURED"]
    assert "01 Succession Carve-Out" not in {f.subject_name for f in findings}


def test_one_prompt_defect_is_one_finding_not_one_per_cell(loaded):
    """The cry-wolf this replaced: nine identical cell violations in a ten-row matter."""
    findings = [
        f
        for f in lint_corpus(loaded)
        if f.code == "BANNED_VALUE_IN_PROMPT" and f.subject_name == "05 Secondary Workstream"
    ]
    assert len(findings) == 1


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


def test_corpus_check_tool_summarises_by_code(loaded):
    server.set_conn(loaded)
    try:
        out = server.corpus_check()
        assert out["columns_checked"] == 591
        assert out["by_code"]["BANNED_VALUE_IN_PROMPT"] == 33
        assert out["columns_with_findings"] < out["columns_checked"]

        scoped = server.corpus_check(table="05")
        assert all(f["subject_name"].startswith("05 ") for f in scoped["findings"])
        assert scoped["finding_count"] < out["finding_count"]
    finally:
        server.set_conn(None)
