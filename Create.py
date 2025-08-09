import streamlit as st
from db import execute_command
from utils import get_country_list  # Make sure this function exists

def show():
    menu = st.radio("What would you like to add?", ["Vaccination", "Contract", "Adverse Event"], horizontal=True)

    if menu == "Vaccination":
        st.markdown("ℹ️ Enter vaccination details for a patient record.")
        with st.form("vaccination_form"):
            country = st.selectbox("Country", get_country_list(), help="Select the country where vaccination occurred.")
            dose_date = st.date_input("Vaccination Date")
            vaccine_type = st.text_input("Vaccine Type")
            age_group = st.selectbox("Age Group", ["0-17", "18-30", "31-50", "51-70", "70+"])
            submit = st.form_submit_button("Add Vaccination")

            if submit:
                query = """
                    INSERT INTO vaccinations (country_name, date_administered, vaccine_type, age_group)
                    VALUES (:country, :date, :type, :age)
                """
                params = {
                    "country": country,
                    "date": str(dose_date),
                    "type": vaccine_type,
                    "age": age_group
                }
                execute_command(query, params)
                st.success(f"✅ Vaccination record added for {country}.")

    elif menu == "Contract":
        st.markdown("ℹ️ Add a vaccine contract record.")
        with st.form("contract_form"):
            country = st.selectbox("Country", get_country_list())
            doses = st.number_input("Total Doses", min_value=1000, step=1000)
            price = st.number_input("Price per Dose (USD)", min_value=0.0, step=0.1)
            manufacturer = st.text_input("Manufacturer")
            contract_date = st.date_input("Contract Date")
            submit = st.form_submit_button("Add Contract")

            if submit:
                query = """
                    INSERT INTO contracts (country_name, total_doses, price_per_dose, manufacturer, contract_date)
                    VALUES (:country, :doses, :price, :manufacturer, :date)
                """
                params = {
                    "country": country,
                    "doses": doses,
                    "price": price,
                    "manufacturer": manufacturer,
                    "date": str(contract_date)
                }
                execute_command(query, params)
                st.success(f"✅ Contract for {doses:,} doses added for {country}.")

    elif menu == "Adverse Event":
        st.markdown("ℹ️ Record an adverse event associated with vaccination.")
        with st.form("event_form"):
            country = st.selectbox("Country", get_country_list())
            severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe"])
            description = st.text_area("Event Description")
            resolved = st.checkbox("Resolved")
            submit = st.form_submit_button("Add Event")

            if submit:
                query = """
                    INSERT INTO adverse_events (country_name, severity, description, resolved)
                    VALUES (:country, :severity, :description, :resolved)
                """
                params = {
                    "country": country,
                    "severity": severity,
                    "description": description,
                    "resolved": resolved
                }
                execute_command(query, params)
                st.success(f"✅ Adverse event logged for {country}.")
