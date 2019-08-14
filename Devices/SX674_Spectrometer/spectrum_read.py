'''
Created on Aug 12, 2019

@author: sean
'''
from Devices.SX674_Spectrometer import *

class Spectrum():
    
    def __init__(self,image_dir,cal_constants):
        self.image=image_dir
        self.calibration=cal_constants

    def read_spectrum(self):
        
        spectrum=image_read.Image(Path(self.image)).read_image()
        window=find_max_window(spectrum)
        spectrum_data=[[],[]]
        
        for i in range(0,len(spectrum.columns)-2): # -1 cuts last datapoint because it is erroneous

            amplitude=np.mean(spectrum.loc[window[1][i]:window[0][i]+window[1][i],i])
            wavelength=np.float(self.calibration[0]+i*self.calibration[1])

            spectrum_data[0].append(wavelength)
            spectrum_data[1].append(amplitude)
        
        spectrum_data[1]=np.flip(spectrum_data[1],axis=0)
        
        return pd.DataFrame(np.transpose(spectrum_data),dtype=float)
