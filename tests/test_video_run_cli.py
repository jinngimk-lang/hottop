import json
from pathlib import Path

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_video_run_cli_materializes_dry_run_workspace(tmp_path):
    render_path = tmp_path / "render.json"
    render_path.write_text(
        json.dumps(
            {
                "schema_version": "hottop.render.v2",
                "topic_id": "cow-snake",
                "topic_title": "anti-polish story",
                "subject_name": "InkClawAgent",
                "expression_form": "faux-film-still",
                "visual_medium": "animation-low-poly",
                "genre_treatment": "cheap rough 3D absurd comedy",
                "distribution_mode": "motion",
                "in_asset_cta_policy": "no-destination",
                "motion_continuity_required": True,
                "category_default": "setup ceremony",
                "deleted_constraint": "deployment ceremony",
                "new_competition_axis": "time to useful work",
                "bridge_type": "role",
                "bridge": "snake as workflow obstruction",
                "frames": [
                    {
                        "index": 1,
                        "scene": "Cow encounters a snake in one workshop.",
                        "caption": "妈——！",
                        "intent": "reaction",
                    },
                    {
                        "index": 2,
                        "scene": "Mother cow enters the same workshop.",
                        "caption": "傻孩子，用 InkClawAgent。",
                        "intent": "solution",
                    },
                ],
                "master_prompt": "original rough 3D",
                "negative_prompt": "glossy ad",
                "punchlines": ["别被蛇绊住。"],
                "risk_flags": [],
                "claim_status": "satire",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_dir = tmp_path / "video-run"

    result = runner.invoke(
        app,
        [
            "video-run",
            str(render_path),
            "--config",
            "config/video/anti-polish-direct.yml",
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.video-run.v1"
    assert payload["execute_requested"] is False
    assert payload["executed"] is False
    assert Path(payload["plan_path"]).is_file()
    assert Path(payload["compositor_manifest_path"]).is_file()
