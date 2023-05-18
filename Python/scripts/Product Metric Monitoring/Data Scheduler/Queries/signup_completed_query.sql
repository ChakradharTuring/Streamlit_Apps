WITH 

dev_info AS (
  SELECT
    dev_id
  , DATE_TRUNC(signup_date, DAY) AS signup_date
  , CASE
      WHEN country IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  FROM turing-230020.curated.phase1_dev_level_data
)

, finish_button AS (
  SELECT
    DISTINCT (CAST (value AS int64)) AS developer_id
  , MIN(created_date) AS finish_signup_date
  FROM turing-230020.raw.metrics AS m
    LEFT JOIN turing-230020.raw.identity AS i ON i.metric_id = m.id
  WHERE
    name = 'ONBOARDING_PAGE_2_SAVE_INFO'
    AND KEY = 'action_user_id'
  GROUP BY 1
)

--Signup completed 
SELECT 
  DATE(fb.finish_signup_date) AS date
, COUNT(DISTINCT developer_id) AS devs_count
FROM dev_info di 
  LEFT JOIN finish_button fb on di.dev_id = fb.developer_id
WHERE 
  fb.finish_signup_date IS NOT NULL
  AND DATE(fb.finish_signup_date) < CURRENT_DATE()
  AND di.geography = '{}'
GROUP BY 1 
ORDER BY 1