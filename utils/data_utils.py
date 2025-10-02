from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import streamlit as st

# Country to continent mapping (covers all countries present in dataset)
COUNTRY_TO_CONTINENT: Dict[str, str] = {
    # Americas
    "USA": "North America",
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Brazil": "South America",
    "Argentina": "South America",
    "Peru": "South America",
    "Colombia": "South America",

    # Europe
    "UK": "Europe",
    "United Kingdom": "Europe",
    "Netherlands": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Greece": "Europe",
    "Denmark": "Europe",

    # Africa
    "South Africa": "Africa",
    "Kenya": "Africa",
    "Ghana": "Africa",
    "Nigeria": "Africa",

    # Asia & Middle East
    "India": "Asia",
    "Sri Lanka": "Asia",
    "China": "Asia",
    "Hong Kong": "Asia",
    "Thailand": "Asia",
    "Malaysia": "Asia",
    "Singapore": "Asia",
    "Vietnam": "Asia",
    "Indonesia": "Asia",
    "Philippines": "Asia",
    "Japan": "Asia",
    "South Korea": "Asia",
    "Taiwan": "Asia",
    "Pakistan": "Asia",
    "Bangladesh": "Asia",
    "Iran": "Asia",
    "Saudi Arabia": "Asia",
    "Qatar": "Asia",
    "Türkiye": "Europe/Asia",
    "Turkey": "Europe/Asia",

    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
}


def _project_root(start: Path) -> Path:
    """Find the project root (where the main CSV resides) walking upwards from start."""
    candidates = [
        start,
        start.parent,
        start.parent.parent,
    ]
    for c in candidates:
        if (c / "urban_pluvial_flood_risk_dataset.csv").exists():
            return c
    return start


def get_data_path(filename: str) -> Path:
    here = Path(__file__).resolve().parent
    root = _project_root(here)
    # common locations: root, root/data
    for p in [root, root / "data"]:
        fp = p / filename
        if fp.exists():
            return fp
    # fall back to current working directory
    return Path(filename)


@st.cache_data(show_spinner=False)
def load_main_data() -> pd.DataFrame:
    fp = get_data_path("urban_pluvial_flood_risk_dataset.csv")
    df = pd.read_csv(fp)

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Coerce numeric fields
    num_cols = [
        "latitude",
        "longitude",
        "elevation_m",
        "drainage_density_km_per_km2",
        "storm_drain_proximity_m",
        "historical_rainfall_intensity_mm_hr",
        "return_period_years",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Clean missing values
    if "elevation_m" in df.columns:
        elev_median = float(np.nanmedian(df["elevation_m"].values))
        df["elevation_m"] = df["elevation_m"].fillna(elev_median)

    if "soil_group" in df.columns:
        if df["soil_group"].dropna().empty:
            soil_mode = "Unknown"
        else:
            soil_mode = (
                df["soil_group"].dropna().astype(str).mode().iloc[0]
                if not df["soil_group"].dropna().empty else "Unknown"
            )
        df["soil_group"] = df["soil_group"].fillna(soil_mode)
        df.loc[df["soil_group"].eq(""), "soil_group"] = soil_mode

    # Risk label parsing and Primary_Risk engineering
    def derive_primary_risk(label: str) -> str:
        if not isinstance(label, str) or label.strip() == "":
            return "Monitor"
        tags = set([t.strip().lower() for t in label.split("|") if t.strip()])
        # Priority order
        if "ponding_hotspot" in tags:
            return "Ponding Hotspot"
        if "low_lying" in tags:
            return "Low Lying"
        # Any explicit event or extreme history indicates critical attention
        if any(t.startswith("event_") for t in tags) or ("extreme_rain_history" in tags):
            return "High Risk Event"
        return "Monitor"

    df["Primary_Risk"] = df["risk_labels"].apply(derive_primary_risk)

    # Continent derivation from country in city_name (e.g., "Chennai, India")
    def extract_country(city: str) -> str:
        if not isinstance(city, str):
            return "Unknown"
        parts = [p.strip() for p in city.split(",")]
        return parts[-1] if parts else "Unknown"

    df["Country"] = df["city_name"].apply(extract_country)
    df["Continent"] = df["Country"].map(COUNTRY_TO_CONTINENT).fillna("Other")

    # Helper flags
    df["Is_High_Risk"] = df["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event"])

    return df


@st.cache_data(show_spinner=False)
def load_gurugram_context() -> Dict[str, pd.DataFrame]:
    files = {
        "topography": "gurugram_terrain_topography.csv",
        "infrastructure": "gurugram_stormwater_infrastructure.csv",
        "hydrology": "gurugram_hydrology_waterbodies.csv",
        "ecology": "gurugram_ecology_landcover.csv",
    }
    out: Dict[str, pd.DataFrame] = {}
    for key, fname in files.items():
        fp = get_data_path(fname)
        out[key] = pd.read_csv(fp)
    return out


def city_options(df: pd.DataFrame) -> List[str]:
    return sorted(df["city_name"].dropna().unique().tolist())


def risk_categories(df: pd.DataFrame) -> List[str]:
    return ["All"] + ["Ponding Hotspot", "Low Lying", "Monitor", "High Risk Event"]


# ---------------------- EDA Helpers ----------------------

def missingness_table(df: pd.DataFrame) -> pd.DataFrame:
    data = []
    for col in df.columns:
        missing = int(df[col].isna().sum())
        pct = float(missing) / len(df) * 100.0 if len(df) else 0.0
        data.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": missing,
            "missing_%": round(pct, 2),
        })
    out = pd.DataFrame(data).sort_values("missing_%", ascending=False)
    return out


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return pd.DataFrame()
    desc = num_df.describe().T
    desc["missing"] = [df[c].isna().sum() for c in num_df.columns]
    return desc


def prepare_data(
    df: pd.DataFrame,
    drop_duplicates: bool = False,
    clip_outliers: bool = False,
) -> pd.DataFrame:
    out = df.copy()

    if drop_duplicates and "segment_id" in out.columns:
        out = out.drop_duplicates(subset=["segment_id"])  # keep first occurrence

    if clip_outliers:
        num_cols = out.select_dtypes(include=[np.number]).columns.tolist()
        for c in num_cols:
            s = out[c]
            q_low, q_hi = s.quantile(0.01), s.quantile(0.99)
            out[c] = s.clip(q_low, q_hi)

    return out


def high_risk_rate_by_city(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["is_hr"] = temp["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event"])  # noqa
    grp = temp.groupby("city_name")["is_hr"].agg(["sum", "count"]).rename(columns={"sum": "high_risk", "count": "total"})
    grp["rate_%"] = grp["high_risk"] / grp["total"] * 100.0
    return grp.reset_index().sort_values("rate_%", ascending=False)


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include=[np.number]).corr(numeric_only=True)
