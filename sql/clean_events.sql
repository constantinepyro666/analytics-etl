DROP TABLE IF EXISTS clean_events;

CREATE TABLE clean_events AS
SELECT DISTINCT
    user_id,

    CASE
        WHEN LOWER(event_type) IN ('signup', 'sign_up', 'singup') THEN 'signup'
        WHEN LOWER(event_type) IN ('view_item', 'view') THEN 'view_item'
        WHEN LOWER(event_type) = 'purchase' THEN 'purchase'
        ELSE NULL
    END AS event_type,

    event_time,
    platform

FROM raw_events
WHERE user_id IS NOT NULL
  AND event_time IS NOT NULL;

DELETE FROM clean_events
WHERE event_type IS NULL;
