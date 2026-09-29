"""Parse the three raw City of Zurich CSVs into tidy DataFrames.

All three are cached under data/raw/ by scripts/download_data.py before these
loaders run — see asset.config for the source registry.
"""

from __future__ import annotations

import pandas as pd

from asset.config import BIOABFALL_CALENDAR, ELOG_KENNZAHLEN, EWZ_LOAD, KHKW, WERDHOELZLI

KHKW_INT_COLUMNS = (
    "Kehrichtdurchsatz",
    "Abtransp_Restprodukte",
    "Waermeabsatz",
    "Stromabsatz",
    "Stromproduktion",
    "Trinkwasserverbrauch",
    "Ammoniakverbrauch",
    "Natronlaugeverbrauch",
    "Salzsaeureverbrauch",
    "Kalkverbrauch",
)


def load_khkw() -> pd.DataFrame:
    """Monthly KVA Hagenholz plant operating data, 2020-01 onward.

    One row per month. `Monat` is parsed to a period-start Timestamp and set
    as a sorted DatetimeIndex so downstream forecasting/detection code can
    rely on a regular monthly index.
    """
    if not KHKW.path.exists():
        raise FileNotFoundError(f"{KHKW.path} missing — run `make data` first")
    df = pd.read_csv(KHKW.path)
    missing = set(KHKW_INT_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"erz_abfallmenge_energie_khkw schema changed, missing columns: {missing}")
    df["Monat"] = pd.to_datetime(df["Monat"], format="%Y-%m")
    df = df.sort_values("Monat").set_index("Monat")
    df.index.name = "month"
    return df[list(KHKW_INT_COLUMNS)]


def load_bioabfall_calendar() -> pd.DataFrame:
    """Bio-waste collection calendar: one row per (PLZ, collection date)."""
    if not BIOABFALL_CALENDAR.path.exists():
        raise FileNotFoundError(f"{BIOABFALL_CALENDAR.path} missing — run `make data` first")
    df = pd.read_csv(BIOABFALL_CALENDAR.path, encoding="utf-8-sig")
    df["Abholdatum"] = pd.to_datetime(df["Abholdatum"])
    return df


def _parse_swiss_number(value: object) -> float:
    """Handle the Swiss thousands separator, e.g. "92'056" -> 92056.0."""
    if isinstance(value, str):
        value = value.replace("'", "")
    return float(value)


def load_elog_kennzahlen(pivot: bool = False) -> pd.DataFrame:
    """City-wide waste/recycling KPIs in long format.

    Set `pivot=True` to reshape to one row per month, one column per
    `Beschreibung` series (only the monthly-interval rows are pivoted).
    """
    if not ELOG_KENNZAHLEN.path.exists():
        raise FileNotFoundError(f"{ELOG_KENNZAHLEN.path} missing — run `make data` first")
    df = pd.read_csv(ELOG_KENNZAHLEN.path)
    df["Datum"] = pd.to_datetime(df["Datum"])
    df["Wert"] = df["Wert"].map(_parse_swiss_number)
    if not pivot:
        return df

    monthly = df[df["Intervall"] == "Monat"]
    wide = monthly.pivot_table(index="Datum", columns="Beschreibung", values="Wert", aggfunc="first")
    wide.index.name = "month"
    return wide.sort_index()


def load_werdhoelzli() -> pd.DataFrame:
    """Daily treated wastewater inflow at Klärwerk Werdhölzli (m³/day), 2020-01 onward.

    One row per day, sorted DatetimeIndex named "date"; the value column is
    `abwasser_m3_pro_d` (float, NaN where the source has no value).
    """
    if not WERDHOELZLI.path.exists():
        raise FileNotFoundError(f"{WERDHOELZLI.path} missing — run `make asset-data` first")
    df = pd.read_csv(WERDHOELZLI.path)
    if {"datum", "abwasser_m3_pro_d"} - set(df.columns):
        raise ValueError("erz_abwassermenge_klaerwerk_werdhoelzli schema changed")
    df["datum"] = pd.to_datetime(df["datum"])
    df = df.sort_values("datum").set_index("datum")
    df.index.name = "date"
    df["abwasser_m3_pro_d"] = df["abwasser_m3_pro_d"].astype(float)
    return df[["abwasser_m3_pro_d"]]


def load_ewz_load() -> pd.DataFrame:
    """15-minute gross electricity delivered in the city of Zurich (kWh), all years concatenated.

    Columns `bruttolastgang` (kWh per 15 min) and `status` (E = plausibilised,
    F/W = provisional); sorted DatetimeIndex named "time".
    """
    frames = []
    for source in EWZ_LOAD:
        if not source.path.exists():
            raise FileNotFoundError(f"{source.path} missing — run `make asset-data` first")
        frames.append(pd.read_csv(source.path))
    df = pd.concat(frames, ignore_index=True)
    if {"zeitpunkt", "bruttolastgang", "status"} - set(df.columns):
        raise ValueError("ewz_bruttolastgang schema changed")
    df["zeitpunkt"] = pd.to_datetime(df["zeitpunkt"])
    df = df.sort_values("zeitpunkt").drop_duplicates("zeitpunkt").set_index("zeitpunkt")
    df.index.name = "time"
    df["bruttolastgang"] = df["bruttolastgang"].astype(float)
    return df[["bruttolastgang", "status"]]
