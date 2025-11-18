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

# Rename columns
df = df.rename(columns={
    "id": "ID",
    "timestamp": "Timestamp",
    "temperature": "Temperature"
})

# Convert timestamp to format dd.mm.yyyy HH:MM:SS
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Timestamp_formatted"] = df["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

# Display formatted table
st.subheader("Temperature Data (Last Measurements)")
st.dataframe(
    df[["ID", "Timestamp_formatted", "Temperature"]].rename(
        columns={"Timestamp_formatted": "Timestamp"}
    )
)

# Trend chart (24h time format)
df_trend = df.copy()
df_trend["Timestamp_24h"] = df_trend["Timestamp"].dt.strftime("%H:%M")

st.subheader("Temperature Trend")
st.line_chart(
    df_trend.set_index("Timestamp")["Temperature"]
)