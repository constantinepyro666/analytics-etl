import pandas as pd
import random
from datetime import datetime, timedelta

NUM_USERS = 1000
EVENTS = ["signup", "view_item", "purchase"]

data = []

start_date = datetime.now() - timedelta(days=7)

for user_id in range(1, NUM_USERS + 1):
    platform = random.choice(["iOS", "Android", "Web"])

    # signup
    signup_time = start_date + timedelta(minutes=random.randint(0, 10000))
    data.append([user_id, "signup", signup_time, platform])

    # несколько событий
    for _ in range(random.randint(1, 5)):
        event_type = random.choice(EVENTS)

        # 💩 добавляем ошибки
        if random.random() < 0.1:
            event_type = None  # null

        if random.random() < 0.1:
            event_type = random.choice(["Signup", "sign_up", "singup"])  # кривые названия

        event_time = signup_time + timedelta(days=random.randint(0, 5))

        row = [user_id, event_type, event_time, platform]
        data.append(row)

        # дубликаты
        if random.random() < 0.1:
            data.append(row)

df = pd.DataFrame(data, columns=["user_id", "event_type", "event_time", "platform"])

df.to_csv("data/raw_events.csv", index=False)

print("Raw data generated!")
