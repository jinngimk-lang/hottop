from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentReachAdapter:
    """Build safe Agent-Reach maintenance commands.

    Agent-Reach is primarily an installer/router/doctor for its upstream tools,
    so Hottop does not pretend it is a universal data wrapper. This adapter
    keeps host-changing installation explicit and lets `doctor` detect whether
    the operator has enabled the optional integration.
    """

    executable: str = "agent-reach"

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def doctor_command(self) -> list[str]:
        return [self.executable, "doctor"]

    def install_check_command(self) -> list[str]:
        return [self.executable, "install", "--env=auto"]

    def install_system_command(self, channels: list[str] | None = None) -> list[str]:
        command = [self.executable, "install", "--env=auto", "--system"]
        normalized = [channel.strip() for channel in (channels or []) if channel.strip()]
        if normalized:
            command.append(f"--channels={','.join(normalized)}")
        return command
