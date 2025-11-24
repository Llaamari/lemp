import streamlit as st
import pymysql
import pandas as pd

st.title("Data Analysis: Weather + Currency + Temperature Data")

# --- WEATHER DATA ---
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="weather_db"
)
df_weather = pd.read_sql("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50", conn)
conn.close()

st.subheader("Weather Data (Helsinki)")
st.dataframe(df_weather)

# --- CURRENCY TREND WITH SELECTBOX AND ALTair ---

st.subheader("EUR Exchange Rate Trend")

# User selects currency from dropdown
available_currencies = sorted(df_fx["currency"].unique())

selected_currency = st.selectbox(
    "Select currency:",
    available_currencies,
    index=0
)

# Filter selected currency
df_selected = df_fx[df_fx["currency"] == selected_currency].copy()

# Ensure timestamp is datetime
df_selected["timestamp"] = pd.to_datetime(df_selected["timestamp"])
df_selected = df_selected.sort_values("timestamp")

# Rename for chart axis clarity
df_selected = df_selected.rename(columns={"timestamp": "Timestamp", "rate": "Rate"})

# Create Altair chart
import altair as alt

currency_chart = alt.Chart(df_selected).mark_line(point=True).encode(
    x=alt.X("Timestamp:T", title="Time"),
    y=alt.Y("Rate:Q", title=f"EUR → {selected_currency}"),
    tooltip=[
        alt.Tooltip("Timestamp:T", title="Time"),
        alt.Tooltip("Rate:Q", title="Rate"),
        alt.Tooltip("currency:N", title="Currency")
    ]
).properties(
    width="container",
    height=400
).interactive()

st.altair_chart(currency_chart, use_container_width=True)

# --- TEMPERATURE DATA ---
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
df_temp = pd.read_sql("SELECT * FROM temperature_data ORDER BY timestamp DESC", conn)
conn.close()

# Rename columns
df_temp = df_temp.rename(columns={
    "id": "ID",
    "timestamp": "Timestamp",
    "temperature": "Temperature"
})

# Convert timestamp to datetime
df_temp["Timestamp"] = pd.to_datetime(df_temp["Timestamp"])

# Create formatted timestamp for display table
df_temp["Timestamp_formatted"] = df_temp["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

# Display formatted table
st.subheader("Temperature Data (Last Measurements)")
st.dataframe(
    df_temp[["ID", "Timestamp_formatted", "Temperature"]].rename(
        columns={"Timestamp_formatted": "Timestamp"}
    )
)

# Trend chart
st.subheader("Temperature Trend")
st.line_chart(df_temp.set_index("Timestamp")["Temperature"])