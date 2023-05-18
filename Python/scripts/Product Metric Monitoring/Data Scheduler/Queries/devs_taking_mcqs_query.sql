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

, tech_mcq_challenge_ids AS (
  SELECT
    dcs.user_id AS developer_id
  , dcs.submit_time AS submit_time
  , dcs.challenge_id
  , CASE
      WHEN dcs.challenge_id IN (147, 148, 149, 162, 209) THEN 'Seniority Assessment'
      WHEN dcs.challenge_id IN (22, 124, 126, 143, 189, 190, 200) THEN 'Soft Skills'
      WHEN dcs.challenge_id IN (168, 177, 178, 201, 220) THEN 'LCI Test'
      WHEN dcs.challenge_id = 133 THEN 'Survey'
      ELSE 'Technical'
    END AS challenge_type
  , dcs.passed
  FROM
    turing-230020.raw.dv2_challenge dc
    JOIN turing-230020.raw.dv2_challenge_submit dcs ON dc.challenge_id = dcs.challenge_id
  WHERE
    dcs.challenge_id NOT IN (1, 2, 3, 4, 5, 6, 22, 23, 27, 100)
    AND dcs.challenge_id NOT IN (
      SELECT
        DISTINCT challenge_id
      FROM
        turing-230020.raw.dv2_challenge
      WHERE
        challenge_name LIKE '%ACC%'
   ) 
)

SELECT 
  DATE (DATE_TRUNC (tmc.submit_time, DAY)) as date
, COUNT (DISTINCT tmc.developer_id) as devs_count
FROM 
  tech_mcq_challenge_ids tmc
  INNER JOIN dev_info di ON di.dev_id = tmc.developer_id
WHERE 
  tmc.challenge_type = 'Technical'
  AND di.geography = '{}'
  AND DATE (DATE_TRUNC (tmc.submit_time, DAY)) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1