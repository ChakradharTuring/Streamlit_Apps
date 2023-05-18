WITH 

dev_info AS (
  SELECT
    DATE_TRUNC (signup_date, DAY) AS date   
  , CASE
      WHEN country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  , dev_id
FROM turing-230020.curated.phase1_dev_level_data
WHERE 
  signup_date IS NOT NULL
ORDER BY 1, 2
)

, ACC AS (
  SELECT 
    submit_id
  , user_id
  , challenge_id
  , total_time
  , submit_time
  , bypass
  , passed
  , total_score_by_problem
  , total_problem
  , total_score_by_cases
  , LEAD(submit_time) OVER (PARTITION BY user_id, challenge_id ORDER BY submit_time, submit_id) AS lead_submit_time
  , DENSE_RANK() OVER (PARTITION BY user_id, challenge_id, bypass ORDER BY submit_time desc) AS bypass_flag_rank
  FROM 
    turing-230020.raw.dv2_challenge_submit AS dcs 
    INNER JOIN curated.phase1_dev_level_data ON user_id = dev_id
  WHERE 
    submit_id IN (SELECT DISTINCT(submit_id) FROM turing-230020.raw.dv2_problem_submit)  
    AND challenge_id = 220
)

SELECT  
  DATE (DATE_TRUNC (a.submit_time,  DAY)) AS date
, COUNT (DISTINCT a.user_id) AS devs_count,
FROM 
  ACC a
  INNER JOIN dev_info di ON di.dev_id = a.user_id
WHERE 
  di.geography = '{}'
  AND DATE (DATE_TRUNC (a.submit_time, DAY)) < CURRENT_DATE()
  AND (a.lead_submit_time IS NULL OR TIMESTAMP_DIFF(a.lead_submit_time, a.submit_time, HOUR) > 1) 
  AND ((a.bypass = 1) OR (a.bypass = 0 AND a.bypass_flag_rank = 1))
  AND a.total_score_by_cases >= 6
GROUP BY 1
ORDER BY 1