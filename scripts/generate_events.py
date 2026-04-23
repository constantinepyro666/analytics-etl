import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname="etl",
    user="analyst",
    password="1234",
    host="postgres",
    port="5432"
)

cur = conn.cursor()

# --- настройки ---
NUM_USERS = 200
DAYS_BACK = 7
EVENTS_PER_RUN = 3000

platforms = ["iOS", "Android", "Web"]

now = datetime.now()

# фиксированный пул пользователей (для retention)
users = list(range(1, NUM_USERS + 1))

for _ in range(EVENTS_PER_RUN):
    user_id = random.choice(users)

    # распределение событий (похоже на реальность)
    event_type = random.choices(
        ["signup", "view_item", "purchase"],
        weights=[0.2, 0.6, 0.2]
    )[0]

    platform = random.choice(platforms)

    # распределяем события по дням
event_time = datetime.now() - timedelta(
    days=random.randint(0, DAYS_BACK),
    hours=random.randint(0, 23),
    minutes=random.randint(0, 59)
)

    cur.execute("""
        INSERT INTO raw_events (user_id, event_type, event_time, platform)
        VALUES (%s, %s, %s, %s)
    """, (user_id, event_type, event_time, platform))

conn.commit()
cur.close()
conn.close()

print("✅ Events generated")
