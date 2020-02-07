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

def moving_average(a, n) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

data_directory='/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/12-5-19_Fiber-Bending/spectra/traces/'

average_temp=[]
std=[]
curvature=[9,8.5,8,7.5,7,6.5,6,5.5]

mpl.rcParams.update({'font.size': 24})

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

            delta_t=input_traces[0]-np.mean(first_trace[0])
            
            average_temp.append(np.mean(delta_t))
            std.append(np.std(delta_t))
            
            window=100
            
            if(file_count%2==0):
                plt.plot(np.arange(len(input_traces[0]))[window-1:]*period,moving_average(delta_t,window),lw=3,label=r'$R_{c}$='+str(curvature[file_count-2]))
                plt.xlabel("Time (sec)")
                plt.ylabel("$\delta \lambda$ (nm)")
                plt.ylim(-0.03,0.02)

        file_count+=1

plt.legend(loc="upper left",fontsize=12,ncol=2)
plt.tight_layout()
plt.show()


plt.plot(curvature,average_temp,lw=3,c='b')
plt.errorbar(curvature,average_temp,yerr=std,lw=3,capsize=5,capthick=3,marker='o',fmt='.',c='brape')
plt.xlabel(r"$R_{c}$ (cm)")
plt.ylabel(r"$\langle\delta \lambda \rangle$ (nm)")
plt.tight_layout()
plt.show()