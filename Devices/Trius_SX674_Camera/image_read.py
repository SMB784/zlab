'''
Created on Aug 11, 2019

@author: sean
'''
from Devices.Trius_SX674_Camera import *

class Image():

    def __init__(self,image_dir):
        self.image_directory=image_dir

    def read_image(self):

        hdul = fits.open(self.image_directory)

        #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
        image=pd.DataFrame(hdul[0].data[:,2:len(hdul[0].data[0,:]-1)]).to_numpy()

        im_fft=fftpack.fft2(image)

        keep_fraction = 0.05

        im_fft2 = im_fft.copy()
        r, c = im_fft2.shape

        im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
        im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
            
        image=pd.DataFrame(fftpack.ifft2(im_fft2).real)
        
        return image