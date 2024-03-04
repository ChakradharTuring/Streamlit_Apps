# Libraries ------------
import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px


# Thresholds ----- will apply based on the metrics chosen - this represents the minimum number of devs present in a cohort
n_p2_threshold = 30
n_dc_threshold = 5
n_ih_threshold = 10
n_mti_threshold = 5
n_hm_threshold = 5


### Data prep---------------------
cost_quality_cities = pd.read_csv("cost_quality_cities.csv")
# cost_quality_cities1 = cost_quality_cities
geo_city_metrics_skill1 = pd.read_csv("city_level_metrics_data_streamlit_24feb28.csv")
# country_list = geo_city_metrics_skill1.groupby('country_ip')['n_devs'].sum().reset_index().sort_values('n_devs',ascending=False).reset_index(drop = True)['country_ip'].iloc[0:12].tolist()
countries = geo_city_metrics_skill1.groupby(['geo_group','country_ip'])['n_devs'].sum().reset_index().groupby(['geo_group']).apply(lambda x : x.nlargest(5,'n_devs'))['country_ip'].tolist()
countries_to_move = ['India', 'Brazil', 'Pakistan']
for country in countries_to_move:
    if country in countries:
        countries.remove(country)

country_list = countries_to_move + countries


geo_city_metrics_skill1['wiki_city_tier'] = geo_city_metrics_skill1['wiki_city_tier'].str.replace('wiki_','')
geo_city_metrics_skill1.rename(columns = {'wiki_city_tier':'City Tier'}, inplace=True)
geo_city_metrics_skill1.rename(columns = {'skill_hm_perc':'HM %','mti_pass_rate' :'MTI Pass %','maxCost_per_su':'Cost per Signup',
                                            'ih_success_rate':'Interview Success %','hourly_rate_median':'Hourly Rate'}, inplace=True)



# Function to plot chosen X vs Y metrics ------------

def city_hotspots(min_devs,min_devs_metric,country_ip, skill_name, yoe_bucket, x_col, y_col):
  
  cost_quality_cities1 = cost_quality_cities.copy()
  
  cost_quality_cities1 = cost_quality_cities1[(cost_quality_cities1['skill_name']==skill_name)].copy()
  cost_quality_cities1 = cost_quality_cities1[(cost_quality_cities1['country']==country_ip)].copy()
  cost_quality_cities1 = cost_quality_cities1[(cost_quality_cities1['yoe']==(yoe_bucket))].copy() 

  cost_df = cost_quality_cities1[cost_quality_cities1['lowcost']>=3]
  quality_df = cost_quality_cities1[cost_quality_cities1['highquality']>=3]

 
  geo_city_metrics_skill2 = geo_city_metrics_skill1.copy()
  geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2[min_devs_metric] >= min_devs].copy()
#   geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2['n_dcs'] >= 1].copy()
  if x_col == 'HM %':
     geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2['n_skill_hms'] >= n_hm_threshold].copy()
  if x_col == 'Interview Success %':
     geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2['n_ihs'] >= n_ih_threshold].copy()
  if x_col == 'MTI Pass %':
     geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2['n_mtis'] >= n_mti_threshold].copy()

  geo_city_metrics_skill2 = geo_city_metrics_skill2[(geo_city_metrics_skill2['skill_name']==skill_name)].copy()
  geo_city_metrics_skill2 = geo_city_metrics_skill2[(geo_city_metrics_skill2['country_ip']==country_ip)].copy()
  geo_city_metrics_skill2 = geo_city_metrics_skill2[(geo_city_metrics_skill2['yoe_bucket']==(yoe_bucket))].copy()

  # geo_city_metrics_skill2 = geo_city_metrics_skill2[geo_city_metrics_skill2['n_ihs'] >= 1].copy()

  metric_cols = ['n_devs', 'n_devs_bi', 'n_accs', 'n_p2_devs', 'n_ntes','n_icfs','n_hms','n_mtis','n_mtigs', 'n_ihs', 'n_dcs','n_skill_hms' ,'Interview Success %', 
                'acc_days_median','p2_days_median', 'nte_days_median', 'icf_days_median','dc_days_median', 'Hourly Rate','hourly_rate_75','hourly_rate_25', 'yoe_median',
                'max_dev_skill_cost', 'n_devs_ads_jobboards', 'HM %','MTI Pass %','Cost per Signup','p2_perc', 'icf_perc']

  geo_city_metrics_skill3 = geo_city_metrics_skill2.groupby(['City Tier','city_ip'])[metric_cols].mean().reset_index()

  # filter_conds = (geo_city_metrics_skill3['skill_name']==skill_name)&(geo_city_metrics_skill3['yoe_bucket'].isin(yoe_bucket))
  # geo_city_metrics_skill4 = geo_city_metrics_skill3[filter_conds].copy()
  geo_city_metrics_skill4 = geo_city_metrics_skill3.copy()
  if x_col == 'HM %':
     nume, deno = 'n_skill_hms', 'n_p2_devs'
  if x_col == 'Interview Success %':
     nume, deno = 'n_dcs', 'n_ihs'
  if x_col == 'MTI Pass %':
     nume, deno = 'n_mtis', 'n_mtigs'
      
  x_num = geo_city_metrics_skill4[nume].sum()/geo_city_metrics_skill4[deno].sum()
  # y_num = geo_city_metrics_skill4['hourly_rate_median'].mean()

  geo_city_metrics_skill5 = geo_city_metrics_skill4[geo_city_metrics_skill4[y_col].notnull()]
  y_num = sum(geo_city_metrics_skill5[y_col]*geo_city_metrics_skill5['n_devs'])/geo_city_metrics_skill4['n_devs'].sum()
  y_max = geo_city_metrics_skill4[y_col].max()*1.15
  y_min = geo_city_metrics_skill4[y_col].min()*0.8
  x_max = geo_city_metrics_skill4[x_col].max()+0.05
  x_min = geo_city_metrics_skill4[x_col].min()-0.05


  color_map = {'tier_1': 'blue', 'tier_2': 'red'}

  if geo_city_metrics_skill4.empty:
    fig = px.scatter(template="plotly_white")
    fig.update_layout(annotations=[dict(x=0.5,y=0.5,xref='paper',yref='paper',text='Not enough data to plot',showarrow=False,font=dict(size=50, color='red'))])
    fig.update_layout(title={'text': "Try a different combination", 'font': {'family': 'Arial', 'size': 36}})
    st.plotly_chart(fig,use_container_width=True)
  else:
    # px.set_mapbox_access_token("pk.eyJ1IjoiY2hha3JhdHVyaW5nIiwiYSI6ImNsc3hqcHgwZDAzdzYya3FwZnIyeTBjbDUifQ.o7bKXiLSb3pcVa8XxJ4pHg")
    fig = px.scatter(geo_city_metrics_skill4, x= x_col , y= y_col, text='city_ip', 
                     # labels={'x': x_col, 'y': y_col}, 
                     title='',
                    color = 'City Tier', 
                    color_discrete_map=color_map,
                    size = geo_city_metrics_skill4['n_devs'].astype(float).tolist() )
    # fig.update_traces(marker=dict(size=12)) 
    # Add lines
    fig.add_shape(
        type="line",
        x0=x_num, y0=0, x1=x_num, y1=y_max,
        line=dict(color="red", width=1,dash="dot")
    )

    fig.add_shape(
        type="line",
        x0=0, y0=y_num, x1=1, y1=y_num,
        line=dict(color="red", width=1,dash="dot")
    )

    fig.update_layout(yaxis=dict(range=[y_min, y_max]))
    fig.update_layout(xaxis=dict(range=[x_min, x_max]))
    fig.update_layout(font=dict(family="Arial",size=16,color="black") )
    fig.update_layout(
    xaxis=dict(
        title=x_col,
        title_font=dict(
            family="Arial",
            size=18,
            color="black"
        )
    ),
    yaxis=dict(
        title=y_col,
        title_font=dict(
            family="Arial",
            size=20,
            color="black"
        )
    ) )
    fig.add_shape(type="rect",
              x0=x_num, y0=y_min, x1=x_max, y1=y_num,
              fillcolor="blue", opacity=0.2, layer="below", line_width=0)
    fig.add_shape(type="rect",
              x0=x_min, y0=y_num, x1=x_num, y1=y_max,
              fillcolor="red", opacity=0.2, layer="below", line_width=0)
   #  fig.update_xaxes(font=dict(family="Arial",size=18,color="black"))
    fig.update_layout(width=700, height=600)
    fig.update_layout(xaxis=dict(tickformat=".0%"))

    st.plotly_chart(fig,use_container_width=True)

    geo_city_metrics_skill4.rename(columns = {'city_ip':'City'},inplace=True)
    display_cols = ['City Tier','City','n_devs', 'n_p2_devs', 'n_ntes','n_icfs',
                  #   'n_hms','n_mtis','n_mtigs', 
                    'n_ihs', 'n_dcs',
                    'n_skill_hms' ,'Interview Success %', 'HM %','MTI Pass %',
               'Hourly Rate','hourly_rate_75','hourly_rate_25', 
                'Cost per Signup','p2_perc', 'icf_perc']
    
    st.subheader("1.LOW COST CITIES")
    st.write(cost_df)
    st.subheader("2.HIGH QUALITY CITIES")
    st.write(quality_df)
    st.subheader("3.CITY LEVEL METRICS")
    st.write(geo_city_metrics_skill4[display_cols])
    pass




########----------- STREAMLIT CONTROLS ---------------------------------------------------

st.set_page_config(layout="wide")

# st.subheader("1.SKILL GEO VIEW")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #C0C0C0;
    }
</style>
""", unsafe_allow_html=True)
# Create a sidebar
st.sidebar.title('Find a Hotspot')

# # Add some controls to the sidebar
# option = st.sidebar.selectbox(
#     'Choose a plot type',
#     ['line', 'bar', 'scatter']
# )

# mindev_metic_var = st.selectbox('Select Metric for Min Devs :', ['n_devs','n_icfs','n_p2_devs'])
mindev_metic_var = 'n_p2_devs'

# Dropdown for minimum devs
# mindev_var = st.selectbox('Select Min Devs in City :', [0,10,20,30,50,75,100,500,1000])
mindev_var = n_p2_threshold


# Dropdown for the skill
skill_var = st.sidebar.selectbox('Select Skill :', ['Python', 'React', 'Go', 'Flutter'])

# Dropdown for the Geo
# geo_var = st.selectbox('Select Geo :', ['LATAM', 'ROW'])

# Dropdown for the Country
country_var = st.sidebar.selectbox('Select Country :', country_list)

# Dropdown for the yoe
yoe_var = st.sidebar.selectbox('Select YOE :', ['>=4', '2-4','0-2'])

# Dropdown for the x_var
x_var = st.sidebar.selectbox('Select X metric :', ['Interview Success %','HM %','MTI Pass %'])

# x_var = ['ih_success_rate','hm_perc','skill_hm_perc']

# Dropdown for the y_var
y_var = st.sidebar.selectbox('Select Y Metric :', ['Hourly Rate','Cost per Signup'])
# y_var = 'hourly_rate_median'


city_hotspots(mindev_var,mindev_metic_var,country_var, skill_var, yoe_var, x_var, y_var)
