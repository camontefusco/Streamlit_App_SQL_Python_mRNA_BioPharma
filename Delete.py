import streamlit as st
from db import execute_command, run_query

def show():
    st.title("🗑️ Delete Records")
    
    menu = st.radio("Which table would you like to delete from?", ["Vaccinations", "Contracts", "Adverse Events"], horizontal=True)
    
    if menu == "Vaccinations":
        df = run_query("""
            SELECT vx.vaccination_id, c.country_name
            FROM vaccinations vx
            JOIN countries_real c ON vx.country_id = c.country_id
        """)
        if not df.empty:
            selected = st.selectbox("Select vaccination ID", df["vaccination_id"])
            if st.button("Delete Vaccination"):
                execute_query("DELETE FROM vaccinations WHERE vaccination_id = %s", (selected,))
                st.success("Vaccination deleted successfully.")
    
    elif menu == "Contracts":
        df = run_query("""
            SELECT ct.contract_id, c.country_name
            FROM contracts ct
            JOIN countries_real c ON ct.country_id = c.country_id
        """)
        if not df.empty:
            selected = st.selectbox(
                "Select contract to update",
                options=df["contract_id"],
                format_func=lambda id: f"{id} - {df[df.contract_id == id]['country_name'].values[0]}"
            )
            if st.button("Delete Contract"):
                execute_query("DELETE FROM contracts WHERE contract_id = %s", (selected,))
                st.success("Contract deleted successfully.")
    
    elif menu == "Adverse Events":
        df = run_query("SELECT event_id, severity FROM adverse_events")
        if not df.empty:
            selected = st.selectbox("Select event ID", df["event_id"])
            if st.button("Delete Event"):
                execute_query("DELETE FROM adverse_events WHERE event_id = %s", (selected,))
                st.success("Adverse event deleted successfully.")
