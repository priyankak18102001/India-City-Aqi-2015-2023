import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="India AQI Dashboard", layout="wide")

st.title("India Air Quality Dashboard")

# Load data
df = pd.read_csv("india_city_aqi_2015_2023.csv")

# Convert Date
df["date"] = pd.to_datetime(df["date"])

st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---- KPI Cards ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Cities", df["City"].nunique())
col3.metric("Average AQI", round(df["AQI"].mean(),2))

st.write("---")

# ---- Charts Section ----

st.subheader("AQI Trend Over Time")
st.line_chart(df.set_index("Date")["AQI"])

st.subheader("AQI Distribution (Histogram)")
fig, ax = plt.subplots()
ax.hist(df["AQI"], bins=30)
st.pyplot(fig)

st.subheader("Average AQI by City")
city_avg = df.groupby("City")["AQI"].mean().sort_values()
st.bar_chart(city_avg)

st.subheader("Top 10 Most Polluted Cities")
top_cities = city_avg.sort_values(ascending=False).head(10)
st.bar_chart(top_cities)

st.subheader("PM2.5 Trend")
st.line_chart(df.set_index("Date")["PM2.5"])

st.subheader("PM10 Trend")
st.line_chart(df.set_index("Date")["PM10"])

st.subheader("NO2 Trend")
st.line_chart(df.set_index("Date")["NO2"])

st.subheader("SO2 Trend")
st.line_chart(df.set_index("Date")["SO2"])

st.subheader("CO Trend")
st.line_chart(df.set_index("Date")["CO"])

st.subheader("O3 Trend")
st.line_chart(df.set_index("Date")["O3"])

st.subheader("Correlation Heatmap")
corr = df[["AQI","PM2.5","PM10","NO2","SO2","CO","O3"]].corr()
st.dataframe(corr)

st.subheader("AQI Box Plot")
fig, ax = plt.subplots()
df.boxplot(column="AQI", ax=ax)
st.pyplot(fig)

st.subheader("Monthly AQI Trend")
df["Month"] = df["Date"].dt.to_period("M").astype(str)
monthly = df.groupby("Month")["AQI"].mean()
st.line_chart(monthly)
