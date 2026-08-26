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


def test_cinematic_delivery_smoke_archives_media_runtime_provenance():
    workflow = Path(".github/workflows/cinematic-delivery-smoke.yml")
    text = workflow.read_text(encoding="utf-8")

    assert "runtime-provenance.json" in text
    assert '"schema_version": "hottop.runtime-provenance.v1"' in text
    assert "platform.python_version()" in text
    assert 'version("moviepy")' in text
    assert 'version("numpy")' in text
    assert 'version("pillow")' in text
    assert '["ffmpeg", "-version"]' in text
    assert '["espeak", "--version"]' in text
    assert "HOTTOP_CAPTION_FONT" in text
    assert "hashlib.sha256(font_path.read_bytes()).hexdigest()" in text
