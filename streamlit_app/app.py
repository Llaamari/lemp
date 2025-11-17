import streamlit as st
import pymysql
import pandas as pd

st.title("Real Data from MySQL (Data Analysis)")

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root
    password="",
    database="testdb
)

# Read real data
df = pd.read_sql("SELECT * FROM temperature_data ORDER BY timestamp DESC", conn)

st.subheader("Temperature Data (Last Measurements)")
st.dataframe(df)

# Optional: line chart
st.subheader("Temperature Trend")
st.line_chart(df.set_index("timestamp")["temperature"])