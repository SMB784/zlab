'''
Created on Dec 6, 2019

@author: sean
'''
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os
from Utilities.TeamDrive_DataDownload import numerical_sort

data_directory='/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/12-5-19_Fiber-Bending/pics/position_average_frames/'

curvature=[0.1177,0.125,0.1333,0.1429,0.1538,0.1667,0.1818]
image_list=[]

def normalize(image):
    image_norm=(image-np.min(image))/(np.max(image)-np.min(image))
    return image_norm


for root,dirs,files in os.walk(data_directory,topdown=True):
    file_count=0
    for file in sorted(files,key=numerical_sort):
        files.sort(key=numerical_sort)
        
        if(file_count>2):
            input_image=pd.read_csv(Path(data_directory)/file,header=None).to_numpy()[255:305,355:405]
            image_list.append(normalize(input_image))

        file_count+=1

fig=plt.figure(figsize=(16, 4))

for i in range(1,len(image_list)+1):
    fig.add_subplot(1,len(image_list), i,title=r'r='+str(curvature[i-1])+' $cm^{-1}$')
    if(i==1):
        plt.imshow(image_list[i-1],plt.cm.gray)
        plt.ylabel("y-axis Pixel #")
        plt.xlabel("x-axis Pixel #")
    else:
        plt.imshow(image_list[0]-image_list[i-1],plt.cm.hsv)
        plt.xlabel("x-axis Pixel #")

plt.tight_layout()
plt.show()