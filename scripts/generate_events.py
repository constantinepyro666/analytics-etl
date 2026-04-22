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

platforms = ["iOS", "Android", "Web"]
events = ["signup", "view_item", "purchase"]

now = datetime.now()

for _ in range(100):
    user_id = random.randint(1, 100)
    event = random.choice(events)
    platform = random.choice(platforms)
    event_time = now - timedelta(minutes=random.randint(0, 60))

    cur.execute("""
        INSERT INTO raw_events (user_id, event_type, event_time, platform)
        VALUES (%s, %s, %s, %s)
    """, (user_id, event, event_time, platform))

conn.commit()
cur.close()
conn.close()
