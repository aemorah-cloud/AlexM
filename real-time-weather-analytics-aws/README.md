# 🌦️ Serverless Weather ETL Dashboard (AWS)

> ⚠️ **Work in Progress (WIP)**  
This project is currently under active development.

---

## 📌 Overview

This project is a **serverless data engineering pipeline** built on AWS that collects real-time weather data, processes it through an ETL workflow, and visualizes insights using a Streamlit dashboard.

The goal is to simulate a real-world **data lake + analytics architecture** using modern cloud tools.

---

## 🧱 Architecture

The system follows a full end-to-end data pipeline:

**Data Flow:**

Weather API  
→ AWS Lambda (hourly ingestion)  
→ Amazon S3 (raw data storage)  
→ AWS Glue (ETL transformation)  
→ Amazon Athena (SQL querying)  
→ Streamlit Dashboard (visualization)

---

## ⚙️ Tech Stack

- ☁️ AWS Lambda – serverless data ingestion
- 🪣 Amazon S3 – raw & processed data storage
- 🔄 AWS Glue – ETL processing & schema catalog
- 📊 Amazon Athena – SQL queries on data lake
- 🐍 Python – backend logic & data processing
- 📈 Streamlit – interactive dashboard
- 🌍 Weather API – real-time external data source

---

## 🚀 Features (Planned / In Progress)

- Hourly automated weather data ingestion
- Scalable S3-based data lake
- ETL pipeline using AWS Glue
- Query engine using Athena SQL
- Interactive dashboard with trends & insights
- Multi-city weather comparison (future enhancement)

---

## 🏗️ Project Status

| Component | Status |
|----------|--------|
| Lambda ingestion | 🚧 In progress |
| S3 data storage | 🚧 In progress |
| Glue ETL | ⏳ Pending |
| Athena queries | ⏳ Pending |
| Streamlit dashboard | ⏳ Pending |

---

## 📂 Repository Structure (Planned)

```bash
aws-weather-etl-pipeline/
│
├── lambda/                # AWS Lambda ingestion function
├── glue/                  # Glue ETL scripts
├── athena/                # SQL queries
├── streamlit_app/        # Dashboard frontend
├── data/                 # Sample data (optional)
├── docs/                 # Architecture diagrams
└── README.md
