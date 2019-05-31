from SX674_Spectrometer import *
from SX674_Spectrometer import numerical_sort, find_max_window

data_root_directory='/home/sean/Desktop/5-29-19/NewSpectrometer/'
# sub_folder='27000uW_10ms_4x4Binning/'
sub_folder='27000uW_250ms_NoBin/'
save_folder='spectralData/'

# calibration=[543.26,0.13497] #4x4 binning
calibration=[543.741,0.068256] #No binning

start=595
stop=630
tolerance=0.2
GeV=601

for root,dirs,files in os.walk(Path(data_root_directory+sub_folder)):
    dirs.sort(key=numerical_sort) # sorts directories by ascending power
    
    for file in sorted(files,key=numerical_sort): 
        files.sort(key=numerical_sort)

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
        spectrumData=pd.DataFrame(np.transpose([wavelength,normalized_amplitude]))
#         spectrumData.to_csv(Path(data_root_directory+sub_folder+save_folder+"spectrum"+str(fileCount)+".csv"),header=None)
#         spectrum.to_csv(Path(data_root_directory+sub_folder+save_folder+"rawDataFile"+str(fileCount)+".csv"),header=None)
