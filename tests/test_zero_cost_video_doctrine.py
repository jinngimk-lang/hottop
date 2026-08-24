from pathlib import Path

from hottop.video_production import load_video_production_config


ROOT = Path(__file__).resolve().parents[1]


def test_cinematic_zero_cost_profile_is_strictly_free_only():
    profile = load_video_production_config(ROOT / "config/video/cinematic-zero-cost.yml")

    assert profile.generation_backend == "zero-cost-router"
    assert profile.style_profile == "cinematic"
    assert profile.roughness_score <= 40
    assert profile.compositor_backend == "moviepy"
    assert profile.encoder_backend == "ffmpeg"
    assert profile.zero_cost is not None
    assert profile.zero_cost.enabled is True
    assert profile.zero_cost.allow_paid_fallback is False
    assert profile.zero_cost.candidates
    assert all(candidate.cost_per_unit == 0 for candidate in profile.zero_cost.candidates)
    assert profile.audio.voice_backend == "espeak"
    assert profile.audio.music_backend == "synthetic"
    assert profile.audio.sfx_backend == "procedural"
    assert profile.audio.original_music_only is True


def test_project_and_skill_persist_zero_cost_hybrid_invariant():
    project = (ROOT / "PROJECT.md").read_text(encoding="utf-8")
    skill = (ROOT / "skills/brand-metaphor-creative/SKILL.md").read_text(encoding="utf-8")
    radar = (ROOT / "docs/integrations/zero-cost-video-radar.md").read_text(encoding="utf-8")

    for text in (project, skill):
        assert "ZERO_COST_MODE=true" in text
        assert "no paid fallback" in text.lower()
        assert "quality gate" in text.lower()
        assert "FramePack" in text
        assert "FastVideo" in text

    assert "OpenMontage" in radar
    assert "architecture only" in radar.lower()
    assert "code license" in radar.lower()
    assert "weights" in radar.lower()
