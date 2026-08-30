from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, field_validator

HASH_CHUNK_BYTES = 1024 * 1024


def _normalize_json_profile(
    value: dict[str, Any] | None,
    *,
    field_name: str,
) -> dict[str, Any] | None:
    if value is None:
        return None
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    normalized: dict[str, Any] = {}
    for key, item in value.items():
        normalized_key = key.strip()
        if not normalized_key:
            raise ValueError(f"{field_name} keys must not be blank")
        if normalized_key in normalized:
            raise ValueError(f"{field_name} keys must be unique after trimming")
        normalized[normalized_key] = item
    try:
        json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{field_name} must contain finite JSON-serializable values"
        ) from exc
    return normalized


def _generation_protocol_blockers(profile: dict[str, Any]) -> list[str]:
    blockers: list[str] = []

    seed = profile.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        blockers.append("generation_protocol seed must be an integer")

    max_new_tokens = profile.get("max_new_tokens")
    if (
        isinstance(max_new_tokens, bool)
        or not isinstance(max_new_tokens, int)
        or max_new_tokens <= 0
    ):
        blockers.append(
            "generation_protocol generation ceiling requires positive integer max_new_tokens"
        )

    sampling_keys = ("temperature", "top_p", "top_k", "sampling_mode")
    if not any(key in profile for key in sampling_keys):
        blockers.append(
            "generation_protocol requires at least one explicit sampling control: "
            "temperature, top_p, top_k or sampling_mode"
        )

    if "temperature" in profile:
        temperature = profile["temperature"]
        if (
            isinstance(temperature, bool)
            or not isinstance(temperature, (int, float))
            or not math.isfinite(float(temperature))
            or temperature < 0
        ):
            blockers.append(
                "generation_protocol temperature must be a finite number greater than or equal to zero"
            )

    if "top_p" in profile:
        top_p = profile["top_p"]
        if (
            isinstance(top_p, bool)
            or not isinstance(top_p, (int, float))
            or not math.isfinite(float(top_p))
            or not 0 < top_p <= 1
        ):
            blockers.append("generation_protocol top_p must be a finite number in (0, 1]")

    if "top_k" in profile:
        top_k = profile["top_k"]
        if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k <= 0:
            blockers.append("generation_protocol top_k must be a positive integer")

    if "sampling_mode" in profile:
        sampling_mode = profile["sampling_mode"]
        if not isinstance(sampling_mode, str) or not sampling_mode.strip():
            blockers.append("generation_protocol sampling_mode must be a nonblank string")

    return blockers


def _hardware_profile_blockers(profile: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    backend = profile.get("backend")
    if not isinstance(backend, str) or not backend.strip():
        blockers.append("hardware_profile backend must be a nonblank string")
        backend_name = None
    else:
        backend_name = backend.strip().lower()

    cpu = profile.get("cpu")
    gpu = profile.get("gpu")
    accelerator = profile.get("accelerator")
    has_cpu_identity = isinstance(cpu, str) and bool(cpu.strip())
    has_gpu_identity = isinstance(gpu, str) and bool(gpu.strip())
    has_accelerator_identity = isinstance(accelerator, str) and bool(accelerator.strip())
    if not (has_cpu_identity or has_gpu_identity or has_accelerator_identity):
        blockers.append(
            "hardware_profile device identity requires a nonblank cpu, gpu or accelerator"
        )

    if backend_name == "cpu":
        if not has_cpu_identity:
            blockers.append("hardware_profile cpu backend requires a nonblank cpu identity")
        logical_cpu_count = profile.get("logical_cpu_count")
        if (
            isinstance(logical_cpu_count, bool)
            or not isinstance(logical_cpu_count, int)
            or logical_cpu_count <= 0
        ):
            blockers.append(
                "hardware_profile cpu backend requires positive integer logical_cpu_count"
            )

    accelerator_backends = {"cuda", "rocm", "hip", "vulkan", "metal", "mps", "xpu"}
    if (
        backend_name in accelerator_backends
        and not has_gpu_identity
        and not has_accelerator_identity
    ):
        blockers.append(
            f"hardware_profile {backend_name} backend requires a nonblank gpu or accelerator identity"
        )
    return blockers


def _execution_profile_blockers(profile: dict[str, Any]) -> list[str]:
    blockers: list[str] = []

    mode = profile.get("mode")
    if not isinstance(mode, str) or not mode.strip():
        blockers.append("execution_profile mode must be a nonblank string")
        mode_name = None
    else:
        mode_name = mode.strip().lower()
        if mode_name not in {"cli", "server"}:
            blockers.append("execution_profile mode must be cli or server")

    for field_name in ("concurrency", "batch_size"):
        value = profile.get(field_name)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            blockers.append(f"execution_profile {field_name} must be a positive integer")

    if mode_name == "server":
        connection_strategy = profile.get("connection_strategy")
        if not isinstance(connection_strategy, str) or not connection_strategy.strip():
            blockers.append(
                "execution_profile server mode requires a nonblank connection_strategy"
            )
        for field_name in ("worker_count", "threads_per_worker"):
            value = profile.get(field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                blockers.append(
                    f"execution_profile server mode requires positive integer {field_name}"
                )

    return blockers


class TtsBenchmarkTrialInput(BaseModel):
    candidate: str
    run_kind: Literal["cold", "warm"]
    wav: str
    latency_seconds: float
    runtime_revision: str
    model_revision: str

    @field_validator("candidate", "wav", "runtime_revision", "model_revision")
    @classmethod
    def _nonblank_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must not be blank")
        return normalized


class TtsBenchmarkInput(BaseModel):
    schema_version: Literal["hottop.tts-benchmark-input.v1"]
    text: str
    language: str
    speaker: str
    generation_protocol: dict[str, Any] | None = None
    hardware_profile: dict[str, Any] | None = None
    execution_profile: dict[str, Any] | None = None
    trials: list[TtsBenchmarkTrialInput]

    @field_validator("text", "language", "speaker")
    @classmethod
    def _nonblank_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must not be blank")
        return normalized

    @field_validator("generation_protocol")
    @classmethod
    def _valid_generation_protocol(
        cls, value: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        return _normalize_json_profile(value, field_name="generation_protocol")

    @field_validator("hardware_profile")
    @classmethod
    def _valid_hardware_profile(
        cls, value: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        return _normalize_json_profile(value, field_name="hardware_profile")

    @field_validator("execution_profile")
    @classmethod
    def _valid_execution_profile(
        cls, value: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        return _normalize_json_profile(value, field_name="execution_profile")


class WavArtifactIdentity(BaseModel):
    path: str
    size_bytes: int
    sha256: str
    duration_seconds: float
    sample_rate: int
    channels: int
    sample_width_bytes: int
    frame_count: int


class TtsBenchmarkTrialEvidence(BaseModel):
    candidate: str
    run_kind: Literal["cold", "warm"]
    runtime_revision: str
    model_revision: str
    latency_seconds: float
    realtime_factor: float | None = None
    realtime_speedup: float | None = None
    wav: WavArtifactIdentity | None = None
    blockers: list[str]


class TtsBenchmarkEvidence(BaseModel):
    schema_version: Literal["hottop.tts-benchmark.v1"] = "hottop.tts-benchmark.v1"
    ready: bool
    executed: Literal[False] = False
    network_access: Literal[False] = False
    auto_download: Literal[False] = False
    listening_required: Literal[True] = True
    text: str
    language: str
    speaker: str
    generation_protocol: dict[str, Any] | None = None
    generation_protocol_sha256: str | None = None
    hardware_profile: dict[str, Any] | None = None
    hardware_profile_sha256: str | None = None
    execution_profile: dict[str, Any] | None = None
    execution_profile_sha256: str | None = None
    trials: list[TtsBenchmarkTrialEvidence]
    blockers: list[str]


def _snapshot_signature(path: Path) -> tuple[int, int, int, int, int, int]:
    stat = path.stat()
    return (
        stat.st_dev,
        stat.st_ino,
        stat.st_size,
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        stat.st_mode,
    )


def _stream_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(HASH_CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json_sha256(profile: dict[str, Any]) -> str:
    canonical = json.dumps(
        profile,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _pcm_has_signal(raw: bytes, *, sample_width: int) -> bool:
    if sample_width == 1:
        return any(sample != 128 for sample in raw)
    return any(byte != 0 for byte in raw)


def _inspect_wav(path: Path) -> tuple[WavArtifactIdentity | None, list[str]]:
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        return None, [f"WAV does not exist: {path}"]
    except OSError:
        return None, [f"WAV could not be resolved: {path}"]

    if not resolved.is_file():
        return None, [f"WAV is not a file: {path}"]

    try:
        snapshot_before = _snapshot_signature(resolved)
    except OSError:
        return None, [f"WAV could not be inspected: {path}"]

    size_bytes = snapshot_before[2]
    if size_bytes <= 0:
        return None, [f"WAV is empty: {path}"]

    blockers: list[str] = []
    try:
        sha256 = _stream_sha256(resolved)
        with wave.open(str(resolved), "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frame_count = wav.getnframes()
            has_signal = False
            while remaining := wav.getnframes() - wav.tell():
                raw = wav.readframes(min(remaining, 16384))
                if _pcm_has_signal(raw, sample_width=sample_width):
                    has_signal = True
        snapshot_after = _snapshot_signature(resolved)
    except (OSError, EOFError, wave.Error):
        return None, [f"WAV is not a readable PCM wave file: {path}"]

    if snapshot_before != snapshot_after:
        return None, [f"WAV changed during benchmark inspection: {path}"]
    if channels <= 0 or sample_rate <= 0 or sample_width <= 0 or frame_count <= 0:
        blockers.append(f"WAV has invalid stream structure: {path}")
    if not has_signal:
        blockers.append(f"WAV contains digital silence: {path}")

    duration_seconds = frame_count / sample_rate if sample_rate > 0 else 0.0
    identity = WavArtifactIdentity(
        path=str(resolved),
        size_bytes=size_bytes,
        sha256=sha256,
        duration_seconds=duration_seconds,
        sample_rate=sample_rate,
        channels=channels,
        sample_width_bytes=sample_width,
        frame_count=frame_count,
    )
    return identity, blockers


def inspect_tts_benchmark(spec_path: Path) -> TtsBenchmarkEvidence:
    """Inspect operator-produced local TTS WAV evidence without executing any runtime."""

    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    spec = TtsBenchmarkInput.model_validate(payload)
    trial_evidence: list[TtsBenchmarkTrialEvidence] = []
    blockers: list[str] = []
    seen_wav_paths: dict[str, int] = {}
    run_kinds_by_candidate: dict[str, set[str]] = {}
    runtime_revisions_by_candidate: dict[str, set[str]] = {}
    model_revisions_by_candidate: dict[str, set[str]] = {}

    generation_protocol_sha256 = None
    if spec.generation_protocol is None:
        blockers.append(
            "benchmark requires generation_protocol to bind seed, sampling and generation ceiling"
        )
    else:
        blockers.extend(_generation_protocol_blockers(spec.generation_protocol))
        generation_protocol_sha256 = _canonical_json_sha256(spec.generation_protocol)

    hardware_profile_sha256 = None
    if spec.hardware_profile is None:
        blockers.append(
            "benchmark requires hardware_profile to bind the latency/RTF measurement environment"
        )
    else:
        blockers.extend(_hardware_profile_blockers(spec.hardware_profile))
        hardware_profile_sha256 = _canonical_json_sha256(spec.hardware_profile)

    execution_profile_sha256 = None
    if spec.execution_profile is None:
        blockers.append(
            "benchmark requires execution_profile to bind mode, concurrency and batch size"
        )
    else:
        blockers.extend(_execution_profile_blockers(spec.execution_profile))
        execution_profile_sha256 = _canonical_json_sha256(spec.execution_profile)

    for index, trial in enumerate(spec.trials):
        run_kinds_by_candidate.setdefault(trial.candidate, set()).add(trial.run_kind)
        runtime_revisions_by_candidate.setdefault(trial.candidate, set()).add(
            trial.runtime_revision
        )
        model_revisions_by_candidate.setdefault(trial.candidate, set()).add(
            trial.model_revision
        )
        wav_path = Path(trial.wav)
        if not wav_path.is_absolute():
            wav_path = spec_path.parent / wav_path
        wav_identity, trial_blockers = _inspect_wav(wav_path)
        if wav_identity is not None:
            previous_trial = seen_wav_paths.get(wav_identity.path)
            if previous_trial is not None:
                trial_blockers.append(
                    "resolved WAV path is reused across trials: "
                    f"trial {previous_trial} and trial {index}: {wav_identity.path}"
                )
            else:
                seen_wav_paths[wav_identity.path] = index

        latency_is_valid = math.isfinite(trial.latency_seconds) and trial.latency_seconds > 0
        if not latency_is_valid:
            trial_blockers.append(
                f"trial {index} latency_seconds must be greater than zero and finite"
            )

        realtime_factor = None
        realtime_speedup = None
        if (
            wav_identity is not None
            and wav_identity.duration_seconds > 0
            and latency_is_valid
        ):
            realtime_factor = trial.latency_seconds / wav_identity.duration_seconds
            realtime_speedup = wav_identity.duration_seconds / trial.latency_seconds

        blockers.extend(f"trial {index}: {blocker}" for blocker in trial_blockers)
        trial_evidence.append(
            TtsBenchmarkTrialEvidence(
                candidate=trial.candidate,
                run_kind=trial.run_kind,
                runtime_revision=trial.runtime_revision,
                model_revision=trial.model_revision,
                latency_seconds=trial.latency_seconds,
                realtime_factor=realtime_factor,
                realtime_speedup=realtime_speedup,
                wav=wav_identity,
                blockers=trial_blockers,
            )
        )

    if not trial_evidence:
        blockers.append("benchmark requires at least one trial")

    required_run_kinds = {"cold", "warm"}
    for candidate, run_kinds in run_kinds_by_candidate.items():
        missing = sorted(required_run_kinds - run_kinds)
        if missing:
            blockers.append(
                f"candidate {candidate} requires both cold and warm trials; missing "
                + ", ".join(missing)
            )

    for candidate, runtime_revisions in runtime_revisions_by_candidate.items():
        if len(runtime_revisions) > 1:
            blockers.append(
                f"candidate {candidate} mixes runtime revisions: "
                + ", ".join(sorted(runtime_revisions))
            )

    for candidate, model_revisions in model_revisions_by_candidate.items():
        if len(model_revisions) > 1:
            blockers.append(
                f"candidate {candidate} mixes model revisions: "
                + ", ".join(sorted(model_revisions))
            )

    return TtsBenchmarkEvidence(
        ready=not blockers,
        text=spec.text,
        language=spec.language,
        speaker=spec.speaker,
        generation_protocol=spec.generation_protocol,
        generation_protocol_sha256=generation_protocol_sha256,
        hardware_profile=spec.hardware_profile,
        hardware_profile_sha256=hardware_profile_sha256,
        execution_profile=spec.execution_profile,
        execution_profile_sha256=execution_profile_sha256,
        trials=trial_evidence,
        blockers=blockers,
    )