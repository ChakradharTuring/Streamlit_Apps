WITH 

data AS (
  SELECT 
    dim_date AS date
  , dim_client_type AS client_type
  , dim_client_category AS client_category
  , SUM(metrics_ms_interview_happened) AS devs_count
  FROM turing-230020.matchingmetrics.product_metrics_throughput_cube_1
  WHERE 
    dim_date IS NOT NULL 
    AND metrics_ms_interview_happened IS NOT NULL
    AND dim_date < CURRENT_DATE()
    AND dim_client_type IS NOT NULL 
    AND dim_client_category IS NOT NULL
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