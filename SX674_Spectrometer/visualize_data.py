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

ratio_trace62mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/62000uW_125ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
ratio_trace27mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/27000uW_250ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
ratio_trace12mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/12500uW_500ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
ratio_trace6mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/6000uW_1000ms_NoBin/processed_data/ratio_temp_values.csv',header=None)
fit_trace62mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/62000uW_125ms_NoBin/processed_data/fit_temp_values.csv',header=None)
fit_trace27mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/27000uW_250ms_NoBin/processed_data/fit_temp_values.csv',header=None)
fit_trace12mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/12500uW_500ms_NoBin/processed_data/fit_temp_values.csv',header=None)
fit_trace6mW=pd.read_csv('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/6000uW_1000ms_NoBin/processed_data/fit_temp_values.csv',header=None)

ratio_fft62mW=ratio_trace62mW
ratio_fft27mW=ratio_trace27mW
ratio_fft12mW=ratio_trace12mW
ratio_fft6mW=ratio_trace6mW

fit_fft62mW=fit_trace62mW
fit_fft27mW=fit_trace27mW
fit_fft12mW=fit_trace12mW
fit_fft6mW=fit_trace6mW

time_increment=[.125,.25,.5,1]
temp=29

ratio_trace_array=(ratio_trace62mW[0].to_numpy()+temp,ratio_trace27mW[0].to_numpy()+temp,\
           ratio_trace12mW[0].to_numpy()+temp,ratio_trace6mW[0].to_numpy()+temp)
fit_trace_array=(fit_trace62mW[0].to_numpy()+temp,fit_trace27mW[0].to_numpy()+temp,\
           fit_trace12mW[0].to_numpy()+temp,fit_trace6mW[0].to_numpy()+temp)

ratio_fft62mW[0]=ratio_trace62mW[0]-np.mean(ratio_trace62mW[0])
ratio_fft27mW[0]=ratio_trace27mW[0]-np.mean(ratio_trace27mW[0])
ratio_fft12mW[0]=ratio_trace12mW[0]-np.mean(ratio_trace12mW[0])
ratio_fft6mW[0]=ratio_trace6mW[0]-np.mean(ratio_trace6mW[0])

fit_fft62mW[0]=fit_trace62mW[0]-np.mean(fit_trace62mW[0])
fit_fft27mW[0]=fit_trace27mW[0]-np.mean(fit_trace27mW[0])
fit_fft12mW[0]=fit_trace12mW[0]-np.mean(fit_trace12mW[0])
fit_fft6mW[0]=fit_trace6mW[0]-np.mean(fit_trace6mW[0])

ratio_res_array=(ratio_fft62mW[0].to_numpy(),ratio_fft27mW[0].to_numpy(),\
           ratio_fft12mW[0].to_numpy(),ratio_fft6mW[0].to_numpy())
fit_res_array=(fit_fft62mW[0].to_numpy(),fit_fft27mW[0].to_numpy(),\
           fit_fft12mW[0].to_numpy(),fit_fft6mW[0].to_numpy())

colors=['blue','green','orange','red']
texts=['62 mW','27 mW','12.5 mW','6 mW']

for i in range(0,len(ratio_res_array)):
    times=np.arange(len(ratio_trace_array[i]))*time_increment[i]
    samples=len(ratio_res_array[i])
    
    ratio_avgs=np.ones(len(ratio_trace_array[i]))*np.mean(ratio_trace_array[i])
    ratio_plus_stdev=ratio_avgs+np.std(ratio_trace_array[i])
    ratio_minus_stdev=ratio_avgs-np.std(ratio_trace_array[i])

    ratio_ffts=np.abs(fftpack.fft(ratio_res_array[i]))
    ratio_freqs=fftpack.fftfreq(len(ratio_res_array[i]))*(1/time_increment[i])
    fit_ffts=np.abs(fftpack.fft(fit_res_array[i]))
    fit_freqs=fftpack.fftfreq(len(fit_res_array[i]))*(1/time_increment[i])

    ax0=fig.add_subplot(grid[0,i])
    ax0.set_xlabel("Time (sec)")
    ax0.set_ylim(29,37)
    patches=[ax0.plot([],[],marker='o',ms=20,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0]]

    ax0.plot(times,ratio_avgs,color='black')
    ax0.plot(times,ratio_plus_stdev,color='black',ls='dashed')
    ax0.plot(times,ratio_minus_stdev,color='black',ls='dashed')
    ax0.plot(times,ratio_trace_array[i],color=colors[i],lw=2)
    
    ax1=fig.add_subplot(grid[1,i])

    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_xlim(0.1,10)
    ax1.set_ylim(0.1,100)
    ax1.loglog(ratio_freqs[1:samples//2],ratio_ffts[1:samples//2],color=colors[i],ls='dashed',lw=2)
    ax1.loglog(fit_freqs[1:samples//2],fit_ffts[1:samples//2],color=colors[i],lw=2)
    ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    xticks=ax1.get_xticks()
    ax1.set_xticklabels(xticks.astype(int))

    ax1.grid(b=True,which='both',axis='both')
    ax0.legend(handles=patches,loc='upper right')

    if i!=0:
        ax0.set_yticklabels([])
        ax1.set_yticklabels([])
    else:
        ax0.set_ylabel("Temperature (C)")
        ax1.set_ylabel("Resolution (C)")

plt.tight_layout()
plt.savefig('/media/sean/Storage/zlab/SX674_Spectrometer/data/5-29-19/NewSpectrometer/fig5.png',bbox_inches='tight')
plt.show()