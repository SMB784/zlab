'''
Created on Nov 6, 2019

@author: sean
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

temp_trace_9mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity/1ms_4x4Bin_50mW/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity/10ms_4x4Bin_23mW/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_2_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity/100ms_4x4Bin_12mW/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_0_5=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity/1000ms_4x4Bin_2mW/processed_data/'+'temp_values.csv',header=None).to_numpy())

# temp_trace_9mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/47000uW_1ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/11000uW_10ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_2_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/730uW_100ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_0_5=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/76uW_1000ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())

temp_trace=[temp_trace_9mW,temp_trace_5mW,temp_trace_2_5mW,temp_trace_0_5]

period=[0.001,0.01,0.1,1.0]
sample_size=len(temp_trace[0][0])
print(sample_size)

temp_noise=2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace[0][0]*1000)[:sample_size//2])
frequency=np.linspace(0.0, 1.0/(2.0*period[0]), int(sample_size/2))

for i in range(1,len(period)):
    temp_noise=np.c_[temp_noise,2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace[i][0]*1000)[:sample_size//2])]
    frequency=np.c_[frequency,np.linspace(0.0, 1.0/(2.0*period[i]), int(sample_size/2))]

temp_noise=np.transpose(temp_noise)
frequency=np.transpose(frequency)

window=5
for i in range(0,len(period)):
    print('Integration time: '+str(period[i]))
    print('Noise average: '+str(np.mean(temp_noise[i][1:])))
    plt.loglog(frequency[i][window:],np.convolve(temp_noise[i][1:],np.ones((window,))/window,mode='valid'),lw=3,zorder=5-i)
    
plt.show()