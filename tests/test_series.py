from __future__ import annotations

import numpy as np
import pandas as pd

from asset.series import (
    flagged_runs,
    monthly_from_daily,
    monthly_from_quarter_hourly,
    seasonal_zscore_monitor,
)


def _daily(n_days: int = 400, seed: int = 0) -> pd.Series:
    idx = pd.date_range("2024-01-01", periods=n_days, freq="D")
    rng = np.random.default_rng(seed)
    return pd.Series(150_000 + rng.normal(0, 5_000, n_days), index=idx)


def test_monthly_from_daily_drops_partial_month():
    s = _daily(400)  # ends 2025-02-04 → February 2025 is partial
    m = monthly_from_daily(s)
    assert m.index[-1] == pd.Timestamp("2025-01-01")
    assert (m["days"] >= 28).all()
    assert set(m.columns) == {"mean", "max", "min", "days"}


def test_monthly_from_quarter_hourly_energy_and_peak():
    idx = pd.date_range("2024-01-01", "2024-02-29 23:45", freq="15min")
    kwh = pd.Series(1000.0, index=idx)
    kwh.iloc[10] = 2000.0
    m = monthly_from_quarter_hourly(kwh)
    assert list(m.index.strftime("%Y-%m")) == ["2024-01", "2024-02"]
    assert m.loc["2024-01", "gwh"].iloc[0] == (31 * 96 * 1000 + 1000) / 1e6
    assert m.loc["2024-01", "peak_mw"].iloc[0] == 2000 * 4 / 1000
    assert abs(m.loc["2024-02", "avg_mw"].iloc[0] - 4.0) < 1e-9


def test_monthly_from_quarter_hourly_drops_sparse_month():
    idx = pd.date_range("2024-01-01", "2024-02-03 23:45", freq="15min")
    m = monthly_from_quarter_hourly(pd.Series(1.0, index=idx))
    assert list(m.index.strftime("%Y-%m")) == ["2024-01"]


def test_seasonal_zscore_flags_injected_outlier():
    idx = pd.date_range("2019-01-01", periods=72, freq="MS")
    base = 200 + 30 * np.sin(2 * np.pi * idx.month / 12)
    s = pd.Series(base, index=idx)
    s.iloc[40] *= 1.6
    mon = seasonal_zscore_monitor(s, k=3.0)
    assert mon["flag"].iloc[40]
    assert mon["flag"].sum() <= 3
    assert mon["z"].iloc[40] > 3


def test_flagged_runs_groups_consecutive_months():
    idx = pd.date_range("2020-01-01", periods=8, freq="MS")
    flags = pd.Series([False, True, True, False, False, True, False, False], index=idx)
    z = pd.Series([0, 3.5, 4.2, 0, 0, -3.1, 0, 0], index=idx, dtype=float)
    runs = flagged_runs(flags, z)
    assert [(r["from"], r["to"], r["months"], r["direction"]) for r in runs] == [
        ("2020-02", "2020-03", 2, "high"),
        ("2020-06", "2020-06", 1, "low"),
    ]
    assert runs[0]["peak_month"] == "2020-03"
