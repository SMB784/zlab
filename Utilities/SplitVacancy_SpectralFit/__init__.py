'''
Created on Aug 9, 2019

@author: sean

The spectrum_fit module in this utility used to read in a pandas dataframe
containing a split-vacancy fluorescence spectrum, fit the peaks with various
user selectable fit functions found in the init file, and output a fit
spectrum and associated fit values 

Required inputs:  upper and lower spectral wavelength bounds, pandas dataframe
containing spectrum, desired fitting function from functions listed below
Returned outputs: fit spectrum and fit values

Example usage:

from SplitVacancy_SpectralFit import *
from SplitVacancy_SpectralFit import spectral_fit

spec_start=600
spec_stop=625
input_spectrum=pd.DataFrame([np.arange(1,625),np.random.rand(1,625)])
spectral_data=spectrum_fit.Fit(spec_start,spec_stop,input_spectrum).fit_spectrum()
print(spectrum)

'''
from lmfit import Model
from pathlib import Path
import numpy as np
import pandas as pd
import re

GeV=601
tolerance=0.3

initial_fit=[]

temp_cal=[] # from center wavelength vs temp: [intercept, slope]

def doubleLorentzianFit(x,c1,c2,\
                w1,w2,\
                h1,h2,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
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

def lorentzianDoubleGaussianFit(x,c1,c2,c3,\
                                w1,w2,w3,\
                                h1,h2,h3,\
                                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c2)**2/(2*w2**2))\
           +h3/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c3)**2/(2*w3**2))\
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