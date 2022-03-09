# code for preprocessing and cleaning our data and features
import json
import pandas as pd
from time import time
import os 
from os.path import join

# read config
with open('config/etl-params.json') as config_json:
    config = config_json.read()
# config is now a dictionary
config = json.loads(config)

trim = config['trim']

'''
Preprocessing for the ARIMA model data
aggregate_data returns a pandas dataframe with mean of total packets sent as the feature and a window size of n

data: a list of csv files from DANE runs
data_path: path to temp_data folder, it should contain all of the data listed in data
out_path: output of the preprocessing, where to put all of the n second aggregations
log_path: where to write the data list used to create the output
filename: name of file to write the aggregated and un aggregated data to, adds prefix timestamp to filename
'''
def stitch_data(data, data_path='../data/raw', temp_path='../data/temp', out_path='../data/out', log_path='../data/out', filename='data.csv'):
    # trims the first 20 seconds (creating the connection)
    df = pd.DataFrame(pd.read_csv(join(data_path, data[0]))[trim:].reset_index().drop('index',axis=1))
    # get total packets of each second
    df['total_pkts'] = df['1->2Pkts'] + df['2->1Pkts']
    df = df[df['total_pkts'] >1].reset_index().drop('index',axis=1)
    df['label'] = data[0]
    # do this for each file in the data folder
    for file in data[1:]:
        dff = pd.DataFrame(pd.read_csv(join(data_path, file))[trim:]).reset_index().drop('index',axis=1)
        dff['total_pkts'] = dff['1->2Pkts'] +df['2->1Pkts']
        dff['label'] = file
        dff = dff[dff.total_pkts > 1].reset_index().drop('index',axis=1)
        df=  pd.concat([df,dff],ignore_index=True)

    # write files used to generate the data
    tm = int(time())
    with open(join(log_path, f'{tm}.txt'), 'w') as f:
        f.write(str(data))

    # write unaggregated data for the mad model
    temp_name = f'{tm}_{filename}'
    df.to_csv(join(temp_path, temp_name))

    return temp_name

'''
Takes in a dataframe and outputs a dataframe aggregated on n seconds
df: dataframe to get n second aggregations on
n: a paramter to change the window size of network traffic. i.e. n=20 would transform the dataset into 20 second windows
'''
def aggregate_data(df, n):
    # cuts off any remainder rows so cardinatity is divisible by n
    df = df[:len(df) - (len(df) %n)]
    # aggregate on n seconds, does it row by row
    df_agg = pd.DataFrame([df[:n]['total_pkts'].mean(),df[:n].label.unique()[0]],index=['total_pkts','label']).T
    for i in range(n,df.shape[0],n):
        df_agg = pd.concat([df_agg,pd.DataFrame([df[i:i+n]['total_pkts'].mean(),df[i:i+n].label.unique()[0]],index=['total_pkts','label']).T],ignore_index=True)
    
    return df_agg, df