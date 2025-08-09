import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.set_page_config(page_title="mRNA BioPharma App", layout="wide")
    st.title("🧬 Welcome to the mRNA BioPharma Streamlit App")
    st.subheader("Explore data on mRNA vaccines, trials, shipments, and outcomes")
    st.info("📍 Home page loaded.")

    st.markdown("""
    This app is designed for:
    - **Pharmacists**: Track coverage, shipment, and usage gaps.
    - **Medical Officers**: Review safety profiles and adverse event trends.
    - **Market Analysts**: Analyze contract value and price efficiency.

    Use the sidebar to navigate between:
    - **CRUD** operations
    - **Visual Dashboards**
    - **Geo Mapping**
    - **PDF Exports**

    ℹ️ *Tip: Hover over tooltips for additional guidance.*
    """)

    st.image(
        "https://github.com/camontefusco/Streamlit_App_SQL_Python_mRNA_BioPharma-/raw/main/banner.png",
        use_container_width=True
    )

    try:
        vax_count = run_query("SELECT COUNT(*) AS count FROM vaccinations").iloc[0]["count"]
        contract_count = run_query("SELECT COUNT(*) AS count FROM contracts").iloc[0]["count"]
        event_count = run_query("SELECT COUNT(*) AS count FROM adverse_events").iloc[0]["count"]
        trial_count = run_query("SELECT COUNT(*) AS count FROM clinical_trials").iloc[0]["count"]

        st.success("✅ Successfully connected to the SQL database.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💉 Vaccinations", f"{vax_count:,}")
        col2.metric("📄 Contracts", f"{contract_count:,}")
        col3.metric("⚠️ Adverse Events", f"{event_count:,}")
        col4.metric("🔬 Clinical Trials", f"{trial_count:,}")

    except Exception as e:
        st.error("❌ Failed to connect to database or fetch counts.")
        st.exception(e)

    st.caption("Built with ❤️ using Python, Streamlit, SQL, and Plotly.")