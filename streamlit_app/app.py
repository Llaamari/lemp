import streamlit as st
import pymysql
import pandas as pd

st.title("Real Data from MySQL (Data Analysis)")

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)

# Read real data
df = pd.read_sql("SELECT * FROM temperature_data ORDER BY timestamp DESC", conn)

# Convert timestamp to proper datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Rename columns
df = df.rename(columns={
    "id": "ID",
    "timestamp": "Timestamp",
    "temperature": "Temperature"
})

# Display table with formatted timestamp
df["Timestamp_formatted"] = df["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

st.subheader("Temperature Data (Last Measurements)")
st.dataframe(
    df[["ID", "Timestamp_formatted", "Temperature"]].rename(
        columns={"Timestamp_formatted": "Timestamp"}
    )
)

# --- FIX FOR 24H AXIS IN TREND CHART ---

# Create a copy for charting
df_chart = df.copy()

# Ensure Timestamp is datetime AND in 24h format
df_chart["Timestamp"] = pd.to_datetime(df_chart["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"))

st.subheader("Temperature Trend")
st.line_chart(
    df_chart.set_index("Timestamp")["Temperature"]
)