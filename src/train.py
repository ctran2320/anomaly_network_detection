"""
code for gererating our models and any algorithms used in anomaly detection
""" 
import numpy as np
import pandas as pd



def eval_arima(X,arima_order,conf,n):
    """ 
    Returns Forecasting arima model and metrics, trained on windows that move through the time series. 
    
    Arguments: 
    X - data matrix
    arima_order - (?)
    conf - (?)
    n - (?)
    
    """ 
    
    
    train, test = X[:n], X[n:]
    history = [x for x in train]
    predictions = list()
    anomalies=[]
    upperLim=[]
    lowerLim=[]
    for t in range(n,len(test)+n):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(method_kwargs={"warn_convergence": False})
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        result = model_fit.get_forecast()
        conf_int = result.conf_int(alpha=conf)
        upperLim.append(conf_int[0,1])
        lowerLim.append(conf_int[0,0])
        if obs >= conf_int[0,0] and obs <= conf_int[0,1]:
            anomalies.append(0)
        else:
            anomalies.append(1)
    rmse = mean_squared_error(test, predictions, squared=False)
    return model_fit.aic,model_fit,test,predictions,anomalies,upperLim,lowerLim

"""
Takes in dataframe, returns median and median absolute deviation
"""
def MAD(data, window_size=100, feature='1->2Pkts'):
    X = data[feature]

    mad = lambda x: np.median(np.fabs(x - np.median(x)))

    window = window_size
    median = []
    m = []

    for i in range(len(X) - window):
        subset = X[i:i+window]
        median = median + [np.median(subset)]
        m = m + [mad(subset)]
    
    return (median, m) 


def eval_models(dataset, p_vals,q_vals,d_vals, conf, n):
    """
    Returns the RMSE of model
    
    Arguments: 
    dataset - 
    p_vals - 
    q_vals - 
    d_vals - 
    conf - 
    n - 
    """
    
    
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_vals:
        for d in d_vals:
            for q in q_vals:
                order = (p,d,q)
                try:
                    aic,model_fit,test,predictions,anomalies,upperLim,lowerLim = eval_arima(dataset, order,conf,n)
                    best_score, best_cfg = aic, order
                    print('ARIMA%s RMSE=%.3f' % (order,aic))
                except:
                    continue