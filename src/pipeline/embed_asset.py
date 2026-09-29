"""Embed data/processed/asset_*.json into dashboard_real.html.

The JSON is written as `const ASSETS={"<id>":{...},...};` between the markers
/*ASSET-DATA-START*/ and /*ASSET-DATA-END*/ inside the cockpit's single inline
script. The markers are added once (right after `const INSTITUTIONS=[...];`)
and the block is replaced on every later run, so the script is idempotent.

Usage:  python src/pipeline/embed_asset.py [--json-dir DIR] [--html PATH]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON_DIR = ROOT / "data" / "processed"
DEFAULT_HTML = ROOT / "dashboard_real.html"
START = "/*ASSET-DATA-START*/"
END = "/*ASSET-DATA-END*/"
ANCHOR = re.compile(r"const INSTITUTIONS=\[[^\n]*\];\n")


def embed(html: str, assets: dict[str, dict]) -> str:
    payload = json.dumps(assets, ensure_ascii=False, separators=(",", ":"))
    if "</script" in payload:
        raise ValueError("payload contains '</script' — refusing to embed")
    block = f"{START}\nconst ASSETS={payload};\n{END}"
    if START in html:
        if html.count(START) != 1 or html.count(END) != 1:
            raise ValueError("asset markers must appear exactly once")
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        return pattern.sub(lambda _: block, html, count=1)
    anchors = ANCHOR.findall(html)
    if len(anchors) != 1:
        raise ValueError(f"expected exactly one INSTITUTIONS anchor, found {len(anchors)}")
    return ANCHOR.sub(lambda m: m.group(0) + block + "\n", html, count=1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = parser.parse_args()
    files = sorted(args.json_dir.glob("asset_*.json"))
    if not files:
        raise SystemExit(f"no asset_*.json in {args.json_dir}")
    assets = {}
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        assets[doc["id"]] = doc
    html = args.html.read_text(encoding="utf-8")
    out = embed(html, assets)
    args.html.write_text(out, encoding="utf-8")
    print(
        f"Embedded {', '.join(f.name for f in files)} ({sum(f.stat().st_size for f in files) / 1024:.0f} KB) into "
        f"{args.html.name} → {args.html.stat().st_size / 1024:.0f} KB, "
        f"markers: {out.count(START)}/{out.count(END)}"
    )


if __name__ == "__main__":
    main()
