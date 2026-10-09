"""Embed i18n/<lang>.json (de, fr, it, rm) into dashboard_real.html.

The dictionaries map the English source string to its translation; missing keys
fall back to English at runtime. The block is written as `const I18N={...};`
between /*I18N-START*/ and /*I18N-END*/ and replaced on every run (idempotent).
`--check` reports keys present in i18n/keys.json but missing in a dictionary.

Usage:  python src/pipeline/embed_i18n.py [--html PATH] [--dir DIR] [--check]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGS = ("de", "fr", "it", "rm")
START, END = "/*I18N-START*/", "/*I18N-END*/"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", type=Path, default=ROOT / "dashboard_real.html")
    ap.add_argument("--dir", type=Path, default=ROOT / "i18n")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    dicts = {}
    for lang in LANGS:
        f = a.dir / f"{lang}.json"
        dicts[lang] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    if a.check:
        keys = json.loads((a.dir / "keys.json").read_text(encoding="utf-8"))
        for lang in LANGS:
            missing = [k for k in keys if k not in dicts[lang]]
            print(f"{lang}: {len(dicts[lang])} entries, {len(missing)} keys without translation")
    payload = json.dumps(dicts, ensure_ascii=False, separators=(",", ":"))
    if "</script" in payload:
        raise ValueError("payload contains '</script'")
    html = a.html.read_text(encoding="utf-8")
    if html.count(START) != 1 or html.count(END) != 1:
        raise SystemExit("i18n markers must appear exactly once")
    out = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        lambda _: f"{START}const I18N={payload};{END}",
        html,
        count=1,
        flags=re.S,
    )
    a.html.write_text(out, encoding="utf-8")
    print(
        f"Embedded {', '.join(f'{k}:{len(v)}' for k, v in dicts.items())} → {a.html.name} {a.html.stat().st_size / 1024:.0f} KB"
    )


if __name__ == "__main__":
    main()
