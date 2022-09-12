WITH 

dev_info AS (
  SELECT
    dev_id
  , DATE_TRUNC (signup_date, DAY) AS signup_date
  , CASE
      WHEN country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  FROM turing-230020.analytics_views.phase1_dev_level_data
)
  
SELECT 
  DATE (DATE_TRUNC (p2.phase2_entry_date, DAY)) AS date
, COUNT(di.dev_id) as devs_count
FROM turing-230020.analytics_views.phase2_dev_level_data p2
  LEFT JOIN dev_info di ON p2.dev_id = di.dev_id
WHERE 
  DATE (DATE_TRUNC (p2.phase2_entry_date, DAY)) < CURRENT_DATE()
  AND di.geography = '{}'
GROUP BY 1
ORDER BY 1