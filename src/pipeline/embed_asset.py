"""Embed data/processed/asset_hagenholz.json into dashboard_real.html.

The JSON is written as `const ASSETS={"hagenholz":{...}};` between the markers
/*ASSET-DATA-START*/ and /*ASSET-DATA-END*/ inside the cockpit's single inline
script. The markers are added once (right after `const INSTITUTIONS=[...];`)
and the block is replaced on every later run, so the script is idempotent.

Usage:  python src/pipeline/embed_asset.py [--json PATH] [--html PATH]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = ROOT / "data" / "processed" / "asset_hagenholz.json"
DEFAULT_HTML = ROOT / "dashboard_real.html"
START = "/*ASSET-DATA-START*/"
END = "/*ASSET-DATA-END*/"
ANCHOR = re.compile(r"const INSTITUTIONS=\[[^\n]*\];\n")


def embed(html: str, data: dict) -> str:
    payload = json.dumps({data["id"]: data}, ensure_ascii=False, separators=(",", ":"))
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
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = parser.parse_args()
    data = json.loads(args.json.read_text(encoding="utf-8"))
    html = args.html.read_text(encoding="utf-8")
    out = embed(html, data)
    args.html.write_text(out, encoding="utf-8")
    print(
        f"Embedded {args.json.name} ({args.json.stat().st_size / 1024:.0f} KB) into "
        f"{args.html.name} → {args.html.stat().st_size / 1024:.0f} KB, "
        f"markers: {out.count(START)}/{out.count(END)}"
    )


if __name__ == "__main__":
    main()
