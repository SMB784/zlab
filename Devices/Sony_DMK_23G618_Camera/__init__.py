'''
Created on Aug 9, 2019

@author: sean

The img_read module in this device used to read .bmp images output by
the Sony DMK-23G618 camera and generates an image dataframe output. 

Required inputs:  .bmp file directory
Returned outputs: numpy array containing greyscale image data

Example usage:

from Devices.Sony_DMK-23G618_Camera import *
from Devices.Sony_DMK-23G618_Camera import img_read

image_directory=/home/foo.bmp
image=img_read.Image(image_directory).read_image()
print(image)
'''
########################## Import built-in modules ###########################
from pathlib import Path
import os
import pandas as pd
import numpy as np
from imageio import imread