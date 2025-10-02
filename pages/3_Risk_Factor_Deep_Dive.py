from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.data_utils import load_main_data
from utils.style import inject_global_css, RISK_COLORS

st.set_page_config(page_title="Risk Factor Deep Dive | Urban Flood Risk Analytics", page_icon="🔬", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

df = load_main_data()

st.header("Investigating the Drivers of Pluvial Flood Risk")

# Tabs for themes
tab1, tab2, tab3 = st.tabs(["Topography & Land Use", "Infrastructure & Hydrology", "Correlational Analysis"])

with tab1:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Elevation vs. Rainfall Intensity")
        fig_scatter = px.scatter(
            df, x="elevation_m", y="historical_rainfall_intensity_mm_hr",
            color="Primary_Risk",
            color_discrete_map=RISK_COLORS,
            labels={"elevation_m": "Elevation (m)", "historical_rainfall_intensity_mm_hr": "Rainfall Intensity (mm/hr)"},
            hover_data=["city_name", "segment_id", "land_use", "soil_group"],
            opacity=0.8,
        )
        fig_scatter.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=480)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Elevation by Risk Category")
        fig_box = px.box(
            df, x="Primary_Risk", y="elevation_m", color="Primary_Risk",
            color_discrete_map=RISK_COLORS,
            category_orders={"Primary_Risk": ["Ponding Hotspot", "Low Lying", "High Risk Event", "Monitor"]},
        )
        fig_box.update_layout(showlegend=False, height=480, margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Ponding Hotspots by Land Use")
    hotspots = df[df["Primary_Risk"] == "Ponding Hotspot"].copy()
    if hotspots.empty:
        st.write("No 'Ponding Hotspot' segments in the dataset.")
    else:
        counts = hotspots["land_use"].fillna("Unknown").value_counts().reset_index()
        counts.columns = ["land_use", "count"]
        fig_treemap = px.treemap(counts, path=["land_use"], values="count", color="count",
                                 color_continuous_scale=["#FEE391", "#F03B20"])  # yellow → red
        fig_treemap.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=420)
        st.plotly_chart(fig_treemap, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Drainage Density by Risk Category")
        fig_violin = px.violin(
            df, x="Primary_Risk", y="drainage_density_km_per_km2", color="Primary_Risk",
            box=True, points=False, color_discrete_map=RISK_COLORS,
        )
        fig_violin.update_layout(showlegend=False, height=480, margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_violin, use_container_width=True)

    with col2:
        st.subheader("Storm Drain Proximity for High-Risk Segments")
        if "storm_drain_proximity_m" in df.columns and not df["storm_drain_proximity_m"].dropna().empty:
            high_risk = df[df["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event"])].copy()
            fig_hist = px.histogram(
                high_risk, x="storm_drain_proximity_m", nbins=30,
                color="Primary_Risk", color_discrete_map=RISK_COLORS,
                labels={"storm_drain_proximity_m": "Proximity to Storm Drain (m)"},
            )
            fig_hist.update_layout(height=480, margin=dict(t=10, l=10, r=10, b=10))
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Storm drain proximity data not available in the main CSV. Skipping this analysis.")

    # Animated storm-drain visualization (optional)
    if "storm_drain_proximity_m" in df.columns and not df["storm_drain_proximity_m"].dropna().empty:
        st.subheader("Animated: Proximity vs. Drainage Density by Risk")
        temp_anim = df.copy()
        # Bin rainfall intensity to reduce frames
        if not temp_anim["historical_rainfall_intensity_mm_hr"].dropna().empty:
            try:
                temp_anim["rain_bin"] = pd.qcut(temp_anim["historical_rainfall_intensity_mm_hr"], q=4, labels=["Q1","Q2","Q3","Q4"], duplicates="drop")
            except Exception:
                temp_anim["rain_bin"] = "All"
        else:
            temp_anim["rain_bin"] = "All"
        fig_anim2 = px.scatter(
            temp_anim,
            x="storm_drain_proximity_m", y="drainage_density_km_per_km2",
            color="Primary_Risk", color_discrete_map=RISK_COLORS,
            animation_frame="rain_bin",
            hover_data=["city_name", "segment_id"],
            labels={"storm_drain_proximity_m":"Drain Proximity (m)", "drainage_density_km_per_km2":"Drainage Density (km/km²)"}
        )
        fig_anim2.update_layout(height=480, margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_anim2, use_container_width=True)

    # Storm drain type proportion (optional)
    st.subheader("Storm Drain Type vs. Risk Proportion")
    if "storm_drain_type" in df.columns and not df["storm_drain_type"].dropna().empty:
        tmp = df.copy()
        tmp["risk_bin"] = np.where(tmp["Primary_Risk"].eq("Monitor"), "Monitor", "High Risk")
        prop = tmp.groupby(["storm_drain_type", "risk_bin"]).size().reset_index(name="count")
        totals = prop.groupby("storm_drain_type")["count"].sum().rename("total")
        prop = prop.join(totals, on="storm_drain_type")
        prop["pct"] = prop["count"] / prop["total"] * 100.0
        prop = prop.pivot_table(index="storm_drain_type", columns="risk_bin", values="pct", fill_value=0.0)
        if "High Risk" in prop.columns:
            prop = prop.sort_values(by="High Risk", ascending=False)

        fig_bar = go.Figure()
        for col in [c for c in ["High Risk", "Monitor"] if c in prop.columns]:
            fig_bar.add_trace(
                go.Bar(
                    x=prop.index.astype(str), y=prop[col], name=col,
                    marker=dict(color="#F03B20" if col == "High Risk" else "#2B8CBE"),
                    hovertemplate="%{x}: %{y:.1f}%<extra></extra>"
                )
            )
        fig_bar.update_layout(barmode="stack", height=420, margin=dict(t=10, l=10, r=10, b=10), yaxis_title="% of segments")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Storm drain type data not available in the main CSV. Skipping this analysis.")

with tab3:
    st.subheader("Correlation Matrix of Numerical Features")
    num_cols = [
        "elevation_m",
        "drainage_density_km_per_km2",
        "storm_drain_proximity_m",
        "historical_rainfall_intensity_mm_hr",
        "return_period_years",
    ]
    use = df[num_cols].copy()
    corr = use.corr(numeric_only=True)
    fig_heat = px.imshow(corr, text_auto=True, color_continuous_scale=["#FEE391", "#F03B20"], aspect="auto")
    fig_heat.update_layout(height=540, margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)
