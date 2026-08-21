import pytest

from hottop.intake import resolve_intent


def test_blank_request_is_rejected():
    with pytest.raises(ValueError, match="blank"):
        resolve_intent("   ")
