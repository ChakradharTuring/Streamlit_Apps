import pandas as pd


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
