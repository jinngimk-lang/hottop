from __future__ import annotations

import re

from .models import ClaimStatus

_QUANTIFIED_PATTERNS = (
    re.compile(r"\b\d+(?:\.\d+)?\s*x\b", re.I),
    re.compile(r"\d+(?:\.\d+)?\s*倍"),
    re.compile(r"\d+(?:\.\d+)?\s*%"),
)
_OBJECTIVE_WORDS = ("更快", "最快", "更便宜", "最低成本", "faster", "cheaper", "fastest")


def classify_claim(text: str, evidence_count: int = 0) -> ClaimStatus:
    has_objective_claim = any(pattern.search(text) for pattern in _QUANTIFIED_PATTERNS) or any(
        token in text.lower() for token in _OBJECTIVE_WORDS
    )
    if not has_objective_claim:
        return "satire"
    return "supported" if evidence_count > 0 else "needs_evidence"
