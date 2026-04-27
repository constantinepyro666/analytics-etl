import psycopg2
import os
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- настройки подключения ---
conn = psycopg2.connect(
    dbname="etl",
    user="analyst",
    password="1234",
    host="postgres",  # в docker будет postgres, локально можно localhost
    port="5432"
)

#run_sql("sql/init.sql")

cur = conn.cursor()

# --- порядок выполнения SQL ---
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

# 🔥 ВОТ СЮДА ДОБАВЛЯЕШЬ
print(f"[{datetime.now()}] 🧹 Cleaning old data")

cur.execute("""
DELETE FROM raw_events
WHERE event_time < NOW() - INTERVAL '2 days';
""")

conn.commit()

cur.close()
conn.close()

print(f"[{datetime.now()}] 🎉 ETL finished")
