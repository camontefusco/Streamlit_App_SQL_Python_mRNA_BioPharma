import streamlit as st
from db import execute_command, run_query

def show():
    st.title("✏️ Update Records")
    
    record_type = st.radio("Choose a record to update", ["Vaccination", "Contract", "Adverse Event"], horizontal=True)
    
    if record_type == "Vaccination":
        df = run_query("""
            SELECT vx.vaccination_id, c.country_name
            FROM vaccinations vx
            JOIN countries_real c ON vx.country_id = c.country_id
        """)
        if df.empty:
            st.info("No vaccination records found.")
        else:
            selected = st.selectbox("Select record ID", df["vaccination_id"])
            new_type = st.text_input("New Vaccine Type")
            if st.button("Update Vaccine Type"):
                execute_query("UPDATE vaccinations SET vaccine_type = %s WHERE vaccination_id = %s", (new_type, selected))
                st.success("Vaccine type updated successfully.")
    
    elif record_type == "Contract":
        df = run_query("""
            SELECT ct.contract_id, c.country_name
            FROM contracts ct
            JOIN countries_real c ON ct.country_id = c.country_id
        """)
        selected = st.selectbox(
            "Select contract to update",
            options=df["contract_id"],
            format_func=lambda id: f"{id} - {df[df.contract_id == id]['country_name'].values[0]}"
        )
        new_price = st.number_input("New Price per Dose", min_value=0.0)
        if st.button("Update Price"):
            execute_query("UPDATE contracts SET price_per_dose = %s WHERE contract_id = %s", (new_price, selected))
            st.success("Contract price updated.")
    
    elif record_type == "Adverse Event":
        df = run_query("SELECT event_id, severity FROM adverse_events")
        selected = st.selectbox("Select event", df["event_id"])
        new_status = st.checkbox("Mark as Resolved")
        if st.button("Update Status"):
            execute_query("UPDATE adverse_events SET resolved = %s WHERE event_id = %s", (new_status, selected))
            st.success("Adverse event resolution updated.")