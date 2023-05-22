import datetime
import numpy as np
import pandas as pd
from prophet import Prophet
from data_fetchers import get_supply_data
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg


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
      , changepoint_prior_scale = 0.001
    )
    
    today = datetime.date.today()
    week_ago = pd.to_datetime(today - datetime.timedelta(days=7), format='%Y-%m-%d')
    months_ago = pd.to_datetime(today - datetime.timedelta(days=97), format='%Y-%m-%d')
    
    if holiday_effect:
        model.add_country_holidays(country_name='US')

    mean_value = data[(data['ds'] > months_ago) & (data['ds'] < week_ago)]['y'].mean()
    data.loc[(data['y'] > (2.5 * mean_value)) & (data['ds'] < week_ago), 'y'] = int(mean_value)
    
    model.fit(data[data['ds'] < week_ago])
    np.random.seed(16)
    forecast = model.predict(data)
    
    performance = pd.merge(data, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')
    performance['anomaly'] = performance.apply(lambda rows: 1 if ((rows.y < rows.yhat_lower)|(rows.y > rows.yhat_upper)) else 0, axis = 1)
    
    performance = performance[performance['ds'] >= week_ago]
    performance = performance.sort_values(by='ds')
    performance['day_name'] = (performance['ds'].dt.day_name()).values

    return performance


def extra_process(data):
    data = data.rename(columns={'ds': 'date'})
    data.drop(columns=['7_day_rolling_mean'], inplace=True)
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data = data.set_index('date')
    data = data.rename(columns={'x': 'y'})
    data = data.asfreq('D')
    data = data.sort_index()

    if not (data.index == pd.date_range(start=data.index.min(), end=data.index.max(),freq=data.index.freq)).all():
        data.asfreq(freq='D', fill_value=0)
    
    return data


def sk_predict(original, data):
    steps = 7
    data_train = data[:-steps]
    data_test  = data[-steps:]
    
    forecaster = ForecasterAutoreg(
          regressor = RandomForestRegressor(random_state=123)
        , lags      = 28
    )
    forecaster.fit(y=data_train['y'])

    predictions = forecaster.predict_interval(steps=steps, interval = [1, 99], n_boot = 500)
    # print(mean_squared_error(y_true = data_test['y'], y_pred = predictions, squared=False))
    predictions = predictions.reset_index().rename(columns={'index': 'ds', 'pred': 'yhat', 'lower_bound': 'yhat_lower', 'upper_bound': 'yhat_upper'})
    predictions = original.merge(predictions, how='inner', on='ds')
    predictions['yhat_lower'] = predictions['yhat_lower'].clip(0)
    predictions['yhat_upper'] = predictions['yhat_upper'].clip(0)
    predictions['anomaly'] = predictions.apply(lambda x: 1 if ((x['y'] < x['yhat_lower']) | (x['y'] > x['yhat_upper'])) else 0, axis = 1)
    predictions['day_name'] = (predictions['ds'].dt.day_name()).values

    return predictions


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
        print('---- Running SKForecast for Metric:', metric, '----')
        
        performance = sk_predict(data.copy(), extra_process(data.copy()))
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


# To test the python file
if __name__=='__main__':
    supply_data = get_supply_data()
    get_anomalies(supply_data)