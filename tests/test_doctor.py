from hottop.doctor import local_doctor


def test_doctor_reports_optional_playwright_cli_reference_capture() -> None:
    report = local_doctor()

    playwright = report["playwright_cli"]
    assert playwright["required"] is False
    assert isinstance(playwright["available"], bool)
    assert playwright["session"] == "hottop-reference"
    assert "visual reference" in playwright["note"].lower()
    assert "persistent" in playwright["note"].lower()
