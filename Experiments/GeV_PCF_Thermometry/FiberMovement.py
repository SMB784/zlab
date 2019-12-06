'''
Created on Dec 4, 2019

@author: sean
'''
import pandas as pd
import numpy as np
from scipy import stats
import scipy.fftpack
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from pathlib import Path
from Utilities.TeamDrive_DataDownload import numerical_sort

data_directory='/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/12-5-19_Fiber-Bending/spectra/traces/'

average_temp=[]
curvature=[0.1111,0.1177,0.125,0.1333,0.1429,0.1538,0.1667,0.1818]

for root,dirs,files in os.walk(data_directory,topdown=True):
    file_count=0
    for file in sorted(files,key=numerical_sort):
        files.sort(key=numerical_sort)
        

        if(file_count>1):

            input_traces=np.transpose(pd.read_csv(Path(data_directory)/file,header=None).fillna(601.0).to_numpy())

            period=0.05
            sample_size=len(input_traces[0])
            if(file_count==2):
                first_trace=input_traces
            
            frequency=np.linspace(0.0, 1.0/(2.0*period), int(sample_size/2))
            temp_noise=np.c_[frequency,2.0/sample_size*np.abs(scipy.fftpack.fft((input_traces[1]/0.0078-np.mean(input_traces[1]/0.0078))*1000)[:sample_size//2])]
            temp_noise=np.transpose(temp_noise)
            
    #         print("avg temp, stdev position 1: "+str(0)+"K, "+str(np.std(input_traces[1]/0.0078-np.mean(input_traces[1]/0.0078)))+'K')
    #         print("avg temp, stdev position 2: "+str(np.abs(np.mean(input_traces[2]/0.0078-np.mean(input_traces[1]/0.0078))))+"K, "+str(np.std(input_traces[2]/0.0078-np.mean(input_traces[1]/0.0078)))+'K')
    #         print("Average noise in position 1, 2: "+str(np.mean(temp_noise[1]))+'mK, '+str(np.mean(temp_noise[2]))+'mK')
    # 
    #         plt.loglog(temp_noise[0][1:],temp_noise[file_count][1:],lw=2,zorder=15-file_count)
    # 
    #         plt.xlabel("Frequency (Hz)")
    #         plt.ylabel("$\delta$T (mK)")
    #         plt.show()

            delta_t=input_traces[0]/0.0078-np.mean(first_trace[0]/0.0078)
            
            average_temp.append(np.mean(delta_t))
            
            plt.plot(np.arange(len(input_traces[0]))*period,delta_t)
            plt.xlabel("Time (sec)")
            plt.ylabel("$\delta$T (K)")
            plt.ylim(-10,10)

        file_count+=1

plt.show()

plt.scatter(curvature,average_temp)
plt.xlabel(r"Curvature ($cm^{-1}$)")
plt.ylabel(r"$\langle\delta T\rangle$ (K)")
plt.show()