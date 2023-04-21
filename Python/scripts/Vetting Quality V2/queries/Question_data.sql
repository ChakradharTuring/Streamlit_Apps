SELECT 
  problem_id, 
  count(distinct problem_choice_id) num_options, 
  string_agg(distinct cast(problem_choice_id as string)) options,
  count(distinct case when valid=1 then problem_choice_id else null end) num_correct_option,
  string_agg(distinct case when valid=1 then cast(problem_choice_id as string) else null end) correct_option,
  case 
    when count(distinct case when valid=1 then problem_choice_id else null end)>1 then 'Multichoice'
    when count(distinct case when valid=1 then problem_choice_id else null end)=1 then 'Single choice'
    else 'Other' end as type_name
FROM `turing-230020.raw.dv2_problem_choice` group by 1