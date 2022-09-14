WITH 

data AS (
  SELECT
    DATE_TRUNC(signup_date, DAY) AS date   
  , CASE
      WHEN country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  , COUNT(*) AS devs_count
FROM turing-230020.analytics_views.phase1_dev_level_data
WHERE 
  DATE (DATE_TRUNC(signup_date, DAY)) < CURRENT_DATE()
GROUP BY 1, 2
ORDER BY 1, 2
)

SELECT 
  date
, devs_count
FROM data 
WHERE 
  geography = '{}'
ORDER BY 1