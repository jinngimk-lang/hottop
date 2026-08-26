from pathlib import Path


def test_cinematic_delivery_smoke_is_scoped_and_uses_delivery_profile():
    workflow = Path(".github/workflows/cinematic-delivery-smoke.yml")
    assert workflow.is_file()

    text = workflow.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in text
    assert '".github/workflows/cinematic-delivery-smoke.yml"' in text
    assert '"config/video/cinematic-software3d-delivery.yml"' in text
    assert '"examples/video/inkclaw-odyssey-witch-pigs.render.json"' in text
    assert "config/video/cinematic-software3d-delivery.yml" in text
    assert "720" in text
    assert "1280" in text
    assert "24/1" in text
    assert "actions/upload-artifact@v4" in text
