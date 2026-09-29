"""Project paths and data-source registry.

Economic/emission constants used by the decision layer (Layer 4) live in
`asset.decision.constants`, each with its own source comment — kept
separate from paths so assumptions are easy to audit in one place.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


@dataclass(frozen=True)
class DataSource:
    """One open-data CSV: where it comes from and where it's cached."""

    name: str
    url: str
    filename: str
    retrieved: str  # ISO date this URL/schema was last verified against the brief

    @property
    def path(self) -> Path:
        return RAW_DIR / self.filename


KHKW = DataSource(
    name="erz_abfallmenge_energie_khkw",
    url=(
        "https://data.stadt-zuerich.ch/dataset/erz_abfallmenge_energie_khkw/"
        "download/erz_abfallmenge_energie_khkw.csv"
    ),
    filename="erz_abfallmenge_energie_khkw.csv",
    retrieved="2026-07-17",
)

BIOABFALL_CALENDAR = DataSource(
    name="entsorgungskalender_bioabfall",
    url=(
        "https://data.stadt-zuerich.ch/dataset/entsorgungskalender_bioabfall/"
        "download/entsorgungskalender_bioabfall_2026.csv"
    ),
    filename="entsorgungskalender_bioabfall.csv",
    retrieved="2026-07-17",
)

ELOG_KENNZAHLEN = DataSource(
    name="erz_elog_kennzahlen",
    url="https://data.stadt-zuerich.ch/dataset/erz_elog_kennzahlen/download/erz_elog_kennzahlen.csv",
    filename="erz_elog_kennzahlen.csv",
    retrieved="2026-07-17",
)

WERDHOELZLI = DataSource(
    name="erz_abwassermenge_klaerwerk_werdhoelzli",
    url=(
        "https://data.stadt-zuerich.ch/dataset/erz_abwassermenge_klaerwerk_werdhoelzli/"
        "download/erz_abwassermenge_klaerwerk_werdhoelzli.csv"
    ),
    filename="erz_abwassermenge_klaerwerk_werdhoelzli.csv",
    retrieved="2026-09-29",
)

# ewz publishes one CSV per year (15-minute gross load of the city of Zurich, since 2019).
EWZ_LOAD = tuple(
    DataSource(
        name=f"ewz_bruttolastgang_{year}",
        url=(
            "https://data.stadt-zuerich.ch/dataset/ewz_bruttolastgang_stadt_zuerich/"
            f"download/{year}_ewz_bruttolastgang.csv"
        ),
        filename=f"{year}_ewz_bruttolastgang.csv",
        retrieved="2026-09-29",
    )
    for year in range(2019, 2027)
)

ALL_SOURCES = (KHKW, BIOABFALL_CALENDAR, ELOG_KENNZAHLEN, WERDHOELZLI, *EWZ_LOAD)

# Werdhölzli / Biogas Zürich AG postcode — used to filter the collection calendar
# for the site-level view in Layer 3.
BIOGAS_ZUERICH_PLZ = 8064


def ensure_dirs() -> None:
    """Create all standard project directories if missing."""
    for d in (RAW_DIR, PROCESSED_DIR, ARTIFACTS_DIR):
        d.mkdir(parents=True, exist_ok=True)
