from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from pathlib import Path
from scipy import stats,fftpack
from scipy.integrate import simps
from lmfit import Model
from TeamDrive_DataDownload import *
import os,re,io,sys

data_root_directory=Path(Path(os.getcwd())/'data/')

GeV=601
tolerance=0.2

calibration=[543.26,0.13497] #4x4 binning
# calibration=[543.741,0.068256] #No binning

initial_fit=[]

temp_cal=[] # from center wavelength vs temp: [intercept, slope]

def find_max_window(df):
    loc=[]
    y_window=[]
    for i in range(0,len(df.columns)-2):

        vals=df[i].values
        baseline=np.mean(df[i].values[0:150])
        maximum=np.max(vals)
        trigger=(maximum-baseline)/2
        vals=vals-baseline
        
        try:
            y_min=np.min(np.argwhere(vals>=trigger))
            y_window.append(np.min(np.argwhere(vals[y_min:len(vals)]<=trigger)))
        except ValueError:  #raised if `y` is empty.
            y_min=0
            y_window.append(0)
        loc.append(y_min)
    return [y_window,loc]

def doubleLorentzianFit(x,c1,c2,\
                w1,w2,\
                h1,h2,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +o1

def lorentzianGaussianFit(x,c1,c2,\
                          w1,w2,\
                          h1,h2,\
                          o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c2)**2/(2*w2**2))\
           +o1

def tripleLorentzianFit(x,c1,c2,c3,\
                w1,w2,w3,\
                h1,h2,h3,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(np.pi*w3)*(w3**2/((x-c3)**2+w3**2))\
           +o1

def lorentzianDoubleGaussianFit(x,c1,c2,c3,\
                                w1,w2,w3,\
                                h1,h2,h3,\
                                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c2)**2/(2*w2**2))\
           +h3/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c3)**2/(2*w3**2))\
           +o1

def doubleLorentzianGaussianFit(x,c1,c2,c3,\
                                w1,w2,w3,\
                                h1,h2,h3,\
                                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(w3*np.sqrt(2*np.pi))*np.exp(-(x-c3)**2/(2*w3**2))\
           +o1

def findValue(bestValues): #input is dictionary output from result.best_values
    center_FWHM=[]
    for key, value in bestValues.items():
        if np.isclose(a=value,b=GeV,atol=tolerance*10):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
    return center_FWHM