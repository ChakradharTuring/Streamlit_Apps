import datetime
import numpy as np
import pandas as pd
from prophet import Prophet


def run_prophet(data):
    """
    Runs the prophet algorithm on the time series data and returns a dataframe with anomalies in the past week. 
    
    Args:
        data (df): Time Series data of a metric in a DataFrame
        
    Returns:
        (df): Predictions by the model for the past week data
    """
    
    holiday_effect = True
    
    model = Prophet(
        daily_seasonality = False
      , yearly_seasonality = True
      , weekly_seasonality = True
      , seasonality_mode = 'multiplicative'
      , interval_width = 0.95
      , changepoint_range = 0.8
    )
    
    today = datetime.date.today()
    week_ago = pd.to_datetime(today - datetime.timedelta(days=7), format='%Y-%m-%d')

    if holiday_effect:
        model.add_country_holidays(country_name='US')
        
    model.fit(data[data['ds'] < week_ago])
    np.random.seed(16)
    forecast = model.predict(data)
    
    performance = pd.merge(data, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')
    performance['anomaly'] = performance.apply(lambda rows: 1 if ((rows.y < rows.yhat_lower)|(rows.y > rows.yhat_upper)) else 0, axis = 1)
    
    performance = performance[performance['ds'] >= week_ago]
    performance = performance.sort_values(by='ds')
    performance['day_name'] = (performance['ds'].dt.day_name()).values

    return performance


def get_anomalies(metric):
    """
    Calls the prophet function on each metric sequentially. 
    
    Args:
        metric (dict): All the metrics of a particular Product
        
    Returns:
        (df): redictions by the model for the past week data
    """

    forecasted_values = dict()
    for metric, data in metric.items():
        print('---- Running Prophet for Metric:', metric, '----')
        
        performance = run_prophet(data)
        forecasted_values[metric] = performance
        
    return forecasted_values


def get_all_anomalies(supply_metrics, matching_metrics, selfserv_metrics):
    """
    Calls the prophet function on each product sequentially. Needed so that we can cache these values, everyday. 
    
    Args:
        supply_metrics (dict): Dictionary having actual values of the supply metrics.
        matching_metrics (dict): Dictionary having actual values of the matching metrics.
        selfserv_metrics (dict): Dictionary having actual values of the selfserv metrics.
        
    Returns:
        (dfs): Predictions by the model for the past week data for each metric
    """

    supply_forecasts = get_anomalies(supply_metrics)
    matching_forecasts = get_anomalies(matching_metrics)
    selfserv_forecasts = get_anomalies(selfserv_metrics)

    return supply_forecasts, matching_forecasts, selfserv_forecasts
