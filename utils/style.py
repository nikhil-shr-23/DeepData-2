from __future__ import annotations
import streamlit as st

PALETTE = {
    "primary": "#2B8CBE",   # blue
    "secondary": "#74A9CF", # light blue
    "accent": "#31A354",    # green
    "warning": "#FDAE6B",   # orange
    "danger": "#DE2D26",    # red
    "muted": "#6B7280",     # gray-500
    "bg": "#F5F7FA",
}

RISK_COLORS = {
    "Ponding Hotspot": "#DE2D26",   # red
    "Low Lying": "#FDAE6B",        # orange
    "Monitor": "#2B8CBE",          # blue
    "High Risk Event": "#9C27B0",   # purple
}


def inject_global_css() -> None:
    css = f"""
    <style>
      /* Card style */
      .policy-card {{
          border: 1px solid #e5e7eb;
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

      .subtle {{ color: #6B7280; }}

      /* Make metrics a bit more compact */
      div[data-testid="stMetricValue"] {{ font-weight: 700; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def risk_color(category: str) -> str:
    return RISK_COLORS.get(category, PALETTE["muted"])  # default gray
