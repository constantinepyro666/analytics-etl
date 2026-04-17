DROP TABLE IF EXISTS daily_metrics;

CREATE TABLE daily_metrics AS
SELECT
    DATE(event_time) AS date,
    platform,
    COUNT(DISTINCT user_id) AS dau
FROM sessions
GROUP BY date, platform
ORDER BY date, platform;
