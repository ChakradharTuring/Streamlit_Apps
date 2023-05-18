WITH 

data AS (
  SELECT 
    DATE (vp_date) AS date
  , CASE 
      WHEN client_category IN ('Unknown', 'Gold', 'Silver', 'Bronze') THEN 'FSS'
      WHEN client_category = 'Enterprise' THEN 'Platinum'
      ELSE client_category
    END AS client_category
  , COUNT(vp_date) AS devs_count
  FROM turing-230020.curated.job_dev_journey
  WHERE 
    vp_date IS NOT NULL
    AND DATE (vp_date) < CURRENT_DATE()
    AND client_type IS NOT NULL 
    AND client_category IS NOT NULL
    AND is_si_selfserve = 1
  GROUP BY 1, 2
  ORDER BY 1, 2
)

SELECT 
  date
, devs_count
FROM data 
WHERE 
  client_category = '{}'
ORDER BY 1