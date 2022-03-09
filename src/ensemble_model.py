from mad import MAD_model
from etl import aggregate_data
import pandas as pd
from arima import Arima_model
import numpy as np

    

class Ensemble():
    """
    Final Model that takes in data and a window size, preprocesses the data, and outputs the final prediction based on the two model's predictions 
    """

    def anomaly_ensemble(self, data, arima_window, mad_window, threshold):
        
        df_a, df_m = aggregate_data(data, arima_window)
        
        # train arima model & get anomalies 
        arima = Arima_model((3,0,2), .01, 75)
        arima_anomalies = arima.arima_model_anomalies(arima, df_a)

        # train mad model & get anomalies 
        mad = MAD_model(mad_window)
        mad_anomalies = mad.MAD_anomalies(mad, df_m.total_pkts)
        mad_anom_agg = mad.aggregate_anomalies(mad_anomalies, arima_window, threshold, df_m) #.25 GOOD threshold

        final_preds = set(arima_anomalies).intersection(set(mad_anom_agg))

        return final_preds