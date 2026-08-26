import hashlib
import json
from pathlib import Path

EVIDENCE_PATH = Path("examples/runs/odyssey-cinematic-software3d-delivery.evidence.json")


def _sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_delivery_evidence_binds_canonical_source_bytes() -> None:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    source = evidence["source"]

    assert source["render_sha256"] == _sha256(source["render"])
    assert source["config_sha256"] == _sha256(source["config"])
