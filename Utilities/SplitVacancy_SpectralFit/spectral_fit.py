'''
Created on Aug 12, 2019

@author: sean
'''
from Utilities.SplitVacancy_SpectralFit import *

class Fit():

    def __init__(self,spec_start,spec_stop,input_data):
        self.start=spec_start
        self.stop=spec_stop
        self.spectrum=input_data

    def fit_spectrum(self):
        
        lambdaStartIndex=self.spectrum[self.spectrum[[0]].apply(np.isclose,b=self.start,atol=tolerance).any(1)].index.tolist()[0]
        lambdaStopIndex=self.spectrum[self.spectrum[[0]].apply(np.isclose,b=self.stop,atol=tolerance).any(1)].index.tolist()[0]

        wavelength=self.spectrum.iloc[lambdaStartIndex:lambdaStopIndex,0].to_numpy()
        amplitude=self.spectrum.iloc[lambdaStartIndex:lambdaStopIndex,1].to_numpy()
        normalized_amplitude=(amplitude-amplitude.min())/(amplitude.max()-amplitude.min())

        result=lmodel.fit(normalized_amplitude,params,x=wavelength)

        raw_spectrum=wavelength
        spectrum_fit=wavelength
        
        raw_spectrum=np.c_[raw_spectrum,normalized_amplitude]
        spectrum_fit=np.c_[spectrum_fit,result.best_fit]
        
        fit_values=np.array(findValue(result.best_values))

        return raw_spectrum,spectrum_fit,fit_values
