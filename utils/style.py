from __future__ import annotations
import streamlit as st

PALETTE = {
    "primary": "#2B8CBE",
    "secondary": "#74A9CF",
    "accent": "#31A354",
    "warning": "#FDAE6B",
    "danger": "#DE2D26",
    "muted": "#6B7280",
    "bg": "#F5F7FA",
}

RISK_COLORS = {
    "Ponding Hotspot": "#DE2D26",
    "Low Lying": "#FDAE6B",
    "Monitor": "#2B8CBE",
    "High Risk Event": "#9C27B0",
}

def inject_global_css() -> None:
    css = f"""
    <style>
      /* Card style */
      .policy-card {{
          border: 1px solid
          border-radius: 12px;
          background: white;
          padding: 1rem 1.25rem;
          box-shadow: 0 1px 2px rgba(0,0,0,0.06);
          margin-bottom: 1rem;
      }}

      .policy-card h4 {{
          margin: 0 0 0.25rem 0;
          color: {PALETTE['primary']};
      }}

      .subtle {{ color:

      /* Make metrics a bit more compact */
      div[data-testid="stMetricValue"] {{ font-weight: 700; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def risk_color(category: str) -> str:
    return RISK_COLORS.get(category, PALETTE["muted"])