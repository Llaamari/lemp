import streamlit as st
import pymysql
import pandas as pd
import altair as alt
import time
from datetime import datetime


# ============================================================
#  AUTO-REFRESH (WORKS IN STREAMLIT 1.51.0)
# ============================================================

REFRESH_INTERVAL = 60  # seconds

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()


# ============================================================
#  PAGE SETTINGS
# ============================================================

st.set_page_config(
    layout="centered",
    page_title="Data Analysis Dashboard"
)

st.title("Data Analysis: Weather + Currency + Temperature Data")


# Tabs
weather_tab, fx_tab, temp_tab = st.tabs([
    "🌦 Weather (Oulu)",
    "💱 Exchange Rates",
    "🌡 Temperature"
])


# ============================================================
#  WEATHER TAB
# ============================================================

with weather_tab:
    st.header("Weather Data (Oulu)")

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="weather_db"
    )
    df_weather = pd.read_sql(
        "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50",
        conn
    )
    conn.close()

    # Rename columns
    df_weather = df_weather.rename(columns={
        "id": "ID",
        "city": "City",
        "temperature": "Temperature",
        "description": "Description",
        "timestamp": "Timestamp"
    })

    # Format timestamp (DD.MM.YYYY HH:MM:SS)
    df_weather["Timestamp"] = pd.to_datetime(df_weather["Timestamp"])
    df_weather["Timestamp"] = df_weather["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

    st.dataframe(df_weather, use_container_width=False)


# ============================================================
#  EXCHANGE RATES TAB
# ============================================================

with fx_tab:
    st.header("Exchange Rates (EUR Base)")

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )
    df_fx = pd.read_sql(
        "SELECT * FROM exchange_rates ORDER BY timestamp DESC LIMIT 200",
        conn
    )
    conn.close()

    # Rename columns
    df_fx = df_fx.rename(columns={
        "id": "ID",
        "base": "Base",
        "currency": "Currency",
        "rate": "Rate",
        "timestamp": "Timestamp"
    })

    df_fx["Timestamp"] = pd.to_datetime(df_fx["Timestamp"])
    df_fx["Timestamp"] = df_fx["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

    st.subheader("Latest Exchange Rate Entries")
    st.dataframe(df_fx, use_container_width=False)

    # Dropdown for currency selection
    st.subheader("EUR Exchange Rate Trend")

    currencies = sorted(df_fx["Currency"].unique())
    selected_currency = st.selectbox("Select currency:", currencies)

    df_selected = df_fx[df_fx["Currency"] == selected_currency].copy()

    # Convert timestamp back to datetime for chart
    df_selected["Timestamp"] = pd.to_datetime(df_selected["Timestamp"])
    df_selected = df_selected.sort_values("Timestamp")
    df_selected = df_selected.rename(columns={"Rate": "RateValue"})

    chart = alt.Chart(df_selected).mark_line(point=True).encode(
        x=alt.X("Timestamp:T", title="Time"),
        y=alt.Y("RateValue:Q", title=f"EUR → {selected_currency}"),
        tooltip=[
            alt.Tooltip("Timestamp:T", title="Time"),
            alt.Tooltip("RateValue:Q", title="Rate"),
            alt.Tooltip("Currency:N", title="Currency")
        ]
    ).properties(height=400).interactive()

    st.altair_chart(chart, use_container_width=True)


# ============================================================
#  TEMPERATURE TAB
# ============================================================

with temp_tab:
    st.header("Temperature Measurements")

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="testdb"
    )
    df_temp = pd.read_sql(
        "SELECT * FROM temperature_data ORDER BY timestamp DESC",
        conn
    )
    conn.close()

    df_temp = df_temp.rename(columns={
        "id": "ID",
        "timestamp": "Timestamp",
        "temperature": "Temperature"
    })

    df_temp["Timestamp"] = pd.to_datetime(df_temp["Timestamp"])
    df_temp["Timestamp_formatted"] = df_temp["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")

    data_tab, trend_tab = st.tabs(["📄 Data Table", "📈 Trend"])

    with data_tab:
        st.subheader("Latest Temperature Readings")
        st.dataframe(
            df_temp[["ID", "Timestamp_formatted", "Temperature"]]
            .rename(columns={"Timestamp_formatted": "Timestamp"}),
            use_container_width=False
        )

    with trend_tab:
        st.subheader("Temperature Trend")
        st.line_chart(df_temp.set_index("Timestamp")["Temperature"])
