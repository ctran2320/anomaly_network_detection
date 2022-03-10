"""
generates metrics of our model if any
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_metrics(preds, aggregated_data, filepath=None):
    """
    Returns model performance metrics given final predictions and training data
    """
    # indeces where changes occure --> Positives

    change_indices = []
    for i in range(len(aggregated_data.anomaly)):
        if aggregated_data.anomaly[i] == 1:
            change_indices.append(i)
    anomalous_sets = [] # Positive sets
    new_set = set()
    first = True
    for i in range(len(aggregated_data.anomaly)):
        if first == True:
            if aggregated_data.anomaly[i] == 1:
                new_set.add()
            first = False
        elif aggregated_data.anomaly[i] == 1:
            new_set.add(i)
        elif aggregated_data.anomaly[i] == 0 and aggregated_data.anomaly[i-1] == 1:
            anomalous_sets.append(new_set)
            new_set = set()
    if len(new_set) != 0:
        anomalous_sets.append(new_set)

    # false positives
    fp = 0
    tn = 0
    negative = set(range(len(aggregated_data)))
    for s in anomalous_sets:
        negative = negative - s
    fp = len(preds.intersection(negative))
    tn = len(negative - preds)

    # false negatives and true positives
    preds = set(preds)
    fn = 0
    tp = 0
    for s in anomalous_sets:
        if len(s.intersection(preds)) == 0:
            fn += 1
        else:
            tp += 1

    precision = tp / (tp+fp)
    recall = tp / (tp+fn)
    f1 = (2*(precision*recall)) / (precision+recall)
    # output ensemble predictions graph,
    if filepath != None:
        plt.plot(aggregated_data.total_pkts)
        for i in preds:
            plt.scatter(i, aggregated_data.total_pkts[i], color='red')
        plt.title('Total Pkts per 20 seconds')
        plt.xlabel('Seconds')
        plt.ylabel('Total Pkts')
        plt.savefig(filepath)

    return precision, recall, f1
   
    