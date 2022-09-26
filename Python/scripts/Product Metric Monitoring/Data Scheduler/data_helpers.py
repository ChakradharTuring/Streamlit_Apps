import datetime
from google.cloud import bigquery
import pandas as pd
import time


def query_result(query):
    """
    Runs the query and returns the output. 
    
    Args:
        query (str): The query text
        
    Returns:
        (df): Output of the query as a dataframe
    """
    
    start_time = time.time()
    
    client = bigquery.Client('turing-230020')
    output = client.query(query).to_dataframe()
    client.close()
    
    end_time = time.time()
    
    print('Query run time:', round (end_time - start_time, 2), 'seconds')

    return output


def data_preprocess(df):
    """
    Preprocesses the data 
    
    Args:
        df (df): The input dataframe
        
    Returns:
        (df): Dataframe processed 
    """

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', utc=True)
    df = df[df['date'] >= '2019-09-01']

    today = datetime.date.today()
    yesterday = pd.to_datetime(today - datetime.timedelta(days=1), format='%Y-%m-%d', utc=True)

    date_range = pd.date_range(df['date'].min(), yesterday)

    df = df.set_index('date')
    df = df.reindex(date_range, fill_value=0)
    df = df.reset_index()
    df.columns = ['ds', 'y']
    df['ds'] = df['ds'].dt.tz_localize(None)
    df['7_day_rolling_mean'] = df['y'].rolling(window=7).mean()
    
    return df


def sum_data(data_1, data_2, data_3=None, data_4=None):
    """
    Sums the different categories of metric.
    
    Args:
        data (dfs): The input dataframes to be summed. 
        
    Returns:
        (df): The summed dataframe.
    """
    
    return pd.concat([data_1, data_2, data_3, data_4]).groupby('ds', as_index=False).sum()
