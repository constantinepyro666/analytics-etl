DROP TABLE IF EXISTS funnel;

CREATE TABLE funnel AS
SELECT
    platform,

    COUNT(DISTINCT CASE WHEN event_type = 'signup' THEN user_id END) AS signup,

    COUNT(DISTINCT CASE WHEN event_type = 'view_item' THEN user_id END) AS view_item,

    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchase

FROM sessions
GROUP BY platform;
