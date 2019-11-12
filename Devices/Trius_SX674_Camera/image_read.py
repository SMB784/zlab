'''
Created on Aug 11, 2019

@author: sean
'''
from Devices.Trius_SX674_Camera import *
import Devices.Trius_SX674_Camera

class Image():

    def __init__(self,*args):
        if len(args) == 1:
            self.image_directory=args[0]
        else:
            self.image_directory=args[0]
            self.dark_directory=args[1]

    def read_image(self):

        hdul = fits.open(self.image_directory)

        #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
        image=pd.DataFrame(hdul[0].data[:,2:len(hdul[0].data[0,:]-1)]).to_numpy(dtype=np.int32)
        im_fft=fftpack.fft2(image)

        keep_fraction = 0.05

        im_fft2 = im_fft.copy()
        r, c = im_fft2.shape

        im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
        im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
 
        image=pd.DataFrame(fftpack.ifft2(im_fft2).real)

        return image
    
    def calculate_dark_frame(self):
        dark_count=0
        for root,dirs,files in os.walk(Path(self.image_directory)/self.dark_directory,topdown=True):
            
            for file in sorted(files,key=numerical_sort):
                files.sort(key=numerical_sort)
                
                dark_fits = fits.open(Path(Path(self.image_directory)/self.dark_directory)/file)
                
                if(dark_count==0):
                    image=pd.DataFrame(dark_fits[0].data[:,2:len(dark_fits[0].data[0,:]-1)]).to_numpy(dtype=np.int32)
                    dark_count+=1
                else:
                    image+=pd.DataFrame(dark_fits[0].data[:,2:len(dark_fits[0].data[0,:]-1)]).to_numpy(dtype=np.int32)
                    dark_count+=1

        return image/dark_count