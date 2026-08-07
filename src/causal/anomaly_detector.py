#!/usr/bin/env python3
"""
FASE 3.3: Anomaly Detection

Identifies unusual movements in time-series data:
- Statistical anomalies (zscore > 3)
- Trend breaks (abrupt changes in slope)
- Volatility spikes (residuals > 2σ)
- Data quality issues

Output:
- Anomaly scores (0-1)
- Anomaly types (outlier, trend_break, spike, quality_issue)
- Alerts and recommendations
"""

import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

print("=" * 80)
print("🔍 FASE 3.3: ANOMALY DETECTION")
print("=" * 80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n📊 1. Loading data...")

with open(DATA_PROCESSED / "real_data_hybrid.json") as f:
    real_data = json.load(f)

print(f"   ✅ Real data loaded")

# ============================================================================
# 2. ANOMALY DETECTION CLASS
# ============================================================================

class AnomalyDetector:
    """Detects anomalies in time-series data"""

    @staticmethod
    def zscore_anomalies(values: List[float], threshold: float = 3.0) -> List[Tuple[int, float]]:
        """
        Detect outliers via z-score.

        Returns:
            [(index, zscore), ...]
        """
        if len(values) < 2:
            return []

        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 1.0

        anomalies = []
        for i, v in enumerate(values):
            z = (v - mean) / std if std > 0 else 0
            if abs(z) > threshold:
                anomalies.append((i, z))

        return anomalies

    @staticmethod
    def trend_break_detection(values: List[float], min_segment_size: int = 3) -> List[Tuple[int, float]]:
        """
        Detect sudden changes in trend.

        Returns:
            [(index, trend_change_magnitude), ...]
        """
        if len(values) < 2 * min_segment_size:
            return []

        anomalies = []

        # Simple piecewise linear approach
        for i in range(min_segment_size, len(values) - min_segment_size):
            # Trend before point i
            before_values = values[i - min_segment_size:i]
            before_slope = (before_values[-1] - before_values[0]) / (min_segment_size - 1) if len(before_values) > 1 else 0

            # Trend after point i
            after_values = values[i:i + min_segment_size]
            after_slope = (after_values[-1] - after_values[0]) / (min_segment_size - 1) if len(after_values) > 1 else 0

            # Slope change magnitude
            slope_change = abs(after_slope - before_slope)

            if slope_change > 0.5:  # Threshold for significant trend change
                anomalies.append((i, slope_change))

        return anomalies

    @staticmethod
    def volatility_spike_detection(values: List[float], window_size: int = 3, threshold: float = 2.0) -> List[Tuple[int, float]]:
        """
        Detect sudden increases in volatility.

        Returns:
            [(index, volatility_zscore), ...]
        """
        if len(values) < window_size * 2:
            return []

        # Calculate residuals (deviations from local mean)
        residuals = []
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            mean = sum(window) / len(window)
            volatility = math.sqrt(sum((v - mean) ** 2 for v in window) / len(window))
            residuals.append(volatility)

        # Z-score of volatility
        mean_vol = sum(residuals) / len(residuals)
        std_vol = math.sqrt(sum((v - mean_vol) ** 2 for v in residuals) / len(residuals)) if len(residuals) > 1 else 1.0

        anomalies = []
        for i, vol in enumerate(residuals):
            z_vol = (vol - mean_vol) / std_vol if std_vol > 0 else 0
            if z_vol > threshold:
                anomalies.append((i + window_size // 2, z_vol))

        return anomalies

    @staticmethod
    def detect_all(values: List[float], years: List[int]) -> Dict:
        """
        Run all anomaly detection methods.

        Returns:
            {
                "zscore_anomalies": [...],
                "trend_breaks": [...],
                "volatility_spikes": [...],
                "anomaly_score": 0-1,
                "anomaly_type": "outlier|trend_break|spike|normal",
                "alert": "High | Medium | Low | None"
            }
        """
        results = {
            "zscore_anomalies": [],
            "trend_breaks": [],
            "volatility_spikes": [],
            "anomalies": [],
            "anomaly_score": 0.0,
            "anomaly_type": "normal",
            "alert": "None"
        }

        if len(values) < 3:
            return results

        # Run detections
        zscore_anom = AnomalyDetector.zscore_anomalies(values, threshold=2.5)
        trend_anom = AnomalyDetector.trend_break_detection(values)
        volatility_anom = AnomalyDetector.volatility_spike_detection(values)

        # Convert to year-based format
        for idx, zscore in zscore_anom:
            if idx < len(years):
                results["zscore_anomalies"].append({
                    "year": years[idx],
                    "value": round(values[idx], 2),
                    "zscore": round(zscore, 2),
                    "type": "outlier"
                })

        for idx, change in trend_anom:
            if idx < len(years):
                results["trend_breaks"].append({
                    "year": years[idx],
                    "trend_change": round(change, 2),
                    "type": "trend_break"
                })

        for idx, vol_z in volatility_anom:
            if idx < len(years):
                results["volatility_spikes"].append({
                    "year": years[idx],
                    "volatility_zscore": round(vol_z, 2),
                    "type": "volatility_spike"
                })

        # Combine all anomalies
        all_anom_count = len(zscore_anom) + len(trend_anom) + len(volatility_anom)

        if all_anom_count > 0:
            # Determine anomaly type
            if len(zscore_anom) > len(trend_anom) and len(zscore_anom) > len(volatility_anom):
                results["anomaly_type"] = "outlier"
            elif len(trend_anom) > len(zscore_anom) and len(trend_anom) > len(volatility_anom):
                results["anomaly_type"] = "trend_break"
            elif len(volatility_anom) > 0:
                results["anomaly_type"] = "volatility_spike"

            # Anomaly score (0-1)
            results["anomaly_score"] = min(1.0, all_anom_count / len(values))

            # Alert level
            if results["anomaly_score"] > 0.5:
                results["alert"] = "High"
            elif results["anomaly_score"] > 0.2:
                results["alert"] = "Medium"
            elif all_anom_count > 0:
                results["alert"] = "Low"

        return results


# ============================================================================
# 2.5 RECOMMENDATION HELPER
# ============================================================================

def get_recommendation(anomalies: Dict) -> str:
    """Generate recommendation based on anomaly type"""
    alert = anomalies.get("alert", "None")
    anomaly_type = anomalies.get("anomaly_type", "normal")

    if alert == "None":
        return "No anomalies detected. Data appears normal."

    if anomaly_type == "outlier":
        return "Check for data quality issues or measurement errors. Verify the extreme value."

    if anomaly_type == "trend_break":
        return "Significant trend change detected. Investigate policy changes or external shocks."

    if anomaly_type == "volatility_spike":
        return "High volatility period detected. Review related policy implementations or events."

    return "Review data for potential issues."

# ============================================================================
# 3. DETECT ANOMALIES FOR ALL INDICATORS
# ============================================================================

print("\n🔄 2. Detecting anomalies...")

detector = AnomalyDetector()
anomaly_results = {}

for domain in real_data["domains"]:
    domain_id = domain["id"]
    domain_label = domain["label"]

    print(f"\n   [{domain_id}] {domain_label}")

    anomaly_results[domain_id] = {}

    metrics_dict = domain["metrics"]
    if isinstance(metrics_dict, dict):
        metrics_items = list(metrics_dict.items())
    else:
        metrics_items = enumerate(metrics_dict, 1)

    for metric_id, metric in metrics_items:
        years_hist = sorted([int(y) for y in metric.get("years", {}).keys()])
        values_hist = [metric["years"][str(y)] for y in years_hist]

        if len(values_hist) < 3:
            continue

        # Detect anomalies
        anomalies = detector.detect_all(values_hist, years_hist)

        anomaly_results[domain_id][metric_id] = {
            "label": metric.get("label", metric_id),
            "last_value": round(values_hist[-1], 2),
            "last_year": years_hist[-1],
            "n_data_points": len(values_hist),
            "anomalies": {
                "zscore_outliers": anomalies.get("zscore_anomalies", []),
                "trend_breaks": anomalies.get("trend_breaks", []),
                "volatility_spikes": anomalies.get("volatility_spikes", [])
            },
            "anomaly_score": round(anomalies["anomaly_score"], 2),
            "anomaly_type": anomalies["anomaly_type"],
            "alert": anomalies["alert"],
            "recommendation": get_recommendation(anomalies)
        }


# ============================================================================
# 4. SAVE RESULTS
# ============================================================================

print("\n\n💾 3. Saving results...")

anomalies_file = DATA_PROCESSED / "anomalies.json"
with open(anomalies_file, "w") as f:
    json.dump({
        "metadata": {
            "generated": datetime.now().isoformat(),
            "method": "multi-method-anomaly-detection",
            "methods": [
                "z-score outlier detection (threshold=2.5)",
                "trend break detection (slope change > 0.5)",
                "volatility spike detection (volatility zscore > 2.0)"
            ],
            "data_period": "2015-2024"
        },
        "anomalies": anomaly_results
    }, f, indent=2)

print(f"   ✅ {anomalies_file}")

# ============================================================================
# 6. SUMMARY STATISTICS
# ============================================================================

print("\n📈 4. Anomaly detection statistics...")

total_indicators = sum(len(v) for d in anomaly_results.values() for v in (d.values() if isinstance(d, dict) else []))
anomalies_found = sum(
    1 for d in anomaly_results.values()
    for ind in (d.values() if isinstance(d, dict) else [])
    if ind.get("alert") != "None"
)

high_alert_count = sum(
    1 for d in anomaly_results.values()
    for ind in (d.values() if isinstance(d, dict) else [])
    if ind.get("alert") == "High"
)

print(f"   📊 Total indicators analyzed: {total_indicators}")
print(f"   📊 Indicators with anomalies: {anomalies_found}")
print(f"   📊 High-alert anomalies: {high_alert_count}")

# Distribution
medium_alert = sum(
    1 for d in anomaly_results.values()
    for ind in (d.values() if isinstance(d, dict) else [])
    if ind.get("alert") == "Medium"
)
low_alert = sum(
    1 for d in anomaly_results.values()
    for ind in (d.values() if isinstance(d, dict) else [])
    if ind.get("alert") == "Low"
)

print(f"   📊 Medium-alert: {medium_alert}, Low-alert: {low_alert}")

# ============================================================================
# 7. SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("✅ FASE 3.3 COMPLETED: ANOMALY DETECTION")
print("=" * 80)
print(f"\n📊 Results:")
print(f"   • Analyzed {total_indicators} indicators")
print(f"   • Found {anomalies_found} indicators with anomalies")
print(f"   • {high_alert_count} high-alert anomalies (require investigation)")
print(f"   • 3 detection methods: z-score, trend breaks, volatility spikes")
print(f"\n📁 Files generated:")
print(f"   • anomalies.json (anomaly scores + recommendations)")
print(f"\n✨ Key features:")
print(f"   ✅ Multi-method anomaly detection")
print(f"   ✅ Anomaly type classification")
print(f"   ✅ Alert level scoring")
print(f"   ✅ Actionable recommendations")
print(f"\n🎯 Next: Dashboard UI integration + documentation")
print("=" * 80)
