"""Offline checks for distributable layout and reproducible generated files."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_package_metadata_and_typed_distribution():
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            pytest.skip("TOML parser unavailable; build backend validates metadata in CI")
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert metadata["project"]["name"] == "reclaimerforge"
    assert metadata["project"]["requires-python"] == ">=3.10"
    assert metadata["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert (ROOT / "src/reclaimerforge/py.typed").is_file()
    assert importlib.util.find_spec("reclaimerforge").origin == str(ROOT / "src/reclaimerforge/__init__.py")


def test_generation_is_reproducible():
    # Snapshot generation is stdlib-only and must not need the Forge checkout.
    paths = [*ROOT.glob("src/reclaimerforge/*.py"), ROOT / "docs/API_SURFACE.md", ROOT / "docs/operations.json"]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    subprocess.run([sys.executable, str(ROOT / "tools/generate.py")], cwd=ROOT, check=True, capture_output=True)
    assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def test_source_inventory_has_no_secret_or_data_files():
    inventory = json.loads((ROOT / "docs/source-inventory.json").read_text())
    assert {"docs/partner-api.md", "README.md", "docs/architecture-plan.md"} <= inventory.keys()
    assert ".env" not in inventory
    assert not any(path.startswith(("storage/", ".venv/")) for path in inventory)
    assert all(len(digest) == 64 for digest in inventory.values())
