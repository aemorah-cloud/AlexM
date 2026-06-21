# 🚗 Used Car Price Prediction (Big Data & Machine Learning)

A Big Data and Machine Learning project focused on predicting used car prices and clustering similar vehicles using scalable data processing tools and cloud platforms.

---

## 🎯 Project Motivation

Understanding used car pricing is essential for both buyers and sellers. A fair market price helps improve decision-making, reduce overpricing, and increase transparency in the automotive market.

This project aims to:
- Identify pricing patterns in used vehicles
- Analyze key factors such as mileage, year, and horsepower
- Build a predictive model for vehicle price estimation
- Segment vehicles into similar groups using clustering (K-Means)

---

## 🧠 Project Objectives

- Predict used car prices using machine learning models
- Apply clustering (K-Means) to group similar vehicles
- Optimize data processing for large-scale datasets (Big Data workflow)
- Compare cloud data platforms based on performance and cost

---

## ☁️ Technologies Used

- Databricks
- Snowflake
- Google BigQuery
- ClickHouse
- Python (Pandas, Scikit-learn)
- Parquet (optimized storage format)

---

## 📊 Dataset Overview

- Size: **9.29 GB**
- Records: **3,000,040 (~150 GB expanded processing estimate)**
- Region: United States (filtered analysis)
- Format optimization: Converted to **Parquet for efficiency**
- Approach: Sampling used due to computational constraints

---

## ⚙️ Big Data Processing Strategy

Due to dataset size limitations, the following optimizations were applied:

- Data sampling for scalable modeling
- Conversion to Parquet format for faster querying
- Distributed processing considerations
- Reduced memory overhead for feature engineering

---

## 💰 Cloud Cost Comparison

| Platform        | Processing Cost | Storage Cost | Notes |
|----------------|----------------|-------------|-------|
| Databricks     | $36.00         | $3.37       | Spark-based processing |
| Snowflake      | $30.05         | $23.00      | High storage cost |
| BigQuery       | $150.00        | $3.00       | Expensive queries |
| ClickHouse     | $12.00         | $15.00      | Most cost-efficient |

---

## 📈 Key Results

### 🔹 Exploratory Analysis
- Boxplot analysis of **mileage vs price**
- Strong negative correlation between mileage and price
- Correlation heatmap identifying key price drivers

### 🔹 Modeling Insights
- Vehicle price is strongly influenced by:
  - Year (newer = higher price)
  - Mileage (higher mileage = lower price)
  - Horsepower (higher = higher value)

### 🔹 Clustering (K-Means)
- Vehicles grouped into similar market segments
- Helps identify:
  - Budget cars
  - Mid-range vehicles
  - High-end vehicles

---

## 📊 Visual Results

### 📦 Mileage vs Price Distribution
(Add your boxplot image here)

### 🔥 Feature Correlation Heatmap
(Add your heatmap image here)

---

## 🚀 Key Takeaways

- Big Data optimization is essential for large-scale ML projects
- Cloud platform choice significantly impacts cost efficiency
- Parquet format drastically improves processing speed
- Clustering adds business value beyond prediction

---

## 📌 Skills Demonstrated

- Big Data Engineering
- Machine Learning (Regression + Clustering)
- Data Cleaning & Feature Engineering
- Cloud Computing (Databricks, BigQuery, Snowflake)
- Cost-performance analysis
- Data Visualization

---
