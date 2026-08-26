#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Any


def _run(command: list[str]) -> dict[str, Any]:
    executable = shutil.which(command[0])
    if executable is None:
        return {"available": False, "command": command, "stdout": None, "stderr": "not found"}
    try:
        completed = subprocess.run(
            [executable, *command[1:]],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
            shell=False,
        )
    except Exception as exc:  # pragma: no cover - defensive operator probe
        return {"available": True, "command": command, "stdout": None, "stderr": str(exc)}
    return {
        "available": True,
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip() or None,
        "stderr": completed.stderr.strip() or None,
    }


def _torch_probe() -> dict[str, Any]:
    try:
        import torch
    except Exception as exc:
        return {"installed": False, "error": str(exc)}

    payload: dict[str, Any] = {
        "installed": True,
        "version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_runtime": getattr(torch.version, "cuda", None),
        "device_count": int(torch.cuda.device_count()),
    }
    if torch.cuda.is_available():
        payload["devices"] = [torch.cuda.get_device_name(index) for index in range(torch.cuda.device_count())]
    return payload


def main() -> None:
    root = Path(os.environ.get("HOTTOP_MODEL_ROOT", Path.home() / "models"))
    disk = shutil.disk_usage(root if root.exists() else Path.home())
    payload = {
        "schema_version": "hottop.dgx-spark-probe.v1",
        "read_only": True,
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "model_root": str(root),
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
        },
        "nvidia_smi": _run(
            [
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total,memory.free",
                "--format=csv,noheader,nounits",
            ]
        ),
        "nvcc": _run(["nvcc", "--version"]),
        "ip_links": _run(["ip", "-j", "link"]),
        "rdma_links": _run(["rdma", "-j", "link", "show"]),
        "torch": _torch_probe(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
