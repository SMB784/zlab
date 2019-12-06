'''
Created on Dec 6, 2019

@author: sean
'''
from Devices.Sony_DMK_23G618_Camera import *

class Image():
    
    def __init__(self,*args):
        self.image_file=args[0]

    def read_image(self):
        
        image_data=imread(self.image_file).astype(float)
        
        return image_data
