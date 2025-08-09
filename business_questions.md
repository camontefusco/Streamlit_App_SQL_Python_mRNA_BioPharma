
# 📊 Business Questions & Insights

This document outlines practical business questions answered by the mRNA BioPharma Streamlit App and how stakeholders can interact with the data visually.

---

## 👤 Country Lead Insights

| Question                                                                 | How to Explore                                                                 |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Which shipments are delayed or incomplete?                               | View Gantt chart on Shipment Timelines                                         |
| Which countries have the lowest vaccination coverage?                    | Use bar chart: "Vaccination Coverage by Country"                              |
| Are vaccine shipments aligned with contract quantities?                  | Compare Contracted Doses vs Doses Shipped                                     |
| Which contracts are most valuable per capita?                            | Calculate: Contract Value / Population → Bar chart                            |
| What’s the shipment pacing trend over time?                              | Time series chart: Doses shipped per month                                    |

---

## 🩺 Medical Officer Insights

| Question                                                                 | How to Explore                                                                 |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| What % of adverse events are severe or unresolved?                       | Pie chart or grouped bar: Severity categories                                 |
| Are adverse events more frequent in specific age groups?                | Age group filters on event data                                               |
| How does real-world efficacy compare to clinical trials?                | Combine vaccination outcome + trial outcomes                                  |
| Which vaccine types have most adverse reports?                          | Filter: Adverse Events by Vaccine Type                                        |
| What is the average time to resolve events?                             | Bar chart: Days to resolution by severity                                     |

---

## 📈 Market Analyst Insights

| Question                                                                 | How to Explore                                                                 |
|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Which countries generate the highest revenue per 1,000 people?          | Bar chart: Revenue / Population × 1000                                        |
| What is the average price per dose by income group?                     | Grouped bar: Price vs Income Tier                                             |
| Are some vaccines more profitable than others?                          | Compare revenue by Vaccine Type                                               |
| What’s the revenue trend over time?                                     | Line chart: Contract Date vs Revenue                                          |
| Which countries receive bulk discounts?                                 | Compare Price per Dose vs Contract Volume                                     |

---

## 🌍 Geospatial Insights

| Insight                                              | How to Explore                                  |
|------------------------------------------------------|--------------------------------------------------|
| Where is coverage highest?                           | Use st.map or PyDeck radius chart by coverage   |
| Which countries report more severe adverse events?   | Map: Color by severity + bubble size by count   |
| Are low-income countries underreporting?             | Filter: Event Rate / Administered Doses         |

---

## 📄 Exportable Insights

- Every filtered chart or table can be exported to **PDF**
- Use the export button on each section of the app

---

Built for stakeholders who need data-driven clarity — without writing SQL.

