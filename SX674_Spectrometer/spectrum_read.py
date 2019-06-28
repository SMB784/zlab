from SX674_Spectrometer import *

start=545
stop=675

baseline=800.0 # No Binning
calibration=[543.741,0.068256] #No binning

# baseline=1100.0 # 4x4 Binning
# calibration=[543.26,0.13497] #4x4 binning

trigger=1.2
gate=10

spectral_data=[]

if directory_exists(find_directory(Path(Path(data_directory)/save_directory)))==True:
    print("Processed data already exists!")
else:
    os.mkdir(Path(Path(data_directory)/save_directory))

    exclude = set([save_directory])
    for root,dirs,files in os.walk(data_directory,topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        #dirs.sort(key=numerical_sort) # sorts directories by ascending number
        file_count=0
    
        for file in sorted(files,key=numerical_sort): 
            files.sort(key=numerical_sort)
    
            hdul = fits.open(Path(data_directory)/file)
            #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
            spectrum=pd.DataFrame(hdul[0].data[:,2:len(hdul[0].data[0,:]-1)])
    
            window=find_max_window(spectrum)
    
            print(Path(data_directory)/file)
    
            
            spectrumArray=[[],[]]
            
            for i in range(0,len(spectrum.columns)-1): # -1 cuts last datapoint because it is erroneous
                amplitude=np.mean(spectrum.loc[window[1][i]:window[0]+window[1][i],i])
                spectrumArray[0].append(np.float(calibration[0]+i*calibration[1]))
                spectrumArray[1].append(amplitude)
    
            spectrumArray[1]=np.flip(spectrumArray[1],axis=0)
            input_data=pd.DataFrame(np.transpose(spectrumArray),dtype=float)
            
            lambdaStartIndex=input_data[input_data[[0]].apply(np.isclose,b=start,atol=tolerance).any(1)].index.tolist()[0]
            lambdaStopIndex=input_data[input_data[[0]].apply(np.isclose,b=stop,atol=tolerance).any(1)].index.tolist()[0]
    
            wavelength=input_data.iloc[lambdaStartIndex:lambdaStopIndex,0].to_numpy()
            amplitude=input_data.iloc[lambdaStartIndex:lambdaStopIndex,1].to_numpy()
            normalized_amplitude=(amplitude-amplitude.min())/(amplitude.max()-amplitude.min())
            
            if(file_count==0):
                spectral_data=wavelength
            
            spectral_data=np.c_[spectral_data,normalized_amplitude]
    
            if(file_count==1):
                plt.plot(wavelength,normalized_amplitude)
                plt.xlim(600,603)
                plt.ylim(0.95,1)
                break
            file_count+=1
    
#     spectral_data=pd.DataFrame(spectral_data)
#     spectral_data.to_csv(Path(Path(data_directory)/(save_directory+processed_data_filename)),index=False,header=None)
plt.show()
