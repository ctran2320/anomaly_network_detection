# For figures that are used for EDA
import pandas as pd
import matplotlib.pyplot as plt
import os
from os import listdir, join
import seaborn as sns
import numpy as np
import sys

from etl import clean_df
from train import MAD

"""
Creates a correlation matrix for the features
"""
def plot_correlation(data_filename, outdir, filename="correlation_matrix.png"):
    raise NotImplementedError()

"""
Creates a time plot of the number of packets being sent per second and where packets are dropped if file exists

conditions data was generated on, format: f"{latency1} {loss1} {latency2} {loss2} {random drops}"
data_path: path with folder of loss logs and packet data
outdir: directry to put the graph
filename: name of the graph image to save
"""
def plot_timeseries(conditions, data_path, outdir, filename="timeseries.png"):
    # list the packet data files
    raw_data_path = join(data_path, 'packet_data')
    raw_files_loss = [join(raw_data_path, f) for f in listdir(raw_data_path)]

    # packet drop data
    raw_data_path = join(data_path, 'loss_logs')
    raw_files = [join(raw_data_path, f) for f in listdir(raw_data_path)]

    # associates conditions with filenames
    metrics = []
    filenames = {}
    for file in raw_files:
        labels = file.split('_')[-1].split('-')
        metrics = metrics + [labels[0] +' '+ labels[1] +' '+ labels[3]+' '+labels[4]+' '+labels[2]]
        filenames[labels[0] +' '+ labels[1] +' '+ labels[3]+' '+labels[4]+' '+labels[2]] = [file]
        
    for file in raw_files_loss:
        labels = file.split('.')[-2].split('-')
        filenames[labels[1] +' '+ labels[2] +' '+ labels[4]+' '+labels[5]+' '+labels[3]] += [file]

    # find the data that meets the conditions
    f = filenames[conditions][0]
    f_drop = filenames[conditions][1]

    data = pd.read_csv(f)
    data_drop = pd.read_csv(f_drop, header=None)
    data_drop.columns = ['drop', 'Time', 'IP1', 'Port1', 'IP2', 'Port2', '?']
    clean = clean_df(data)
    plt.plot(clean['1->2Pkts'])

    port = data_drop['Port1']
    time = data_drop['Time'] - data['Time'].min()
    max_pkts = clean['1->2Pkts'].max()

    for i in range(len(time)):
        # confirmation (computer 2)
        if port[i] == 5001:
            plt.vlines(time[i], 0, max_pkts, colors='C1', alpha=0.3)
            pass
        # data (computer 1)
        else:
            plt.vlines(time[i], 0, max_pkts, colors='C2', alpha=0.3)
            pass

    plt.vlines(180, 0, max_pkts, colors='C3')

    plt.title(f'packets per second, conditions: {conditions}')
    plt.ylabel('packets per second')
    plt.xlabel('time')

    # plt.legend()
    # saves graph to directory
    plt.savefig(os.path.join(outdir, filename))

def plot_MAD(conditions, data_path, outdir, filename=['median.png', 'MAD.png']):
    # list the packet data files
    raw_data_path = join(data_path, 'packet_data')
    raw_files_loss = [join(raw_data_path, f) for f in listdir(raw_data_path)]

    # packet drop data
    raw_data_path = join(data_path, 'loss_logs')
    raw_files = [join(raw_data_path, f) for f in listdir(raw_data_path)]

    # associates conditions with filenames
    metrics = []
    filenames = {}
    for file in raw_files:
        labels = file.split('_')[-1].split('-')
        metrics = metrics + [labels[0] +' '+ labels[1] +' '+ labels[3]+' '+labels[4]+' '+labels[2]]
        filenames[labels[0] +' '+ labels[1] +' '+ labels[3]+' '+labels[4]+' '+labels[2]] = [file]
        
    for file in raw_files_loss:
        labels = file.split('.')[-2].split('-')
        filenames[labels[1] +' '+ labels[2] +' '+ labels[4]+' '+labels[5]+' '+labels[3]] += [file]

    f = filenames[conditions][0]
    data = pd.read_csv(f)
    clean = clean_df(data)
    X = clean['1->2Pkts']
    median, median_dev = MAD(clean)
    
    plt.figure()
    plt.plot(X, alpha=0.3, label='1->2pkts')
    plt.plot(X.index[(len(X)-len(median)):],median, label='median')
    plt.vlines(180, 0, max(X), colors='C3')
    plt.title(f'1->2 packets, conditions: {conditions}')
    plt.ylabel('packets')
    plt.xlabel('time')    
    plt.legend()
    plt.savefig(join(outdir, filename[0]))

    plt.figure()
    plt.plot(X, alpha=0.3, label='1->2pkts')
    plt.plot(X.index[(len(X)-len(median)):], median_dev, label='MAD')
    plt.vlines(180, 0, max(X), colors='C3')
    plt.title(f'MAD, conditions: {conditions}')
    plt.ylabel('Median Absolute Deviation (1->2pkts)')
    plt.xlabel('time')    
    plt.legend()
    plt.savefig(join(outdir, filename[1]))
