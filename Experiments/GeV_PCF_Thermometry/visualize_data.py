import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


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

fit_trace62mW=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-22-19/34000uW_1ms/processed_data/temp_values.csv',header=None)
fit_trace27mW=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-22-19/18000uW_20ms/processed_data/temp_values.csv',header=None)
fit_trace12mW=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-22-19/6300uW_100ms/processed_data/temp_values.csv',header=None)
fit_trace6mW=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-22-19/430uW_1000ms/processed_data/temp_values.csv',header=None)

time_increment=[.001,.02,.1,1]
power_increment=[34,18,6.3,.43]
temp=21-np.min(fit_trace6mW.to_numpy())

fit_trace_array=(fit_trace62mW[0].to_numpy()+temp,fit_trace27mW[0].to_numpy()+temp,\
           fit_trace12mW[0].to_numpy()+temp,fit_trace6mW[0].to_numpy()+temp)

colors=['blue','green','orange','red']
texts=['35 mW','20 mW','5 mW','0.5 mW']

ax0_1=fig.add_subplot(grid[0,0])
ax0_2=fig.add_subplot(grid[1,0],sharex=ax0_1)

ax0_1.xaxis.set_visible(False)
ax0_1.spines['bottom'].set_visible(False)
ax0_1.set_ylim(44,50)
ax0_2.spines['top'].set_visible(False)
ax0_2.set_ylim(20,28)

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
    times=np.arange(len(fit_trace_array[i]))*time_increment[i]+time_increment[i]
    
    if(i==0):
        stdev=np.std(fit_trace_array[i][:])
        ax0_1.semilogx(times[:],fit_trace_array[i][:],color=colors[i],lw=3)
    else:
        stdev=np.std(fit_trace_array[i])
        ax0_2.semilogx(times,fit_trace_array[i],color=colors[i],lw=3)
    stdev_array[1].append(1000*stdev/(np.sqrt(1/time_increment[i])))
    stdev_array[0].append(power_increment[i])

    ax1.scatter(stdev_array[0][i],stdev_array[1][i],c=colors[i],s=200,zorder=10)    

ax1.plot(stdev_array[0],stdev_array[1],c='black',lw=2,ls='dashed',zorder=0)

ax0_1.annotate('(a)', xy=(-0.2, 1), xycoords='axes fraction')
ax1.annotate('(b)', xy=(-0.2, 1), xycoords='axes fraction')

plt.tight_layout()
plt.savefig('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/fig5.png',bbox_inches='tight')
plt.show()