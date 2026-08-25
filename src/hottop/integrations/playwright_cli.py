from __future__ import annotations

import shutil
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class PlaywrightCliAdapter:
    """Build safe, ephemeral Playwright CLI commands for visual-reference capture.

    Hottop uses Playwright CLI as an optional acquisition adapter rather than a
    browser-authentication layer. Commands default to an in-memory session and
    never enable a persistent profile unless a future explicit operator action
    adds that capability.
    """

    executable: str = "playwright-cli"
    session: str = "hottop-reference"

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def _prefix(self) -> list[str]:
        return [self.executable, f"-s={self.session}"]

    def open_command(self, url: str, *, mobile: bool = False) -> list[str]:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("visual reference URL must use http or https")
        command = [*self._prefix(), "open", url]
        if mobile:
            command.append("--mobile")
        return command

    def screenshot_command(self, filename: str, *, hires: bool = False) -> list[str]:
        if not filename.strip():
            raise ValueError("screenshot filename must not be blank")
        command = [*self._prefix(), "screenshot", f"--filename={filename}"]
        if hires:
            command.append("--hires")
        return command

    def close_command(self) -> list[str]:
        return [*self._prefix(), "close"]
