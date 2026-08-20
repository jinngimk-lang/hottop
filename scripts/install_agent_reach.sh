#!/usr/bin/env bash
set -euo pipefail

PIN="93ae1d18c37b707dec053c7c4f9d91cd8ef8943d"
VENV="${AGENT_REACH_VENV:-$HOME/.agent-reach-venv}"
PYTHON="${PYTHON:-python3}"

"$PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install "https://github.com/Panniantong/Agent-Reach/archive/${PIN}.zip"

# Safe default from Agent-Reach upstream: inspect only; no system package/config writes.
"$VENV/bin/agent-reach" install --env=auto
"$VENV/bin/agent-reach" doctor || true

cat <<EOF
Agent-Reach is installed in: $VENV
The script intentionally stopped at check-only mode.
If you intentionally want Agent-Reach to modify/install host dependencies, run:
  $VENV/bin/agent-reach install --env=auto --system
Authenticated channels (X/Reddit/Xiaohongshu/etc.) require operator-provided login state/cookies and must never be committed to this repository.
EOF
