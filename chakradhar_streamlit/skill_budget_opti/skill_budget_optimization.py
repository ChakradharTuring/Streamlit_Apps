# !pip install geoip2[all]
# !pip install ydata-profiling
# !pip install sweetviz
# !pip install --upgrade ydata_profiling
# !pip install pulp
# !pip install streamlit
# !pip install xlsxwriter

# import streamlit as st
# import pandas as pd
# import numpy as np
# from pulp import *
# import pandas_gbq as gbq
# import pydata_google_auth
# from google.colab import auth
# from oauth2client.client import GoogleCredentials
# from gspread_dataframe import get_as_dataframe, set_with_dataframe
# import warnings
# # from ydata_profiling import ProfileReport
# # import sweetviz as sv
# warnings.filterwarnings('ignore')

# # pd.set_option('display.max_columns',None)
# # pd.set_option('display.max_colwidth',None)

# # from google.colab import drive
# # drive.mount('/content/drive')

# # SCOPES = [
# #     'https://www.googleapis.com/auth/cloud-platform',
# #     'https://www.googleapis.com/auth/drive',
# # ]

# # PROJECT_ID = 'turing-230020'
# # db_qry = '''
# # SELECT * from `turing-230020.devdb_mirror.ms2_job_match_status`
# # LIMIT 10;
# # '''
# # _ = gbq.read_gbq(
# #     db_qry,
# #     project_id=PROJECT_ID
# # )

# # Gets the top channels for each SKILL_GEO as there is a (max of 50% of total budget) constraint applied on each channel spend here
# # Gets the maximum icf_90 possible for each SKILL_GEO

# def get_topchannels_for_skill_geo(skill,geo_group,objective,total_spend_allowed_per_channel_perc,rate,yoe):

#   total_spend_allowed_per_channel_perc = total_spend_allowed_per_channel_perc/100

#   if cost_var == 'minCost_per_su':
#     channel_cost = 'min_dev_skill_cost'
#   if cost_var == 'maxCost_per_su':
#     channel_cost = 'max_dev_skill_cost'

#   if objective == 'p2':
#     cost_per_signup = 'SU -> P2 Conv'
#   if objective == 'icf':
#     cost_per_signup = 'su_to_icf_perc'
#   if objective == 'icf_90':
#     cost_per_signup = 'su_to_icf_90_perc'
#     # n_icfs = 'n_icf_90'
#   if objective == 'icf_30':
#     cost_per_signup = 'su_to_icf_30_perc'
#   if objective == 'icf_60':
#     cost_per_signup = 'su_to_icf_60_perc'
#   if objective == 'icf_365':
#     cost_per_signup = 'su_to_icf_365_perc'

#   # print("\n")
#   # print(skill, geo_group)

#   filter = (stack_channel_cost_req['geo_group']==geo_group)&(stack_channel_cost_req['skill_name']==skill)&(stack_channel_cost_req['rate_bucket']<rate)&(stack_channel_cost_req['yoe_bucket']>=yoe)
#   stack_channel_cost_req1 = stack_channel_cost_req[filter].copy()
#   if stack_channel_cost_req1.shape[0] >0 :
#     stack_channel_cost_req1['coeff'] = stack_channel_cost_req1[cost_per_signup]/stack_channel_cost_req1[cost_var]
#     # current_spend_df = stack_channel_cost_req1[['channel_ms',channel_cost]].sort_values('channel_ms').rename(columns = {channel_cost:'current_spend'})

#     # Create a LP maximization problem
#     prob = LpProblem("Optimization Problem", LpMaximize)

#     # Variables
#     variables = {}
#     for index, row in stack_channel_cost_req1.iterrows():
#         variables[row['city_channel']] = LpVariable(row['city_channel'], lowBound=0)

#     # Objective function
#     prob += lpSum([row['coeff'] * variables[row['city_channel']] for index, row in stack_channel_cost_req1.iterrows()])

#     # Constraint on Total spend
#     prob += lpSum(variables.values()) <= total_spend_allowed*(1+extra_total_spend_allowed)

#     # Constraint: Each variable should not exceed 50% of total budget
#     for index, row in stack_channel_cost_req1.iterrows():
#         # current_value = row['min_dev_skill_cost']
#         variable = variables[row['city_channel']]
#         prob += variable <= (total_spend_allowed_per_channel_perc) * total_spend_allowed

#     # Solve the problem
#     prob.solve()

#     # print("Status:", LpStatus[prob.status])
#     # print("\n")
#     optimal_solution = pd.DataFrame(columns=["city_channel"+objective, "reco_spend_"+objective])
#     for v in prob.variables():
#         optimal_solution = optimal_solution.append({"city_channel" +objective : v.name, "reco_spend_" +objective : v.varValue}, ignore_index=True)




#     icf_max_count = value(prob.objective)
#     # print("Max", objective, "=", objective,value(prob.objective))
#     # print("\n")
#     optimal_solution = optimal_solution[optimal_solution["reco_spend_" +objective]>0]
#     # display(optimal_solution)
#     # print("\n")
#     dcs_req = positions*(1/0.8)
#     icfs_req = dcs_req*(1/0.02)
#     signups_req = icfs_req*(1/0.04)
#     used_budget = optimal_solution["reco_spend_" +objective].sum()
#     budget = icfs_req*(used_budget/icf_max_count)
#     spend_per_position = budget/positions

#     # print("\n")
#     # print("Budget_needed : " , budget)
#     # print("Spend/Position : " , spend_per_position)

#     return optimal_solution , value(prob.objective), budget, spend_per_position
#     # print(prob)

# extra_spend_allowed_per_channel = 0.0 # how much more  % spend over current spend is allowed. This can be used instead of total_spend_allowed_per_channel_perc
# extra_total_spend_allowed = 0.0 # This can be used if the budget is not fixed and can be varied

# total_spend_allowed = 1000 # Total Budget allowed 
# total_spend_allowed_per_channel_perc = 10
# objective = 'icf_90'
# cost_var = 'maxCost_per_su'

# input_path = '/streamlit_data_24feb21.csv'
# # input_path = r"https://drive.google.com/file/d/1-0SPQ5TaKeLteMC7KS8_ZZdjqB0Bllkh/view?usp=drive_link"
# stack_channel_cost_req = pd.read_csv(input_path)




# # skill = 'Python'
# # geo_group = 'LATAM'
# # rate = 15
# # yoe = 2
# # positions = 100





# # Dropdown for the skill
# skill_var = st.selectbox('Select Skill :', ['Python', 'React', 'Go', 'Flutter'])

# # Dropdown for the Geo
# geo_var = st.selectbox('Select Geo :', ['LATAM', 'ROW'])


# # User input for RATE
# rate_var = st.number_input('Enter Max Rate:', value= 10)

# # User input for YoE
# yoe_var = st.number_input('Enter Min YoE:', value= 2)

# # User input for Positions
# positions_var = st.number_input('Enter postions to be filled :', value= 10)



# optimal_solution,icf_max_count, budget, spend_per_position =  get_topchannels_for_skill_geo(skill,geo_group,objective,total_spend_allowed_per_channel_perc,rate,yoe)

# st.write('Budget needed:', budget)

# st.write('Spend per Position:', spend_per_position)



import pandas as pd
import streamlit as st

input_path = 'streamlit_data_24feb21.csv'
stack_channel_cost_req = pd.read_csv(input_path)
st.write('stack_channel_cost_req:', stack_channel_cost_req.head(10))