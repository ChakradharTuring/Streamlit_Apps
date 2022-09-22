import datetime 
import pandas as pd


def get_anomalous_metrics(anomalies):
    """
    Function to get all the metrics showing anomalous behaviour and sorting them based on number of anomalies.  
    
    Args:
        anomalies (dict): Data predictions and the actual values by the model

    Returns:
         (list): Sorted list of metrics which are anomalous. 
    """

    if no_anomalies(anomalies):
        return ['No Anomalies',]
    
    ordered_anomalies = sort_anomalies(anomalies)
    return ordered_anomalies
    

def sort_anomalies(anomalies):
    """
    Function to sort anomaloius metrics based on number of anomalies.  
    
    Args:
        anomalies (dict): All the anomalous metrics

    Returns:
         (dict): Sorted list of anomalous metrics
    """

    ordered_anomalies = {}
    for metric, data in anomalies.items():
        data_last_week = data[data['anomaly']==1]
        today = datetime.date.today()
        yesterday = pd.to_datetime(today - datetime.timedelta(days=2), format='%Y-%m-%d')
        if (not data_last_week.empty) and (data_last_week.ds.max() == yesterday):
            ordered_anomalies[metric] = len(data_last_week)
    
    ordered_anomalies = dict(sorted(ordered_anomalies.items(), key=lambda item: item[1], reverse=True))
    return list(ordered_anomalies.keys())

    
def no_anomalies(anomalies):
    """
    Function to check if there are any anomalies present in the data
    
    Args:
        anomalies (dict): Data predictions and the actual values by the model

    Returns:
         (bool): True if the data has no anomalies, else False
    """

    no_anomaly = True
    
    for _, data in anomalies.items():
        data_last_week = data[data['anomaly']==1]
        if data_last_week.empty:
            continue
        no_anomaly = False
        
    return no_anomaly


def change_dict_df(object, dict_to_df=0):
    """
    Function to change dictionary to dataframe and vice versa. 
    
    Args:
        object (dict or df): Depending on which to convert
        dict_to_df (int): 0 to convert dict_to_df or 1 for vice versa
    """
    
    if dict_to_df:
        return pd.DataFrame(list (object.items()), columns=['Metric', 'DF'])
    
    return dict(zip(object.Metric, object.DF))
