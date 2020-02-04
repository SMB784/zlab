'''
Created on Feb 4, 2020

@author: sean

The spectrum_read module in this device used to read .csv spectrum
files output by the custom Labview softawre for the science surplus
spectrometer and generates a spectrum dataframe output. 

Required inputs:  .csv spectrum file directory
Returned outputs: pandas dataframe containing wavelength and amplitude
data

Example usage:

from Devices.Labview_Spectrometer import *
from Devices.Labview_Spectrometer import SpectrumRead

data_directory=/home/foo.csv
cal_constants=[543.26,0.13497]
spectrum=SpectrumRead.Spectrum(data_directory).read_spectrum()
print(spectrum)
'''
########################## Import built-in modules ###########################
from pathlib import Path
import os
import pandas as pd
import numpy as np