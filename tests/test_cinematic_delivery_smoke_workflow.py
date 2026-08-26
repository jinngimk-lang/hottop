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
    assert 'executable_info("ffmpeg", "-version")' in text
    assert 'executable_info("ffprobe", "-version")' in text
    assert 'executable_info("espeak", "--version")' in text
    assert "HOTTOP_CAPTION_FONT" in text
    assert "hashlib.sha256(font_path.read_bytes()).hexdigest()" in text


def test_cinematic_delivery_runtime_provenance_binds_executable_bytes():
    workflow = Path(".github/workflows/cinematic-delivery-smoke.yml")
    text = workflow.read_text(encoding="utf-8")

    assert "shutil.which" in text
    assert '"resolved_path"' in text
    assert '"size_bytes"' in text
    assert '"sha256"' in text
    assert "hashlib.sha256(path.read_bytes()).hexdigest()" in text
    assert 'runtime["executables"]["ffmpeg"]["sha256"]' in text
    assert 'runtime["executables"]["ffprobe"]["sha256"]' in text
    assert 'runtime["executables"]["espeak"]["sha256"]' in text


def test_cinematic_delivery_runtime_provenance_binds_cpu_identity():
    workflow = Path(".github/workflows/cinematic-delivery-smoke.yml")
    text = workflow.read_text(encoding="utf-8")

    assert "def cpu_info()" in text
    assert '"cpu": cpu_info(),' in text
    assert "platform.machine()" in text
    assert 'Path("/proc/cpuinfo")' in text
    assert '"model_name"' in text
    assert '"vendor_id"' in text
    assert '"cpuinfo_sha256"' in text
    assert 'runtime["cpu"]["machine"]' in text
    assert 'runtime["cpu"]["model_name"]' in text
    assert 'runtime["cpu"]["cpuinfo_sha256"]' in text


def test_cinematic_delivery_smoke_gates_real_final_mp4_seam_quality():
    workflow = Path(".github/workflows/cinematic-delivery-smoke.yml")
    text = workflow.read_text(encoding="utf-8")

    assert "seam-quality.json" in text
    assert '"schema_version": "hottop.software3d-seam-quality.v1"' in text
    assert "HOTTOP_SEAM_QUALITY" in text
    assert "assert max_seam_delta <= 8.0" in text
    assert "assert max_seam_ratio <= 5.5" in text
