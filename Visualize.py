import streamlit as st
import pandas as pd
from db import run_query
import plotly.express as px
from io import BytesIO

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    plt = None
    sns = None

def fig_to_bytes_matplotlib(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', dpi=150)
    buf.seek(0)
    return buf

def fig_to_bytes_plotly(fig):
    img_bytes = fig.to_image(format="png", engine="kaleido")
    return BytesIO(img_bytes)

def show():
    st.title("📊 Visual Analytics")

    qualitative_colors = px.colors.qualitative.Plotly

    ############### 1. Total Contracted Revenue per Country ###############
    df1 = run_query("""
        SELECT country_name, SUM(total_doses * price_per_dose) AS total_revenue
        FROM Contracts
        JOIN countries_real USING (country_id)
        GROUP BY country_name
    """)
    fig1 = px.bar(df1, x="country_name", y="total_revenue",
                  title="Total Contracted Revenue per Country",
                  labels={"country_name": "Country", "total_revenue": "Total Revenue (USD)"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig1, use_container_width=True)
    buf1 = fig_to_bytes_plotly(fig1)
    st.download_button(
        label="📥 Download Revenue Chart",
        data=buf1,
        file_name="total_revenue_per_country.png",
        mime="image/png",
        key="download1"
    )

    ############### 2. Dose Delivery Completion Rate per Contract ###############
    df2 = run_query("""
        SELECT contract_id, country_name,
               total_doses,
               SUM(doses_shipped) AS shipped,
               ROUND(SUM(doses_shipped)/total_doses * 100, 2) AS delivery_rate_percent
        FROM Contracts
        JOIN countries_real USING (country_id)
        JOIN Shipments USING (contract_id)
        GROUP BY contract_id, country_name, total_doses
    """)
    fig2 = px.bar(df2, x="contract_id", y="delivery_rate_percent",
                  color="country_name",
                  title="Dose Delivery Completion Rate per Contract (%)",
                  labels={"contract_id": "Contract ID", "delivery_rate_percent": "Delivery Rate (%)"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig2, use_container_width=True)
    buf2 = fig_to_bytes_plotly(fig2)
    st.download_button(
        label="📥 Download Delivery Completion Chart",
        data=buf2,
        file_name="dose_delivery_completion_rate.png",
        mime="image/png",
        key="download2"
    )

    ############### 3. Country-Level Vaccination Coverage ###############
    df3 = run_query("""
        SELECT c.country_name,
               SUM(v.doses_given) AS total_doses_administered,
               c.population,
               ROUND(SUM(v.doses_given)/c.population * 100, 2) AS coverage_percent
        FROM Vaccinations v
        JOIN countries_real c USING (country_id)
        GROUP BY c.country_name, c.population
    """)
    fig3 = px.bar(df3, x="country_name", y="coverage_percent",
                  title="Vaccination Coverage by Country (%)",
                  labels={"country_name": "Country", "coverage_percent": "Coverage (%)"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig3, use_container_width=True)
    buf3 = fig_to_bytes_plotly(fig3)
    st.download_button(
        label="📥 Download Vaccination Coverage Chart",
        data=buf3,
        file_name="vaccination_coverage_by_country.png",
        mime="image/png",
        key="download3"
    )

    if plt and sns:
        fig_mpl, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df3, x="country_name", y="coverage_percent",
                    hue="country_name", ax=ax, palette="Set2", legend=False)
        ax.set_title("Vaccination Coverage by Country (Seaborn)")
        ax.set_ylabel("Coverage (%)")
        ax.set_xlabel("Country")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig_mpl)

        buf_mpl = fig_to_bytes_matplotlib(fig_mpl)
        st.download_button(
            label="📥 Download Vaccination Coverage (Seaborn) Chart",
            data=buf_mpl,
            file_name="vaccination_coverage_seaborn.png",
            mime="image/png",
            key="download_seaborn"
        )
    else:
        st.warning("Install matplotlib and seaborn to see the Seaborn chart and download option.")

    ############### 4. Severe Adverse Events per Million Doses ###############
    df4 = run_query("""
        SELECT 
          c.country_name,
          COUNT(CASE WHEN severity = 'Severe' THEN 1 END) AS severe_events,
          SUM(v.doses_given) AS total_doses,
          ROUND(COUNT(CASE WHEN severity = 'Severe' THEN 1 END)/SUM(v.doses_given) * 1000000, 2) AS events_per_million
        FROM Adverse_Events a
        JOIN Vaccinations v USING (vaccination_id)
        JOIN countries_real c ON v.country_id = c.country_id
        GROUP BY c.country_name
    """)
    fig4 = px.bar(df4, x="country_name", y="events_per_million",
                  title="Severe Adverse Events per Million Doses by Country",
                  labels={"country_name": "Country", "events_per_million": "Events per Million Doses"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig4, use_container_width=True)
    buf4 = fig_to_bytes_plotly(fig4)
    st.download_button(
        label="📥 Download Severe Adverse Events Chart",
        data=buf4,
        file_name="severe_adverse_events_per_million.png",
        mime="image/png",
        key="download4"
    )

    ############### 5. Top 5 Countries by Revenue (Pie Chart) ###############
    df5 = run_query("""
        SELECT c.country_name, SUM(total_doses * price_per_dose) AS revenue
        FROM Contracts
        JOIN countries_real c USING (country_id)
        GROUP BY c.country_name
        ORDER BY revenue DESC
        LIMIT 5
    """)
    fig5 = px.pie(df5, values='revenue', names='country_name',
                  title='Top 5 Countries by Revenue',
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig5, use_container_width=True)
    buf5 = fig_to_bytes_plotly(fig5)
    st.download_button(
        label="📥 Download Top 5 Revenue Countries Pie",
        data=buf5,
        file_name="top5_revenue_countries_pie.png",
        mime="image/png",
        key="download5"
    )

    ############### 6. Average Efficacy Rate by Trial Phase ###############
    df6 = run_query("""
        SELECT phase, ROUND(AVG(efficacy_rate), 2) AS avg_efficacy
        FROM Clinical_Trials
        GROUP BY phase
    """)
    fig6 = px.bar(df6, x='phase', y='avg_efficacy',
                  title='Average Clinical Trial Efficacy by Phase',
                  labels={"phase": "Trial Phase", "avg_efficacy": "Avg Efficacy Rate (%)"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig6, use_container_width=True)
    buf6 = fig_to_bytes_plotly(fig6)
    st.download_button(
        label="📥 Download Trial Efficacy Chart",
        data=buf6,
        file_name="avg_efficacy_by_phase.png",
        mime="image/png",
        key="download6"
    )

    ############### 7. Trial Participants by Income Level (Pie) ###############
    df7 = run_query("""
        SELECT income_level, SUM(participants) AS total_participants
        FROM Clinical_Trials
        JOIN countries_real USING (country_id)
        GROUP BY income_level
    """)
    fig7 = px.pie(df7, names='income_level', values='total_participants',
                  title='Trial Participants by Income Level',
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig7, use_container_width=True)
    buf7 = fig_to_bytes_plotly(fig7)
    st.download_button(
        label="📥 Download Trial Participants Pie",
        data=buf7,
        file_name="trial_participants_income_level_pie.png",
        mime="image/png",
        key="download7"
    )

    ############### 8. Top 5 Busiest Vaccination Days ###############
    df8 = run_query("""
        SELECT date_administered, SUM(doses_given) AS total_given
        FROM Vaccinations
        GROUP BY date_administered
        ORDER BY total_given DESC
        LIMIT 5
    """)
    fig8 = px.bar(df8, x='date_administered', y='total_given',
                  title='Top 5 Busiest Vaccination Days',
                  labels={"date_administered": "Date", "total_given": "Doses Given"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig8, use_container_width=True)
    buf8 = fig_to_bytes_plotly(fig8)
    st.download_button(
        label="📥 Download Busiest Vaccination Days Chart",
        data=buf8,
        file_name="top5_busiest_vaccination_days.png",
        mime="image/png",
        key="download8"
    )

    ############### 9. Age Group Distribution of Doses ###############
    df9 = run_query("""
        SELECT age_group, SUM(doses_given) AS total_doses
        FROM Vaccinations
        GROUP BY age_group
    """)
    fig9 = px.bar(df9, x='age_group', y='total_doses',
                  title='Age Group Distribution of Doses',
                  labels={"age_group": "Age Group", "total_doses": "Total Doses"},
                  color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig9, use_container_width=True)
    buf9 = fig_to_bytes_plotly(fig9)
    st.download_button(
        label="📥 Download Age Group Distribution Chart",
        data=buf9,
        file_name="age_group_distribution_doses.png",
        mime="image/png",
        key="download9"
    )

    ############### 10. Monthly Dose Administration Trends ###############
    df10 = run_query("""
        SELECT DATE_FORMAT(date_administered, '%Y-%m') AS month, SUM(doses_given) AS total_doses
        FROM Vaccinations
        GROUP BY month
        ORDER BY month
    """)
    fig10 = px.line(df10, x='month', y='total_doses',
                    title='Monthly Dose Administration Trends',
                    labels={"month": "Month", "total_doses": "Total Doses"},
                    color_discrete_sequence=qualitative_colors)
    st.plotly_chart(fig10, use_container_width=True)
    buf10 = fig_to_bytes_plotly(fig10)
    st.download_button(
        label="📥 Download Monthly Dose Trends Chart",
        data=buf10,
        file_name="monthly_dose_administration_trends.png",
        mime="image/png",
        key="download10"
    )
