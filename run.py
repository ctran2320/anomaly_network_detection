import os
import sys
import json
import pandas as pd

sys.path.insert(0, 'src')
#from etl import 
#from eda import 
#from train import 
from utils import convert_notebook
from os import listdir, remove
from os.path import isfile, join, expanduser
from time import time
#from metrics import 

"""
Sets up all the directories that may have been in the .gitignore or start off empty
"""
def init_():
    if not os.path.isdir('data/'):
        os.mkdir('data')
        os.mkdir(raw_data_path)
        os.mkdir(temp_path)
        os.mkdir(out_path)
    if not os.path.isdir(img_path):
        os.mkdir(img_path)
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    if not os.path.isdir('test/testtemp'):
        os.mkdir('test/testtemp')
    if not os.path.isdir('test/test_features'):
        os.mkdir('test/test_features')

"""
removes all temporary/output files generated in directory.
"""
def clean_():
    # for dr_ in [temp_path, out_path, model_path, img_path]:
    for dr_ in [temp_path, out_path]:
        for f in listdir(dr_):
            remove(join(dr_, f))

"""
preps the data and features, all the data in the out should be ready to be input in train
"""
def etl_(raw_data_path=raw_data_path, temp_path=temp_path, out_path=out_path, test=False):
    '''etl target logic. Generates temporary files that are cleaned.'''
    ## dump featurized data into temp folder
    data_csv_files = [join(raw_data_path, f) for f in listdir(raw_data_path)]
    return

"""
generates the figures used in the report, does not include metrics
"""
def eda_(data_folder_path=figure_data_path, img_path=img_path):
    return

"""
Saves trained model to pickle
"""
def train_(data_path=out_path, model_path=model_path, model_name='model', test=False):
    '''trains a model to predict latency and packet loss with the output of etl and features.'''
    return