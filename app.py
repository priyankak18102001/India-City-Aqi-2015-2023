import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="India AQI Dashboard", layout="wide")

st.title("India Air Quality Dashboard")

# Load data
df = pd.read_csv("india_city_aqi_2015_2023.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Convert Date column
df["date"] = pd.to_datetime(df["date"])

st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---- KPI Cards ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Cities", df["city"].nunique())
col3.metric("Average AQI", round(df["aqi"].mean(), 2))

st.write("---")

# ---- AQI Trend ----
st.subheader("AQI Trend Over Time")
st.line_chart(df.set_index("date")["aqi"])

st.write(
    f"Insight: The average AQI across all records is **{round(df['aqi'].mean(),2)}**. "
    "This chart shows how air quality changes over time."
)

# ---- Histogram ----
st.subheader("AQI Distribution (Histogram)")
fig, ax = plt.subplots()
ax.hist(df["aqi"], bins=30)
st.pyplot(fig)

st.write(
    "Insight: The histogram shows how AQI values are distributed. "
    "If most values are in higher bins, it means pollution levels are generally high."
)

# ---- Average AQI by City ----
st.subheader("Average AQI by City")
city_avg = df.groupby("city")["aqi"].mean().sort_values()
st.bar_chart(city_avg)

st.write(
    f"Insight: The city with highest average AQI is **{city_avg.idxmax()}**, "
    "which indicates higher pollution compared to other cities."
)

# ---- Top Polluted Cities ----
st.subheader("Top 10 Most Polluted Cities")
top_cities = city_avg.sort_values(ascending=False).head(10)
st.bar_chart(top_cities)

st.write(
    "Insight: These cities consistently record higher AQI values and may need stronger pollution control measures."
)

# ---- Pollutant Trends ----
pollutants = ["pm2.5", "pm10", "no2", "so2", "co", "o3"]

for pol in pollutants:
    if pol in df.columns:
        st.subheader(f"{pol.upper()} Trend")
        st.line_chart(df.set_index("date")[pol])
        st.write(
            f"Insight: This chart shows how {pol.upper()} levels change over time and how it may impact AQI."
        )

# ---- Correlation ----
st.subheader("Correlation Table")
corr_cols = [col for col in ["aqi","pm2.5","pm10","no2","so2","co","o3"] if col in df.columns]
corr = df[corr_cols].corr()
st.dataframe(corr)

st.write(
    "Insight: Higher correlation values indicate pollutants that strongly influence AQI."
)

# ---- Box Plot ----
st.subheader("AQI Box Plot")
fig, ax = plt.subplots()
df.boxplot(column="aqi", ax=ax)
st.pyplot(fig)

st.write(
    "Insight: The box plot shows median AQI and spread. "
    "Outliers represent days with extremely high pollution."
)

# ---- Monthly Trend ----
st.subheader("Monthly AQI Trend")
df["month"] = df["date"].dt.to_period("M").astype(str)
monthly = df.groupby("month")["aqi"].mean()
st.line_chart(monthly)

st.write(
    "Insight: Monthly trend helps identify seasonal patterns in air quality."
)
