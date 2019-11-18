'''
Created on Aug 9, 2019

@author: sean

The spectrum_read module in this device used to read .csv spectrum
files output by the Science Surplus spectrometer and generates a 
spectrum dataframe output. 

Required inputs:  .csv spectrum file directory
Returned outputs: pandas dataframe containing wavelength and amplitude
data

Example usage:

from Devices.ScienceSurplus_Spectrometer import *
from Devices.ScienceSurplus_Spectrometer import spectrum_read

data_directory=/home/foo.csv
cal_constants=[543.26,0.13497]
spectrum=spectrum_read.Spectrum(image_directory).read_spectrum()
print(spectrum)
'''
########################## Import built-in modules ###########################
from pathlib import Path
import os
import pandas as pd
import numpy as np