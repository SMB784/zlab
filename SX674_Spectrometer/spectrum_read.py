from SX674_Spectrometer import *

download_dir=data_download.Download(data_root_directory).download_data()
save_dir='processed_data/'
processed_data_filename='spectral_data.csv'

ax=plt.gca()

# baseline=800.0 # No Binning
# calibration=[543.741,0.068256] #No binning

baseline=1100.0 # 4x4 Binning
calibration=[543.26,0.13497] #4x4 binning

start=558
stop=673

trigger=1.2
gate=10

spectral_data=[]



if directory_exists(save_dir,find_directory(Path(download_dir),save_dir))==True:
    print("Processed data already exists!")
else:

    exclude = set([save_dir])
    for root,dirs,files in os.walk(download_dir,topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        #dirs.sort(key=numerical_sort) # sorts directories by ascending number
        file_count=0
    
        for file in sorted(files,key=numerical_sort): 

            files.sort(key=numerical_sort)
            
            image=image_read.Image(Path(download_dir)/file).read_image()

            spectrum=pd.DataFrame(image)

            window=find_max_window(spectrum)
    
            print(Path(download_dir)/file)

            spectrumArray=[[],[]]
            
            for i in range(0,len(spectrum.columns)-2): # -1 cuts last datapoint because it is erroneous
                amplitude=np.max(spectrum.loc[window[1][i]:window[0][i]+window[1][i],i])

                spectrumArray[0].append(np.float(calibration[0]+i*calibration[1]))
                spectrumArray[1].append(amplitude)

            spectrumArray[1]=np.flip(spectrumArray[1],axis=0)

            input_data=pd.DataFrame(np.transpose(spectrumArray),dtype=float)

            lambdaStartIndex=input_data[input_data[[0]].apply(np.isclose,b=start,atol=tolerance).any(1)].index.tolist()[0]
            lambdaStopIndex=input_data[input_data[[0]].apply(np.isclose,b=stop,atol=tolerance).any(1)].index.tolist()[0]

            wavelength=input_data.iloc[lambdaStartIndex:lambdaStopIndex,0].to_numpy()
            amplitude=input_data.iloc[lambdaStartIndex:lambdaStopIndex,1].to_numpy()

            normalized_amplitude=(amplitude-amplitude.min())/\
            (amplitude.max()-amplitude.min())

            if(file_count==0):
                spectral_data=wavelength
            
            spectral_data=np.c_[spectral_data,normalized_amplitude]

#             # Comment out the block below to suppress plotting
#             if(file_count==0):
#                 plt.plot(wavelength,normalized_amplitude,color='red')
#                 file_count+=1
#                 plt.show()
#             else:
#                 break

    # Comment out the block below to suppress data saving
            file_count+=1
    os.mkdir(Path(Path(download_dir)/save_dir))
    spectral_data=pd.DataFrame(spectral_data)
    spectral_data.to_csv(Path(Path(download_dir)/(save_dir+processed_data_filename)),index=False,header=None)

print("Done reading data!")

