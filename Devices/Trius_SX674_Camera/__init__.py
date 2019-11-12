'''
Created on Aug 11, 2019

@author: sean

The image_read module in this device is used to read .FIT spectral image
files output by the Trius SX674 Camera and generates an image in the form
of a pixel dataframe. 

Required inputs:  .FIT image file directory
Returned outputs: pandas dataframe containing pixel values from the image

Example usage:

from Devices.Trius_SX674_spectrometer import *
from Devices.Trius_SX674_spectrometer import image_read

image_directory=/home/foo.FIT
image=image_read.Image(image_directory).read_image()
plot_image(image)

'''
from astropy.io import fits
import pandas as pd
import numpy as np
from scipy import stats,fftpack
import matplotlib.pyplot as plt
import os
from pathlib import Path
from Utilities.TeamDrive_DataDownload import numerical_sort

def plot_image(image):
    plt.imshow(image,plt.cm.gray)
    plt.show()
