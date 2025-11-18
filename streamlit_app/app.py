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

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Create formatted timestamp for display table
df["Timestamp_formatted"] = df["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

# Display formatted table without index column (0,1,2...)
st.subheader("Temperature Data (Last Measurements)")
st.dataframe(
    df[["ID", "Timestamp_formatted", "Temperature"]]
      .rename(columns={"Timestamp_formatted": "Timestamp"})
      .reset_index(drop=True)
)

# Trend chart
st.subheader("Temperature Trend")
st.line_chart(df.set_index("Timestamp")["Temperature"])