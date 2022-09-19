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
    cs.user_id
  , cs.challenge_id
  , di.geography
  , MAX (cs.submit_id) AS submit_id
  FROM 
    turing-230020.devdb_mirror.dv2_challenge_submit cs
    INNER JOIN dev_info di ON di.dev_id = cs.user_id 
  WHERE 
    cs.challenge_id IN (176, 234, 211, 173, 199, 164, 152, 120, 134, 115, 135, 284, 156, 123, 186, 160, 172, 163, 113, 142, 187, 208, 188, 202, 130, 154, 141, 138, 112, 236)
    AND cs.bypass = 0
    GROUP BY 1,2,3
)

, int_table AS (
  SELECT 
    DATE_TRUNC (cs.submit_time, DAY) as date
  , bd.user_id
  , cs.challenge_id
  , bd.geography
  , cs.passed
  FROM 
    turing-230020.devdb_mirror.dv2_challenge_submit cs  
    INNER JOIN base_data bd ON (bd.user_id = cs.user_id AND bd.challenge_id = cs.challenge_id)
  ORDER BY 1 DESC, 2
)

SELECT 
  DATE (DATE_TRUNC (date, DAY)) as date
, COUNT (DISTINCT user_id) as devs_count
FROM int_table
WHERE 
  geography = '{}'
  AND DATE (DATE_TRUNC (date, DAY)) < CURRENT_DATE()
  AND passed = 1
GROUP BY 1
ORDER BY 1