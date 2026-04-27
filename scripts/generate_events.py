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
BASE_USERS = 150
NEW_USERS_PER_RUN = random.randint(5, 20)
CHURN_RATE = 0.05
EVENTS_PER_RUN = 2000

platforms = ["iOS", "Android", "Web"]

# --- получаем текущих пользователей из базы ---
cur.execute("SELECT DISTINCT user_id FROM raw_events")
existing_users = [row[0] for row in cur.fetchall()]

if not existing_users:
    existing_users = list(range(1, BASE_USERS + 1))

# --- churn (часть пользователей уходит) ---
active_users = [
    u for u in existing_users
    if random.random() > CHURN_RATE
]

# --- новые пользователи ---
max_user_id = max(active_users) if active_users else 0
new_users = list(range(max_user_id + 1, max_user_id + 1 + NEW_USERS_PER_RUN))

users = active_users + new_users

now = datetime.now()

for _ in range(EVENTS_PER_RUN):

    user_id = random.choice(users)

    # --- жизненный цикл пользователя ---
    if user_id in new_users:
        event_type = "signup"
    else:
        event_type = random.choices(
            ["view_item", "purchase"],
            weights=[0.8, 0.2]
        )[0]

    # --- активность пользователей разная ---
    activity_boost = random.random()

    if activity_boost < 0.2:
        # очень активные (сегодня)
        event_time = now - timedelta(
            minutes=random.randint(0, 120)
        )
    elif activity_boost < 0.6:
        # обычные (сегодня)
        event_time = now - timedelta(
            hours=random.randint(0, 24)
        )
    else:
        # редкие (несколько дней назад)
        event_time = now - timedelta(
            days=random.randint(1, 7),
            hours=random.randint(0, 23)
        )

    platform = random.choices(
        platforms,
        weights=[0.3, 0.5, 0.2]
    )[0]

    cur.execute("""
        INSERT INTO raw_events (user_id, event_type, event_time, platform)
        VALUES (%s, %s, %s, %s)
    """, (user_id, event_type, event_time, platform))

conn.commit()
cur.close()
conn.close()

print(f"✅ Events generated | users={len(users)} new={len(new_users)}")
