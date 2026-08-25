import pytest

from hottop.models import ComparisonCandidate


def test_comparison_candidate_normalizes_optional_category():
    candidate = ComparisonCandidate(
        name="Named Competitor",
        category="  workflow software  ",
        relation="direct-competitor",
    )

    assert candidate.category == "workflow software"


def test_comparison_candidate_rejects_blank_optional_category():
    with pytest.raises(ValueError, match="comparison candidate category must not be blank"):
        ComparisonCandidate(
            name="Named Competitor",
            category="   ",
            relation="direct-competitor",
        )
