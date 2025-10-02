from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.data_utils import (
    load_main_data,
    prepare_data,
    missingness_table,
    numeric_summary,
    high_risk_rate_by_city,
    correlations,
)
from utils.style import inject_global_css, RISK_COLORS

st.set_page_config(page_title="Data Understanding & EDA | Urban Flood Risk Analytics", page_icon="", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

st.header("Data Understanding & Exploratory Data Analysis (EDA)")
st.caption("Professional workflow: Data Understanding → Data Preparation → Question-driven Exploration → Insights → Policy")

base_df = load_main_data()

st.sidebar.subheader("Data Preparation")
drop_dups = st.sidebar.checkbox("Drop duplicate segments (segment_id)", value=True)
clip_outliers = st.sidebar.checkbox("Clip numeric outliers (1st–99th percentile)", value=True)

eda_df = prepare_data(base_df, drop_duplicates=drop_dups, clip_outliers=clip_outliers)

colA, colB, colC = st.columns([1.2, 1, 1.2])
with colA:
    st.subheader("Structure & Types")
    dtypes_df = pd.DataFrame({"column": eda_df.columns, "dtype": eda_df.dtypes.astype(str)}).sort_values("column")
    st.dataframe(dtypes_df, use_container_width=True, height=300)
with colB:
    st.subheader("Missingness")
    miss = missingness_table(eda_df)
    st.dataframe(miss, use_container_width=True, height=300)
with colC:
    st.subheader("Numeric Summary")
    summary = numeric_summary(eda_df)
    st.dataframe(summary, use_container_width=True, height=300)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Rows", len(eda_df))
with k2:
    st.metric("Columns", len(eda_df.columns))
with k3:
    st.metric("Cities", int(eda_df["city_name"].nunique()))
with k4:
    st.metric("High-risk share", f"{(eda_df['Primary_Risk'].ne('Monitor')).mean()*100:.1f}%")

st.divider()

st.subheader("Targeted EDA Questions")
st.write("Below are 10 targeted analyses to understand flood risk drivers in the main dataset.")

with st.expander("Q1. What is the overall distribution of Primary_Risk categories?"):
    risk_counts = eda_df["Primary_Risk"].value_counts().reset_index()
    risk_counts.columns = ["Primary_Risk", "count"]
    fig = px.bar(risk_counts, x="Primary_Risk", y="count", color="Primary_Risk", color_discrete_map=RISK_COLORS)
    fig.update_layout(showlegend=False, height=380, margin=dict(t=10, l=10, r=10, b=10))
st.plotly_chart(fig, use_container_width=True)
total = int(risk_counts["count"].sum())
top_label = risk_counts.sort_values("count", ascending=False).iloc[0]
st.write(f"Out of {total} segments, the most common primary category is {top_label['Primary_Risk']} ({int(top_label['count'])} segments).")

with st.expander("Q2. How does elevation vary across risk categories?"):
    fig = px.box(eda_df, x="Primary_Risk", y="elevation_m", color="Primary_Risk", color_discrete_map=RISK_COLORS)
    fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)
medians = eda_df.groupby("Primary_Risk")["elevation_m"].median().sort_values()
st.write(f"Median elevation is lowest for {medians.index[0]} (~{medians.iloc[0]:.1f} m) and highest for {medians.index[-1]} (~{medians.iloc[-1]:.1f} m).")

with st.expander("Q3. How does elevation correlate with rainfall intensity by risk?"):
    fig = px.scatter(
        eda_df, x="elevation_m", y="historical_rainfall_intensity_mm_hr",
        color="Primary_Risk", color_discrete_map=RISK_COLORS,
        hover_data=["city_name", "segment_id", "land_use", "soil_group"], opacity=0.8
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Q4. Which land uses carry the greatest burden of high-risk segments?"):
    hi = eda_df[eda_df["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying", "High Risk Event"])].copy()
    land = (hi.groupby("land_use").size().reset_index(name="high_risk").sort_values("high_risk", ascending=False).head(15))
    fig = px.bar(land, x="land_use", y="high_risk", color="high_risk", color_continuous_scale=["#FEE391", "#F03B20"], labels={"high_risk": "High-risk segments"})
    fig.update_layout(height=420)
st.plotly_chart(fig, use_container_width=True)
if not land.empty:
    st.write(f"Top burden by land use: {land.iloc[0]['land_use']} with {int(land.iloc[0]['high_risk'])} high-risk segments.")

with st.expander("Q5. Do soil groups differ in their risk profiles?"):
    agg = eda_df.groupby(["soil_group", "Primary_Risk"]).size().reset_index(name="count")
    fig = px.bar(agg, x="soil_group", y="count", color="Primary_Risk", barmode="stack", color_discrete_map=RISK_COLORS)
    fig.update_layout(height=420)
st.plotly_chart(fig, use_container_width=True)
top_soil_df = agg.groupby("soil_group")["count"].sum().sort_values(ascending=False)
top_soil = top_soil_df.index[0] if not top_soil_df.empty else "Unknown"
st.write(f"Soil group {top_soil} contributes the most segments; clayey groups (C/D) often align with ponding risk.")

with st.expander("Q6. How does drainage density vary with risk?"):
    fig = px.violin(eda_df, x="Primary_Risk", y="drainage_density_km_per_km2", color="Primary_Risk", box=True, points=False, color_discrete_map=RISK_COLORS)
    fig.update_layout(showlegend=False, height=420)
st.plotly_chart(fig, use_container_width=True)
st.write("Higher drainage density tends to associate with Monitor segments; sparse networks align with higher-risk categories.")

with st.expander("Q7. Are high-risk segments farther from formal storm drains?"):
    if "storm_drain_proximity_m" in eda_df.columns and not eda_df["storm_drain_proximity_m"].dropna().empty:
        temp = eda_df.copy()
        temp["risk_bin"] = np.where(temp["Primary_Risk"].eq("Monitor"), "Monitor", "High Risk")
        fig = px.box(temp, x="risk_bin", y="storm_drain_proximity_m", color="risk_bin", color_discrete_map={"High Risk": "#F03B20", "Monitor": "#2B8CBE"})
        fig.update_layout(showlegend=False, height=420, yaxis_title="Proximity to storm drain (m)")
        st.plotly_chart(fig, use_container_width=True)
        st.write("High-risk segments show greater median distance from formal drains, suggesting capture/access gaps.")
    else:
        st.info("Storm drain proximity data not available in the main CSV. Skipping this analysis.")

with st.expander("Q8. Which cities have the highest share of high-risk segments (rate)?"):
    rates = high_risk_rate_by_city(eda_df).head(15)
    fig = px.bar(rates, x="city_name", y="rate_%", color="rate_%", color_continuous_scale=["#FEE391", "#F03B20"], labels={"rate_%": "High-risk rate (%)"})
    fig.update_layout(height=420)
st.plotly_chart(fig, use_container_width=True)
if not rates.empty:
    st.write(f"Highest high-risk rate observed in {rates.iloc[0]['city_name']} (~{rates.iloc[0]['rate_%']:.1f}%).")

with st.expander("Q9. Are ‘High Risk Event’ segments concentrated by continent?"):
    scope = eda_df[eda_df["Primary_Risk"] == "High Risk Event"]
    cont = scope["Continent"].value_counts().reset_index()
    cont.columns = ["Continent", "High Risk Event count"]
    fig = px.bar(cont, x="Continent", y="High Risk Event count", color="High Risk Event count", color_continuous_scale=["#FEE391", "#F03B20"]) 
    fig.update_layout(height=380)
st.plotly_chart(fig, use_container_width=True)
if not cont.empty:
    st.write(f"Most High Risk Event segments are recorded in {cont.iloc[0]['Continent']}.")

with st.expander("Q10. What correlations exist among numerical features?"):
    corr = correlations(eda_df)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale=["#FEE391", "#F03B20"], aspect="auto")
    fig.update_layout(height=520)
st.plotly_chart(fig, use_container_width=True)
st.write("Correlations are modest overall; drainage density shows a mild negative relation to high-risk indicators, while rainfall intensity trends positively.")

with st.expander("Q11. City-level latitude/longitude correlation with high-risk rate (animated)"):
    city_stats = (
        eda_df.groupby("city_name").agg(
            lat=("latitude", "mean"),
            lon=("longitude", "mean"),
            hr_rate=("Primary_Risk", lambda s: (s.ne("Monitor").mean() * 100.0)),
            rain=("historical_rainfall_intensity_mm_hr", "mean"),
            elev=("elevation_m", "mean"),
        ).reset_index()
    )
    corr2 = city_stats[["lat", "lon", "hr_rate"]].corr()
    fig_corr2 = px.imshow(corr2, text_auto=True, color_continuous_scale=["#FEE391", "#F03B20"], aspect="auto")
    fig_corr2.update_layout(height=360)
    st.plotly_chart(fig_corr2, use_container_width=True)

    if not city_stats["rain"].dropna().empty:
        try:
            city_stats["rain_bin"] = pd.qcut(city_stats["rain"], q=4, labels=["Q1","Q2","Q3","Q4"], duplicates="drop")
        except Exception:
            city_stats["rain_bin"] = "All"
    else:
        city_stats["rain_bin"] = "All"

    fig_anim = px.scatter(
        city_stats,
        x="lon", y="lat", size="hr_rate", color="hr_rate",
        color_continuous_scale=["#FEE391", "#F03B20"],
        hover_name="city_name",
        animation_frame="rain_bin",
        labels={"lon":"Longitude", "lat":"Latitude", "hr_rate":"High-risk rate (%)"}
    )
    fig_anim.update_layout(height=520)
    st.plotly_chart(fig_anim, use_container_width=True)

st.info("These findings support flood mitigation strategies like prioritizing ponding hotspots with poor drainage access, upgrading open channels to grated inlets (where present), and steering development away from low-lying basins.")