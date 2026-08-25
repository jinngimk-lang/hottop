from hottop.doctor import local_doctor


def test_doctor_reports_optional_playwright_cli_reference_capture() -> None:
    report = local_doctor()

    playwright = report["playwright_cli"]
    assert playwright["required"] is False
    assert isinstance(playwright["available"], bool)
    assert playwright["session"] == "hottop-reference"
    assert "visual reference" in playwright["note"].lower()
    assert "persistent" in playwright["note"].lower()


def test_doctor_reports_optional_rsshub_configuration(monkeypatch) -> None:
    monkeypatch.delenv("RSSHUB_BASE_URL", raising=False)
    missing = local_doctor()["rsshub"]
    assert missing["required"] is False
    assert missing["configured"] is False
    assert missing["base_url"] is None
    assert "external feed router" in missing["note"].lower()

    monkeypatch.setenv("RSSHUB_BASE_URL", "https://rsshub.example/")
    configured = local_doctor()["rsshub"]
    assert configured["configured"] is True
    assert configured["base_url"] == "https://rsshub.example"
