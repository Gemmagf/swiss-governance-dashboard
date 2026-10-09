"""Contract tests for the two embedding scripts (pure functions, no data download)."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / "pipeline" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


embed_asset = _load("embed_asset")


def test_embed_asset_adds_markers_once_and_is_idempotent():
    html = '<script>\nconst INSTITUTIONS=["BFS"];\nconst x=1;\n</script>'
    assets = {"a": {"id": "a", "n_months": 3}}
    once = embed_asset.embed(html, assets)
    assert once.count(embed_asset.START) == 1 and once.count(embed_asset.END) == 1
    assert 'const ASSETS={"a":{"id":"a","n_months":3}};' in once
    twice = embed_asset.embed(once, {"a": {"id": "a", "n_months": 4}})
    assert twice.count(embed_asset.START) == 1
    assert '"n_months":4' in twice and '"n_months":3' not in twice


def test_embed_asset_refuses_script_terminator():
    html = "const INSTITUTIONS=[];\n"
    with pytest.raises(ValueError):
        embed_asset.embed(html, {"a": {"id": "a", "note": "</script>"}})


def test_embed_asset_requires_anchor():
    with pytest.raises(ValueError):
        embed_asset.embed("no anchor here", {"a": {"id": "a"}})


def test_i18n_dictionaries_cover_the_key_inventory():
    i18n = ROOT / "i18n"
    keys = json.loads((i18n / "keys.json").read_text(encoding="utf-8"))
    assert len(keys) > 500
    for lang in ("de", "fr", "it", "rm"):
        d = json.loads((i18n / f"{lang}.json").read_text(encoding="utf-8"))
        # every entry must be a known key, and every multi-word key with real words must be translated
        assert not [k for k in d if k not in keys], f"{lang}: stale entries"
        missing = [
            k
            for k in keys
            if k not in d
            and " " in k.strip()
            and "_PER_K" not in k
            and re.search(r"[A-Za-z]{2,}", k)
        ]
        assert not missing, f"{lang}: untranslated keys {missing[:5]}"
        assert all(isinstance(v, str) for v in d.values())


def test_dashboard_embeds_assets_and_i18n_once():
    html = (ROOT / "dashboard_real.html").read_text(encoding="utf-8")
    assert html.count("/*ASSET-DATA-START*/") == 1 and html.count("/*ASSET-DATA-END*/") == 1
    assert html.count("/*I18N-START*/") == 1 and html.count("/*I18N-END*/") == 1
    assert html.count("<script>") == 1
