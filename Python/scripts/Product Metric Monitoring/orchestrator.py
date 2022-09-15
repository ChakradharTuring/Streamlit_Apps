from deploy_app import make_app
from env import API_KEY
from helper_functions import change_dict_df
import pins
import streamlit as st


@st.cache(ttl=60*60*6, suppress_st_warning=True)
def read_data():
    """
    Function to read automated dataframes.  
    """
    
    board = pins.board_rsconnect(server_url='https://rstudio-connect.turing.com/', api_key=API_KEY, allow_pickle_read=True)

    supply_metrics = change_dict_df(board.pin_read('bhanu_mittal/janus_supply_data'))
    matching_metrics = change_dict_df(board.pin_read('bhanu_mittal/janus_matching_data'))
    selfserv_metrics = change_dict_df(board.pin_read('bhanu_mittal/janus_selfserv_data'))
    glossary = change_dict_df(board.pin_read('bhanu_mittal/janus_glossary'))
    
    supply_forecasts = change_dict_df(board.pin_read('bhanu_mittal/janus_supply_forecasts'))
    matching_forecasts = change_dict_df(board.pin_read('bhanu_mittal/janus_matching_forecasts'))
    selfserv_forecasts = change_dict_df(board.pin_read('bhanu_mittal/janus_selfserv_forecasts'))
   
    return supply_metrics, matching_metrics, selfserv_metrics, glossary, supply_forecasts, matching_forecasts, selfserv_forecasts


def run_monitoring():
    """
    The main function. Get's all data, run predictions and makes the app
    """

    supply_metrics, matching_metrics, selfserv_metrics, glossary, supply_forecasts, matching_forecasts, selfserv_forecasts = read_data()
    
    make_app(supply_forecasts, matching_forecasts, selfserv_forecasts, supply_metrics, matching_metrics, selfserv_metrics, glossary)
    
        
if __name__ == '__main__':
    run_monitoring()
