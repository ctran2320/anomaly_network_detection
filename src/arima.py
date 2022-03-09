import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error


""" 
Arima model class 
"""



class Arima_model():
    """
    A class representing the arima model 
    
    """
    
    def __init__(self, arima_order, conf, test_n):
        """
        initialize model object with given parameters
        
        inputs:
        arima_order - 
        conf - 
        test_n - 
        """
        self.arima_order = arima_order
        self.conf = conf
        self.test_n = test_n
        
        
    def eval_arima(self, X):
        """
        returns model statistics and anomaly predictions. 
        
        inputs:
        X - dataset 
        
        """
        
        train, test = X[:self.test_n], X[self.test_n:]
        history = [x for x in train]
        predictions = list()
        anomalies = []
        upperLim = []
        lowerLim = []
        counter = self.test_n
        for t in range(self.test_n, len(test) + self.test_n):
            model = ARIMA(history, order = self.arima_order)
            model_fit = model.fit(method_kwargs={"warn_convergence": False})
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            result = model_fit.get_forecast()
            conf_int = result.conf_int(alpha=self.conf)
            upperLim.append(conf_int[0,1])
            lowerLim.append(conf_int[0,0])
            if obs <= conf_int[0,0] or obs >= conf_int[0,1]:
                anomalies.append(counter)
                
            counter += 1    
                
        rmse = mean_squared_error(test, predictions, squared=False)
        return model_fit.aic, model_fit, test, predictions, anomalies, upperLim, lowerLim
    
    def arima_model_anomalies(self, model, data):
        """
        Trains 
        """
           
        rmse, model, test, preds,anomalies,upper,lower = model.eval_arima(np.log(data.total_pkts.astype(float)))
        
        # buffer of 40 seconds for each anomaly 
        
        buffers = []
        for i in anomalies:
            for j in [-3,-2,-1, 0,1,2,3]:
                buffers.append(i+j)
        
    
        return buffers