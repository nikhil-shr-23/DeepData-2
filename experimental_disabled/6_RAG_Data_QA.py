from __future__ import annotations
import streamlit as st

from utils.style import inject_global_css

st.set_page_config(page_title="Data Q&A (RAG) | Urban Flood Risk Analytics", page_icon="🧭", layout="wide")
inject_global_css()

st.header("Data Q&A (RAG)")
st.info("This feature is temporarily disabled per your request. The project remains focused on the main urban_pluvial_flood_risk_dataset.csv and the Gurugram case study page as a separate, local example.")
