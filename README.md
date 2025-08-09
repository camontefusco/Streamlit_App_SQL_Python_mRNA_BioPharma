# Streamlit_App_SQL_Python_mRNA_BioPharma
# 🧬 mRNA Biopharma Streamlit App

**An interactive, multi-page Streamlit app for exploring synthetic mRNA vaccine data — trials, shipments, contracts, coverage, and adverse events.**

![Banner](banner.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/your-username/SQL_Tableau_mRNA_BioPharma_DB/main/app.py)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📊 What This App Does

This no-code-friendly app helps:
- 💉 **Pharmacists** track vaccination coverage, shipments, and second-dose drop-offs.
- 🧪 **Medical officers** analyze clinical trial data, efficacy, and adverse events.
- 📈 **Market analysts** estimate revenue, price per dose, and country comparisons.
- 🌍 **Country leads** monitor vaccine delivery performance and population impact.

## 🧱 Tech Stack

| Area              | Tools Used                             |
|-------------------|----------------------------------------|
| **Frontend UI**   | Streamlit (multi-page)                 |
| **Database**      | MySQL with SQLAlchemy ORM              |
| **Visualization** | Plotly, PyDeck, native Streamlit charts |
| **Mapping**       | PyDeck Choropleth + name-corrections   |
| **Styling**       | Custom CSS: dark theme, DNA/molecule visuals |
| Map Enhancements  | Country name alignment and time-based choropleth aggregation                |

---

## 🧰 Features

- ✅ CRUD (Create, Read, Update, Delete) operations on all major entities
- 🗂 Dashboard navigation across Vaccinations, Trials, Events, Shipments
- 📅 Date filters and range pickers on all charts
- 🌍 Geo Maps showing vaccine coverage and event severity by country
- 🧠 Context-aware dropdowns (e.g., country names pulled from database)

---

## 🧑‍💼 Business Value

| Role               | Key Insights Provided                        |
|-------------------|-----------------------------------------------|
| Country Lead      | Identify coverage gaps or shipment delays      |
| Medical Officer   | Track trends in severe adverse events          |
| Market Analyst    | Understand contract performance by country     |
| Decision Makers   | Access visual, exportable data for briefings   |

More insights in the `/docs/business_questions.md`.

---

## 📂 Folder Structure
```bash
📦mRNA_BioPharma_App
├── /app/
│ ├── Home.py
│ ├── Create.py
│ ├── Read.py
│ ├── Update.py
│ ├── Delete.py
│ ├── Visualize.py
│ └── Map.py
├── /data/
│ ├── synthetic_countries.csv
│ ├── synthetic_contracts.csv
│ ├── synthetic_clinical_trials.csv
│ ├── synthetic_shipments.csv
│ ├── synthetic_vaccinations.csv
│ └── adverse_events.csv
├── /sql/
│ ├── mRNA_BioPharma_DB_SQLSchema.sql
│ └── SQL_queries.sql
├── /docs/
│ ├── Homepage.png
│ ├── Visual Analytics.png
│ ├── mRNA Vaccination Data Map.png
│ └── business_questions.md
├── requirements.txt
└── README.md
```

## ⚙️ Local Setup

### ✅ Prerequisites

```yaml
- Python 3.9+
- MySQL or SQLite
- Streamlit: `pip install streamlit`
```
### ▶️ Run App Locally

```bash
git clone https://github.com/camontefusco/SQL_Tableau_mRNA_BioPharma_DB.git
cd SQL_Tableau_mRNA_BioPharma_DB
pip install -r requirements.txt
streamlit run app/Main.py
```

## 🧪 Sample SQL Query
```sql
-- Total contracted revenue by country
SELECT country_name, SUM(total_doses * price_per_dose) AS total_revenue
FROM Contracts
JOIN countries_real USING (country_id)
GROUP BY country_name;
```

## 📬 Contact
Carlos Montefusco
📧 cmontefusco@gmail.com
🔗 GitHub: /camontefusco

## 📄 License
MIT License

Built with ❤️ using Python, Streamlit, SQL, and lots of open-source data inspiration.
