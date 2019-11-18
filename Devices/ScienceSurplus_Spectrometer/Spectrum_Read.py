'''
Created on Nov 16, 2019

@author: sean
'''
from Devices.ScienceSurplus_Spectrometer import *

class Spectrum():
    
    def __init__(self,*args):
        self.spectrum_file=args[0]

    def read_spectrum(self):
        
        read_fields=[1,3]
        spectrum_data=pd.read_csv(self.spectrum_file,skiprows=5,usecols=read_fields,header=None,dtype=float)
        spectrum_data.columns=[0,1]
        
        return spectrum_data
