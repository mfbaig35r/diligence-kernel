"""Matching playbook fields to corpus columns by meaning.

The lexical scorer this replaced resolved 42% of fields while 95% of their terms appeared
somewhere in the corpus, and called covered concepts gaps. These tests pin the properties that
made the replacement trustworthy rather than merely different.
"""

from __future__ import annotations

import json

import pytest

from diligence_kernel import crosswalk as cw


class StubEmbedder:
    """Deterministic vectors from character counts, so tests need no network."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def __call__(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        out = []
        for t in texts:
            low = t.lower()
            out.append([low.count(c) + 0.1 for c in "abcdefghij"])
        return out


def test_cosine_is_a_cosine():
    assert cw.cosine([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cw.cosine([1, 0], [0, 1]) == pytest.approx(0.0)
    assert cw.cosine([1, 1], [2, 2]) == pytest.approx(1.0), "scale-invariant"
    assert cw.cosine([], [1]) == 0.0, "no vector, no similarity"
    assert cw.cosine([0, 0], [1, 1]) == 0.0, "a zero vector cannot be compared"


def test_embeddings_are_cached_by_content(tmp_path, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_EMBED_CACHE", str(tmp_path / "cache.json"))
    embedder = StubEmbedder()

    first = cw.embed_all(["alpha", "beta"], embedder=embedder)
    assert set(first) == {"alpha", "beta"}
    assert len(embedder.calls) == 1

    # Re-running the same texts must not call the embedder again.
    again = cw.embed_all(["alpha", "beta"], embedder=embedder)
    assert again == first
    assert len(embedder.calls) == 1

    # A new text embeds only itself.
    cw.embed_all(["alpha", "gamma"], embedder=embedder)
    assert embedder.calls[-1] == ["gamma"]


def test_a_changed_text_is_re_embedded(tmp_path, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_EMBED_CACHE", str(tmp_path / "cache.json"))
    embedder = StubEmbedder()
    cw.embed_all(["the original"], embedder=embedder)
    cw.embed_all(["the original, edited"], embedder=embedder)
    assert embedder.calls[-1] == ["the original, edited"]


def test_duplicate_texts_are_embedded_once(tmp_path, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_EMBED_CACHE", str(tmp_path / "cache.json"))
    embedder = StubEmbedder()
    cw.embed_all(["same", "same", "other"], embedder=embedder)
    assert sorted(embedder.calls[0]) == ["other", "same"]


def test_a_corrupt_cache_is_rebuilt_not_fatal(tmp_path, monkeypatch):
    path = tmp_path / "cache.json"
    path.write_text("{not json")
    monkeypatch.setenv("DILIGENCE_KERNEL_EMBED_CACHE", str(path))
    embedder = StubEmbedder()
    assert cw.embed_all(["alpha"], embedder=embedder)


def test_rank_returns_best_first_and_applies_the_threshold():
    columns = [
        {"table": "01", "name": "Near", "text": "near"},
        {"table": "02", "name": "Far", "text": "far"},
    ]
    vectors = {"probe": [1.0, 0.0], "near": [0.99, 0.14], "far": [0.0, 1.0]}
    matches = cw.rank(vectors["probe"], columns, vectors, top=3, threshold=0.4)
    assert [m.column for m in matches] == ["Near"], "Far is below the threshold"
    assert matches[0].score > 0.9

    loose = cw.rank(vectors["probe"], columns, vectors, top=3, threshold=0.0)
    assert [m.column for m in loose] == ["Near", "Far"], "best first"


def test_a_column_with_no_vector_is_skipped_not_scored_zero():
    columns = [{"table": "01", "name": "Missing", "text": "never embedded"}]
    assert cw.rank([1.0, 0.0], columns, {}, threshold=0.0) == []


def test_column_text_carries_the_purpose_sentence():
    """A name like `Evidence Basis` says little; the corpus writes a purpose for each column."""
    text = cw.column_text("Evidence Basis", "how the coverage was evidenced.", "20 Insurance")
    assert "Evidence Basis" in text
    assert "20 Insurance" in text
    assert "how the coverage was evidenced" in text
    assert cw.column_text("Bare", None, "01 Contracts").endswith("in 01 Contracts")


def test_the_coverage_threshold_sits_below_the_calibrated_minimum():
    """0.48 was the lowest score on a pair confirmed by reading the corpus."""
    assert cw.COVERED_AT < 0.48, "a covered concept must not be reported as a gap"
    assert cw.DEFAULT_THRESHOLD <= cw.COVERED_AT


def test_field_result_reports_coverage_by_layer():
    extraction = cw.FieldResult("3.4.1", "governing law", "extraction")
    assert not extraction.covered, "an extraction field with no match is not covered"
    extraction.matches = [cw.Match("01", "Governing Law", 0.9)]
    assert extraction.covered

    # 00a answers these outside the extraction columns by design.
    for layer in ("human", "missing", "synthesis"):
        assert cw.FieldResult("3.4.2", "rate the risk", layer).covered


def test_the_extracted_playbook_is_well_formed():
    """Skipped where the playbook is not checked out: it is a separate private repository."""
    from diligence_kernel import playbook

    path = playbook.fields_path()
    if path is None:
        pytest.skip(f"no playbook checkout; set {playbook.ENV_VAR}")
    payload = json.loads(path.read_text())
    assert len(payload["prompts"]) == 16
    assert sum(len(p["fields"]) for p in payload["prompts"]) == 92
    assert "model-generated" in payload["provenance"], "the provenance caveat travels with the data"
    for p in payload["prompts"]:
        assert p["id"].startswith("3.4.")
        assert p["moves"]
        # The hyphenated line breaks the PDF introduces must have been rejoined.
        assert not any(f.endswith("-") or "- " in f[:40] and "drag- " in f for f in p["fields"])


def test_the_kernel_runs_without_a_playbook_checkout(monkeypatch, tmp_path):
    """The crosswalk is analysis, not runtime: a missing playbook must not raise on import."""
    from diligence_kernel import playbook

    monkeypatch.setenv(playbook.ENV_VAR, str(tmp_path / "nowhere"))
    assert playbook.playbook_dir() is None
    assert playbook.fields_path() is None
    with pytest.raises(FileNotFoundError) as excinfo:
        playbook.require_fields()
    assert playbook.ENV_VAR in str(excinfo.value), "the error says how to point at one"


def test_an_explicit_path_wins_over_the_sibling(monkeypatch, tmp_path):
    from diligence_kernel import playbook

    (tmp_path / playbook.FIELDS_FILE).write_text("{}")
    monkeypatch.setenv(playbook.ENV_VAR, str(tmp_path))
    assert playbook.fields_path() == tmp_path / playbook.FIELDS_FILE
