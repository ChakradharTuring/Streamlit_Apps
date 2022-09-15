import datetime
from helper_functions import get_anomalous_metrics
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def make_app(supply_forecasts, matching_forecasts, selfserv_forecasts, supply_metrics, matching_metrics, selfserv_metrics, glossary):
    """
    Main function to make the streamlit app. 
    
    Args:
        supply_forecasts (dict): Dictionary having predictions for the supply metrics.  
        matching_forecasts (dict): Dictionary having predictions for the matching metrics. 
        selfserv_forecasts (dict): Dictionary having predictions for the selfserv metrics.
        supply_metrics (dict): Dictionary having actual values of the supply metrics.
        matching_metrics (dict): Dictionary having actual values of the matching metrics.
        selfserv_metrics (dict): Dictionary having actual values of the selfserv metrics.
        glossary (dict): Glossary explaining all metrics
    """

    st.title("Janus (Early Monitoring)")
    
    options = ['Anomalies', 'Data Reports', 'Glossary']
    page = st.radio('What do you want to see?', options, horizontal=True)
    
    if page == 'Anomalies':
        page_anomalies(supply_forecasts, matching_forecasts, selfserv_forecasts, supply_metrics, matching_metrics, selfserv_metrics)
        
    if page == 'Data Reports':
        page_data_report(supply_metrics, matching_metrics, selfserv_metrics)
    
    if page == 'Glossary':
        page_glossary(glossary)

    
def page_anomalies(supply_forecasts, matching_forecasts, selfserv_forecasts, supply_metrics, matching_metrics, selfserv_metrics):
    """
    This function focuses on making page anomalies. 
    
    Args:
        supply_forecasts (dict): Dictionary having predictions for the supply metrics.  
        matching_forecasts (dict): Dictionary having predictions for the matching metrics. 
        selfserv_forecasts (dict): Dictionary having predictions for the selfserv metrics.
        supply_metrics (dict): Dictionary having actual values of the supply metrics.
        matching_metrics (dict): Dictionary having actual values of the matching metrics.
        selfserv_metrics (dict): Dictionary having actual values of the selfserv metrics.
    """

    anomaly_options = ['Supply', 'Matching', 'SefServ']
    anomaly_page = st.radio('Choose Product:', anomaly_options, horizontal=True)
    
    if anomaly_page == 'Supply':
        render_anomaly(supply_metrics, supply_forecasts, ['Manually Select', 'RoW', 'LATAM'])
    
    if anomaly_page == 'Matching':
        render_anomaly(matching_metrics, matching_forecasts, ['Manually Select', 'FSS New', 'FSS Existing', 'Enterprise New', 'Enterprise Existing', 'FSS', 'Enterprise', 'Others'])
        
    if anomaly_page == 'SefServ':
        render_anomaly(selfserv_metrics, selfserv_forecasts, ['Manually Select', 'FSS New', 'FSS Existing', 'Enterprise New', 'Enterprise Existing', 'FSS', 'Enterprise', 'Others'])

    
def render_anomaly(metrics, forecasts, metric_category_list):
    """
    This function shows all the available anomalies and gives the user option to select the anomaly they want to see.  
    
    Args:
        metrics (dict): Dictionary having actual values of the metrics.  
        forecasts (dict): Dictionary having predictions for the metrics.  
        metric_category_list (list): This is the list of defined categories that we have here at Turing, such as RoW, LATAM, Platinum Existing etc. 
    """

    anomalous_metrics = get_anomalous_metrics(forecasts)
    
    metrics_list = []
    for metric, _ in forecasts.items():
        metrics_list.append(metric)
        globals()[metric] = False

    if anomalous_metrics[0] == 'No Anomalies':
        st.write('No Anomalies')
    else:
        metric_category = st.radio('Choose the anomalies you want to see:', metric_category_list, horizontal=True)
        show_all = st.checkbox('Show All Metrics in this category (irrespective of it being an anomaly)?')
        
        if show_all:
            concerned_metrics = metrics_list.copy()
        else:
            concerned_metrics = anomalous_metrics.copy() 
        
        if metric_category == 'Others':
            for metric in concerned_metrics:
                globals()[metric] = True
                names = ['fss_new', 'fss_existing', 'enterprise_new', 'enterprise_existing']
                for name in names:
                    if name in metric:
                        globals()[metric] = False
        elif metric_category != 'Manually Select':
            for metric in concerned_metrics:
                name = metric_category.lower().replace(' ', '_')
                if name in metric:
                    globals()[metric] = True
        else:
            anomalous_metric_list = st.multiselect('', anomalous_metrics)
            for anomalous_metric in anomalous_metric_list:
                globals()[anomalous_metric] = True
        
        generate_graphs(metrics_list, forecasts, metrics)


def generate_graphs(anomalies, forecast, metrics):
    """
    This function focuses on rendering graphs for the anomalies. 
    
    Args:
        anomalies (list): List of anomalous metrics.   
        forecast (dict): Dictionary having predictions for the metrics. 
        metrics (dict): Dictionary having actual values of the metrics.
    """

    for anomalous_metric in anomalies:
        if globals()[anomalous_metric]:
            data = metrics[anomalous_metric]

            today = datetime.date.today()
            week_ago = pd.to_datetime(today - datetime.timedelta(days=7), format='%Y-%m-%d')
            data = data[data['ds'] >= week_ago]
            
            forecast_metric = forecast[anomalous_metric]
            anomaly = forecast_metric[forecast_metric['anomaly']==1]

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], line=dict(color='#90D8D5', width=3), name='Actual Values'))
            fig.add_trace(go.Scatter(x=forecast_metric['ds'], y=forecast_metric['yhat_upper'], line=dict(color='#FCB94C', width=3, dash='dash'), name='Upper Bound Confidence'))
            fig.add_trace(go.Scatter(x=forecast_metric['ds'], y=forecast_metric['yhat_lower'], line=dict(color='#FCB94C', width=3, dash='dash'), name='Lower Bound Confidence'))            
            fig.add_trace(go.Scatter(x=anomaly['ds'], y=anomaly['y'], mode='markers', marker=dict(size=8), marker_color='#CC2A27', name='Anomalies'))            
            fig.update_layout(
                xaxis_title="Date"
              , yaxis_title=anomalous_metric
              , showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)


def page_data_report(supply_metrics, matching_metrics, selfserv_metrics):
    """
    This function focuses on making data reports page. 
    
    Args:
        supply_metrics (dict): Dictionary having actual values of the supply metrics.
        matching_metrics (dict): Dictionary having actual values of the matching metrics.
        selfserv_metrics (dict): Dictionary having actual values of the selfserv metrics.
    """

    data_options = ['Supply', 'Matching', 'SefServ']
    data_page = st.radio('Choose Product:', data_options, horizontal=True)
    
    if data_page == 'Supply':
        render_data(supply_metrics)
    
    if data_page == 'Matching':
        render_data(matching_metrics)
        
    if data_page == 'SefServ':
        render_data(selfserv_metrics)


def render_data(metrics):
    """
    This helps with taking input from the user, i.e. for which metric does the user want the data report.
    
    Args:
        metrics (dict): Dictionary having actual values of the product provided.
    """

    today = datetime.date.today()
    yesterday = pd.to_datetime(today - datetime.timedelta(days=1), format='%Y-%m-%d')
    week_ago = pd.to_datetime(today - datetime.timedelta(days=7), format='%Y-%m-%d')
    
    metrics_list = []
    for metric, _ in metrics.items():
        metrics_list.append(metric)

    show_metric_list = st.multiselect('Choose metrics:', metrics_list)
    dates = st.date_input('Report Date:', [], key=0)
    show_df = st.checkbox('Show Dataframe?')
    show_graph = st.checkbox('Show Graph?')

    try:
        if (dates[1] >= dates[0]) and (len(show_metric_list) > 0) and (show_df or show_graph):
            generate_report(show_metric_list, dates[0], dates[1], metrics, show_df, show_graph)
        else:
            st.write('<font color="red">Select the options to render data!</font>', unsafe_allow_html=True)
    except:
        st.write('<font color="red">Select the options to render data!</font>', unsafe_allow_html=True)


def generate_report(show_metric_list, start_date, end_date, metrics, show_df, show_graph):
    """
    Based on the user inputs, this renders the data report for the user. 
    
    Args:
        show_metric_list (list): These are the metrics for which we want to show the data reports. 
        start_date (date): The start date to be considered which fetching data. 
        end_date (date): The end date to be considered which fetching data. 
        metrics (dict): All the data for the metrics
        show_df (dict): Flag to ask user if they want data to be shown as a DataFrame.
        show_graph (dict): Flag to ask user if they want data to be shown as a Graph.
    """

    for metric in show_metric_list:
        data = metrics[metric]

        data = data[data['ds'] >= pd.to_datetime(start_date)]
        data = data[data['ds'] <= pd.to_datetime(end_date)]
    
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], line=dict(color='#90D8D5', width=3), name='Data'))
        fig.update_layout(
            xaxis_title="Date"
          , yaxis_title=metric
          , showlegend=False
        )
        
        render_data = data[['ds', 'y']].rename({'ds': 'Date', 'y': metric}, axis=1)

        if show_df:
            st.write(render_data)
        
        if show_graph:
            st.plotly_chart(fig, use_container_width=True)


def page_glossary(glossary):
    """
    Showcases the glossary
    
    Args:
        glossary (dict): Metrics and their explanation. 
    """

    glossary = (pd.DataFrame(glossary.items())).rename({0: 'Metric', 1: 'Metric Definition'}, axis=1)

    st.table(glossary)
