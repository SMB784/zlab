'''
Created on Aug 11, 2019

@author: sean
'''
from astropy.io import fits
import pandas as pd
import numpy as np
from scipy import stats,fftpack
import matplotlib.pyplot as plt

def plot_image(image):
    plt.imshow(np.abs(np.fliplr(image)),plt.cm.gray)
    plt.show()
