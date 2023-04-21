with challenge_version as(
SELECT  challenge_id,
        challenge_name,
        concat('V-', ROW_NUMBER() OVER(PARTITION BY lower(challenge_name) ORDER BY challenge_id)) as version
FROM raw.dv2_challenge
WHERE challenge_name IN ('Python', 'ReactJS', 'Angular', 'NodeJS','Javascript','JavaScript', 'SQL', 'React Native', 'TypeScript', 'HTML/CSS/Javascript', 'Java', 'VueJS',
'iOS Swift','Android + Kotlin','REST API','HTML/CSS','Redux','Ruby on Rails','GraphQL','C#','PHP','Android','Kubernetes','AWS','Golang') and challenge_id not in 
(113,120,123,411,431, 426,427,428,438,444)
qualify case when challenge_name in ('React Native', 'TypeScript', 'HTML/CSS/Javascript',
'iOS Swift','Android + Kotlin','REST API','HTML/CSS','Redux','GraphQL','C#','PHP','Android','Kubernetes','AWS','Golang') then ROW_NUMBER() OVER(PARTITION BY lower(challenge_name) ORDER BY challenge_id ) = 1 else True END
order by challenge_name,challenge_id
),

python_mcq as(
SELECT 
  cs.user_id,
  cs.submit_id,
  submit_time, 
  cs.challenge_id,
  ch_ver.challenge_name,
  ch_ver.version,
  total_score_by_problem,
  total_problem,
  passed
--  round(dev_percentile,0) dev_percentile
FROM `raw.dv2_challenge_submit` cs
inner join challenge_version ch_ver using(challenge_id) 
--left join (SELECT * FROM EXTERNAL_QUERY("projects/turing-230020/locations/us/connections/machine-learning-prod", "SELECT * FROM prod.dev_mcq_score;") where challenge_name in ('{{Select_MCQ}}')) mcq_per on cs.user_id=mcq_per.dev_id 
WHERE ch_ver.challenge_name in ('%s') and bypass <> 1 and total_problem > 0 -- and submit_time >= '2022-12-20'
qualify row_number() over(partition by cs.user_id order by submit_time desc)=1
)

SELECT
  user_id as developer_id,
  submit_id,
  python_mcq.submit_time as mcq_submit_time, 
  python_mcq.challenge_id,
  python_mcq.challenge_name,
  python_mcq.version,
  python_mcq.total_score_by_problem,
  python_mcq.total_problem,
  python_mcq.passed as mcq_passed,
--  round(python_mcq.dev_percentile,0) dev_percentile,
  round(100*python_mcq.total_score_by_problem/python_mcq.total_problem,2) mcq_percentage,
  ntile(5) over(order by total_score_by_problem/total_problem) n_rank,
  row_number() over(partition by user_id) as rn,
  case 
    when round(100*total_score_by_problem/total_problem,0) between 0 and 25 then '0-25'
    when round(100*total_score_by_problem/total_problem,0) between 26 and 50 then '26-50'
    when round(100*total_score_by_problem/total_problem,0) between 51 and 75 then '51-75'
    when round(100*total_score_by_problem/total_problem,0) between 76 and 100 then '76-100'
    ELSE NULL END correct_percentage_bin,
  prb.* except(submit_id)
from python_mcq
inner join (SELECT submit_id, problem_id, answer,score_by_answer, problem_submit_time
FROM `turing-230020.raw.dv2_problem_submit`) prb using(submit_id)
where user_id in (SELECT distinct dev_id FROM `turing-230020.curated.phase1_dev_level_data` where email is not null and lower(email) not like '%turing.com')
qualify ROW_NUMBER() OVER(PARTITION BY developer_id, problem_id ORDER BY problem_submit_time DESC) = 1