from __future__ import annotations

from typing import Any

from .integrations.agent_reach import AgentReachAdapter


def local_doctor() -> dict[str, Any]:
    agent_reach = AgentReachAdapter()
    return {
        "core": "ok",
        "agent_reach": {
            "available": agent_reach.available(),
            "doctor_command": agent_reach.doctor_command(),
            "safe_install_check": agent_reach.install_check_command(),
        },
        "crawl4ai": {
            "status": "optional",
            "default_url": "http://127.0.0.1:11235",
            "health_path": "/health",
        },
    }
