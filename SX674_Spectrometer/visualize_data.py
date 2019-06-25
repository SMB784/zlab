import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import stats
import matplotlib as mpl
import sys

fontsize=16
plt.rcParams.update({'font.size':fontsize})
grid=plt.GridSpec(2,4)

fig,ax=plt.subplots(figsize=(12,6))
ax.axis('off')

trace62mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/62000uW_125ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace27mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/27000uW_250ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace12mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/12500uW_500ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace6mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/6000uW_1000ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace62mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/62000uW_125ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace27mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/27000uW_250ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace12mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/12500uW_500ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
trace6mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/6000uW_1000ms_NoBin/processed_data/ratio_temp_values.csv',header=None)

fft62mW=trace62mW
fft27mW=trace27mW
fft12mW=trace12mW
fft6mW=trace6mW

time_increment=[.125,.25,.5,1]
temp=29

trace_array=(trace62mW[0].to_numpy()+temp,trace27mW[0].to_numpy()+temp,\
           trace12mW[0].to_numpy()+temp,trace6mW[0].to_numpy()+temp)

fft62mW[0]=trace62mW[0]-np.mean(trace62mW[0])
fft27mW[0]=trace27mW[0]-np.mean(trace27mW[0])
fft12mW[0]=trace12mW[0]-np.mean(trace12mW[0])
fft6mW[0]=trace6mW[0]-np.mean(trace6mW[0])

res_array=(fft62mW[0].to_numpy(),fft27mW[0].to_numpy(),\
           fft12mW[0].to_numpy(),fft6mW[0].to_numpy())

colors=['blue','green','orange','red']
texts=['62 mW','27 mW','12.5 mW','6 mW']

for i in range(0,len(res_array)):
    times=np.arange(len(trace_array[i]))*time_increment[i]
    avgs=np.ones(len(trace_array[i]))*np.mean(trace_array[i])
    plus_stdev=avgs+np.std(trace_array[i])
    minus_stdev=avgs-np.std(trace_array[i])
    
    ffts=np.abs(fftpack.fft(res_array[i]))

    freqs=fftpack.fftfreq(len(res_array[i]))*(1/time_increment[i])
    samples=len(res_array[i])
    
    ax0=fig.add_subplot(grid[0,i])
    ax0.set_xlabel("Time (sec)")
    ax0.set_ylim(temp-5,temp+5)
    patches=[ax0.plot([],[],marker='o',ms=20,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0]]

    print(trace_array[i])
    ax0.plot(times,avgs,color='black')
    ax0.plot(times,plus_stdev,color='black',ls='dashed')
    ax0.plot(times,minus_stdev,color='black',ls='dashed')
    ax0.plot(times,trace_array[i],color=colors[i],lw=2)
    
    ax1=fig.add_subplot(grid[1,i])

    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_xlim(0.1,10)
    ax1.set_ylim(0.1,100)
    ax1.loglog(freqs[0:samples//2],ffts[0:samples//2],color=colors[i])
    ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    xticks=ax1.get_xticks()
    ax1.set_xticklabels(xticks.astype(int))

    ax0.grid(b=True,which='both',axis='both')
    ax1.grid(b=True,which='both',axis='both')

    if i!=0:
        ax0.legend(handles=patches,loc='upper right')
        ax0.yaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
    else:
        ax0.set_ylabel("Temperature (C)")
        ax0.legend(handles=patches,loc='lower right')
        ax1.set_ylabel("Resolution (C)")

plt.tight_layout()
plt.savefig('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/ratio_noise_data.png',bbox_inches='tight')
plt.show()