import numpy as np 
import matplotlib.pyplot as plt

'''
the data (x) is a 1 dimentional numpy array of the 1->2 packets
'''



class MAD_model():
    '''
    inputs
    window_size: size of window to shift over
    thresh_height: height of the threshold to detect an anomaly on
    '''
    def __init__(self, window_size, IQR_mult=1.5):
        self.window_size = window_size
        self.IQR_mult = IQR_mult
        self.window = np.zeros(window_size)
        # median, median absolute deviation and deviation from median if needed later
        # for the most recent data passed into rolling_stats
        self.median = None
        self.mad = None
        self.dm = None
    
    '''
    Computes the rolling MAD, Median and average deviation from the median
    returns transform: a function of the 3 stats above
    '''
    def rolling_stats(self, x):
        mad_f = lambda x: np.percentile(np.fabs(x - np.percentile(x, 50)), 60)
        
        median = []
        dm = []
        mad = []
        
        for i in range(len(x)-self.window_size):
            subset = x[i:i+self.window_size]
            m = np.median(subset)
            median = median + [m]
            dm = dm + [np.sum(subset-m)/self.window_size]
            mad = mad + [mad_f(subset)]
        
        transform = np.array(mad)*dm / median
        self.median = median
        self.mad = mad
        self.dm = dm
        
        return transform
    
    '''
    detects an anomaly if the function of median, mad and dm are above a certain threshold
    return the indexes of where the anomaly is, already adjusted to the window size
    '''
    def detect_anomaly(self, x):
        transform = self.rolling_stats(x)
        anomaly_index = []
        '''
        index = np.arange(len(transform))
        anomaly_index = index[(transform > self.thresh)] + self.window_size // 2
        '''
        
        for i in np.arange(len(transform) - self.window_size) + self.window_size:
            subset = transform[i:i+self.window_size]
            
            thresh = 100 / (self.window_size / 100)
          
            if thresh < transform[i]:
                anomaly_index = anomaly_index + [i]
        
        return np.array(anomaly_index) + self.window_size // 2
   
    '''
    Turns 1 second time stamps for anomalies into n second aggregations if the % of 
    anomalies in the window is above a threshold
    '''
    def aggregate_anomalies(self, data, n, thresh, original_dataframe):
        len_og_df = original_dataframe.shape[0]
        data = data[:len_og_df-(len_og_df%n)]
        anomalies = set(data)
        t = range(len_og_df)
        aggregation = []
        for i in range(0, len_og_df // n - 1):
            window = set(t[i*n:(i+1)*n])
            percent = len(anomalies.intersection(window)) / n
            if percent > thresh:
                aggregation.append(i)
        return aggregation

    '''
    plots the data and anomolous region detected given the data and conditions
    '''
    def plot_region(self, x, conditions, shift_time=None,  filepath=None):
        anom_region = self.detect_anomaly(x)
        
        plt.plot(x, label='1->2pkts')
        
        plt.vlines(anom_region, min(x), max(x), colors='C3', alpha=.2)
        
        if shift_time != None:
            plt.vlines(180, 0, max(x), colors='C3')
        
        plt.title(f'1->2 packets, conditions: {conditions}')
        plt.ylabel('packets')
        plt.xlabel('time') 
        plt.legend()
        
        if filepath != None:
            plt.savefig(filepath)


    def MAD_anomalies(self, model, data): 
        """
        Outputs list of anomaly predictions 
        """
        X = np.array(data)
        anomalies_indexes = model.detect_anomaly(X)
        
        buffers = []
        for i in anomalies_indexes:
            for j in [-2,-1,0,1,2]:
                buffers.append(i+j)
            
        return buffers


