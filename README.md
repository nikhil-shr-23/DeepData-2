# Urban Flood Risk Analytics (Streamlit)

A multi-page Streamlit dashboard for the Deep Data Hackathon 2.0: Analyzing Urban Pluvial Flood Risk. Built for policymakers and urban planners with interactive Plotly visualizations and data-driven insights.

## Project Structure

- `app.py` – Home: Project Overview 🌍
- `pages/2_Global_Risk_Landscape.py` – Global Risk Landscape 
- `pages/3_Risk_Factor_Deep_Dive.py` – Risk Factor Deep Dive 
- `pages/4_Case_Study_Gurugram.py` – Case Study: Gurugram, India 🇮
- `pages/5_Insights_and_Policy.py` – Insights & Policy Recommendations 
- `utils/data_utils.py` – Cached data loaders, cleaning, feature engineering
- `utils/style.py` – Color palettes and CSS helpers
- `.streamlit/config.toml` – Theme configuration

## Quickstart

1. Create a virtual environment (recommended) and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Use the left sidebar to navigate between pages.

## Notes

- All charts use Plotly for interactivity and hover tooltips.
- Data loading is cached via `@st.cache_data` for performance.
- Primary risk categories are derived from the `risk_labels` column into: `Ponding Hotspot`, `Low Lying`, `Monitor`, and `High Risk Event`.
