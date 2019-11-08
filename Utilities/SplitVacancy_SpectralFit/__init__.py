'''
Created on Aug 9, 2019

@author: sean

The spectrum_fit module in this utility used to read in a pandas dataframe
containing a split-vacancy fluorescence spectrum, fit the peaks with various
user selectable fit functions found in the init file, and output a fit
spectrum and associated fit values 

Required inputs:  start and stop spectral wavelengths, pandas dataframe
containing spectrum
Returned outputs: windowed spectrum, fit spectrum for specified window,
and fit values

Example usage:

from SplitVacancy_SpectralFit import *
from SplitVacancy_SpectralFit import spectral_fit

spec_start=600
spec_stop=625
input_spectrum=pd.DataFrame([np.arange(1,625),np.random.rand(1,625)])
spectral_data=spectral_fit.Fit(spec_start,spec_stop,input_spectrum,fit_model).fit_spectrum()
print(spectral_data)

'''
from lmfit import Model
from pathlib import Path
import numpy as np
import pandas as pd
import re

tolerance=0.5

initial_fit=[[601.0,612,625],\
            [4.5,11,20],\
            [1,1,1],0]

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

def findValue(bestValues,peak_wavelength): #input is dictionary output from result.best_values
    center_FWHM=[]
    for key, value in bestValues.items():
        # returns center wavelength and FWHM values if center wavelength is
        # within tolerance*2 of the GeV center wavelength, else returns 0
        if np.isclose(a=value,b=peak_wavelength,atol=tolerance*2):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
        else:
            center_FWHM.append(0)
            center_FWHM.append(0)
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

lmodel=Model(doubleLorentzianFit)

lmodel.set_param_hint('c1',min=598,max=605)
lmodel.set_param_hint('c2',min=610,max=620)
lmodel.set_param_hint('c3',min=620,max=630)
                
lmodel.set_param_hint('w1',min=0)
lmodel.set_param_hint('w2',min=5,max=20)
lmodel.set_param_hint('w3',min=0,max=50)

params=lmodel.make_params(c1=initial_fit[0][0],w1=initial_fit[1][0],h1=initial_fit[2][0],\
                          c2=initial_fit[0][1],w2=initial_fit[1][1],h2=initial_fit[2][1],\
                          c3=initial_fit[0][2],w3=initial_fit[1][2],h3=initial_fit[2][2],\
                          o1=initial_fit[3])