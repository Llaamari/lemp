import streamlit as st
import pymysql
import pandas as pd
import altair as alt

st.set_page_config(layout="centered", page_title="Data Analysis")

st.title("Real Data from MySQL (Data Analysis)")

# --- DB connection (adjust credentials if needed) ---
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)

# Read data (ensure you select the timestamp column as-is)
df = pd.read_sql("SELECT id, timestamp, temperature FROM temperature_data", conn)
conn.close()

# --- Defensive column handling & renaming ---
# Accept either 'timestamp' or 'Timestamp' from DB
if "timestamp" in df.columns and "Timestamp" not in df.columns:
    df = df.rename(columns={"timestamp": "Timestamp"})
elif "Timestamp" in df.columns and "timestamp" not in df.columns:
    # keep as is
    pass
# Rename other columns if needed
df = df.rename(columns={c: c.capitalize() for c in df.columns if c.lower() in ("id", "temperature")})

# Now ensure the expected column names exist
# After renaming above we expect: 'ID', 'Timestamp', 'Temperature'
# If timestamp column is still lowercase, try both
ts_col = None
for candidate in ("Timestamp", "timestamp", "time", "date"):
    if candidate in df.columns:
        ts_col = candidate
        break

if ts_col is None:
    st.error("No timestamp column found in data. Columns: " + ", ".join(df.columns))
    st.stop()

# --- Parse timestamp robustly ---
# If values are strings with AM/PM or mixed formats, use dayfirst=True to favor dd.mm formats.
df["Timestamp_parsed"] = pd.to_datetime(df[ts_col], dayfirst=True, errors="coerce")

# If parsing failed for many rows, try without dayfirst
if df["Timestamp_parsed"].isna().sum() > 0 and df["Timestamp_parsed"].isna().mean() > 0.5:
    df["Timestamp_parsed"] = pd.to_datetime(df[ts_col], errors="coerce")

# If still NaT values exist, show warning but continue with parsed rows
if df["Timestamp_parsed"].isna().any():
    st.warning("Some timestamp rows could not be parsed and will be ignored in the trend chart.")

# Replace Timestamp with parsed datetime for consistency
df["Timestamp"] = df["Timestamp_parsed"]

# --- Ensure Temperature is numeric ---
if "Temperature" in df.columns:
    df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

# --- Formatting for display table ---
display_df = df.copy()
display_df["Timestamp"] = display_df["Timestamp"].dt.strftime("%d.%m.%Y %H:%M:%S")
# Keep column order and rename for presentation
cols = []
if "ID" in display_df.columns:
    cols.append("ID")
cols.append("Timestamp")
if "Temperature" in display_df.columns:
    cols.append("Temperature")

st.subheader("Temperature Data (Last Measurements)")
st.dataframe(display_df[cols].sort_values("Timestamp", ascending=False).reset_index(drop=True))

# --- Prepare data for trend chart ---
chart_df = df.dropna(subset=["Timestamp", "Temperature"]).copy()
# sort ascending by time
chart_df = chart_df.sort_values("Timestamp")

if chart_df.empty:
    st.info("No valid timestamp+temperature rows available for the trend chart.")
else:
    st.subheader("Temperature Trend (24h time)")

    # Use Altair for precise axis formatting (24h)
    # Create a chart where x is temporal (datetime) and axis formatted to HH:MM
    base = alt.Chart(chart_df).encode(
        x=alt.X("Timestamp:T", axis=alt.Axis(format="%H:%M", title="Time (24h)")),
        y=alt.Y("Temperature:Q", title="Temperature (°C)")
    )

    line = base.mark_line(point=True).interactive()
    st.altair_chart(line.properties(height=400), use_container_width=True)

    # Also show a small stats row
    st.markdown(
        f"**Rows plotted:** {len(chart_df)}  &nbsp; • &nbsp; "
        f"**Min:** {chart_df['Temperature'].min():.2f} °C  &nbsp; • &nbsp; "
        f"**Max:** {chart_df['Temperature'].max():.2f} °C  &nbsp; • &nbsp; "
        f"**Mean:** {chart_df['Temperature'].mean():.2f} °C"
    )