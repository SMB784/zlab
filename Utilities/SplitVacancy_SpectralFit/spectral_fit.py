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

        initial_fit=[[601.0,612,625],\
                     [4.5,11,40],\
                     [1,1,1],0]

        lmodel=Model(lorentzianGaussianFit)

        lmodel.set_param_hint('c1',min=598,max=605)
        lmodel.set_param_hint('c2',min=610,max=630)
        lmodel.set_param_hint('c3',min=605,max=630)
                
        lmodel.set_param_hint('w1',min=0)
        lmodel.set_param_hint('w2',min=5,max=20)
        lmodel.set_param_hint('w3',min=0,max=50)
                        
        params=lmodel.make_params(c1=initial_fit[0][0],w1=initial_fit[1][0],h1=initial_fit[2][0],\
                                  c2=initial_fit[0][1],w2=initial_fit[1][1],h2=initial_fit[2][1],\
                                  c3=initial_fit[0][2],w3=initial_fit[1][2],h3=initial_fit[2][2],\
                                  o1=initial_fit[3])
        
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
