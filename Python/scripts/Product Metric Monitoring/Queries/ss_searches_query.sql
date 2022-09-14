WITH

data AS (
  SELECT 
    dim_date AS date
  , dim_client_category AS client_category
  , COUNT (DISTINCT Query_made) AS devs_count
  FROM turing-230020.matchingmetrics.product_metrics_pre_throughput_cube_2
  WHERE 
    dim_date IS NOT NULL 
    AND Query_made IS NOT NULL
    AND dim_date < CURRENT_DATE()
    AND dim_client_category IS NOT NULL
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