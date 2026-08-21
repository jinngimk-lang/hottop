from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .intake import CreativeIntent, CreativeStyle, Platform
from .models import PromotionContext

ProjectShape = Literal[
    "consumer-product",
    "software-b2b",
    "entertainment-culture",
    "fashion-beauty-retail",
    "service-local",
    "campaign-idea",
    "generic",
]


class PlatformProfile(BaseModel):
    platform: Platform
    preferred_forms: list[str] = Field(default_factory=list)
    hook_priority: float = Field(ge=0, le=1)
    motion_priority: float = Field(ge=0, le=1)
    evidence_priority: float = Field(ge=0, le=1)
    early_product_bias: float = Field(ge=0, le=1)
    copy_density: Literal["low", "medium", "high"]
    notes: list[str] = Field(default_factory=list)


class StyleProfile(BaseModel):
    style: CreativeStyle
    text_density: Literal["low", "medium", "high"]
    reversal_weight: float = Field(ge=0, le=1)
    punchline_weight: float = Field(ge=0, le=1)
    product_texture_weight: float = Field(ge=0, le=1)
    world_building_weight: float = Field(ge=0, le=1)
    realism_weight: float = Field(ge=0, le=1)
    notes: list[str] = Field(default_factory=list)


class ProjectShapeProfile(BaseModel):
    shape: ProjectShape
    bridge_biases: list[str] = Field(default_factory=list)
    format_biases: list[str] = Field(default_factory=list)
    medium_biases: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class RoutingHints(BaseModel):
    platform: PlatformProfile
    style: StyleProfile
    project_shape: ProjectShapeProfile
    preferred_forms: list[str] = Field(default_factory=list)
    creative_emphasis: list[str] = Field(default_factory=list)
    product_visibility: str


_PLATFORM_PROFILES: dict[Platform, PlatformProfile] = {
    "xiaohongshu": PlatformProfile(
        platform="xiaohongshu",
        preferred_forms=["swipe-reveal", "single-visual-metaphor"],
        hook_priority=0.92,
        motion_priority=0.45,
        evidence_priority=0.35,
        early_product_bias=0.45,
        copy_density="medium",
        notes=["strong cover hook", "3–5 frame carousel when reveal adds value", "save/share motivation"],
    ),
    "douyin": PlatformProfile(
        platform="douyin",
        preferred_forms=["product-as-prop", "four-panel", "swipe-reveal"],
        hook_priority=0.98,
        motion_priority=0.98,
        evidence_priority=0.30,
        early_product_bias=0.62,
        copy_density="low",
        notes=["first-second hook", "fast escalation", "3–8 second beat logic"],
    ),
    "wechat": PlatformProfile(
        platform="wechat",
        preferred_forms=["single-visual-metaphor", "swipe-reveal"],
        hook_priority=0.75,
        motion_priority=0.30,
        evidence_priority=0.45,
        early_product_bias=0.70,
        copy_density="low",
        notes=["one strong visual", "brand clarity", "concise shareable copy"],
    ),
    "weibo": PlatformProfile(
        platform="weibo",
        preferred_forms=["single-visual-metaphor", "four-panel"],
        hook_priority=0.90,
        motion_priority=0.35,
        evidence_priority=0.42,
        early_product_bias=0.55,
        copy_density="low",
        notes=["fast topical recognition", "one-line punchline"],
    ),
    "instagram": PlatformProfile(
        platform="instagram",
        preferred_forms=["single-visual-metaphor", "swipe-reveal", "product-as-prop"],
        hook_priority=0.90,
        motion_priority=0.65,
        evidence_priority=0.30,
        early_product_bias=0.50,
        copy_density="low",
        notes=["strong art direction", "minimal copy", "carousel/reel friendly"],
    ),
    "x": PlatformProfile(
        platform="x",
        preferred_forms=["single-visual-metaphor", "four-panel"],
        hook_priority=0.91,
        motion_priority=0.25,
        evidence_priority=0.55,
        early_product_bias=0.52,
        copy_density="low",
        notes=["fast recognition", "short punchline/thread compatibility"],
    ),
    "linkedin": PlatformProfile(
        platform="linkedin",
        preferred_forms=["split-old-vs-new", "single-visual-metaphor"],
        hook_priority=0.70,
        motion_priority=0.20,
        evidence_priority=0.92,
        early_product_bias=0.70,
        copy_density="medium",
        notes=["professional tension", "category insight", "evidence-aware reframe"],
    ),
    "paid-social": PlatformProfile(
        platform="paid-social",
        preferred_forms=["single-visual-metaphor", "product-as-prop", "split-old-vs-new"],
        hook_priority=0.94,
        motion_priority=0.70,
        evidence_priority=0.65,
        early_product_bias=0.95,
        copy_density="low",
        notes=["brand attribution", "conversion clarity", "do not hide product too long"],
    ),
    "generic-social": PlatformProfile(
        platform="generic-social",
        preferred_forms=["single-visual-metaphor", "swipe-reveal", "four-panel"],
        hook_priority=0.82,
        motion_priority=0.50,
        evidence_priority=0.50,
        early_product_bias=0.60,
        copy_density="low",
        notes=["portable social grammar"],
    ),
    "auto": PlatformProfile(
        platform="auto",
        preferred_forms=["single-visual-metaphor", "swipe-reveal", "four-panel"],
        hook_priority=0.80,
        motion_priority=0.45,
        evidence_priority=0.50,
        early_product_bias=0.58,
        copy_density="low",
        notes=["preserve platform switchability"],
    ),
}

_STYLE_PROFILES: dict[CreativeStyle, StyleProfile] = {
    "funny-meme": StyleProfile(
        style="funny-meme",
        text_density="medium",
        reversal_weight=0.95,
        punchline_weight=0.98,
        product_texture_weight=0.40,
        world_building_weight=0.35,
        realism_weight=0.45,
        notes=["recognition + reversal", "escalation", "product-specific punchline"],
    ),
    "minimal-premium": StyleProfile(
        style="minimal-premium",
        text_density="low",
        reversal_weight=0.45,
        punchline_weight=0.35,
        product_texture_weight=0.82,
        world_building_weight=0.40,
        realism_weight=0.82,
        notes=["one dominant object", "negative space", "single strong metaphor"],
    ),
    "cinematic": StyleProfile(
        style="cinematic",
        text_density="low",
        reversal_weight=0.58,
        punchline_weight=0.40,
        product_texture_weight=0.62,
        world_building_weight=0.98,
        realism_weight=0.92,
        notes=["camera language", "dramatic reveal", "material realism"],
    ),
    "animation-native": StyleProfile(
        style="animation-native",
        text_density="low",
        reversal_weight=0.72,
        punchline_weight=0.62,
        product_texture_weight=0.52,
        world_building_weight=0.88,
        realism_weight=0.20,
        notes=["stylized motion", "transformation", "animation-native timing"],
    ),
    "documentary-real": StyleProfile(
        style="documentary-real",
        text_density="low",
        reversal_weight=0.38,
        punchline_weight=0.30,
        product_texture_weight=0.45,
        world_building_weight=0.35,
        realism_weight=0.99,
        notes=["credible behavior", "observational framing", "low artifice"],
    ),
    "social-native": StyleProfile(
        style="social-native",
        text_density="medium",
        reversal_weight=0.72,
        punchline_weight=0.70,
        product_texture_weight=0.48,
        world_building_weight=0.35,
        realism_weight=0.68,
        notes=["scroll-stop hook", "creator/social rhythm", "compact overlays"],
    ),
    "commercial-product": StyleProfile(
        style="commercial-product",
        text_density="low",
        reversal_weight=0.48,
        punchline_weight=0.35,
        product_texture_weight=0.99,
        world_building_weight=0.45,
        realism_weight=0.92,
        notes=["material and texture", "sensory cues", "product-led metaphor"],
    ),
    "auto": StyleProfile(
        style="auto",
        text_density="low",
        reversal_weight=0.55,
        punchline_weight=0.55,
        product_texture_weight=0.55,
        world_building_weight=0.50,
        realism_weight=0.60,
        notes=["defer to hotspot medium and product shape"],
    ),
}


def get_platform_profile(platform: Platform) -> PlatformProfile:
    return _PLATFORM_PROFILES[platform]


def get_style_profile(style: CreativeStyle) -> StyleProfile:
    return _STYLE_PROFILES[style]


def infer_project_shape(category: str) -> ProjectShapeProfile:
    normalized = category.strip().lower()
    if any(term in normalized for term in ("food", "beverage", "consumer", "餐饮", "食品", "饮料")):
        return ProjectShapeProfile(
            shape="consumer-product",
            bridge_biases=["shape-material", "action-motion", "emotion-ritual"],
            format_biases=["swipe-reveal", "single-visual-metaphor", "product-as-prop"],
            medium_biases=["commercial-product", "social-native"],
            notes=["sensory and physical product truth first"],
        )
    if any(term in normalized for term in ("software", "saas", "ai", "technology", "软件", "工具")):
        return ProjectShapeProfile(
            shape="software-b2b",
            bridge_biases=["function", "role", "language-symbol"],
            format_biases=["split-old-vs-new", "single-visual-metaphor", "four-panel"],
            medium_biases=["technology-realism", "internet-native"],
            notes=["workflow pain and category-default deletion"],
        )
    if any(term in normalized for term in ("film", "movie", "animation", "entertainment", "电影", "动画", "娱乐")):
        return ProjectShapeProfile(
            shape="entertainment-culture",
            bridge_biases=["role", "action-motion", "language-symbol"],
            format_biases=["faux-film-still", "four-panel", "single-visual-metaphor"],
            medium_biases=["live-action-cinematic", "animation-2d", "animation-3d"],
            notes=["source-medium recognition without protected assets"],
        )
    if any(term in normalized for term in ("fashion", "beauty", "retail", "cosmetic", "时尚", "美妆", "零售")):
        return ProjectShapeProfile(
            shape="fashion-beauty-retail",
            bridge_biases=["shape-material", "emotion-ritual", "language-symbol"],
            format_biases=["single-visual-metaphor", "swipe-reveal", "product-as-prop"],
            medium_biases=["commercial-product", "social-native"],
            notes=["visual ownership and platform-native polish"],
        )
    if any(term in normalized for term in ("service", "restaurant", "local", "服务", "门店", "本地")):
        return ProjectShapeProfile(
            shape="service-local",
            bridge_biases=["emotion-ritual", "function", "role"],
            format_biases=["single-visual-metaphor", "four-panel"],
            medium_biases=["documentary-social", "commercial-product"],
            notes=["real-world ritual and credible outcome"],
        )
    if any(term in normalized for term in ("campaign", "idea", "keyword", "概念", "活动", "关键词")):
        return ProjectShapeProfile(
            shape="campaign-idea",
            bridge_biases=["language-symbol", "role", "function"],
            format_biases=["single-visual-metaphor", "split-old-vs-new"],
            medium_biases=["internet-native", "documentary-social"],
            notes=["semantic and symbolic decoding"],
        )
    return ProjectShapeProfile(
        shape="generic",
        bridge_biases=["function", "action-motion", "language-symbol"],
        format_biases=["single-visual-metaphor", "swipe-reveal", "four-panel"],
        medium_biases=["internet-native"],
        notes=["use subject semantics and hotspot grammar"],
    )


def derive_routing_hints(intent: CreativeIntent, promotion_context: PromotionContext) -> RoutingHints:
    platform = get_platform_profile(intent.platform.value)
    style = get_style_profile(intent.style.value)
    project_shape = infer_project_shape(promotion_context.category)
    preferred_forms = list(dict.fromkeys(platform.preferred_forms + project_shape.format_biases))
    emphasis = list(project_shape.notes)
    if intent.creative_ambition.value == "category-breaking":
        emphasis.extend(["constraint deletion", "new competition axis", "old premise as antagonist"])
    elif intent.creative_ambition.value == "breakout":
        emphasis.extend(["surprising bridge", "ownability", "strong reveal mechanics"])
    elif intent.creative_ambition.value == "witty":
        emphasis.extend(["recognition + reversal", "concise delight"])
    else:
        emphasis.extend(["clarity", "low-risk recognition"])
    if style.punchline_weight >= 0.7:
        emphasis.append("punchline")
    if style.product_texture_weight >= 0.8:
        emphasis.append("product texture")
    return RoutingHints(
        platform=platform,
        style=style,
        project_shape=project_shape,
        preferred_forms=preferred_forms,
        creative_emphasis=list(dict.fromkeys(emphasis)),
        product_visibility=intent.product_visibility.value,
    )
