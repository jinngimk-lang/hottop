from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator

ModelStatus = Literal[
    "operator_local_ready",
    "benchmark_ready",
    "benchmark_candidate",
    "interop_only",
    "license_blocked",
    "paid_optional",
]
RuntimeStatus = Literal["unprobed", "operator_provisioned", "not_provisioned", "blocked"]
CostClass = Literal["self_owned_compute", "free_shared_capacity", "paid_service"]


class ModelHubEntry(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    family: str = Field(min_length=1)
    modalities: list[str] = Field(min_length=1)
    capabilities: list[str] = Field(min_length=1)
    repository: str = Field(min_length=1)
    code_license: str = Field(min_length=1)
    weights_license: str = Field(min_length=1)
    status: ModelStatus
    cost_class: CostClass
    integration_ready: bool = False
    runtime_status: RuntimeStatus = "unprobed"
    operator_profiles: list[str] = Field(default_factory=list)
    integration_strategy: str = Field(min_length=1)
    runtime_boundary: str = Field(min_length=1)
    priority: int = Field(default=100, ge=0)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_runtime_truth(self) -> ModelHubEntry:
        if self.status in {"license_blocked", "paid_optional"} and self.integration_ready:
            raise ValueError("blocked or paid-optional entries cannot be integration-ready defaults")
        if self.runtime_status == "operator_provisioned" and not self.integration_ready:
            raise ValueError("operator-provisioned runtime requires an admitted Hottop integration")
        return self


class ModelHubPolicy(BaseModel):
    zero_cost_default: bool = True
    paid_fallback: bool = False
    auto_download_models: bool = False
    auto_install_upstream: bool = False
    vendor_upstream_code: bool = False
    require_code_license: bool = True
    require_weights_license: bool = True


class ModelHub(BaseModel):
    schema_version: Literal["hottop.model-hub.v1"] = "hottop.model-hub.v1"
    policy: ModelHubPolicy
    models: list[ModelHubEntry]

    @model_validator(mode="after")
    def validate_registry(self) -> ModelHub:
        ids = [entry.id for entry in self.models]
        if len(ids) != len(set(ids)):
            raise ValueError("model hub model ids must be unique")
        if not self.policy.zero_cost_default or self.policy.paid_fallback:
            raise ValueError("Hottop model hub must remain zero-cost first with no paid fallback")
        if self.policy.auto_download_models or self.policy.auto_install_upstream:
            raise ValueError("model hub must not auto-download models or auto-install upstream projects")
        return self


def load_model_hub(path: Path) -> ModelHub:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ModelHub.model_validate(raw)


def select_models(
    hub: ModelHub,
    *,
    capability: str | None = None,
    modality: str | None = None,
    operator_profile: str | None = None,
    zero_cost_only: bool = True,
    integration_ready_only: bool = False,
    runtime_ready_only: bool = False,
) -> list[ModelHubEntry]:
    """Return safe candidates without installing, downloading or executing anything."""

    selected: list[ModelHubEntry] = []
    blocked_statuses = {"license_blocked", "paid_optional"}
    for entry in hub.models:
        if capability is not None and capability not in entry.capabilities:
            continue
        if modality is not None and modality not in entry.modalities:
            continue
        if operator_profile is not None and operator_profile not in entry.operator_profiles:
            continue
        if zero_cost_only and entry.cost_class == "paid_service":
            continue
        if integration_ready_only and (
            not entry.integration_ready or entry.status in blocked_statuses
        ):
            continue
        if runtime_ready_only and entry.runtime_status != "operator_provisioned":
            continue
        selected.append(entry)

    return sorted(selected, key=lambda entry: (entry.priority, entry.id))
