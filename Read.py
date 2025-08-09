import streamlit as st
import pandas as pd
from db import execute_command, run_query
import streamlit as st
from db import run_query

def show():
    st.title("🔎 View Data Records")
    
    menu = st.selectbox("Choose a table to view", ["Vaccinations", "Contracts", "Adverse Events"])
    
    if menu == "Vaccinations":
        df = run_query("SELECT * FROM vaccinations")
        st.subheader("📋 Vaccination Records")
        with st.expander("🔍 Filter Options"):
            age_group = st.multiselect("Filter by Age Group", df["age_group"].unique())
            if age_group:
                df = df[df["age_group"].isin(age_group)]
        st.dataframe(df)
    
    elif menu == "Contracts":
        df = run_query("SELECT * FROM contracts")
        st.subheader("📄 Contracts")
        with st.expander("💰 Contract Filters"):
            max_price = st.slider("Maximum Price per Dose", 0, 50, 25)
            df = df[df["price_per_dose"] <= max_price]
        st.dataframe(df)
    
    elif menu == "Adverse Events":
        df = run_query("SELECT * FROM adverse_events")
        st.subheader("🚨 Adverse Events")
        with st.expander("⚙️ Event Filters"):
            severity = st.multiselect("Filter by Severity", df["severity"].unique())
            if severity:
                df = df[df["severity"].isin(severity)]
        st.dataframe(df)