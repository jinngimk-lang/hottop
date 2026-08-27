from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator

LearningKind = Literal["positive", "negative", "mixed", "packaging"]
ReuseMode = Literal["mechanism_and_grammar_only", "guardrail_only", "packaging_pattern"]
AssetStorage = Literal["metadata_only", "git_lfs", "external_object_store"]


class ReferenceAsset(BaseModel):
    media_type: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    storage: AssetStorage
    source_kind: str = Field(min_length=1)
    rights_mode: str = Field(min_length=1)
    note: str | None = None


class HotspotMemory(BaseModel):
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    recognition_hook: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    mechanism_terms: list[str] = Field(default_factory=list)


class CreativeReference(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    learning_kind: LearningKind
    reuse_mode: ReuseMode
    hotspot: HotspotMemory
    product_bridge: str = ""
    product_role: list[str] = Field(default_factory=list)
    story_outcome_change: str = ""
    visual_grammar: list[str] = Field(default_factory=list)
    dialogue_grammar: list[str] = Field(default_factory=list)
    audio_grammar: list[str] = Field(default_factory=list)
    format_grammar: list[str] = Field(default_factory=list)
    why_it_works: list[str] = Field(default_factory=list)
    user_feedback: list[str] = Field(default_factory=list)
    what_not_to_copy: list[str] = Field(default_factory=list)
    negative_patterns: list[str] = Field(default_factory=list)
    promotion_lessons: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    assets: list[ReferenceAsset] = Field(default_factory=list)

    @model_validator(mode="after")
    def negative_examples_are_guardrails(self) -> CreativeReference:
        if self.learning_kind == "negative" and self.reuse_mode != "guardrail_only":
            raise ValueError("negative creative references must be guardrail_only")
        return self


class CreativeMemoryPolicy(BaseModel):
    store_failures: bool = True
    store_user_feedback: bool = True
    store_platform_performance_when_available: bool = True
    retrieve_before_generation_when_useful: bool = True
    fresh_hotspot_research_still_required: bool = True
    copy_old_visual_templates: bool = False
    third_party_assets_metadata_only_by_default: bool = True


class CreativeReferenceLibrary(BaseModel):
    schema_version: Literal["hottop.creative-reference-library.v1"] = (
        "hottop.creative-reference-library.v1"
    )
    learning_mode: Literal["retrieval_plus_few_shot_preference_memory"] = (
        "retrieval_plus_few_shot_preference_memory"
    )
    reinforcement_learning: bool = False
    policy: CreativeMemoryPolicy
    references: list[CreativeReference]

    @model_validator(mode="after")
    def ids_are_unique(self) -> CreativeReferenceLibrary:
        ids = [item.id for item in self.references]
        if len(ids) != len(set(ids)):
            raise ValueError("creative reference ids must be unique")
        if self.reinforcement_learning:
            raise ValueError("the current reference library is not reinforcement learning")
        if self.policy.copy_old_visual_templates:
            raise ValueError("creative memory must retrieve mechanism/grammar, not copy templates")
        return self


class ReferenceMatch(BaseModel):
    reference: CreativeReference
    score: int = Field(ge=0)
    matched_dimensions: int = Field(ge=0)
    matched_terms: list[str] = Field(default_factory=list)


def load_creative_library(path: Path) -> CreativeReferenceLibrary:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return CreativeReferenceLibrary.model_validate(raw)


def _normalize(values: list[str]) -> set[str]:
    return {value.strip().lower().replace("-", "_").replace(" ", "_") for value in values if value.strip()}


def _match(query: list[str], candidates: list[str]) -> set[str]:
    return _normalize(query) & _normalize(candidates)


def retrieve_references(
    library: CreativeReferenceLibrary,
    *,
    mechanism_terms: list[str] | None = None,
    visual_grammar_terms: list[str] | None = None,
    product_role_terms: list[str] | None = None,
    tag_terms: list[str] | None = None,
    negative_pattern_terms: list[str] | None = None,
    include_negative: bool = False,
    limit: int = 5,
) -> list[ReferenceMatch]:
    """Rank reusable creative memory without turning old cases into templates."""

    mechanism_terms = mechanism_terms or []
    visual_grammar_terms = visual_grammar_terms or []
    product_role_terms = product_role_terms or []
    tag_terms = tag_terms or []
    negative_pattern_terms = negative_pattern_terms or []

    matches: list[ReferenceMatch] = []
    for reference in library.references:
        if reference.learning_kind == "negative" and not include_negative and not negative_pattern_terms:
            continue

        dimension_matches: list[tuple[int, set[str]]] = [
            (4, _match(mechanism_terms, reference.hotspot.mechanism_terms)),
            (3, _match(visual_grammar_terms, reference.visual_grammar)),
            (3, _match(product_role_terms, reference.product_role)),
            (1, _match(tag_terms, reference.tags)),
            (5, _match(negative_pattern_terms, reference.negative_patterns)),
        ]
        matched_sets = [terms for _, terms in dimension_matches if terms]
        score = sum(weight * len(terms) for weight, terms in dimension_matches)

        if score == 0:
            continue

        matches.append(
            ReferenceMatch(
                reference=reference,
                score=score,
                matched_dimensions=len(matched_sets),
                matched_terms=sorted(set().union(*matched_sets)),
            )
        )

    matches.sort(key=lambda item: (-item.score, -item.matched_dimensions, item.reference.id))
    return matches[: max(0, limit)]
