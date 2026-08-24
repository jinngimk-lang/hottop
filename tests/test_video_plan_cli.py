import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_video_plan_command_builds_configured_motion_plan(tmp_path):
    render_path = tmp_path / "render-v2.json"
    render_path.write_text(
        json.dumps(
            {
                "schema_version": "hottop.render.v2",
                "topic_id": "trend-rough-3d",
                "topic_title": "rough 3D absurd comedy",
                "subject_name": "InkClawAgent",
                "expression_form": "faux-film-still",
                "visual_medium": "animation-low-poly",
                "genre_treatment": "intentionally cheap 3D absurdist comedy",
                "distribution_mode": "motion",
                "in_asset_cta_policy": "no-destination",
                "motion_continuity_required": True,
                "frames": [
                    {
                        "index": 1,
                        "scene": "A rough 3D cow codes in one messy workshop while a snake approaches.",
                        "caption": "哎呀！又来绊我！",
                        "intent": "setup and obstruction",
                    },
                    {
                        "index": 2,
                        "scene": "The cow calls its mother and the camera follows its eyeline to the doorway.",
                        "caption": "妈——！",
                        "intent": "continuous reaction",
                    },
                    {
                        "index": 3,
                        "scene": "The mother enters the same workshop and points to InkClawAgent.",
                        "caption": "傻孩子，用 InkClawAgent。",
                        "intent": "deadpan solution",
                    },
                ],
                "master_prompt": "rough low-budget 3D comedy",
                "negative_prompt": "glossy AI ad, copied film frame",
                "punchlines": ["别被蛇绊住。"],
                "risk_flags": ["original staging only"],
                "claim_status": "satire",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "video-plan",
            str(render_path),
            "--config",
            "config/video/anti-polish-short.yml",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.video-plan.v1"
    assert payload["style_profile"] == "anti-polish"
    assert payload["generation_backend"] == "wan22-ti2v-5b"
    assert payload["compositor_backend"] == "motion-canvas"
    assert payload["encoder_backend"] == "ffmpeg"
    assert payload["shots"][1]["continuity_instruction"]
    assert any(cue["kind"] == "dialogue" for cue in payload["audio_cues"])
