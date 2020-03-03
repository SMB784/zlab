'''
Created on Aug 17, 2019

@author: sean
'''
#################################################################################
############################# Import Declarations ###############################
#################################################################################

############################# Data import/analysis ##############################

import os
import csv
import re
import numpy as np
import pandas as pd
from lmfit import Model
from scipy import stats
import scipy.fftpack

################################# Data plotting #################################

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import *#(EngFormatter,MaxNLocator)

#################################################################################
############################## Data Import Block ################################
#################################################################################

data_read_directory=str(os.getcwd())+'/data/Microdiamond_Calibration/'
write_directory=str(os.getcwd())+'/Manuscript_Files/Rev1_Draft/'

########################## Fit Data Import/Analysis #############################


input_data=pd.read_csv(data_read_directory+"data.csv")

start=585.0
stop=800
GeV=601.8
tolerance=.5

initial=[[601.5,614,624,650,700],\
         [4,16,75,75,75],\
         [35000,23000,19000,13000,7000],1]

def fitFunction(x,c1,c2,c3,c4,c5,\
                w1,w2,w3,w4,w5,\
                h1,h2,h3,h4,h5,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
+h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
+h3/(np.pi*w3)*(w3**2/((x-c3)**2+w3**2))\
+h4/(np.pi*w4)*(w4**2/((x-c4)**2+w4**2))\
+h5/(np.pi*w5)*(w5**2/((x-c5)**2+w5**2))\
+o1

def findValue(bestValues): #input is dictionary output from result.best_values
    center_FWHM=[]


    for key, value in bestValues.items():
        if np.isclose(a=value,b=GeV,atol=tolerance/2):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
    return center_FWHM

lmodel=Model(fitFunction)

params=lmodel.make_params(c1=initial[0][0],w1=initial[1][0],h1=initial[2][0],\
                          c2=initial[0][1],w2=initial[1][1],h2=initial[2][1],\
                          c3=initial[0][2],w3=initial[1][2],h3=initial[2][2],\
                          c4=initial[0][3],w4=initial[1][3],h4=initial[2][3],\
                          c5=initial[0][4],w5=initial[1][4],h5=initial[2][4],\
                          o1=initial[3])

# finds location in dataframe of start and stop wavelength within tolerance
lambdaStartIndex=input_data[input_data[["Wavelength"]].apply(np.isclose,b=start,atol=tolerance).any(1)].index.tolist()[0]
lambdaStopIndex=input_data[input_data[["Wavelength"]].apply(np.isclose,b=stop,atol=tolerance).any(1)].index.tolist()[0]

spectralData=[]
SNRData=[]
# sets dataframe to include only wavelengths between start and hstop wavelength
wavelength=input_data.iloc[lambdaStartIndex:lambdaStopIndex,0].to_numpy()
spectralData=wavelength
SNRData=wavelength

# sets 0 mW baseline amplitude to be subtracted out
baseline=input_data.iloc[lambdaStartIndex:lambdaStopIndex,1].to_numpy()

for i in range(2,7):
    #defines amplitude
    amplitude=input_data.iloc[lambdaStartIndex:lambdaStopIndex,i].to_numpy()
    # appends amplitude to spectralData for each laser power value
    spectralData=np.c_[spectralData,amplitude]
    # calculates noise deviation from fit
    result=lmodel.fit(amplitude-baseline,params,x=wavelength)
    SNRData=np.c_[SNRData,amplitude-result.best_fit]
   
spectralData=np.transpose(spectralData)
SNRData=np.transpose(SNRData)

############################### Fit Data Import #################################

input_data=csv.reader(open(data_read_directory+'FitData.csv','rt'),delimiter=',')
fitData=[[],[],[],[]]

rowCount=0
colCount=0
for row in input_data:
    if(rowCount==0):
        rowCount+=1
        continue
    for i in row:
        if(colCount==0 or colCount==1 or colCount==2 or colCount==5):
            fitData[rowCount-1].append(float(row[colCount]))
        colCount+=1
    rowCount+=1
    colCount=0

rowCount=0
colCount=0

FWHM_start=597
FWHM_stop=607
# average between 597 and 607
for i in range(0,len(fitData[0])):
    avg=0
    n=0
    for j in range(0,len(SNRData[0])):
        if(SNRData[0][j]>FWHM_start and SNRData[0][j]<FWHM_stop):
            avg+=SNRData[i+1][j]
            n+=1
    peakAvgNoise=avg/n
    SNR=fitData[i][1]/peakAvgNoise
    fitData[i].append(SNR)

fitData=np.transpose(fitData)

########################## Calibration Data Import###############################

input_data=pd.read_csv(data_read_directory+'Calibration.csv',header=None)

power=input_data[0].to_numpy()
cal_wavelength=input_data[1].to_numpy()
cal_width=input_data[2].to_numpy()

m_wavelength=stats.linregress(power,cal_wavelength)
m_width=stats.linregress(power,cal_width)

wavelength_fit=power[:]*m_wavelength[0]+m_wavelength[1]
width_fit=power[:]*m_width[0]+m_width[1]

############################# Temp Trace Import #################################

temp_trace=np.transpose(pd.read_csv(str(os.getcwd())+'/data/Imaging/wire_off_temp_trace.csv',header=None).to_numpy())

period=0.2
sample_size=100

temp_noise=2.0/sample_size*np.abs(scipy.fftpack.fft(temp_trace[1]*1000)[:sample_size//2])
frequency=np.linspace(0.0, 1.0/(2.0*period), int(sample_size/2))

#################################################################################
############################## Plot Setup Block #################################
#################################################################################

fontsize=24
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(2,2)

fig,ax=plt.subplots(figsize=(12,8))
 
ax.xaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

yformat=EngFormatter()

#################################################################################
############################## Upper Left Plot ##################################
#################################################################################

colors=['red']
texts=['$\lambda_c$']

UL_ax=fig.add_subplot(grid[0,0])

UL_ax.set_xlabel("T ($\degree C$)")
UL_ax.set_ylabel("$\lambda_c$ (nm)")
UL_ax.set_ylim(601.17,601.24)
UL_ax.yaxis.set_major_locator(ticker.MaxNLocator(4))
UL_ax.annotate('$\Delta \lambda_c$/$\Delta T$=\n0.0078', xy=(0.5, 0.1), xycoords='axes fraction')

UL_ax.scatter(power,cal_wavelength,marker='s',s=200,facecolors='w',edgecolors='black')
UL_ax.plot(power,wavelength_fit,c='black',lw=3,ls='dashed')

UL_ax.annotate('(a)',xy=(0.01,0.87),xycoords='axes fraction')

#################################################################################
############################## Upper Right Plot #################################
#################################################################################

fit_trace_1=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/47000uW_1ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_2=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/11000uW_10ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_3=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/730uW_100ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_4=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/76uW_1000ms_4x4Bin/processed_data/temp_values.csv',header=None)

time_increment=[.001,.02,.1,1]
power_increment=[47,18,6.3,.43]
temp=-np.min(fit_trace_4.to_numpy())

fit_trace_array=(fit_trace_1[0].to_numpy()+temp,fit_trace_2[0].to_numpy()+temp,\
           fit_trace_3[0].to_numpy()+temp,fit_trace_4[0].to_numpy()+temp)

temp_array=(np.mean(fit_trace_1[0].to_numpy())+temp,np.mean(fit_trace_2[0].to_numpy())+temp,\
           np.mean(fit_trace_3[0].to_numpy())+temp,1.0)

UR_ax1=fig.add_subplot(grid[0,1])

stdev_array=[[],[]]

for i in range(0,len(fit_trace_array)):

    stdev=np.std(fit_trace_array[i])
    stdev_array[1].append(1000*stdev/(np.sqrt(1/time_increment[i])))
    stdev_array[0].append(power_increment[i])

    UR_ax1.scatter(stdev_array[0][i],stdev_array[1][i],c='black',s=200,zorder=10)


# loglogfit=[np.linspace(0.5,100.0,100),1802*np.linspace(0.5,100.0,100)**(-1.11)]
# UR_ax1.loglog(loglogfit[0],loglogfit[1],c='black',lw=3,ls='dashed',zorder=0)
UR_ax1.loglog(stdev_array[0],stdev_array[1],c='black',lw=3,ls='dashed',zorder=0)
UR_ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax1.set_xlabel("$P_{Laser}$ (mW)")
UR_ax1.set_ylim(10,2500)
UR_ax1.yaxis.set_ticks([10,100,1000],minor=False)
UR_ax1.set_ylabel("$\eta_T$  (mK / $\sqrt{Hz}$)")


UR_ax2=UR_ax1.twinx()
UR_ax2.scatter(stdev_array[0],temp_array,c='red',s=200,zorder=20)
UR_ax2.loglog(stdev_array[0],temp_array,c='red',lw=3,ls='dotted',zorder=20)

UR_ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax2.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax2.yaxis.set_ticks([1,30,50],minor=True)
UR_ax2.set_yticklabels(['0','30','50'],minor=True,color='r')
UR_ax2.yaxis.set_ticks([10],minor=False)
UR_ax2.set_yticklabels(['10'],minor=False,color='r')
UR_ax2.set_ylabel("$\delta T$ ($\degree C$)",color='r')
UR_ax2.tick_params(axis='y', colors='red',which='both')
UR_ax2.spines['right'].set_color('red')
UR_ax2.set_ylim(0.7,60)
UR_ax2.set_xlim(0.3,70)

UR_ax1.annotate('(b)',xy=(0.01,0.87),xycoords='axes fraction',zorder=10)

print(stdev_array[0])
print(stdev_array[1])
print(temp_array)

#################################################################################
############################## Lower Left Plot ##################################
#################################################################################

LL_ax0=fig.add_subplot(grid[1,0])

LL_ax0.set_xscale('log')
LL_ax0.set_xlabel("$P_{Laser}$ (mW)")
LL_ax0.set_ylabel("SNR (dB)")
LL_ax0.set_ylim(15,50)
LL_ax0.yaxis.set_major_locator(ticker.MaxNLocator(4))

LL_ax1=LL_ax0.twinx()
LL_ax1.set_xscale('log')
LL_ax1.set_yscale('log')
LL_ax1.set_ylabel('$\delta T (\degree C)$',color='r')
LL_ax1.tick_params(axis='y', colors='red',which='both')
LL_ax1.yaxis.set_ticklabels([],color='r')
LL_ax1.spines['right'].set_color('red')
LL_ax1.set_ylim(0.8,40)
LL_ax1.set_xlim(0.35,12)
LL_ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
LL_ax1.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
LL_ax1.yaxis.set_ticks([1,30],minor=True)
LL_ax1.set_yticklabels(['0','30'],minor=True)
LL_ax1.yaxis.set_ticks([10],minor=False)
LL_ax1.set_yticklabels(['10'],minor=False)
LL_ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

fitData[3,0]=fitData[3,0]+1

LL_ax0.scatter(fitData[0],20*np.log10(fitData[4]),c='black',s=200,zorder=10)
LL_ax0.plot(fitData[0],20*np.log10(fitData[4]),c='black',lw=3,ls='dashed',zorder=20)

LL_ax1.scatter(fitData[0],fitData[3],c='r',s=200,zorder=0)
LL_ax1.plot(fitData[0],fitData[3],c='red',lw=3,ls='dotted',zorder=20)

LL_ax0.annotate('(c)',xy=(0.01,0.87),xycoords='axes fraction')

#################################################################################
############################## Lower Right Plot #################################
#################################################################################

LR_ax=fig.add_subplot(grid[1,1])

noise_frequency=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/frequency.csv',header=None).to_numpy()
temp_noise=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/temp_noise.csv',header=None).to_numpy()

LR_ax.set_xlabel('$\\nu_{noise}$ (Hz)')
LR_ax.set_ylabel('$T_{noise}$ (mK)')
LR_ax.set_ylim(0.5,2000)
LR_ax.set_xlim(.01,20)

LR_ax.loglog(noise_frequency[0][1:len(noise_frequency[0])],temp_noise[0][1:len(temp_noise[0])],lw=3,color='black')

LR_ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
LR_ax.xaxis.set_major_locator(LogLocator(numticks=4))
# LR_ax.xaxis.set_minor_formatter(ticker.NullFormatter())
LR_ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
LR_ax.yaxis.set_minor_formatter(ticker.ScalarFormatter())
LR_ax.yaxis.set_major_locator(LogLocator(numticks=4))
LR_ax.yaxis.set_minor_locator(LogLocator(numticks=10))
# LR_ax.yaxis.set_minor_formatter(ticker.NullFormatter())

LR_ax.annotate('(d)',xy=(0.01,0.87),xycoords='axes fraction')

############################## End of Plots ######################################

plt.tight_layout()
plt.savefig(write_directory+"Fig2_rev1_sub.png",bbox_inches='tight')
plt.show()