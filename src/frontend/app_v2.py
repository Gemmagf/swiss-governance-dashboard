"""
Swiss Governance Dashboard — Phase 1 Complete
Real-time urban governance intelligence for 26 Swiss cantons
Inspired by: zuerich-panell-gestio.html + ch-datencockpit.html
"""

import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import sys

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_STATIC = PROJECT_ROOT / "data" / "static" / "geojson"

# Constants
CANTONS = ["AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR",
           "JU", "LU", "NE", "NW", "OW", "SG", "SH", "SO", "SZ", "TG",
           "TI", "UR", "VD", "VS", "ZG", "ZH"]

CANTON_NAMES = {
    "ZH": "Zurich", "BE": "Bern", "LU": "Lucerne", "UR": "Uri", "SZ": "Schwyz",
    "OW": "Obwalden", "NW": "Nidwalden", "GL": "Glarus", "ZG": "Zug", "FR": "Fribourg",
    "SO": "Solothurn", "BS": "Basel-Stadt", "BL": "Basel-Landschaft", "SH": "Schaffhausen",
    "AR": "Appenzell A.Rh.", "AI": "Appenzell I.Rh.", "SG": "St. Gallen", "GR": "Grisons",
    "AG": "Aargau", "TG": "Thurgau", "TI": "Ticino", "VD": "Vaud", "VS": "Valais",
    "NE": "Neuchâtel", "JU": "Jura", "GE": "Geneva"
}

YEAR_START, YEAR_END = 2015, 2024
SCENARIOS = {"opt": "Optimistic", "base": "Baseline", "str": "Stress"}

DOMAINS = {
    "water": {"label": "Water", "icon": "💧", "color": "#17789B"},
    "education": {"label": "Education", "icon": "📚", "color": "#A8761B"},
    "mobility": {"label": "Mobility", "icon": "🚗", "color": "#2B4EA2"},
    "energy_climate": {"label": "Energy & Climate", "icon": "⚡", "color": "#2E7D4F"},
    "housing": {"label": "Housing", "icon": "🏠", "color": "#8A3E6B"},
    "waste": {"label": "Waste", "icon": "♻️", "color": "#6B7A2E"},
    "air_environment": {"label": "Air & Environment", "icon": "🌍", "color": "#5B5BA6"},
}

DOMAIN_INDICATORS = {
    "water": ["water_consumption", "water_network_loss", "water_quality", "annual_precipitation"],
    "education": ["school_enrollment", "student_teacher_ratio", "childcare_places", "spending_per_student"],
    "mobility": ["public_transit_trips", "bike_modal_share", "motorized_traffic", "network_punctuality"],
    "energy_climate": ["co2_emissions", "renewable_energy_share", "final_energy_consumption", "solar_capacity"],
    "housing": ["median_rent", "vacancy_rate", "housing_completions", "cooperative_housing"],
    "waste": ["urban_waste_generated", "separate_collection_rate", "organic_waste_collection", "waste_management_cost"],
    "air_environment": ["no2_concentration", "pm10_concentration", "green_space_per_capita", "heat_days"],
}

# Page config
st.set_page_config(
    page_title="Swiss Governance Dashboard",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    :root {
        --accent: #17789B;
        --accent-soft: #E3EEF2;
        --ink: #10161C;
        --ink-2: #4A555F;
        --paper: #E9EBE6;
    }

    .metric-card {
        background: white;
        border-top: 3px solid var(--accent);
        border-radius: 4px;
        padding: 12px 14px;
        margin: 8px 0;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: var(--ink);
        letter-spacing: -0.5px;
    }

    .kpi-label {
        font-size: 11px;
        color: var(--ink-2);
        margin-bottom: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .header-bar {
        border-bottom: 2px solid var(--ink);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .domain-tab {
        padding: 16px;
        border-left: 4px solid var(--accent);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load processed indicator data."""
    try:
        parquet_file = DATA_PROCESSED / "indicators_canton_2015_2024.parquet"
        if parquet_file.exists():
            df = pd.read_parquet(parquet_file)
            return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return None

@st.cache_data
def load_geojson():
    """Load canton boundaries."""
    try:
        geojson_file = DATA_STATIC / "swiss_cantons.geojson"
        if geojson_file.exists():
            with open(geojson_file, "r") as f:
                return json.load(f)
    except:
        pass
    return None

def format_value(value, unit):
    """Format numeric value with unit."""
    if pd.isna(value):
        return "—"
    if unit == "CHF":
        return f"CHF {value:,.0f}"
    elif unit == "%":
        return f"{value:.1f}%"
    elif unit == "/100":
        return f"{value:.1f}"
    else:
        return f"{value:.1f}"

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # HEADER
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown("""
        # 🇨🇭 Swiss Governance Dashboard
        **Real-time intelligence for 26 cantons** | Phase 1: Data Foundation
        """)
    with col2:
        st.markdown(f"**{datetime.now().strftime('%Y-%m-%d %H:%M')}**")

    st.markdown("---")

    # Load data
    df = load_data()
    if df is None:
        st.error("❌ No data. Run: `python src/pipeline/etl.py`")
        return

    # SIDEBAR CONTROLS
    st.sidebar.markdown("### ⚙️ Controls")

    year = st.sidebar.slider(
        "Reference year",
        min_value=YEAR_START,
        max_value=YEAR_END,
        value=YEAR_END,
    )

    scenario = st.sidebar.selectbox(
        "Scenario",
        options=["opt", "base", "str"],
        format_func=lambda x: SCENARIOS[x],
    )

    canton = st.sidebar.selectbox(
        "Canton",
        options=["CH"] + CANTONS,
        format_func=lambda x: "🇨🇭 All Switzerland" if x == "CH" else f"{x} • {CANTON_NAMES.get(x, x)}",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"📊 **Year:** {year}")
    st.sidebar.markdown(f"🎯 **Scenario:** {SCENARIOS[scenario]}")
    if canton != "CH":
        st.sidebar.markdown(f"📍 **Canton:** {CANTON_NAMES.get(canton, canton)}")

    # MAIN CONTENT: TABS FOR DOMAINS
    tab_names = [f"{info['icon']} {info['label']}" for info in DOMAINS.values()]
    tabs = st.tabs(tab_names)

    domain_keys = list(DOMAINS.keys())

    for tab, domain_key in zip(tabs, domain_keys):
        with tab:
            domain_info = DOMAINS[domain_key]

            # Domain header
            st.markdown(f"### {domain_info['icon']} {domain_info['label']}")

            # Get indicators for this domain
            indicators = DOMAIN_INDICATORS[domain_key]

            # KPI Grid
            cols = st.columns(2)
            for idx, indicator_id in enumerate(indicators):
                col = cols[idx % 2]

                with col:
                    # Filter data
                    if canton == "CH":
                        indicator_data = df[
                            (df["indicator_id"] == indicator_id) &
                            (df["year"] == year)
                        ]
                        if not indicator_data.empty:
                            value = indicator_data["value"].mean()
                        else:
                            value = None
                    else:
                        indicator_data = df[
                            (df["canton"] == canton) &
                            (df["indicator_id"] == indicator_id) &
                            (df["year"] == year)
                        ]
                        if not indicator_data.empty:
                            value = indicator_data.iloc[0]["value"]
                        else:
                            value = None

                    if not indicator_data.empty:
                        unit = indicator_data.iloc[0]["unit"]
                        label = indicator_data.iloc[0]["indicator_label"]
                        target = indicator_data.iloc[0].get("target_2030")

                        # Display metric
                        st.metric(
                            label=label,
                            value=format_value(value, unit),
                            delta=f"Target 2030: {format_value(target, unit)}" if pd.notna(target) else None,
                        )

            # Evolution chart
            st.markdown("---")
            st.markdown("#### Evolution 2015–2024")

            first_indicator = indicators[0]
            if canton == "CH":
                evolution = df[
                    (df["indicator_id"] == first_indicator)
                ].groupby("year")["value"].mean().reset_index()
            else:
                evolution = df[
                    (df["canton"] == canton) &
                    (df["indicator_id"] == first_indicator)
                ].sort_values("year")

            if not evolution.empty:
                fig = px.line(
                    evolution,
                    x="year" if "year" in evolution.columns else evolution.index,
                    y="value",
                    markers=True,
                    title=f"{first_indicator.replace('_', ' ').title()}",
                )
                fig.update_traces(line_color=domain_info["color"])
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    hovermode="x unified",
                )
                st.plotly_chart(fig, use_container_width=True)

    # FOOTER
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("📊 **Data sources:** BFS, BAFU, opendata.swiss, Swisstopo | 26/26 cantons | 32 indicators | 2015–2024")
    with col2:
        st.caption("**Phase 1** ✅ | Phase 2 🔄")

if __name__ == "__main__":
    main()
