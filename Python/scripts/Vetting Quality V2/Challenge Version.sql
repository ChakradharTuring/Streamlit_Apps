with ch_ver as(
SELECT  challenge_id,
        challenge_name,
        concat('V-', ROW_NUMBER() OVER(PARTITION BY lower(challenge_name) ORDER BY challenge_id)) as version
FROM raw.dv2_challenge
WHERE challenge_name IN ('Python', 'ReactJS', 'Angular', 'NodeJS','Javascript','JavaScript', 'SQL', 'React Native', 'TypeScript', 'HTML/CSS/Javascript', 'Java', 'VueJS',
'iOS Swift','Android + Kotlin','REST API','HTML/CSS','Redux','Ruby on Rails','GraphQL','C#','PHP','Android','Kubernetes','AWS','Golang') and challenge_id not in (113,120,123,411,431,444)
qualify case when challenge_name in ('React Native', 'TypeScript', 'HTML/CSS/Javascript',
'iOS Swift','Android + Kotlin','REST API','HTML/CSS','Redux','Ruby on Rails','GraphQL','C#','PHP','Android','Kubernetes','AWS','Golang') then ROW_NUMBER() OVER(PARTITION BY lower(challenge_name) ORDER BY challenge_id ) = 1 else True END
order by challenge_name,challenge_id
)

SELECT 
  challenge_id, challenge_name, version, 
  count(distinct user_id) num_attempt,
  count(distinct case when passed=1 then user_id else null end) num_pass
from ch_ver 
left join `turing-230020.raw.dv2_challenge_submit` cs using(challenge_id)
group by 1,2,3 order by challenge_name,challenge_id

