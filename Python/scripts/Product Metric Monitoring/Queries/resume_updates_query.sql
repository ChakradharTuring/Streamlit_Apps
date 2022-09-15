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

, update_data AS (
  SELECT  
    DISTINCT (CAST (i.value AS int64)) AS developer_id
  , MIN (m.created_date) AS created_time
  , MAX (m.updated_date) AS updated_time
  , CASE 
    WHEN DATE (MIN (m.created_date)) < DATE (MAX (m.updated_date)) THEN 'update' 
    ELSE 'first upload' 
    END AS resume_upload_status
  FROM 
    turing-230020.devdb_mirror.metrics  m
    LEFT JOIN turing-230020.devdb_mirror.identity AS i ON i.metric_id = m.id
  WHERE 
    m.category = 'PROFILE_ONBOARDING'
    AND m.name= 'RESUME_UPLOAD' 
    AND i.key = 'action_user_id'
  GROUP BY 1
  ORDER BY resume_upload_status DESC
)

SELECT 
  DATE_TRUNC (DATE (ud.updated_time), DAY) AS date
, COUNT (DISTINCT ud.developer_id) AS devs_count
FROM
  update_data ud
  LEFT JOIN dev_info di ON di.dev_id = ud.developer_id
WHERE 
  ud.resume_upload_status = 'update'
  AND di.geography = '{}'
  AND DATE_TRUNC (DATE (ud.updated_time), DAY) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1