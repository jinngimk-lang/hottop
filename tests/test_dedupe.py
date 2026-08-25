from hottop.dedupe import merge_candidates
from hottop.models import Evidence, TrendCandidate


def test_merge_candidates_combines_same_url_and_cross_source_count():
    a = TrendCandidate(
        id="a",
        title="The Odyssey breaks IMAX record",
        url="https://example.com/story?utm_source=x",
        source="dailyhot",
        evidence=[Evidence(url="https://source-a.test/x", source="a")],
    )
    b = TrendCandidate(
        id="b",
        title="The Odyssey breaks IMAX record",
        url="https://example.com/story",
        source="newsnow",
        evidence=[Evidence(url="https://source-b.test/y", source="b")],
    )
    merged = merge_candidates([a, b])
    assert len(merged) == 1
    assert merged[0].metrics["cross_source_count"] == 2
    assert {e.source for e in merged[0].evidence} == {"a", "b"}


def test_merge_candidates_uses_normalized_title_when_urls_differ():
    a = TrendCandidate(
        id="a",
        title=" Gemini 3.7 Flash：Agent 工作流 ",
        url="https://a.test/1",
        source="a",
    )
    b = TrendCandidate(
        id="b",
        title="gemini 3.7 flash agent 工作流",
        url="https://b.test/2",
        source="b",
    )
    merged = merge_candidates([a, b])
    assert len(merged) == 1
    assert merged[0].metrics["cross_source_count"] == 2
