'''
Created on Aug 11, 2019

@author: sean
'''
from Trius_SX674_Camera import *

class Image():

    def __init__(self,image_dir):
        self.image_directory=image_dir

    def read_image(self):

        hdul = fits.open(self.image_directory)

        #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
        image=pd.DataFrame(hdul[0].data[:,2:len(hdul[0].data[0,:]-1)])
        return image
