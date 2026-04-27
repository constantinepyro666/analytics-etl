import psycopg2
import os
from datetime import datetime

# 🔥 ОБЯЗАТЕЛЬНО СЮДА (глобально)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- подключение ---
conn = psycopg2.connect(
    dbname="etl",
    user="analyst",
    password="1234",
    host="postgres",
    port="5432"
)

cur = conn.cursor()

sql_files = [
    "sql/clean_events.sql",
    "sql/sessions.sql",
    "sql/daily_metrics.sql",
    "sql/funnel.sql",
    "sql/retention.sql"
]

print(f"[{datetime.now()}] 🚀 ETL started")

for file in sql_files:
    try:
        file_path = os.path.join(BASE_DIR, file)

        print(f"[{datetime.now()}] ▶ Running {file_path}")

        with open(file_path, "r") as f:
            sql = f.read()

        cur.execute(sql)
        conn.commit()

        print(f"[{datetime.now()}] ✅ Finished {file}")

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error in {file}: {e}")
        conn.rollback()

# очистка
print(f"[{datetime.now()}] 🧹 Cleaning old data")

cur.execute("""
DELETE FROM raw_events
WHERE event_time < NOW() - INTERVAL '2 days';
""")

conn.commit()

cur.close()
conn.close()

print(f"[{datetime.now()}] 🎉 ETL finished")
