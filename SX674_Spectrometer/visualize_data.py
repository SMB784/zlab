import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from SX674_Spectrometer import *
import SX674_Spectrometer

fontsize=16
plt.rcParams.update({'font.size':fontsize})
grid=plt.GridSpec(2,2)

fig,ax=plt.subplots(figsize=(12,6))


ax.set_ylabel("Temperature (C)")
ax.yaxis.set_label_coords(-0.0625,0.5)
ax.xaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

fit_trace62mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-28-19/NewSpectrometer/62000uW_5ms/processed_data/fit_temp_values.csv',header=None)
fit_trace27mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-28-19/NewSpectrometer/27000uW_10ms/processed_data/fit_temp_values.csv',header=None)
fit_trace12mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-28-19/NewSpectrometer/12000uW_20ms/processed_data/fit_temp_values.csv',header=None)
fit_trace6mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-28-19/NewSpectrometer/2800uW_100ms/processed_data/fit_temp_values.csv',header=None)

time_increment=[.005,.01,.02,.1]
power_increment=[62,27,12,3]
temp=22

fit_trace_array=(fit_trace62mW[0].to_numpy()+temp,fit_trace27mW[0].to_numpy()+temp,\
           fit_trace12mW[0].to_numpy()+temp,fit_trace6mW[0].to_numpy()+temp)

colors=['blue','green','orange','red']
texts=['62 mW','27 mW','12 mW','3 mW']

ax0_1=fig.add_subplot(grid[0,0])
ax0_2=fig.add_subplot(grid[1,0],sharex=ax0_1)

ax0_1.xaxis.set_visible(False)
ax0_1.spines['bottom'].set_visible(False)
ax0_1.set_ylim(83,88)
ax0_2.spines['top'].set_visible(False)
ax0_2.set_ylim(17,23)
ax0_1.set_xlim(0,0.8)
ax0_2.set_xlim(0,0.8)

ax0_2.set_xlabel("Time (sec)")

patches=[ax0_1.plot([],[],marker='o',ms=20,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

ax1=fig.add_subplot(grid[0:,1])

ax1.set_xlabel("Laser Power (mW)")
ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
ax1.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

ax1.legend(handles=patches,loc='upper right')

ax1.set_ylabel("Sensitivity (mK/$\sqrt{Hz}$)")

stdev_array=[[],[],[]]

for i in range(0,len(fit_trace_array)):
    times=np.arange(len(fit_trace_array[i]))*time_increment[i]
    
    if(i==0):
        length=160
        stdev=np.std(fit_trace_array[i][0:length])
        ax0_1.plot(times[0:length],fit_trace_array[i][0:length],color=colors[i],lw=3)
    else:
        stdev=np.std(fit_trace_array[i])
        ax0_2.plot(times,fit_trace_array[i],color=colors[i],lw=3)
    print(stdev)
    stdev_array[1].append(1000*stdev/(np.sqrt(1/time_increment[i])))
    stdev_array[0].append(power_increment[i])

    ax1.scatter(stdev_array[0][i],stdev_array[1][i],c=colors[i],s=200,zorder=10)    

ax1.plot(stdev_array[0],stdev_array[1],c='black',lw=2,ls='dashed',zorder=0)

ax0_1.annotate('(a)', xy=(-0.2, 1), xycoords='axes fraction')
ax1.annotate('(b)', xy=(-0.2, 1), xycoords='axes fraction')

plt.tight_layout()
plt.savefig('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-28-19/NewSpectrometer/fig5.png',bbox_inches='tight')
plt.show()