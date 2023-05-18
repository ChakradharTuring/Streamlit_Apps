WITH 

data AS (
  SELECT 
    DATE_TRUNC (DATE (dsv.timestamp), DAY) AS date
  , dsv.dev_id
  , CASE
    WHEN p1.country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
    ELSE 'ROW' 
    END AS geography
  FROM 
    turing-230020.curated.dev_session_visit_data dsv
    INNER JOIN turing-230020.curated.phase2_dev_level_data p2 ON p2.dev_id = dsv.dev_id
    LEFT JOIN turing-230020.curated.phase1_dev_level_data p1 ON p1.dev_id = dsv.dev_id
)

SELECT 	
  date
, COUNT (DISTINCT dev_id) AS devs_count
FROM data
WHERE 
  dev_id IS NOT NULL 
  AND geography = '{}'
  AND DATE (DATE_TRUNC (date, DAY)) >= '2022-01-01'
  AND DATE (DATE_TRUNC (date, DAY)) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1         