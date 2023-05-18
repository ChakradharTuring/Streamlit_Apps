WITH 

data AS (
  SELECT 
    DATE (packet_sent_time) AS date
  , client_type
  , CASE 
      WHEN client_category IN ('Unknown', 'Gold', 'Silver', 'Bronze') THEN 'FSS'
      WHEN client_category = 'Enterprise' THEN 'Platinum'
      ELSE client_category
    END AS client_category
  , COUNT(packet_sent_time) AS devs_count
  FROM turing-230020.curated.job_dev_journey
  WHERE 
    packet_sent_time IS NOT NULL
    AND DATE (packet_sent_time) < CURRENT_DATE()
    AND client_type IS NOT NULL 
    AND client_category IS NOT NULL
    AND is_si_selfserve = 0
  GROUP BY 1, 2, 3
  ORDER BY 1, 2, 3
)

SELECT 
  date
, devs_count
FROM data 
WHERE 
  client_category = '{}'
  AND client_type = '{}'
ORDER BY 1