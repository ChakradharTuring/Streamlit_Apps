WITH

data AS (
  SELECT 
    dim_date AS date
  , COUNT (DISTINCT Sign_in_failure) / COUNT (DISTINCT Signin_attempt) AS devs_count
  FROM turing-230020.matchingmetrics.product_metrics_pre_throughput_cube_2
  WHERE 
    dim_date IS NOT NULL 
    AND Signin_attempt IS NOT NULL
    AND dim_date < CURRENT_DATE()
    AND dim_client_category IS NOT NULL
  GROUP BY 1
  ORDER BY 1
)

SELECT 
  date
, devs_count
FROM data 
ORDER BY 1