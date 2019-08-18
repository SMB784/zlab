'''
Created on Aug 17, 2019

@author: sean
'''
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

################################# Data plotting #################################

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import EngFormatter

#################################################################################
############################## Data Import Block ################################
#################################################################################

data_read_directory=str(os.getcwd())+'/data/Microdiamond_Calibration/'
write_directory=str(os.getcwd())+'/Manuscript_Files/'

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

#################################################################################
############################## Plot Setup Block #################################
#################################################################################

fontsize=16
marker_size=12
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(6,2)

fig,ax=plt.subplots(figsize=(12,12))

ax.set_ylabel("Temperature (C)")
ax.yaxis.set_label_coords(0.54,0.85)
ax.xaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

#################################################################################
############################## Upper Left Plot ##################################
#################################################################################

colors=['red']
texts=['$\lambda_c$']

UL_ax=fig.add_subplot(grid[0:-4,0])
patches=[UL_ax.plot([],[],marker='o',ms=marker_size,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

UL_ax.set_xlabel("Temperature (C)")
UL_ax.set_ylabel("$\lambda_c$ (nm)")
UL_ax.annotate('$\Delta \lambda_c$/$\Delta T$=0.0078', xy=(0.05, 0.9), xycoords='axes fraction')
UL_ax.annotate('(c)', xy=(-0.275, 0.95), xycoords='axes fraction')
UL_ax.legend(loc=('lower right'),handles=patches,fontsize=fontsize,bbox_to_anchor=(1,0),framealpha=0,labelspacing=0,handletextpad=0.1)

UL_ax.scatter(power,cal_wavelength,marker='s',s=75,facecolors='w',edgecolors='r')
UL_ax.plot(power,wavelength_fit,c='red',lw=3,ls='dashed')

UL_ax.annotate('(a)', xy=(-0.275, 0.95), xycoords='axes fraction')

#################################################################################
############################## Upper Right Plot #################################
#################################################################################

fit_trace_1=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/47000uW_1ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_2=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/11000uW_10ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_3=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/730uW_100ms_4x4Bin/processed_data/temp_values.csv',header=None)
fit_trace_4=pd.read_csv('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/7-23-19_D2/76uW_1000ms_4x4Bin/processed_data/temp_values.csv',header=None)

time_increment=[.001,.02,.1,1]
power_increment=[47,18,6.3,.43]
temp=21-np.min(fit_trace_4.to_numpy())

fit_trace_array=(fit_trace_1[0].to_numpy()+temp,fit_trace_2[0].to_numpy()+temp,\
           fit_trace_3[0].to_numpy()+temp,fit_trace_4[0].to_numpy()+temp)

colors=['blue','green','orange','red']
texts=['50 mW','20 mW','5 mW','0.5 mW']

UR_ax=fig.add_subplot(grid[0:2,1])
UR_ax.set_ylim(20,80)
UR_ax.set_xlim(0.0005,150)
UR_ax.set_xlabel("Time (sec)")
patches=[UR_ax.plot([],[],marker='o',ms=20,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

for i in range(0,len(fit_trace_array)):
    times=np.arange(len(fit_trace_array[i]))*time_increment[i]+time_increment[i]

    UR_ax.loglog(times,fit_trace_array[i],color=colors[i],lw=3)

UR_ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
UR_ax.annotate('(b)', xy=(-0.275, 0.95), xycoords='axes fraction')

#################################################################################
############################## Middle Left Plot #################################
#################################################################################

ML_ax=fig.add_subplot(grid[2:-2,0])

ML_ax.set_xlabel("Laser Power (mW)")
ML_ax.set_ylim(10,1500)
ML_ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
ML_ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

patches=[ML_ax.plot([],[],marker='o',ms=marker_size,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]
ML_ax.legend(loc=('upper right'),handles=patches,fontsize=fontsize,framealpha=0,labelspacing=0,bbox_to_anchor=(1,1),handletextpad=0.1)

ML_ax.set_ylabel("$\eta_T$ (mK / $\sqrt{Hz}$)")

stdev_array=[[],[]]

for i in range(0,len(fit_trace_array)):

    times=np.arange(len(fit_trace_array[i]))*time_increment[i]+time_increment[i]

    stdev=np.std(fit_trace_array[i])
   
    stdev_array[1].append(1000*stdev/(np.sqrt(1/time_increment[i])))
    stdev_array[0].append(power_increment[i])

    ML_ax.scatter(stdev_array[0][i],stdev_array[1][i],c=colors[i],s=200,zorder=10)    

ML_ax.semilogy(stdev_array[0],stdev_array[1],c='black',lw=2,ls='dashed',zorder=0)
ML_ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ML_ax.annotate('(c)', xy=(-0.275, 0.95), xycoords='axes fraction')

#################################################################################
############################# Middle Right Plot #################################
#################################################################################

colors=['blue','green','orange','red']
texts=['9.5 mW','3 mW','1.52 mW','0.5 mW']

yformat=EngFormatter()
MR_ax=fig.add_subplot(grid[2:-2,1])

patches=[MR_ax.plot([],[],marker='o',ms=marker_size,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

MR_ax.yaxis.set_major_formatter(yformat)
MR_ax.set_xlabel("Wavelength (nm)")
MR_ax.set_ylabel("$I_{PL}$ (a.u.)")
MR_ax.set_xlim(590,700)

MR_ax.legend(loc=('upper right'),handles=patches,fontsize=fontsize,framealpha=0,labelspacing=0,bbox_to_anchor=(1,1),handletextpad=0.1)

spectra=np.flip(spectralData[2:6],axis=0)
for i in range(0,len(spectra)):
    MR_ax.plot(spectralData[0],spectra[i],c=colors[i],lw=3)

MR_ax.annotate('(d)', xy=(-0.275, 0.95), xycoords='axes fraction')

#################################################################################
############################## Lower Left Plot ##################################
#################################################################################

LL_ax0=fig.add_subplot(grid[4:,0])

colors=['black','red']
texts=['Max $I_{PL}$','SNR']
patches=[LL_ax0.plot([],[],marker='o',ms=marker_size,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

LL_ax0.yaxis.set_major_formatter(yformat)
LL_ax0.xaxis.set_major_locator(plt.MaxNLocator(3))

LL_ax0.set_xlabel("Laser Power (mW)")
LL_ax0.set_ylabel("Max $I_{PL}$ (a.u.)")
LL_ax0.legend(loc=('upper left'),handles=patches,fontsize=fontsize,framealpha=0,labelspacing=0,bbox_to_anchor=(0,1),handletextpad=0.1)

LL_ax1=LL_ax0.twinx()
LL_ax1.set_ylabel("SNR (a.u.)")
LL_ax1.yaxis.set_major_locator(plt.MaxNLocator(3))

LL_ax0.plot(fitData[0],fitData[1],c=colors[0],lw=3)
LL_ax1.plot(fitData[0],fitData[4],c=colors[1],lw=3,ls='dashed')

LL_ax0.annotate('(e)', xy=(-0.275, 0.95), xycoords='axes fraction')

#################################################################################
############################## Lower Right Plot #################################
#################################################################################

colors=['black','red']
texts=['$\lambda_c$','$\Delta T$']

LR_ax0=fig.add_subplot(grid[4:,1])
patches=[LR_ax0.plot([],[],marker='o',ms=marker_size,ls="",mec=None,color=colors[i],label="{:s}".format(texts[i]))[0] for i in range (len(texts))]

LR_ax0.xaxis.set_major_locator(plt.MaxNLocator(3))
LR_ax0.set_xlabel("Laser Power (mW)")

LR_ax0.yaxis.set_major_locator(plt.MaxNLocator(3))
LR_ax0.set_ylabel("$\lambda_c$ (nm)")

LR_ax0.legend(loc=('lower right'),handles=patches,fontsize=fontsize,bbox_to_anchor=(1,0.35),framealpha=0,labelspacing=0,handletextpad=0.1)

LR_ax1=LR_ax0.twinx()
LR_ax1.set_ylabel("$\Delta$T (C)")
LR_ax1.yaxis.set_major_locator(plt.MaxNLocator(3))

LR_ax0.plot(fitData[0],np.flip(fitData[2]),c=colors[0],lw=3)
LR_ax1.plot(fitData[0],fitData[3],c=colors[1],lw=3,ls='dashed')

LR_ax0.annotate('(f)', xy=(-0.275, 0.95), xycoords='axes fraction')

############################## End of Plots ######################################

plt.tight_layout()
plt.savefig(write_directory+"Fig2.png",bbox_inches='tight')
# plt.show()
