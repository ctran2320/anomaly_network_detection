# generates metrics of our model if any
import pandas as pd
import matplotlib as plt
import numpy as np

def plot_results(preds, data,anomalies, n, log=False):
    preds = pd.DataFrame(preds)
    preds['time'] = np.arange(n,len(preds)+n)
    preds= preds.rename({0:'preds'},axis=1).set_index('time')
    preds['anomaly'] = anomalies
    preds['actual'] =data.total_pkts[n:]
    anom = preds[preds.anomaly==1]
    if log == True:
        plt.plot(np.log(data.total_pkts),label='actual')
        plt.plot(preds.preds,label='preds')
        plt.scatter(anom.index,np.log(anom.actual),label='anomaly',c='r',s=100)
    if log == False:
        plt.plot(data.total_pkts,label='actual')
        plt.scatter(anom.index,anom.actual,label='anomaly',c='r',s=100)
    plt.legend()
    plt.xlabel('Time (10s)')
    plt.ylabel('Total Packets Sent')
    plt.title('Anomaly Detection 40-5000-320-1250 (99% CI)')
    plt.savefig('output.png', dpi=300)