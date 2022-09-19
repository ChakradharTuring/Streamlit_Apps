WITH 

dev_info AS (
  SELECT
    DATE_TRUNC (signup_date, DAY) AS date   
  , CASE
      WHEN country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  , dev_id
FROM turing-230020.analytics_views.phase1_dev_level_data
WHERE 
  signup_date IS NOT NULL
ORDER BY 1, 2
)

, base_data AS ( 
  SELECT 
    user_id
  , MAX (submit_id) AS submit_id
  FROM turing-230020.devdb_mirror.dv2_challenge_submit
  WHERE challenge_id = 220
  GROUP BY 1
)

SELECT 
  DATE (DATE_TRUNC (cs.submit_time, DAY)) AS date
, (COUNT (DISTINCT IF (auto_submit = 'user_quit', cs.user_id, NULL))) / (COUNT (DISTINCT cs.user_id)) AS devs_count
FROM 
  turing-230020.devdb_mirror.dv2_challenge_submit cs
  INNER JOIN turing-230020.devdb_mirror.dv2_problem_submit ps ON ps.submit_id = cs.submit_id
  INNER JOIN dev_info di on di.dev_id = cs.user_id 
WHERE 
  cs.submit_id IN (SELECT DISTINCT submit_id FROM base_data)
  AND di.geography = 'LATAM'
  AND DATE (DATE_TRUNC (cs.submit_time, DAY)) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1