from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, field_validator

HASH_CHUNK_BYTES = 1024 * 1024


class TtsBenchmarkTrialInput(BaseModel):
    candidate: str
    run_kind: Literal["cold", "warm"]
    wav: str
    latency_seconds: float
    runtime_revision: str

    @field_validator("candidate", "wav", "runtime_revision")
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
    trials: list[TtsBenchmarkTrialInput]

    @field_validator("text", "language", "speaker")
    @classmethod
    def _nonblank_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must not be blank")
        return normalized


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

    for index, trial in enumerate(spec.trials):
        wav_path = Path(trial.wav)
        if not wav_path.is_absolute():
            wav_path = spec_path.parent / wav_path
        wav_identity, trial_blockers = _inspect_wav(wav_path)
        latency_is_valid = math.isfinite(trial.latency_seconds) and trial.latency_seconds > 0
        if not latency_is_valid:
            trial_blockers.append(
                f"trial {index} latency_seconds must be finite and greater than zero"
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
                latency_seconds=trial.latency_seconds,
                realtime_factor=realtime_factor,
                realtime_speedup=realtime_speedup,
                wav=wav_identity,
                blockers=trial_blockers,
            )
        )

    if not trial_evidence:
        blockers.append("benchmark requires at least one trial")

    return TtsBenchmarkEvidence(
        ready=not blockers,
        text=spec.text,
        language=spec.language,
        speaker=spec.speaker,
        trials=trial_evidence,
        blockers=blockers,
    )