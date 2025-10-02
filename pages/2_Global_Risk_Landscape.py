from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.data_utils import load_main_data, city_options, risk_categories
from utils.style import inject_global_css, RISK_COLORS

st.set_page_config(page_title="Global Risk Landscape | Urban Flood Risk Analytics", page_icon="🗺️", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

df = load_main_data()

st.header("Mapping Flood Vulnerabilities Worldwide")

# Sidebar filters
st.sidebar.subheader("Filters")
city_list = st.sidebar.multiselect("City", options=city_options(df), default=[])
primary_sel = st.sidebar.selectbox("Primary Risk", options=risk_categories(df), index=0)

filtered = df.copy()
if city_list:
    filtered = filtered[filtered["city_name"].isin(city_list)]
if primary_sel != "All":
    filtered = filtered[filtered["Primary_Risk"] == primary_sel]

# Dynamic filter description
desc_parts = []
if city_list:
    if len(city_list) == 1:
        desc_parts.append(f"City: {city_list[0]}")
    else:
        desc_parts.append(f"Cities: {len(city_list)} selected")
else:
    desc_parts.append("Cities: All")
if primary_sel != "All":
    desc_parts.append(f"Primary Risk: {primary_sel}")
else:
    desc_parts.append("Primary Risk: All")
filters_desc = " • ".join(desc_parts)
st.caption(filters_desc)

# --- Map (Scattergeo) ---
cat_order = ["Ponding Hotspot", "Low Lying", "High Risk Event", "Monitor"]
fig_map = go.Figure()
for cat in [c for c in cat_order if c in filtered["Primary_Risk"].unique()]:
    sub = filtered[filtered["Primary_Risk"] == cat]
    fig_map.add_trace(
        go.Scattergeo(
            lon=sub["longitude"],
            lat=sub["latitude"],
            mode="markers",
            name=cat,
            marker=dict(size=6, color=RISK_COLORS.get(cat, "#6B7280"), opacity=0.85),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Segment: %{customdata[1]}<br>"
                "Elevation: %{customdata[2]:.2f} m<br>Risk: %{customdata[3]}<extra></extra>"
            ),
            customdata=sub[["city_name", "segment_id", "elevation_m", "Primary_Risk"]].values,
        )
    )

fig_map.update_layout(
    height=520,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="right", x=0.99),
    geo=dict(
        showland=True, landcolor="#efefef", showcountries=True, countrycolor="#cfcfcf",
        projection_type="natural earth"
    ),
)

st.plotly_chart(fig_map, use_container_width=True)

# --- Comparative Analysis ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top 15 Cities by High-Risk Segments — {filters_desc}")
    # Use filtered data but restrict to hotspot + low-lying categories
    hi = filtered[filtered["Primary_Risk"].isin(["Ponding Hotspot", "Low Lying"])].copy()
    top = (
        hi.groupby("city_name").size().sort_values(ascending=False).head(15).reset_index(name="count")
    )
    fig_bar = go.Figure(
        go.Bar(
            x=top["count"], y=top["city_name"], orientation="h",
            marker=dict(color="#F03B20"),
            hovertemplate="%{y}: %{x} segments<extra></extra>"
        )
    )
    fig_bar.update_layout(height=480, yaxis=dict(autorange="reversed"), margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader(f"Risk Level Distribution by Continent — {filters_desc}")
    scope = filtered.copy()
    piv = scope.pivot_table(index="Continent", columns="Primary_Risk", values="segment_id", aggfunc="count", fill_value=0)
    piv = piv[[c for c in cat_order if c in piv.columns]] if not piv.empty else piv

    fig_stack = go.Figure()
    for cat in piv.columns:
        fig_stack.add_trace(
            go.Bar(
                x=piv.index, y=piv[cat], name=cat,
                marker=dict(color=RISK_COLORS.get(cat, "#9CA3AF")),
                hovertemplate="%{x} — " + cat + ": %{y}<extra></extra>"
            )
        )
    fig_stack.update_layout(barmode="stack", height=480, margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_stack, use_container_width=True)
