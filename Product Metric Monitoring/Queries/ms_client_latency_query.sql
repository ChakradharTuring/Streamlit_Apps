WITH

data AS (
  SELECT 
    dim_date AS date
  , metric_ms_fe_search_time_taken_seconds
  FROM turing-230020.matchingmetrics.product_metrics_pre_throughput_cube_3
  WHERE 
    dim_date IS NOT NULL
    AND dim_date < CURRENT_DATE()
  ORDER BY 1
)

SELECT 
  DISTINCT date
, PERCENTILE_DISC (metric_ms_fe_search_time_taken_seconds, 0.5) OVER (PARTITION BY date) AS devs_count
FROM data 
ORDER BY 1