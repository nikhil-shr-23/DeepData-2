# Next.js shell for embedding the Streamlit app

This lightweight Next.js app provides a web shell with an iframe to display your deployed Streamlit dashboard.

Quickstart

1) Install deps

   npm install

2) Run locally (expects Streamlit on 8501)

   export NEXT_PUBLIC_STREAMLIT_URL=http://localhost:8501
   npm run dev

3) Deploy
- Build: npm run build
- Start: NEXT_PUBLIC_STREAMLIT_URL=https://your-streamlit-url npm start

Notes
- This app is intentionally minimal so you can layer your own animations and UI while using Streamlit for analytics.
