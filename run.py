from mimetypes import init
import os
import sys
import json
import pandas as pd
import shutil

sys.path.insert(0, 'src')
from etl import *
from ensemble_model import *
from eda import *
from metrics import *
#from eda import 
#from train import 
from utils import convert_notebook
from os import listdir, remove
from os.path import isfile, join, expanduser
from time import time
#from metrics import 

# read config
with open('config/run-params.json') as config_json:
    config = config_json.read()
with open('config/ensemble-params.json') as ensemble_json:
    ensemble_config = ensemble_json.read()
with open('config/eda-params.json') as eda_json:
    eda_config = eda_json.read()
# config is now a dictionary
config = json.loads(config)
ensemble_config = json.loads(ensemble_config)
eda_config = json.loads(eda_config)

"""
Sets up all the directories that may have been in the .gitignore or start off empty
"""
def init_():
    # init data folder
    if not os.path.isdir(config['data_path']):
        os.mkdir(config['data_path'])
        os.mkdir(config['raw_path'])
        os.mkdir(config['temp_path'])
        os.mkdir(config['out_path'])
        os.mkdir(config['log_path'])
    if not os.path.isdir(config['fig_path']):
        os.mkdir(config['fig_path'])
    if not os.path.isdir(config['model_path']):
        os.mkdir(config['model_path'])
    if not os.path.isdir(config['test_path']):
        os.mkdir(config['test_path'])
        os.mkdir(join(config['test_path'], 'EDA_data'))
        os.mkdir(join(config['test_path'], 'EDA_data/losslog'))
        os.mkdir(join(config['test_path'], 'EDA_data/packet_data'))

"""
removes all temporary/output files generated in directory.
"""
def clean_():
    # remove folders
    for dir in [config['data_path'], config['fig_path']]:
        shutil.rmtree(dir)
    # remake deleted folders
    init_()

"""
preps the data and features, all the data in the out should be ready to be input in train
data: a list of csv files to stitch together
data_path: folder all of the data csvs are at
"""
def etl_(data, data_path, temp_path, out_path, log_path, filename):
    '''etl target logic. Generates temporary files that are cleaned.'''
    ## dump processed data into temp folder
    return stitch_data(data, data_path=data_path, temp_path=temp_path, out_path=out_path, log_path=log_path, filename=filename)

"""
generates the figures used in the report, does not include metrics
"""
def eda_(conditions):
    plot_timeseries(conditions)
    return

'''
takes all the data listed in the config and trains the model and gives indexes of anomalies
'''
def train_(data_file, ARIMA_window_size, MAD_window_size, threshold):
    df = pd.read_csv(join(config['temp_path'], data_file))
    model = Ensemble()
    predictions = model.anomaly_ensemble(df, ARIMA_window_size, MAD_window_size, threshold)
    with open('predictions.txt', 'a') as f:
        f.write(f'datafile: {data_file}, window size: {ARIMA_window_size}, anomalies: {predictions}')
    return predictions

'''
gets the metrics of the resulting model given a dataset and generates figures
'''
def metrics_(preds, agg_data, filename):
    precision, recall, f1 = get_metrics(preds, agg_data, filename)
    with open('metrics.txt', 'a') as f:
        f.write(f'precision: {precision}, recall: {recall}, F1-score: {f1}')


def main(targets):
    init_()
    # goes under the assumption that all the datafiles have their latency and loss in the name
    # cleans and adds features for all of the csv in the raw data folder
    if 'etl' in targets or 'data' in targets:
        """
        data = generate_data(**data_config)
        save_data(data, **data_config)
        """
        data = ['40_40_5000_a.csv', '40_40_5000_b.csv', '40_40_5000_c.csv','40_40_5000_d.csv', '40_40_5000_e.csv','40_40_5000_m.csv','40_5000_160_1250_a.csv', '40_40_5000_f.csv', '40_40_5000_g.csv', '40_5000_160_1250_b.csv','40_40_5000_h.csv', '40_40_5000_i.csv', '40_5000_160_1250_c.csv', '40_40_5000_j.csv', '40_5000_160_1250_d.csv','40_40_5000_k.csv','40_40_5000_l.csv', '40_5000_160_1250_e.csv']
        etl_(data, config['raw_path'], 
                   config['temp_path'], 
                   config['out_path'],
                   config['log_path'],
                   'data.csv')
        
    if 'eda' in targets:
        conditions = eda_config['conditions'] 
        eda_(conditions)

    if 'train' in targets:
        # this is the filename of the output of etl in the temp folder
        if ensemble_config['data'] == 'None':
            files = os.listdir(config['temp_path'])
            filename = files[0]
        else:
            filename = ensemble_config['data']
        train_(filename, ensemble_config['ARIMA_window_size'], 
                         ensemble_config['MAD_window_size'], 
                         ensemble_config['threshold'])

    if 'metrics' in targets:
        if ensemble_config['data'] == 'None':
            files = os.listdir(config['temp_path'])
            filename = files[0]
        else:
            filename = ensemble_config['data']
        preds = train_(filename, ensemble_config['ARIMA_window_size'], 
                         ensemble_config['MAD_window_size'], 
                         ensemble_config['threshold'])
        df = pd.read_csv(join(config['temp_path'], filename))
        agg_data = aggregate_data(df, ensemble_config['ARIMA_window_size'])
        outfile = 'figures/anomalies.png'
        metrics_(preds, agg_data, outfile)
        
    if 'clean' in targets:
        clean_()

    if 'all' in targets:
        # etl
        data = ['40_40_5000_a.csv', '40_40_5000_b.csv', '40_40_5000_c.csv','40_40_5000_d.csv', '40_40_5000_e.csv','40_40_5000_m.csv','40_5000_160_1250_a.csv', '40_40_5000_f.csv', '40_40_5000_g.csv', '40_5000_160_1250_b.csv','40_40_5000_h.csv', '40_40_5000_i.csv', '40_5000_160_1250_c.csv', '40_40_5000_j.csv', '40_5000_160_1250_d.csv','40_40_5000_k.csv','40_40_5000_l.csv', '40_5000_160_1250_e.csv']
        etl_(data, config['raw_path'], 
            config['temp_path'], 
            config['out_path'],
            config['log_path'],
            'data.csv')

        # eda
        conditions = eda_config['conditions'] 
        eda_(conditions)
        
        # train
        if ensemble_config['data'] == 'None':
            files = os.listdir(config['temp_path'])
            filename = files[0]
        else:
            filename = ensemble_config['data']
            
        train_(filename, ensemble_config['ARIMA_window_size'], 
                         ensemble_config['MAD_window_size'], 
                         ensemble_config['threshold'])

        # metrics
        if ensemble_config['data'] == 'None':
            files = os.listdir(config['temp_path'])
            filename = files[0]
        else:
            filename = ensemble_config['data']

        preds = train_(filename, ensemble_config['ARIMA_window_size'], 
                         ensemble_config['MAD_window_size'], 
                         ensemble_config['threshold'])
        df = pd.read_csv(join(config['temp_path'], filename))
        agg_data = aggregate_data(df, ensemble_config['ARIMA_window_size'])
        outfile = 'figures/anomalies.png'
        metrics_(preds, agg_data, outfile)

    else:
        return

if __name__ == '__main__':

    targets = sys.argv[1:]
    main(targets)