"""Streamlit app for Swiss Governance Dashboard."""

import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.i18n import i18n
from utils.constants import CANTONS, YEAR_START, YEAR_END, SCENARIOS

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_STATIC = PROJECT_ROOT / "data" / "static" / "geojson"


# Page configuration
st.set_page_config(
    page_title=i18n.t("app_title", "en"),
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #0066cc;
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
    except Exception as e:
        st.warning(f"⚠️ Could not load map: {e}")
    return None


def get_indicator_data(df, canton, indicator, year):
    """Get specific indicator value."""
    result = df[
        (df["canton"] == canton) &
        (df["indicator_id"] == indicator) &
        (df["year"] == year)
    ]
    if not result.empty:
        return result.iloc[0]
    return None


def format_value(value, unit):
    """Format a numeric value with unit."""
    if pd.isna(value):
        return "—"
    if unit == "CHF":
        return f"CHF {value:,.0f}"
    elif unit == "%":
        return f"{value:.1f}%"
    elif unit == "/100":
        return f"{value:.1f}"
    else:
        return f"{value:.1f} {unit}"


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Sidebar: Language selection
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        language = st.sidebar.selectbox(
            i18n.t("select_language", "en"),
            options=list(i18n.get_language_options().keys()),
            format_func=lambda x: i18n.get_language_options()[x],
            key="language_select"
        )
    st.session_state.language = language

    # Header
    st.markdown(f"# {i18n.t('app_title', language)}")
    st.markdown(f"**{i18n.t('app_subtitle', language)}**")

    # Load data
    df = load_data()
    if df is None:
        st.error("❌ No data available. Please run: `python src/pipeline/etl.py`")
        return

    # Sidebar: Controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ " + i18n.t("timeline", language))

    year = st.sidebar.slider(
        i18n.t("timeline", language),
        min_value=YEAR_START,
        max_value=YEAR_END,
        value=YEAR_END,
        step=1,
    )

    scenario = st.sidebar.selectbox(
        i18n.t("scenario", language),
        options=["opt", "base", "str"],
        format_func=lambda x: i18n.t(
            "optimistic" if x == "opt" else "baseline" if x == "base" else "stress",
            language
        ),
    )

    canton = st.sidebar.selectbox(
        i18n.t("select_canton", language),
        options=["CH"] + CANTONS,
        format_func=lambda x: i18n.t("all_switzerland", language) if x == "CH" else x,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🗓️ **Year:** {year}")
    st.sidebar.markdown(f"📊 **Scenario:** {i18n.t('optimistic' if scenario == 'opt' else 'baseline' if scenario == 'base' else 'stress', language)}")
    if canton != "CH":
        st.sidebar.markdown(f"🗺️ **Canton:** {canton}")

    # Main content: Tabs for domains
    domains = {
        "water": i18n.t("water", language),
        "education": i18n.t("education", language),
        "mobility": i18n.t("mobility", language),
        "energy_climate": i18n.t("energy_climate", language),
        "housing": i18n.t("housing", language),
        "waste": i18n.t("waste", language),
        "air_environment": i18n.t("air_environment", language),
    }

    tabs = st.tabs(list(domains.values()))

    # Domain-specific indicators
    domain_indicators = {
        "water": [
            "water_consumption", "water_network_loss", "water_quality", "annual_precipitation"
        ],
        "education": [
            "school_enrollment", "student_teacher_ratio", "childcare_places", "spending_per_student"
        ],
        "mobility": [
            "public_transit_trips", "bike_modal_share", "motorized_traffic", "network_punctuality"
        ],
        "energy_climate": [
            "co2_emissions", "renewable_energy_share", "final_energy_consumption", "solar_capacity"
        ],
        "housing": [
            "median_rent", "vacancy_rate", "housing_completions", "cooperative_housing"
        ],
        "waste": [
            "urban_waste_generated", "separate_collection_rate", "organic_waste_collection", "waste_management_cost"
        ],
        "air_environment": [
            "no2_concentration", "pm10_concentration", "green_space_per_capita", "heat_days"
        ],
    }

    for tab, (domain_key, domain_name) in zip(tabs, domains.items()):
        with tab:
            st.markdown(f"## {domain_name}")

            indicators_in_domain = domain_indicators[domain_key]

            # Get data for these indicators
            if canton == "CH":
                # National aggregate
                domain_data = df[
                    (df["indicator_id"].isin(indicators_in_domain)) &
                    (df["year"] == year)
                ].groupby("indicator_id")["value"].mean()
            else:
                # Canton-specific
                domain_data = df[
                    (df["canton"] == canton) &
                    (df["indicator_id"].isin(indicators_in_domain)) &
                    (df["year"] == year)
                ].set_index("indicator_id")["value"]

            # Display KPI cards in a grid
            cols = st.columns(2)
            for idx, indicator_id in enumerate(indicators_in_domain):
                col = cols[idx % 2]
                with col:
                    indicator_row = df[
                        (df["indicator_id"] == indicator_id) &
                        ((df["canton"] == canton) if canton != "CH" else True) &
                        (df["year"] == year)
                    ]

                    if not indicator_row.empty:
                        if canton == "CH":
                            value = indicator_row["value"].mean()
                        else:
                            value = indicator_row.iloc[0]["value"]

                        unit = indicator_row.iloc[0]["unit"]
                        label = indicator_row.iloc[0]["indicator_label"]
                        target = indicator_row.iloc[0].get("target_2030")

                        st.metric(
                            label=label,
                            value=format_value(value, unit),
                            delta=f"Target 2030: {format_value(target, unit)}" if pd.notna(target) else None,
                        )
                    else:
                        st.warning(f"❓ No data for {indicator_id}")

            # Evolution chart
            st.markdown("---")
            st.markdown(f"### {i18n.t('evolution_forecast', language)}")

            # Show evolution for first indicator in domain
            first_indicator = indicators_in_domain[0]
            evolution_data = df[
                (df["indicator_id"] == first_indicator) &
                ((df["canton"] == canton) if canton != "CH" else True)
            ].sort_values("year")

            if not evolution_data.empty:
                fig = px.line(
                    evolution_data,
                    x="year",
                    y="value",
                    title=f"{evolution_data.iloc[0]['indicator_label']} ({evolution_data.iloc[0]['unit']})",
                    markers=True,
                    labels={
                        "year": i18n.t("timeline", language),
                        "value": i18n.t("evolution_forecast", language)
                    }
                )
                fig.add_hline(
                    y=evolution_data.iloc[0].get("target_2030"),
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Target 2030"
                )
                st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #888; font-size: 12px;">
            <p>📊 {i18n.t('data_source', language)}: BFS, BAFU, opendata.swiss, Swisstopo</p>
            <p>🔄 {i18n.t('last_updated', language)}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Phase 1:</strong> Real data exploration • <strong>Phase 2:</strong> Probabilistic forecasting + AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
