from __future__ import annotations

import re
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field, field_validator

IntentSource = Literal["explicit", "inferred", "defaulted"]
CampaignGoal = Literal[
    "awareness",
    "pain-point-contrast",
    "product-launch",
    "conversion",
    "brand-memory",
    "hotspot-participation",
    "category-reframe",
    "auto",
]
Platform = Literal[
    "xiaohongshu",
    "douyin",
    "wechat",
    "weibo",
    "instagram",
    "x",
    "linkedin",
    "paid-social",
    "generic-social",
    "auto",
]
CreativeStyle = Literal[
    "funny-meme",
    "minimal-premium",
    "cinematic",
    "animation-native",
    "documentary-real",
    "social-native",
    "commercial-product",
    "auto",
]
CreativeAmbition = Literal["safe", "witty", "breakout", "category-breaking"]
ProductVisibility = Literal["metaphor-first", "balanced", "product-first"]
HotspotPreference = Literal[
    "film",
    "animation",
    "tech",
    "internet",
    "social",
    "consumer",
    "native-meme",
    "current-best",
    "auto",
]

T = TypeVar("T")


class IntentValue(BaseModel, Generic[T]):
    value: T
    source: IntentSource
    confidence: float = Field(ge=0, le=1)


class CreativeIntent(BaseModel):
    request: str = Field(min_length=1)
    promotion_target: IntentValue[str | None]
    campaign_goal: IntentValue[CampaignGoal]
    platform: IntentValue[Platform]
    style: IntentValue[CreativeStyle]
    creative_ambition: IntentValue[CreativeAmbition]
    product_visibility: IntentValue[ProductVisibility]
    audience: IntentValue[str | None]
    hotspot_preference: IntentValue[HotspotPreference]
    constraints: list[str] = Field(default_factory=list)

    @field_validator("promotion_target")
    @classmethod
    def normalize_promotion_target(cls, target: IntentValue[str | None]) -> IntentValue[str | None]:
        if target.value is None:
            return target
        normalized = target.value.strip()
        if normalized == target.value:
            return target
        return target.model_copy(update={"value": normalized})


class GuidedQuestion(BaseModel):
    field: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    options: list[str] = Field(default_factory=list, max_length=6)
    allow_free_text: bool = True


class InteractionState(BaseModel):
    ready_to_create: bool
    question: GuidedQuestion | None = None
    missing_high_impact_fields: list[str] = Field(default_factory=list)
    asked_fields: list[str] = Field(default_factory=list)
    question_budget_remaining: int = Field(ge=0, le=3)


def _default(value: T) -> IntentValue[T]:
    return IntentValue(value=value, source="defaulted", confidence=0.0)


def _inferred(value: T, confidence: float) -> IntentValue[T]:
    return IntentValue(value=value, source="inferred", confidence=confidence)


def _explicit(value: T) -> IntentValue[T]:
    return IntentValue(value=value, source="explicit", confidence=1.0)


def _infer_target(request: str) -> IntentValue[str | None]:
    patterns = [
        r"给(?P<target>.+?)做(?:一个|一版|一张|一下|个)",
        r"(?:宣传|推广)(?:一下)?(?P<target>.+?)(?:，|,|。|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, request)
        if match:
            target = match.group("target").strip(" ：:，,。")
            if target:
                return _inferred(target, 0.78)
    return _default(None)


def _infer_platform(text: str) -> IntentValue[Platform]:
    mapping: list[tuple[tuple[str, ...], Platform, float]] = [
        (("小红书", "xiaohongshu", "rednote"), "xiaohongshu", 0.98),
        (("抖音", "douyin", "tiktok china"), "douyin", 0.98),
        (("朋友圈", "微信", "wechat"), "wechat", 0.92),
        (("微博", "weibo"), "weibo", 0.98),
        (("instagram", " ins ", " ig "), "instagram", 0.95),
        (("linkedin", "领英"), "linkedin", 0.98),
        (("付费投放", "广告投放", "paid social"), "paid-social", 0.92),
    ]
    lowered = f" {text.lower()} "
    for terms, value, confidence in mapping:
        if any(term in lowered for term in terms):
            return _inferred(value, confidence)
    if re.search(r"(^|\s)x($|\s)|twitter", lowered):
        return _inferred("x", 0.88)
    return _default("auto")


def _infer_style(text: str) -> IntentValue[CreativeStyle]:
    lowered = text.lower()
    rules: list[tuple[tuple[str, ...], CreativeStyle, float]] = [
        (("高级", "极简", "premium", "minimal"), "minimal-premium", 0.86),
        (("搞笑", "有梗", "梗图", "meme", "funny"), "funny-meme", 0.90),
        (("动画", "anime", "卡通", "二次元"), "animation-native", 0.90),
        (("纪实", "真实生活", "documentary"), "documentary-real", 0.88),
        (("社媒感", "原生社媒", "social-native"), "social-native", 0.86),
        (("商业广告", "产品摄影", "commercial product"), "commercial-product", 0.86),
        (("电影感", "大片感", "cinematic"), "cinematic", 0.92),
    ]
    for terms, value, confidence in rules:
        if any(term in lowered for term in terms):
            return _inferred(value, confidence)
    return _default("auto")


def _infer_ambition(text: str) -> IntentValue[CreativeAmbition]:
    lowered = text.lower()
    if any(
        term in lowered
        for term in ("打破类目", "破框", "颠覆", "重构旧范式", "constraint deletion", "category reframe")
    ):
        return _inferred("category-breaking", 0.95)
    if any(term in lowered for term in ("出圈", "爆点", "强记忆", "breakout")):
        return _inferred("breakout", 0.92)
    if any(term in lowered for term in ("稳妥", "保守", "safe")):
        return _inferred("safe", 0.90)
    if any(term in lowered for term in ("有梗", "好玩", "witty")):
        return _inferred("witty", 0.86)
    return _default("witty")


def _infer_visibility(text: str) -> IntentValue[ProductVisibility]:
    lowered = text.lower()
    if any(
        term in lowered
        for term in (
            "别一上来全露",
            "最后再揭示",
            "最后揭示",
            "延迟揭示",
            "先别露产品",
            "metaphor-first",
            "reveal",
        )
    ):
        return _inferred("metaphor-first", 0.93)
    if any(term in lowered for term in ("产品优先", "一开始就露", "先露产品", "product-first")):
        return _inferred("product-first", 0.92)
    return _default("balanced")


def _infer_hotspot(text: str) -> IntentValue[HotspotPreference]:
    lowered = text.lower()
    rules: list[tuple[tuple[str, ...], HotspotPreference, float]] = [
        (("电影", "film", "movie", "cinema"), "film", 0.94),
        (("动漫", "动画热点", "anime", "animation"), "animation", 0.94),
        (("科技", "ai热点", "tech"), "tech", 0.88),
        (("网络热点", "互联网热点", "internet"), "internet", 0.86),
        (("社会话题", "社会热点", "social"), "social", 0.86),
        (("消费", "餐饮热点", "consumer"), "consumer", 0.82),
        (("原生梗", "native meme"), "native-meme", 0.88),
        (("今天最适合", "当前最好", "current best"), "current-best", 0.84),
    ]
    for terms, value, confidence in rules:
        if any(term in lowered for term in terms):
            return _inferred(value, confidence)
    return _default("auto")


def _infer_goal(text: str) -> IntentValue[CampaignGoal]:
    lowered = text.lower()
    if any(term in lowered for term in ("破框", "重构", "旧范式", "category reframe")):
        return _inferred("category-reframe", 0.90)
    if any(term in lowered for term in ("转化", "下单", "购买", "conversion")):
        return _inferred("conversion", 0.90)
    if any(term in lowered for term in ("品牌心智", "记住品牌", "brand memory")):
        return _inferred("brand-memory", 0.88)
    if any(term in lowered for term in ("痛点", "旧方案", "竞品对比")):
        return _inferred("pain-point-contrast", 0.84)
    if any(term in lowered for term in ("新品", "发布", "launch")):
        return _inferred("product-launch", 0.78)
    if any(term in lowered for term in ("热点", "联动", "蹭热点")):
        return _inferred("hotspot-participation", 0.82)
    return _default("auto")


def resolve_intent(request: str, overrides: dict[str, object] | None = None) -> CreativeIntent:
    request = request.strip()
    if not request:
        raise ValueError("request must not be blank")

    inferred = CreativeIntent(
        request=request,
        promotion_target=_infer_target(request),
        campaign_goal=_infer_goal(request),
        platform=_infer_platform(request),
        style=_infer_style(request),
        creative_ambition=_infer_ambition(request),
        product_visibility=_infer_visibility(request),
        audience=_default(None),
        hotspot_preference=_infer_hotspot(request),
        constraints=[],
    )

    if not overrides:
        return inferred

    payload = inferred.model_dump()
    intent_fields = {
        "promotion_target",
        "campaign_goal",
        "platform",
        "style",
        "creative_ambition",
        "product_visibility",
        "audience",
        "hotspot_preference",
    }
    for key, value in overrides.items():
        if key == "constraints":
            payload[key] = list(value) if isinstance(value, (list, tuple, set)) else [str(value)]
        elif key in intent_fields:
            payload[key] = _explicit(value).model_dump()
    return CreativeIntent.model_validate(payload)


_QUESTION_SPECS: dict[str, GuidedQuestion] = {
    "promotion_target": GuidedQuestion(
        field="promotion_target",
        prompt="这次主要宣传什么？",
        options=["品牌", "产品", "服务", "功能", "活动", "概念/关键词"],
    ),
    "campaign_goal": GuidedQuestion(
        field="campaign_goal",
        prompt="最希望观众记住什么？",
        options=["卖点认知", "痛点破局", "品牌心智", "新品发布", "转化行动", "热点借势"],
    ),
    "platform": GuidedQuestion(
        field="platform",
        prompt="主要发到哪里？",
        options=["小红书", "抖音", "微信", "微博/X", "Instagram", "LinkedIn"],
    ),
    "style": GuidedQuestion(
        field="style",
        prompt="这次更想要哪种感觉？",
        options=["搞笑有梗", "极简高级", "电影大片", "动画脑洞", "真实纪实", "潮流社媒"],
    ),
    "creative_ambition": GuidedQuestion(
        field="creative_ambition",
        prompt="这次想做到多大胆？",
        options=["稳妥传播", "有梗好玩", "强记忆/出圈", "破框重构"],
    ),
    "product_visibility": GuidedQuestion(
        field="product_visibility",
        prompt="产品希望多早出现？",
        options=["隐喻优先", "平衡", "产品优先"],
    ),
}


def _missing_high_impact_fields(intent: CreativeIntent) -> list[str]:
    missing: list[str] = []
    if not intent.promotion_target.value:
        missing.append("promotion_target")
    if intent.campaign_goal.value == "auto":
        missing.append("campaign_goal")
    if intent.platform.value == "auto":
        missing.append("platform")
    if intent.style.value == "auto":
        missing.append("style")
    if intent.creative_ambition.source == "defaulted":
        missing.append("creative_ambition")
    if intent.product_visibility.source == "defaulted" and (
        intent.campaign_goal.value == "conversion" or intent.platform.value == "paid-social"
    ):
        missing.append("product_visibility")
    return missing


def next_question(
    intent: CreativeIntent,
    *,
    asked_fields: list[str] | None = None,
    budget: int = 3,
) -> InteractionState:
    asked = list(dict.fromkeys(asked_fields or []))
    capped_budget = max(0, min(budget, 3))
    remaining = max(0, capped_budget - len(asked))
    missing = [field for field in _missing_high_impact_fields(intent) if field not in asked]

    if remaining == 0 or not missing:
        return InteractionState(
            ready_to_create=True,
            question=None,
            missing_high_impact_fields=missing,
            asked_fields=asked,
            question_budget_remaining=remaining,
        )

    field = missing[0]
    return InteractionState(
        ready_to_create=False,
        question=_QUESTION_SPECS[field],
        missing_high_impact_fields=missing,
        asked_fields=asked,
        question_budget_remaining=remaining - 1,
    )
