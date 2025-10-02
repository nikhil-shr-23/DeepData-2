from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_utils import load_gurugram_context
from utils.style import inject_global_css
import plotly.graph_objects as go

st.set_page_config(page_title="Case Study: Gurugram | Urban Flood Risk Analytics", page_icon="🇮🇳", layout="wide")
inject_global_css()

st.sidebar.title("Project: Urban Flood Risk Analytics")

ctx = load_gurugram_context()

st.header("A Local Deep Dive: The Challenges of Rapid Urbanization in Gurugram")
st.caption("Secondary, local example. This page uses only Gurugram CSV datasets.")

intro_text = (
    "Gurugram's bowl-shaped topography funnels stormwater from the Aravalli ridges toward "
    "low-lying urban basins. Rapid urbanization and the disappearance of natural water bodies "
    "have altered drainage pathways, increasing pluvial flood exposure during intense cloudbursts. "
    "This page synthesizes topography, hydrology, ecology, and infrastructure context from "
    "Gurugram-only datasets."
)
st.write(intro_text)

col1, col2, col3, col4 = st.columns(4)

with col1:
    topo = ctx["topography"]
    gradient_row = topo[topo["Parameter"].str.contains("Natural Gradient", case=False, na=False)]
    gradient = gradient_row["Value"].iloc[0] if not gradient_row.empty else 78
    st.info(f"Topography: Bowl-shaped with a Natural Gradient of {gradient} m")

with col2:
    hyd = ctx["hydrology"]
    lost_row = hyd[hyd["Water_Body_Type"].str.contains("Water Bodies Lost", case=False, na=False)]
    lost = int(lost_row["Quantitative_Value"].iloc[0]) if not lost_row.empty else 389
    st.info(f"Hydrology: {lost} Water Bodies Lost Since 1956")

with col3:
    eco = ctx["ecology"]
    urban_row = eco[eco["Land_Cover_Type"].str.contains("Urban Built-up Area", case=False, na=False)]
    pct_change = urban_row["Change_Trend_1989_2021"].iloc[0] if not urban_row.empty else "+967%"
    st.info(f"Land Cover: {pct_change} Increase in Urban Built-up Area")

with col4:
    infra = ctx["infrastructure"]
    leg1 = infra[infra["Infrastructure_Type"].str.contains("Primary Drainage Leg", case=False, na=False)]
    cap = leg1["Capacity_Specifications"].iloc[0] if not leg1.empty else "~5000 cumecs"
    st.info(f"Infrastructure: Primary Drainage Capacity: {cap.split()[0]} {cap.split()[1] if len(cap.split())>1 else ''}")

colA, colB = st.columns([1.2, 1])

with colA:
    st.subheader("Ecology & Land Cover (Share of City Area)")
    eco = ctx["ecology"].copy()
    if not eco.empty:
        fig_ec = px.bar(eco.sort_values("Percentage_City_Area", ascending=False), x="Land_Cover_Type", y="Percentage_City_Area",
                        color="Percentage_City_Area", color_continuous_scale=["#74A9CF", "#2B8CBE"],
                        labels={"Percentage_City_Area":"% of city area"})
        fig_ec.update_layout(height=420, margin=dict(t=10,l=10,r=10,b=10), xaxis_tickangle=-30)
        st.plotly_chart(fig_ec, use_container_width=True)
    else:
        st.write("No ecology data available.")

with colB:
    st.subheader("Hydrology: Water Bodies Status")
    hyd = ctx["hydrology"].copy()
    if not hyd.empty:
        subset = hyd[hyd["Water_Body_Type"].isin([
            "Natural Water Bodies (1956)", "Current Water Bodies (2024)", "Water Bodies Lost"
        ])]
        fig_hy = px.bar(subset, x="Water_Body_Type", y="Quantitative_Value", color="Water_Body_Type",
                        color_discrete_sequence=["#2B8CBE", "#FDAE6B", "#DE2D26"],
                        labels={"Quantitative_Value":"Count"})
        fig_hy.update_layout(height=420, showlegend=False, margin=dict(t=10,l=10,r=10,b=10))
        st.plotly_chart(fig_hy, use_container_width=True)
    else:
        st.write("No hydrology data available.")

st.subheader("Stormwater Infrastructure Snapshot")
inf = ctx["infrastructure"].copy()
if not inf.empty:
    st.dataframe(inf, use_container_width=True, height=300)
    counts = inf["Infrastructure_Type"].value_counts().reset_index()
    counts.columns = ["Infrastructure_Type", "count"]
    fig_in = px.bar(counts, x="Infrastructure_Type", y="count", color="count", color_continuous_scale=["#74A9CF", "#2B8CBE"], labels={"count":"Entries"})
    fig_in.update_layout(height=360, margin=dict(t=10,l=10,r=10,b=10))
    st.plotly_chart(fig_in, use_container_width=True)
else:
    st.write("No infrastructure data available.")

st.subheader("Download Gurugram Datasets")
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.download_button(
        "Download Ecology & Land Cover CSV",
        data=ctx["ecology"].to_csv(index=False),
        file_name="gurugram_ecology_landcover.csv",
        mime="text/csv"
    )
    st.download_button(
        "Download Hydrology & Waterbodies CSV",
        data=ctx["hydrology"].to_csv(index=False),
        file_name="gurugram_hydrology_waterbodies.csv",
        mime="text/csv"
    )
with col_d2:
    st.download_button(
        "Download Stormwater Infrastructure CSV",
        data=ctx["infrastructure"].to_csv(index=False),
        file_name="gurugram_stormwater_infrastructure.csv",
        mime="text/csv"
    )
    st.download_button(
        "Download Terrain & Topography CSV",
        data=ctx["topography"].to_csv(index=False),
        file_name="gurugram_terrain_topography.csv",
        mime="text/csv"
    )

st.info("These Gurugram datasets are included as an additional, local case study to support the consortium use case: serving as a data analyst for a global urban resilience consortium (similar to the World Bank's Urban Flood Resilience program). The focus is on EDA-driven insights to guide strategies that reduce flood risks, enhance drainage systems, and build city-wide resilience—no machine learning models are required.")

st.subheader("Summary")
st.write(
    "Gurugram's bowl-shaped terrain, major loss of natural water bodies, and rapid expansion of built-up areas reduce infiltration and concentrate runoff. Strengthening primary drains, restoring natural channels, and expanding green infrastructure in urbanized basins can mitigate localized ponding and pluvial flood risk."
)