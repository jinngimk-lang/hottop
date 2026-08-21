import pytest
from hottop.integrations.playwright_cli import PlaywrightCliAdapter


def test_playwright_cli_builds_ephemeral_visual_reference_commands() -> None:
    adapter = PlaywrightCliAdapter(executable="playwright-cli", session="hottop-reference")

    assert adapter.open_command("https://example.com/ad", mobile=True) == [
        "playwright-cli",
        "-s=hottop-reference",
        "open",
        "https://example.com/ad",
        "--mobile",
    ]
    assert adapter.screenshot_command("artifacts/reference.png", hires=True) == [
        "playwright-cli",
        "-s=hottop-reference",
        "screenshot",
        "--filename=artifacts/reference.png",
        "--hires",
    ]
    assert adapter.close_command() == ["playwright-cli", "-s=hottop-reference", "close"]


def test_playwright_cli_rejects_non_http_reference_urls() -> None:
    adapter = PlaywrightCliAdapter()

    with pytest.raises(ValueError, match="http"):
        adapter.open_command("file:///tmp/private.html")
