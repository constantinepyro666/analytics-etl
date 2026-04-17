DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions AS
WITH ordered_events AS (
    SELECT
        user_id,
        event_type,
        event_time,
        platform,

        LAG(event_time) OVER (
            PARTITION BY user_id
            ORDER BY event_time
        ) AS prev_time

    FROM clean_events
),

session_flags AS (
    SELECT *,
        CASE
            WHEN prev_time IS NULL THEN 1
            WHEN event_time - prev_time > INTERVAL '30 minutes' THEN 1
            ELSE 0
        END AS is_new_session
    FROM ordered_events
),

session_numbers AS (
    SELECT *,
        SUM(is_new_session) OVER (
            PARTITION BY user_id
            ORDER BY event_time
        ) AS session_id
    FROM session_flags
)

SELECT
    user_id,
    event_type,
    event_time,
    platform,
    session_id
FROM session_numbers;
