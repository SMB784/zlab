'''
Created on Aug 9, 2019

@author: sean

The spectrum_read module in this device used to read .FIT spectral image
files output by the Trius SX674 Camera. 

Required inputs:  .FIT image file directory, camera calibration values
Returned outputs: pandas dataframe containing wavelength and amplitude data

Example usage:

from SX674_spectrometer import *
from SX674_spectrometer import spectrum_read

image_directory=/home/foo.FIT
cal_constants=[543.26,0.13497]
spectrum=spectrum_read.Spectrum(image_directory,cal_constants).read_spectrum()
print(spectrum)

'''
########################## Import bolt-on modules ############################
from Devices.Trius_SX674_Camera import *
from Devices.Trius_SX674_Camera import image_read
########################## Import built-in modules ###########################
from pathlib import Path
import os

trigger=1.2

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