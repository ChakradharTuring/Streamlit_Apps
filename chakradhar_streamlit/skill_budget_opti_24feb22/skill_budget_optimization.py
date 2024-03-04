
# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px


# Read Data -----------

stack_city_channel_cost = pd.read_csv("streamlit_channel_for_city_24feb22.csv")

stack_city_channel_cost2 = pd.read_csv("streamlit_channel_for_city_corrected_24feb23.csv")
stack_city_channel_cost2['city_tier'] = stack_city_channel_cost2['city_tier'].astype(str)
stack_city_channel_cost2['su_to_icf_perc'] = stack_city_channel_cost2['n_icfs']/stack_city_channel_cost2['n_devs']
stack_city_channel_cost2['su_to_p2_perc'] = stack_city_channel_cost2['n_p2_devs']/stack_city_channel_cost2['n_devs']


# Function to convert the top channels text in hover to vertical
def convert_to_vert(x):
    s = ""
    for key, values in x.items():

        s = s + "<br>" + key + "<br>" + "<br>" 
        s = s+  "<br>".join(values) + "<br>"
        # for value in values:
        #     s = s + f
        #     s += f"{value}\n"
        # # s = s + value.join("\n")
    return s




# Gets and plots top 20 cities by Skill, Geo and chosen Metric

def get_top_cities(skill, geo, metric):

  if geo == 'LATAM':
    lat=-5
    lon=-74
  if geo == 'ROW':
    lat=23
    lon=88   


  filter_conds = (stack_city_channel_cost2['skill_name']==skill)&(stack_city_channel_cost2['geo_group']==geo)

  stack_city_channel_cost4 = stack_city_channel_cost2[filter_conds].groupby(['city_tier']).apply(lambda x: x.nlargest(20, 'n_devs')).reset_index(drop=True)


  stack_city_channel_cost5 = stack_city_channel_cost4[['skill_name','geo_group','city_ip']].merge(stack_city_channel_cost[['skill_name','geo_group','city_ip','channel_type','channel_ms','n_icfs']], on = ['skill_name','geo_group','city_ip'], how = 'left')
  stack_city_channel_cost6 = stack_city_channel_cost5.groupby(['skill_name','geo_group','city_ip','channel_type']).apply(lambda x: x.nlargest(5, 'n_icfs')).reset_index(drop=True)
  stack_city_channel_cost7 = stack_city_channel_cost6.groupby(['skill_name', 'geo_group', 'city_ip','channel_type'])['channel_ms'].apply(list).reset_index(name='channel_ms_list')
  stack_city_channel_cost8 = stack_city_channel_cost7.groupby(['skill_name', 'geo_group', 'city_ip']).apply(lambda x: dict(zip(x['channel_type'], x['channel_ms_list']))).reset_index(name='channel_info')
  stack_city_channel_cost9 = stack_city_channel_cost8.merge(stack_city_channel_cost4, on = ['skill_name', 'geo_group', 'city_ip'], how = 'left')
  stack_city_channel_cost10 = stack_city_channel_cost9.copy()
  stack_city_channel_cost10['channel_info_str'] = stack_city_channel_cost10['channel_info'].apply(lambda  x: convert_to_vert(x))

  # rename_cols_dict = {'n_icfs' :'No of ICFs', 'n_p2_devs', 'su_to_icf_perc','su_to_p2_perc','icf_days_median', 'p2_days_median','minCost_per_su','maxCost_per_su','hourly_rate_median'}


  color_map = {'1': 'blue', '2': 'red'}

  px.set_mapbox_access_token("pk.eyJ1IjoiY2hha3JhdHVyaW5nIiwiYSI6ImNsc3hqcHgwZDAzdzYya3FwZnIyeTBjbDUifQ.o7bKXiLSb3pcVa8XxJ4pHg")

  # skill_city_geo_icf_perc3 = skill_city_geo_icf_perc2[(skill_city_geo_icf_perc2['skill_name']==skill)&(skill_city_geo_icf_perc2['skill_name']==geo)]
  fig = px.scatter_mapbox(stack_city_channel_cost10, 
                      lat='lat', 
                      lon='lng', 
                      # size=(stack_city_channel_cost10[metric].tolist()),
                      size = metric,
                      color = 'city_tier',
                      color_discrete_map=color_map,
                      text='city_ip',
                      # hover_name=(stack_city_channel_cost10["channel_info_str"].tolist()),
                      hover_name = "channel_info_str",
                      hover_data={ 'channel_info_str': False, metric : True,'city_ip': True, 'lat': False, 'lng': False, 'city_tier': False},
                      zoom = 2)

  fig.update_geos(showcountries=True, countrycolor="Black", showland=True, showocean=True, oceancolor='LightBlue',showcoastlines=True)
  fig.update_layout(width=1200, height=900)
  fig.update_traces(textfont=dict(color='black', size = 15))
  fig.update_layout(hovermode='x', hoverlabel=dict(bgcolor='white', font_size=15, font_family='Arial'))


  fig.update_layout(
          # title = 'South Am',
          # geo_scope='south america',
          # center=dict(lat=-23.533773, lon=-46.625290)
          geo=dict(
        center=dict(
            # lat=-5,
            # lon=-74
            lat = lat,
            lon = lon
        )
        , 
        # scope='europe',
        # projection_scale=10
    )

      )
  st.plotly_chart(fig,use_container_width=True)

  # fig.show()


### --------------  Streamlit Configurations -----------------------------

st.set_page_config(layout="wide")

# st.subheader("1.SKILL GEO VIEW")

# Dropdown for the skill
skill_var = st.selectbox('Select Skill :', ['Python', 'React', 'Go', 'Flutter'])

# Dropdown for the Geo
geo_var = st.selectbox('Select Geo :', ['LATAM', 'ROW'])

# Dropdown for the Metric_var
metric_var = st.selectbox('Select Metric :', ['n_icfs', 'n_p2_devs', 'su_to_icf_perc','su_to_p2_perc','icf_days_median', 'p2_days_median','minCost_per_su','maxCost_per_su','hourly_rate_median'])

# Dropdown for minimum devs
# mindev_var = st.selectbox('Select Min Devs in City :', [0,25,50,100,500,1000])


get_top_cities(skill_var, geo_var, metric_var)