from __future__ import annotations

import os
from typing import Any

from .integrations.agent_reach import AgentReachAdapter
from .integrations.playwright_cli import PlaywrightCliAdapter


def local_doctor() -> dict[str, Any]:
    agent_reach = AgentReachAdapter()
    playwright_cli = PlaywrightCliAdapter()
    crawl4ai_url = os.getenv("CRAWL4AI_URL", "http://127.0.0.1:11235").rstrip("/")
    crawl4ai_token = os.getenv("CRAWL4AI_TOKEN")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    firecrawl_url = os.getenv("FIRECRAWL_URL", "https://api.firecrawl.dev").rstrip("/")
    rsshub_raw = (os.getenv("RSSHUB_BASE_URL") or "").strip()
    rsshub_url = rsshub_raw.rstrip("/") if rsshub_raw else None

    return {
        "core": "ok",
        "agent_reach": {
            "required": False,
            "available": agent_reach.available(),
            "doctor_command": agent_reach.doctor_command(),
            "safe_install_check": agent_reach.install_check_command(),
        },
        "playwright_cli": {
            "required": False,
            "available": playwright_cli.available(),
            "session": playwright_cli.session,
            "note": (
                "optional visual reference capture; uses an ephemeral session by default and does not "
                "enable persistent browser profiles or authentication"
            ),
        },
        "crawl4ai": {
            "required": False,
            "configured": bool(crawl4ai_url),
            "base_url": crawl4ai_url,
            "token_configured": bool(crawl4ai_token),
            "health_path": "/health",
            "note": "optional self-hosted enrichment; reachability is checked only when invoked",
        },
        "firecrawl": {
            "required": False,
            "configured": bool(firecrawl_key),
            "base_url": firecrawl_url,
            "api_version": "v2",
            "note": "optional hosted fallback; missing API key never fails core doctor",
        },
        "rsshub": {
            "required": False,
            "configured": bool(rsshub_url),
            "base_url": rsshub_url,
            "note": (
                "optional external feed router; Hottop reuses RSS parsing and does not vendor RSSHub"
            ),
        },
    }
