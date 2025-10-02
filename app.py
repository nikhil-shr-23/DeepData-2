from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_utils import load_main_data
from utils.style import inject_global_css, PALETTE

st.set_page_config(page_title="Urban Flood Risk Analytics", page_icon="", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

df = load_main_data()

st.title("Urban Pluvial Flood Risk: A Global Analysis for a Resilient Future")
st.caption("Deep Data Hackathon 2.0 • Urban Resilience Consortium")

st.write(
    "This dashboard centers on the main urban_pluvial_flood_risk_dataset.csv to analyze urban road segments and identify pluvial flood vulnerabilities for policymakers and urban planners. It synthesizes topography, infrastructure, hydrology, and land use to reveal actionable insights. Gurugram context is included as a secondary, local example."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cities Analyzed", int(df["city_name"].nunique()))
with col2:
    st.metric("Total Segments Profiled", int(len(df)))
with col3:
    st.metric("Ponding Hotspot Segments", int((df["Primary_Risk"] == "Ponding Hotspot").sum()))
with col4:
    high_risk = df[df["Primary_Risk"] != "Monitor"]
    common_lu = (
        high_risk["land_use"].dropna().astype(str).str.strip().value_counts().idxmax()
        if not high_risk.empty and not high_risk["land_use"].dropna().empty else "N/A"
    )
    st.metric("Most Common Land Use at Risk", common_lu)

with st.expander("Explore the Raw Data", expanded=False):
    st.dataframe(df, use_container_width=True, height=420)

with st.expander("More KPIs from Main Dataset", expanded=False):
    tab_num, tab_cat = st.tabs(["Numerical KPIs", "Categorical Top Values"])
    with tab_num:
        n1, n2, n3, n4, n5 = st.columns(5)
        with n1:
            st.metric("Median Elevation (m)", f"{df['elevation_m'].median():.2f}")
        with n2:
            st.metric("Mean Rainfall Intensity (mm/hr)", f"{df['historical_rainfall_intensity_mm_hr'].mean():.1f}")
        with n3:
            st.metric("Median Return Period (yrs)", f"{df['return_period_years'].median():.0f}")
        with n4:
            st.metric("Avg Drainage Density (km/km²)", f"{df['drainage_density_km_per_km2'].mean():.2f}")
        with n5:
            st.metric("Median Drain Proximity (m)", f"{df['storm_drain_proximity_m'].median():.1f}")
    with tab_cat:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            top_lu = df['land_use'].dropna().astype(str).str.strip().value_counts().idxmax() if not df['land_use'].dropna().empty else 'N/A'
            st.metric("Top Land Use", top_lu)
        with c2:
            top_soil = df['soil_group'].dropna().astype(str).str.strip().value_counts().idxmax() if not df['soil_group'].dropna().empty else 'N/A'
            st.metric("Top Soil Group", top_soil)
        with c3:
            top_drain = df['storm_drain_type'].dropna().astype(str).str.strip().value_counts().idxmax() if not df['storm_drain_type'].dropna().empty else 'N/A'
            st.metric("Top Drain Type", top_drain)
        with c4:
            top_dem = df['dem_source'].dropna().astype(str).str.strip().value_counts().idxmax() if not df['dem_source'].dropna().empty else 'N/A'
            st.metric("Top DEM Source", top_dem)
        with c5:
            top_rain = df['rainfall_source'].dropna().astype(str).str.strip().value_counts().idxmax() if not df['rainfall_source'].dropna().empty else 'N/A'
            st.metric("Top Rainfall Source", top_rain)

st.info(
    "Navigate pages via the left sidebar: Data Understanding & EDA, Global Risk Landscape, Risk Factor Deep Dive, Case Study: Gurugram, and Insights & Policy Recommendations."
)