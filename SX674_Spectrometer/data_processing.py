from astropy.io import fits
import pandas as pd
import numpy as np
from lmfit import Model
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
import os,re

data_root_directory='/home/sean/Desktop/5-29-19/NewSpectrometer/'
# sub_folder='27000uW_10ms_4x4Binning/'
sub_folder='27000uW_250ms_NoBin/'
save_folder='spectralData/'
plt.figure(figsize=(10,8))

baseline=800.0 # No Binning
# baseline=1100.0 # 4x4 Binning
trigger=1.2
gate=10
# calibration=[543.26,0.13497] #4x4 binning
calibration=[543.741,0.068256] #No binning

# start=595
# stop=620.0
start=595
stop=630
tolerance=0.2
GeV=601

initial=[[601.0,612,625],\
         [4.5,11,40],\
         [1,1,1],0]

numbers=re.compile(r'(\d+)')

def tripleLorentzianFit(x,c1,c2,c3,\
                w1,w2,w3,\
                h1,h2,h3,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(np.pi*w3)*(w3**2/((x-c3)**2+w3**2))\
           +o1
           
def doubleLorentzianFit(x,c1,c2,\
                w1,w2,\
                h1,h2,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +o1

def findValue(bestValues): #input is dictionary output from result.best_values
    center_FWHM=[]
    for key, value in bestValues.items():
        if np.isclose(a=value,b=GeV,atol=tolerance*20):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
    return center_FWHM

def numericalSort(value):
    parts=numbers.split(value)
    parts[1::2]=map(int,parts[1::2])
    return parts
pd.options.display.max_rows=1451
np.set_printoptions(threshold=np.inf)

def find_max_window(df):
    rollingArray=df[0:len(df[0])].rolling(window=gate).mean()[gate-1:len(df[0])]
    loc=[]
    y_window=[]
    for i in range(0,len(df.columns)):
        vals=rollingArray[i].values
#         try:
#             y_min=np.min(np.argwhere(vals>=baseline*trigger))
#             y_max=y_min+np.min(np.argwhere(vals[y_min:len(vals)]<=baseline*trigger))
#             y_window.append(y_max-y_min)
# 
#         except:
#             y_min=0
#             y_window.append(0)
# 
#         loc.append(y_min)
#     return[y_window,loc]
        try:
            y=np.min(np.argwhere(vals>=baseline*trigger))
            y_window.append(np.min(np.argwhere(vals[y:len(vals)]<=baseline*trigger)))
        except:
            y=0
            y_window.append(0)
        loc.append(y)
 
    return [np.max(y_window),loc]



#######################################################################################################
for root,dirs,files in os.walk(Path(data_root_directory+sub_folder)):
    dirs.sort(key=numericalSort) # sorts directories by ascending power
    
    for file in sorted(files,key=numericalSort): 
        files.sort(key=numericalSort)

        hdul = fits.open(Path(data_root_directory+sub_folder)/file)
        #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
        spectrum=hdul[0].data[:,2:len(hdul[0].data[0,:]-1)]
        spectrum=pd.DataFrame(spectrum)
        window=find_max_window(spectrum)
        
        spectrumArray=[[],[]]
        
        for i in range(0,len(spectrum.columns)-1): # -1 cuts last datapoint because it is erroneous
#             amplitude=np.mean(spectrum.loc[window[1][i]:window[0][i]+window[1][i],i])
            amplitude=np.mean(spectrum.loc[window[1][i]:window[0]+window[1][i],i])
            spectrumArray[0].append(np.float(calibration[0]+i*calibration[1]))
            spectrumArray[1].append(amplitude)
        
        spectrumArray[1]=np.flip(spectrumArray[1])

        input_data=pd.DataFrame(np.transpose(spectrumArray),dtype=float)
        
        lambdaStartIndex=input_data[input_data[[0]].apply(np.isclose,b=start,atol=tolerance).any(1)].index.tolist()[0]
        lambdaStopIndex=input_data[input_data[[0]].apply(np.isclose,b=stop,atol=tolerance).any(1)].index.tolist()[0]

        wavelength=input_data.iloc[lambdaStartIndex:lambdaStopIndex,0].as_matrix()
        amplitude=input_data.iloc[lambdaStartIndex:lambdaStopIndex,1].as_matrix()

        normalized_amplitude=(amplitude-amplitude.min())/(amplitude.max()-amplitude.min())

#         plt.plot(wavelength,normalized_amplitude)
#         plt.plot(wavelength,result.best_fit,ls='dashed')
        spectrumData=pd.DataFrame(np.transpose([wavelength,amplitude]))
#         spectrumData.to_csv(Path(data_root_directory+sub_folder+save_folder+"spectrum"+str(fileCount)+".csv"),header=None)
#         spectrum.to_csv(Path(data_root_directory+sub_folder+save_folder+"rawDataFile"+str(fileCount)+".csv"),header=None)
