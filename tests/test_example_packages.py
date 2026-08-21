import json
from pathlib import Path

from hottop.creative_package import CreativePackageInput, build_creative_package


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    ROOT / "examples/creative-packages/consumer-swipe-reveal.json",
    ROOT / "examples/creative-packages/software-category-reframe.json",
    ROOT / "examples/creative-packages/social-native-meme.json",
]


def test_representative_creative_packages_validate_and_render_v2():
    for path in EXAMPLES:
        payload = CreativePackageInput.model_validate(json.loads(path.read_text(encoding="utf-8")))
        result = build_creative_package(payload)

        assert result.schema_version == "hottop.creative-package.v1"
        assert result.selected_render.schema_version == "hottop.render.v2"
        assert result.selected_concept.strategy.bridge
        assert result.selected_concept.strategy.expression_form
