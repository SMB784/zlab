'''
Created on Nov 6, 2019

@author: sean
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

# Low Res Spectrometer

# temp_trace_9mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/air_50_ms_filter_1-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/air_75ms_filter_2-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_2_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/air_1250ms_filter_3-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_0_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/air_1750ms_filter_3-2/processed_data/'+'temp_values.csv',header=None).to_numpy())
# 
# temp_trace_9mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/water_50ms_filter_1-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_5mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/water_75ms_filter_2-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_2_5mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/water_1250ms_filter_3-0/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_0_5_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/water_1750ms_filter_3-2/processed_data/'+'temp_values.csv',header=None).to_numpy())

# High Res Spectrometer

temp_trace_9mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/1ms_4x4Bin_50mW_air/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/10ms_4x4Bin_23mW_air/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_2_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/100ms_4x4Bin_12mW_air/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_0_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/1000ms_4x4Bin_2mW_air/processed_data/'+'temp_values.csv',header=None).to_numpy())
 
temp_trace_9mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/1ms_4x4Bin_50mW_water/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_5mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/10ms_4x4Bin_23mW_water/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_2_5mW_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/100ms_4x4Bin_12mW_water/processed_data/'+'temp_values.csv',header=None).to_numpy())
temp_trace_0_5_water=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/1000ms_4x4Bin_2mW_water/processed_data/'+'temp_values.csv',header=None).to_numpy())

# Old Data

# temp_trace_9mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/47000uW_1ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/11000uW_10ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_2_5mW=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/730uW_100ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())
# temp_trace_0_5=np.transpose(pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/76uW_1000ms_4x4Bin/processed_data/'+'temp_values.csv',header=None).to_numpy())

temp_trace_water=[temp_trace_9mW_water,temp_trace_5mW_water,temp_trace_2_5mW_water,temp_trace_0_5_water]
temp_trace=[temp_trace_9mW,temp_trace_5mW,temp_trace_2_5mW,temp_trace_0_5mW]

temps_water=temp_trace_water
temps_air=temp_trace

# low res spectrometer exposure times
# period=[0.05,0.075,1.25,1.75]

# high res spectrometer exposure times
period=[0.001,0.01,0.1,1.0]

sample_size=len(temp_trace[0][0])

temp_noise=2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace[0][0]*1000)[:sample_size//2])
temp_noise_water=2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace_water[0][0]*1000)[:sample_size//2])

frequency=np.linspace(0.0, 1.0/(2.0*period[0]), int(sample_size/2))

for i in range(1,len(period)):
    temp_noise=np.c_[temp_noise,2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace[i][0]*1000)[:sample_size//2])]
    temp_noise_water=np.c_[temp_noise_water,2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace_water[i][0]*1000)[:sample_size//2])]
    frequency=np.c_[frequency,np.linspace(0.0, 1.0/(2.0*period[i]), int(sample_size/2))]

temp_noise=np.transpose(temp_noise)
temp_noise_water=np.transpose(temp_noise_water)
frequency=np.transpose(frequency)
colors=['red','orange','green','blue']


# Low Res file creation
# pd.DataFrame(temp_noise).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/temp_noise.csv',index=False,header=None)
# pd.DataFrame(frequency).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/frequency.csv',index=False,header=None)
# 
# pd.DataFrame(temp_noise_water).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/temp_noise.csv',index=False,header=None)
# pd.DataFrame(frequency).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/water/frequency.csv',index=False,header=None)

# High Res file creation
pd.DataFrame(temp_noise).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/temp_noise.csv',index=False,header=None)
pd.DataFrame(frequency).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Air/frequency.csv',index=False,header=None)
 
pd.DataFrame(temp_noise_water).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/temp_noise.csv',index=False,header=None)
pd.DataFrame(frequency).to_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/PCF_Sensitivity_Water/frequency.csv',index=False,header=None)


window=1
for i in range(0,len(period)):
    print('Temperature average in water (t='+str(period[i]*1000)+'ms): '+str(np.mean(temps_water[i])))
    print('Noise average in water (t='+str(period[i]*1000)+'ms): '+str(np.mean(temp_noise_water[i][1:])))
    print('Temperature average in air (t='+str(period[i]*1000)+'ms): '+str(np.mean(temp_trace[i])))
    print('Noise average in air (t='+str(period[i]*1000)+'ms): '+str(np.mean(temp_noise[i][1:]))+'\n')
    # water plots
    plt.loglog(frequency[i][window:],np.convolve(temp_noise_water[i][1:],np.ones((window,))/window,mode='valid'),lw=2,ls='dotted',color=colors[i],zorder=15-i)
    # air plots
    plt.loglog(frequency[i][window:],np.convolve(temp_noise[i][1:],np.ones((window,))/window,mode='valid'),lw=3,color=colors[i],zorder=5-i)
    
plt.show()