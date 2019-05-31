from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from lmfit import Model
import os,re

data_root_directory='/home/sean/Desktop/5-29-19/NewSpectrometer/' # data directory goes here
sub_folder='27000uW_250ms_NoBin/' # data subfolder goes here
save_folder='spectralData/'

GeV=601

baseline=800.0 # No Binning
# baseline=1100.0 # 4x4 Binning
trigger=1.2
gate=10

# calibration=[543.26,0.13497] #4x4 binning
calibration=[543.741,0.068256] #No binning

numbers=re.compile(r'(\d+)')

def numerical_sort(value):
    parts=numbers.split(value)
    parts[1::2]=map(int,parts[1::2])
    return parts

def find_max_window(df):
    rollingArray=df[0:len(df[0])].rolling(window=gate).mean()[gate-1:len(df[0])]
    loc=[]
    y_window=[]
    for i in range(0,len(df.columns)):
        vals=rollingArray[i].values
        try:
            y=np.min(np.argwhere(vals>=baseline*trigger))
            y_window.append(np.min(np.argwhere(vals[y:len(vals)]<=baseline*trigger)))
        except:
            y=0
            y_window.append(0)
        loc.append(y)
    return [np.max(y_window),loc]
