"""Fetch and cache the City of Zurich open-data CSVs for the asset drill-down.

Thin CLI wrapper around `asset.data.fetch.download` (idempotent; pass --force
to re-download). Files are cached under data/raw/ and are not committed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from asset.data.fetch import download  # noqa: E402

if __name__ == "__main__":
    download(force="--force" in sys.argv)
