WITH 

opp_data AS (
 SELECT DISTINCT
   ov.account
 , CASE
     WHEN ((O.service_customer__c IS TRUE) OR (O.teams__c is True)) THEN 'Services'
     WHEN ov.client_category='1.Platinum' THEN 'Enterprise'
     WHEN ov.client_category='2.Gold' THEN 'Gold'
     WHEN ov.client_category='3.Silver' THEN 'Silver'
     WHEN ov.client_category='4.Bronze' THEN 'Bronze'
     ELSE 'Unknown'
   END AS client_category
 FROM
   curated.opportunity_value ov
   LEFT JOIN salesforce_prod.Opportunity O on ov.opportunityid = O.id
  WHERE
   job_id NOT IN (SELECT DISTINCT job_id FROM curated.test_jobs_master_table WHERE job_id IS NOT NULL)
)

, data AS (
  SELECT
    DATE (ssua.created_at) AS date
    , CASE 
      WHEN ((od.client_category IN ('Unknown', 'Gold', 'Silver', 'Bronze')) OR (ssu.customer_category IN ('Unknown', 'Gold', 'Silver', 'Bronze'))) THEN 'FSS'
      WHEN od.client_category = 'Enterprise' THEN 'Platinum'
      ELSE od.client_category
    END AS client_category
    , COUNT (ssua.user_id) AS devs_count
  FROM
    raw.self_serve_user_activity ssua 
    LEFT JOIN raw.self_serve_user ssu ON ssua.user_id = ssu.id
    LEFT JOIN opp_data od ON ssu.company_name = od.account
  WHERE
    (ssu.email NOT LIKE '%turing.com'
    OR (
      ssua.action = 'SIGN_IN_FAILED'
      AND REPLACE(JSON_EXTRACT(payload, '$.email'), '"', '') NOT LIKE '%turing.com'
    ))
    AND ACTION = 'DEVELOPER_PROFILE_VIEW'
    AND internal_user = 0
  GROUP BY 1, 2
)

SELECT 
  date
, devs_count
FROM data 
WHERE 
  client_category = '{}'
ORDER BY 1 DESC
