from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.data_utils import load_main_data
from utils.style import inject_global_css, RISK_COLORS

st.set_page_config(page_title="Insights & Policy | Urban Flood Risk Analytics", page_icon="", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

df = load_main_data()

st.header("From Data to Action: Strategies for Urban Flood Resilience")

insights = [
    (
        "Insight 1: Low-lying segments with clay-like soils (Group D) are disproportionately identified as ponding hotspots.",
        "low_lying_clay",
    ),
    (
        "Insight 2: High rainfall intensity combined with low elevation elevates pluvial flood risk.",
        "rain_elev",
    ),
    (
        "Insight 3: Greater distance from storm drains correlates with higher risk occurrence.",
        "drain_distance",
    ),
    (
        "Insight 4: Grated inlets associate with a lower share of high-risk segments than open channels or no drainage.",
        "inlet_effectiveness",
    ),
    (
        "Insight 5: Commercial and residential corridors contribute most to high-risk exposure across cities.",
        "land_use_burden",
    ),
]

for title, key in insights:
    with st.expander(title, expanded=False):
        if key == "low_lying_clay":
            scope = df[df["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event", "Monitor"])].copy()
            scope["is_hotspot"] = scope["Primary_Risk"].eq("Ponding Hotspot")
            agg = scope.groupby(["soil_group", "Primary_Risk"]).size().reset_index(name="count")
            fig = px.bar(agg, x="soil_group", y="count", color="Primary_Risk", barmode="stack",
                         color_discrete_map=RISK_COLORS,
                         labels={"soil_group": "Soil Group", "count": "Segment count"})
            fig.update_layout(height=380, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.write("Clayey soils (Group D) impede infiltration; in low-lying settings this often manifests as surface ponding.")

        elif key == "rain_elev":
            fig = px.density_heatmap(
                df, x="elevation_m", y="historical_rainfall_intensity_mm_hr",
                nbinsx=30, nbinsy=30, color_continuous_scale=["#FEE391", "#F03B20"],
                labels={"elevation_m": "Elevation (m)", "historical_rainfall_intensity_mm_hr": "Rainfall Intensity (mm/hr)"}
            )
            fig.update_layout(height=380, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.write("Clusters of low elevation and high-intensity rainfall coincide with elevated risk segments in multiple cities.")

        elif key == "drain_distance":
            tmp = df.copy()
            tmp["risk_bin"] = np.where(tmp["Primary_Risk"].eq("Monitor"), "Monitor", "High Risk")
            fig = px.box(tmp, x="risk_bin", y="storm_drain_proximity_m", color="risk_bin",
                         color_discrete_map={"High Risk": "#F03B20", "Monitor": "#2B8CBE"},
                         labels={"storm_drain_proximity_m": "Distance to nearest storm drain (m)", "risk_bin": "Risk group"})
            fig.update_layout(showlegend=False, height=380, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.write("Segments farther from formal drainage show higher dispersion in distance and a higher median, indicating access matters.")

        elif key == "inlet_effectiveness":
            tmp = df.copy()
            tmp["risk_bin"] = np.where(tmp["Primary_Risk"].eq("Monitor"), "Monitor", "High Risk")
            agg = tmp.groupby(["storm_drain_type", "risk_bin"]).size().reset_index(name="count")
            totals = agg.groupby("storm_drain_type")["count"].sum().rename("total")
            agg = agg.join(totals, on="storm_drain_type")
            agg["pct"] = agg["count"]/agg["total"]*100
            fig = px.bar(agg, x="storm_drain_type", y="pct", color="risk_bin", barmode="stack",
                         color_discrete_map={"High Risk": "#F03B20", "Monitor": "#2B8CBE"},
                         labels={"pct": "% of segments"})
            fig.update_layout(height=380, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.write("Grated inlets typically indicate formal, covered capture which reduces blockage and improves capacity versus open channels.")

        elif key == "land_use_burden":
            hi = df[df["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event"])].copy()
            agg = hi.groupby("land_use").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
            fig = px.bar(agg, x="land_use", y="count", color="count", color_continuous_scale=["#FEE391", "#F03B20"], labels={"count": "High-risk segments"})
            fig.update_layout(height=380, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.write("Built-up land uses (commercial, residential) dominate high-risk segments, reflecting imperviousness and runoff concentration.")

st.subheader("Actionable Policy Recommendations")

card_css = "policy-card"

st.markdown(f"<div class='{card_css}'>" \
            f"<h4>Recommendation 1: Prioritized Infrastructure Upgrades</h4>" \
            f"<div class='subtle'>Invest in increasing drainage density and converting open channels to high-capacity grated inlets in segments with elevations below 10m and high rainfall intensity.</div>" \
            f"</div>", unsafe_allow_html=True)

st.markdown(f"<div class='{card_css}'>" \
            f"<h4>Recommendation 2: Data-Driven Zoning Policies</h4>" \
            f"<div class='subtle'>Revise urban planning regulations to restrict new commercial and residential development in identified low-lying zones, promoting green land use instead.</div>" \
            f"</div>", unsafe_allow_html=True)

st.markdown(f"<div class='{card_css}'>" \
            f"<h4>Recommendation 3: Nature-Based Solutions</h4>" \
            f"<div class='subtle'>Implement green infrastructure projects like permeable pavements and bioswales in areas with poor soil drainage (Group C & D) to enhance natural water absorption, inspired by the ecological restoration seen in Gurugram's Aravalli Biodiversity Park.</div>" \
            f"</div>", unsafe_allow_html=True)

st.markdown(f"<div class='{card_css}'>" \
            f"<h4>Recommendation 4: Maintenance and Debris Management</h4>" \
            f"<div class='subtle'>Institute routine drain cleaning schedules before peak monsoon periods, with rapid-response teams for blockage removal in identified hotspot corridors.</div>" \
            f"</div>", unsafe_allow_html=True)

st.markdown(f"<div class='{card_css}'>" \
            f"<h4>Recommendation 5: Early-Warning and Hotspot Monitoring</h4>" \
            f"<div class='subtle'>Deploy low-cost sensors and community reporting for real-time monitoring at recurrent ponding hotspots, feeding into emergency routing and temporary road closures.</div>" \
            f"</div>", unsafe_allow_html=True)