'''
Created on Aug 12, 2019

@author: sean
'''
from Devices.SX674_Spectrometer import *

class Spectrum():
    
    def __init__(self,*args):
        if len(args)==2:
            self.image=args[0]
            self.calibration=args[1]
            self.found_dark_frame=False
        else:
            self.image=args[0]
            self.dark_frame=args[1]
            self.calibration=args[2]
            self.found_dark_frame=True
    def read_spectrum(self):
        
        if self.found_dark_frame==True:
            spectrum=image_read.Image(Path(self.image)).read_image()-self.dark_frame
        else:
            spectrum=image_read.Image(Path(self.image)).read_image()
        window=find_max_window(spectrum)
        spectrum_data=[[],[]]
        
        for i in range(0,len(spectrum.columns)-2): # -1 cuts last datapoint because it is erroneous

            amplitude=np.max(spectrum.loc[window[1][i]:window[0][i]+window[1][i],i])
            wavelength=np.float(self.calibration[0]+i*self.calibration[1])

            spectrum_data[0].append(wavelength)
            spectrum_data[1].append(amplitude)
        
        spectrum_data[1]=np.flip(spectrum_data[1],axis=0)
        
        return pd.DataFrame(np.transpose(spectrum_data),dtype=float)
