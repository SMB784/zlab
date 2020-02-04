'''
Created on Feb 4, 2020

@author: Sean
'''
from Devices.Labview_Spectrometer import *

class Spectrum():
    
    def __init__(self,*args):
        self.spectrum_file=args[0]

    def read_spectrum(self):
        
        read_fields=[0,2]
        spectrum_data=pd.read_csv(self.spectrum_file,skiprows=5,usecols=read_fields,header=None,dtype=float)
        spectrum_data.columns=[0,1]
        pixels=spectrum_data[0].astype(float)
        spectrum_data[0]=169.3+0.6413*pixels-6.398*10**(-5)*pixels**2-4.061*10**(-9)*pixels**3

        return spectrum_data
