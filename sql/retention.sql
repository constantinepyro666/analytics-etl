DROP TABLE IF EXISTS retention;

CREATE TABLE retention AS
WITH first_visit AS (
    SELECT
        user_id,
        MIN(DATE(event_time)) AS cohort_date
    FROM sessions
    GROUP BY user_id
),
activity AS (
    SELECT
        s.user_id,
        DATE(s.event_time) AS activity_date,
        f.cohort_date,
        DATE(s.event_time) - f.cohort_date AS day
    FROM sessions s
    JOIN first_visit f USING(user_id)
)
SELECT
    cohort_date,
    day,
    COUNT(DISTINCT user_id) AS users
FROM activity
GROUP BY cohort_date, day
ORDER BY cohort_date, day;
