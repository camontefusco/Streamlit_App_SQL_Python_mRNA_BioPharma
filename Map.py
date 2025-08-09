import os
import json
import pandas as pd
import streamlit as st
import pydeck as pdk
from db import run_query

name_corrections = {
    # Americas
    "United States of America": "United States",
    "United States": "United States",
    "Brazil": "Brazil",
    "Canada": "Canada",
    "Mexico": "Mexico",
    "Argentina": "Argentina",
    "Colombia": "Colombia",
    # Asia
    "India": "India",
    "China": "China",
    "Indonesia": "Indonesia",
    "Pakistan": "Pakistan",
    "Bangladesh": "Bangladesh",
    "Japan": "Japan",
    "Republic of Korea": "South Korea",
    "South Korea": "South Korea",
    "Saudi Arabia": "Saudi Arabia",
    "Turkey": "Turkey",
    # Europe
    "Germany": "Germany",
    "France": "France",
    "United Kingdom": "United Kingdom",
    "Spain": "Spain",
    "Italy": "Italy",
    "Poland": "Poland",
    "Sweden": "Sweden",
    "Norway": "Norway",
    "Russia": "Russia",
    "Russian Federation": "Russia",
    # Africa
    "South Africa": "South Africa",
    "Nigeria": "Nigeria",
    "Egypt": "Egypt",
    "Kenya": "Kenya",
    "Ethiopia": "Ethiopia",
    # Oceania
    "Australia": "Australia",
}

def corrected_name(name):
    return name_corrections.get(name, name)

@st.cache_data(show_spinner=False)
def load_geojson():
    current_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(current_dir, 'countries.geojson')
    with open(geojson_path, 'r') as f:
        return json.load(f)

def color_scale(rate):
    rate_float = float(rate)
    green = int(min(max(rate_float, 0), 100) * 2.55)
    red = 255 - green
    return [red, green, 0]

def show():
    st.title("Global mRNA BioPharma Vaccination Data Map")
    st.markdown("""
    ### Instructions:
    - Use the slider below to select a date up to which vaccination data is aggregated.
    - The map shows vaccination rates per country based on the selected date.
    - Colors range from red (low vaccination rate) to green (high vaccination rate).
    - Hover over countries to see details.
    - Use the buttons in the sidebar to download the filtered data as a CSV or Excel file.
    """)

    geojson = load_geojson()

    date_query = "SELECT MIN(date_administered) as min_date, MAX(date_administered) as max_date FROM Vaccinations"
    date_df = run_query(date_query)
    min_date = pd.to_datetime(date_df.iloc[0]['min_date']).date()
    max_date = pd.to_datetime(date_df.iloc[0]['max_date']).date()

    selected_date = st.slider(
        "Select date up to which vaccination data is aggregated:",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="YYYY-MM-DD"
    )

    query = f"""
    SELECT
        c.country_name,
        c.population,
        c.region,
        c.income_level,
        COALESCE(SUM(v.doses_given), 0) AS total_doses_given,
        ROUND((COALESCE(SUM(v.doses_given), 0) / c.population) * 100, 2) AS vaccination_rate
    FROM
        countries_real c
    LEFT JOIN
        Vaccinations v ON c.country_id = v.country_id 
            AND v.dose_number = 2 
            AND v.date_administered <= '{selected_date.strftime('%Y-%m-%d')}'
    GROUP BY
        c.country_id, c.country_name, c.population, c.region, c.income_level
    HAVING
        vaccination_rate BETWEEN 0 AND 100
    ORDER BY
        vaccination_rate DESC
    """

    df = run_query(query)

    df['color'] = df['vaccination_rate'].apply(color_scale)

    st.dataframe(df[['country_name', 'population', 'total_doses_given', 'vaccination_rate']])

    for feature in geojson['features']:
        geo_name = feature['properties'].get('ADMIN') or feature['properties'].get('name')
        corrected_geo_name = corrected_name(geo_name)
        feature['properties']['display_name'] = str(corrected_geo_name)  # force string

        matching_row = df[df['country_name'] == corrected_geo_name]
        if not matching_row.empty:
            rate = matching_row.iloc[0]['vaccination_rate']
            rate = float(rate) if rate is not None else 0.0  # native float
            fill_color = color_scale(rate)
            fill_color = [int(c) for c in fill_color]  # ensure list of ints
            feature['properties']['fill_color'] = fill_color
            feature['properties']['vaccination_rate'] = rate
        else:
            feature['properties']['fill_color'] = [200, 200, 200]  # grey fallback
            feature['properties']['vaccination_rate'] = None

    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        opacity=0.7,
        stroked=False,
        filled=True,
        get_fill_color="properties.fill_color",
        get_line_color=[255, 255, 255],
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1.5,
        pitch=0,
    )

    tooltip = {
        "html": "<b>{display_name}</b><br/>Vaccination Rate: {vaccination_rate}%",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(r)

    csv_data = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"vaccination_data_until_{selected_date.strftime('%Y-%m-%d')}.csv",
        mime="text/csv"
    )

    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='VaccinationData')
    processed_data = output.getvalue()
    st.sidebar.download_button(
        label="📥 Download Filtered Data as Excel",
        data=processed_data,
        file_name=f"vaccination_data_until_{selected_date.strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    show()
