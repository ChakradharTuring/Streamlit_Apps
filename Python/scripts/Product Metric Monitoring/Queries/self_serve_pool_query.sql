WITH 

table1 AS (
  SELECT 
    dd.user_id
  , dd.status
  , dd.hourly_rate
  , v4.is_deleted
  , dda.dev_status
  , dda.starts_in_weeks
  , dda.developer_availability_type
  , dd.availability_last_updated
  , tdf.flag
  , CASE
    WHEN dd.status = 'available supply' AND dd.hourly_rate > 4.5 AND dd.hourly_rate < 65.5 AND v4.is_deleted != 1 AND dda.dev_status = 'ready-to-interview' AND dda.starts_in_weeks <= 4 AND DATE_DIFF (TIMESTAMP (CURRENT_DATE()), TIMESTAMP (dda.availability_last_updated), DAY) <= 30 AND (dda.developer_availability_type IN ('fulltime','pre-fulltime') OR tdf.flag = 'need-quick-rematch') THEN 1 
    ELSE 0 
    END AS SS_Flag
  , CASE
      WHEN ci.country_name IN ('Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Bolivia, Plurinational State of', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras' , 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and The Grenadines', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela', 'Venezuela, Bolivarian Republic of') THEN 'LATAM' 
      ELSE 'ROW' 
    END AS geography
  FROM 
    turing-230020.devdb_mirror.developer_detail AS dd 
    LEFT JOIN turing-230020.curated.dev_availability_all AS dda ON dd.user_id = dda.user_id 
    LEFT JOIN turing-230020.devdb_mirror.user_list_v4 AS v4 ON dd.user_id = v4.id
    LEFT JOIN turing-230020.devdb_mirror.tpm_developer_flags AS tdf ON dd.user_id = tdf.developer_id
    LEFT JOIN turing-230020.analytics_views.country_information AS ci ON ci.country_id = dd.country_id
)

, dev_info AS (
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

SELECT 
  di.date
, COUNT (DISTINCT table1.user_id) AS devs_count
FROM 
  table1 
  LEFT JOIN dev_info di ON di.dev_id = table1.user_id
WHERE 
  table1.SS_Flag = 1
  AND di.geography = '{}'
  AND DATE (DATE_TRUNC (di.date, DAY)) < CURRENT_DATE()
GROUP BY 1
ORDER BY 1