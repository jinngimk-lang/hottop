import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_video_doctor_reports_missing_local_dependencies_without_installing(tmp_path):
    result = runner.invoke(
        app,
        [
            "video-doctor",
            "--config",
            "config/video/anti-polish-short.yml",
            "--project-root",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.video-execution-status.v1"
    assert payload["ready"] is False
    assert payload["auto_install"] is False
    assert payload["auto_download_models"] is False
    assert payload["actions_required"]
