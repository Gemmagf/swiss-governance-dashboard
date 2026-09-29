"""Generic monthly-series tools for "series" assets (Klärwerk Werdhölzli, ewz grid load).

These assets have one primary monthly series (plus a few derived extras) rather
than the seven process ratios of KVA Hagenholz, so the multivariate T²/Q
monitor does not apply. Instead each month is compared with its own calendar
month across years (seasonal ratio) and scored with a robust z-score
(median / MAD). Everything here is computed from the data; no constants.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

MAD_TO_SIGMA = 1.4826  # consistency constant: MAD is about 0.6745 sigma for a normal distribution


def monthly_from_daily(daily: pd.Series, min_days: int = 28) -> pd.DataFrame:
    """Aggregate a daily series to calendar months (mean, max, min, days).

    Months with fewer than `min_days` observations (a partial current month,
    or gaps) are dropped rather than reported as if complete.
    """
    g = daily.resample("MS")
    out = pd.DataFrame({"mean": g.mean(), "max": g.max(), "min": g.min(), "days": g.count()})
    out = out[out["days"] >= min_days]
    out.index.name = "month"
    return out


def monthly_from_quarter_hourly(values_kwh: pd.Series, min_share: float = 0.95) -> pd.DataFrame:
    """Aggregate 15-minute energy (kWh) to calendar months.

    Returns energy in GWh, the average load in MW, the peak 15-minute load in MW,
    the number of intervals and the gap adjustment applied. Months with fewer
    than `min_share` of the expected intervals are dropped (a partial current
    month is never extrapolated); months above the threshold with a few missing
    intervals are scaled by expected/observed so a lost day does not read as a
    demand drop. `gap_factor` reports that scaling (1.0 = complete).
    """
    g = values_kwh.resample("MS")
    energy_kwh = g.sum()
    count = g.count()
    expected = pd.Series(
        [pd.Period(m, "M").days_in_month * 96 for m in energy_kwh.index], index=energy_kwh.index
    )
    peak_kwh = g.max()
    gap_factor = (expected / count.replace(0, np.nan)).fillna(1.0)
    out = pd.DataFrame(
        {
            "gwh": energy_kwh * gap_factor / 1e6,
            "avg_mw": energy_kwh / (count * 0.25) / 1000,
            "peak_mw": peak_kwh * 4 / 1000,
            "intervals": count,
            "gap_factor": gap_factor,
        }
    )
    out = out[count >= min_share * expected]
    out.index.name = "month"
    return out


def seasonal_zscore_monitor(series: pd.Series, k: float = 3.0) -> pd.DataFrame:
    """Flag months that deviate from their calendar-month norm.

    ratio = value / mean of the same calendar month across all years;
    z = (ratio - median(ratio)) / (MAD_TO_SIGMA * MAD(ratio)); flag = |z| > k.
    Robust statistics keep a single extreme month from inflating the scale.
    """
    s = series.astype(float)
    month_mean = s.groupby(s.index.month).transform("mean")
    ratio = s / month_mean
    med = float(np.median(ratio))
    mad = float(np.median(np.abs(ratio - med)))
    scale = MAD_TO_SIGMA * mad if mad > 0 else float(ratio.std(ddof=1)) or 1.0
    z = (ratio - med) / scale
    return pd.DataFrame({"ratio": ratio, "z": z, "flag": z.abs() > k}, index=s.index)


def flagged_runs(flags: pd.Series, z: pd.Series) -> list[dict]:
    """Consecutive flagged months as episodes (from, to, months, direction, peak z)."""
    runs: list[dict] = []
    current: list[pd.Timestamp] = []
    for t, f in flags.items():
        if f:
            current.append(t)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    out = []
    for r in runs:
        zs = z.loc[r]
        peak = zs.abs().idxmax()
        out.append(
            {
                "from": r[0].strftime("%Y-%m"),
                "to": r[-1].strftime("%Y-%m"),
                "months": len(r),
                "direction": "high" if zs.loc[peak] > 0 else "low",
                "peak_z": float(round(zs.loc[peak], 2)),
                "peak_month": peak.strftime("%Y-%m"),
            }
        )
    return out
