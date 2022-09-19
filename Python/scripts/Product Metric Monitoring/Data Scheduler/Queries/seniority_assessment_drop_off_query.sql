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
  , challenge_id 
  , MAX (track_challenge_id) AS track_challenge_id
  FROM turing-230020.devdb_mirror.dv2_track_challenge
  GROUP BY 1, 2
)
  
, int_table AS (
  SELECT 
    bd.user_id
  , bd.challenge_id
  , c.challenge_name
  , dtc.start_at AS attempt_date
  , dtc.current_step 
  , (LENGTH (dtc.randomized_problems) - LENGTH (REPLACE (dtc.randomized_problems, ",", "")) + 1) as total_mcqs
  FROM 
    base_data as bd
    LEFT JOIN turing-230020.devdb_mirror.dv2_track_challenge AS dtc ON dtc.track_challenge_id = bd.track_challenge_id and dtc.user_id = bd.user_id
    INNER JOIN turing-230020.devdb_mirror.dv2_challenge c on c.challenge_id = bd.challenge_id
)

, data AS (
  SELECT 
    it.* EXCEPT (current_step, total_mcqs)
  , CASE 
      WHEN current_step < total_mcqs THEN 1 
      ELSE 0 
    END AS is_drop_off
  , di.geography
  FROM 
    int_table it
    INNER JOIN dev_info di ON di.dev_id = it.user_id
  WHERE 
    it.challenge_id NOT IN (218, 220, 201)
    AND it.challenge_name NOT LIKE '%ACC%'
  ORDER BY 1, 2
)    

SELECT 
  DATE (DATE_TRUNC (attempt_date, DAY)) as date
, (COUNT (DISTINCT IF (is_drop_off = 1, user_id, NULL))) / COUNT (DISTINCT user_id) AS devs_count
FROM data
WHERE 
  challenge_id IN (147, 148, 149, 162, 209)
  AND geography = '{}'
  AND DATE (DATE_TRUNC (attempt_date, DAY)) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1