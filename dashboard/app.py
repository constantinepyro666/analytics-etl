import streamlit as st
import pandas as pd
import psycopg2

# --- подключение к базе ---
conn = psycopg2.connect(
    dbname="etl",
    user="analyst",
    password="1234",
    host="postgres",
    port="5432"
)

# --- заголовок ---
st.title("📊 Product Analytics Dashboard (ETL)")

# =========================
# DAU
# =========================
st.header("DAU (Daily Active Users)")

dau_df = pd.read_sql("SELECT * FROM daily_metrics", conn)

dau_pivot = dau_df.pivot(
    index="date",
    columns="platform",
    values="dau"
)

st.line_chart(dau_pivot)

# =========================
# Retention
# =========================
st.header("Retention")

ret_df = pd.read_sql("SELECT * FROM retention", conn)

st.dataframe(ret_df)

# =========================
# Funnel
# =========================
st.header("Funnel")

funnel_df = pd.read_sql("SELECT * FROM funnel", conn)

st.dataframe(funnel_df)

# =========================
# Debug / Data Preview
# =========================
st.header("Data Preview")

preview_df = pd.read_sql("""
SELECT *
FROM sessions
ORDER BY event_time DESC
LIMIT 100
""", conn)

st.dataframe(preview_df)

# --- закрытие соединения ---
conn.close()
