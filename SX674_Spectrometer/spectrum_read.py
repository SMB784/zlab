from SX674_Spectrometer import *

drive_URL=input("Please enter URL for TeamDrive data, or press ENTER to use existing data: ")
print("Searching for data...")
if(drive_URL==''):
    print("Existing data found in these directories:\n")
    selection=directory_select(data_root_directory)

else:

    find_file=find_file(drive_URL)
    
    try:
        download_dir=Path(data_root_directory/find_file['title'].split('.')[0])
        
        if find_directory(download_dir)==False:
            print("Data located on TeamDrive, downloading data...")
            download_from_teamdrive(find_file)
            print("Data downloaded from TeamDrive to following directories:\n")
            selection=directory_select(data_root_directory)
        else:
            print("Existing data from TeamDrive found in these directories:\n")
            selection=directory_select(data_root_directory)
    except:
        print("File not found on TeamDrive.  Check URL and run program again")
        sys.exit()    



#drive_URL = "https://drive.google.com/open?id=1eR65LvN4WQiiEW5uGWzsY6CoNnzwoFn3"


sub_folder='27000uW_250ms_NoBin/' # data subfolder goes here

start=595
stop=630

spectral_data=[]

for root,dirs,files in os.walk(Path(data_root_directory+sub_folder)):
    dirs.sort(key=numerical_sort) # sorts directories by ascending number
    file_count=0

    for file in sorted(files,key=numerical_sort): 
        files.sort(key=numerical_sort)

        hdul = fits.open(Path(data_root_directory+sub_folder)/file)
        #reads in data from file, converts to float type, drops first two and last columns (keep 2->len-1)
        spectrum=hdul[0].data[:,2:len(hdul[0].data[0,:]-1)]
        spectrum=pd.DataFrame(spectrum)
        window=find_max_window(spectrum)

        print(data_root_directory+sub_folder+file)
        
        spectrumArray=[[],[]]
        
        for i in range(0,len(spectrum.columns)-1): # -1 cuts last datapoint because it is erroneous
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
        
        if(file_count==0):
            spectral_data=wavelength
        
        spectral_data=np.c_[spectral_data,normalized_amplitude]
        
#         if(file_count==1):
#             plt.plot(wavelength,normalized_amplitude)
#             plt.show()
#             break

#         spectral_data.to_csv(Path(data_root_directory+sub_folder+save_folder+"spectrum"+str(file_count)+".csv"),header=None)
#         spectrum.to_csv(Path(data_root_directory+sub_folder+save_folder+"rawDataFile"+str(file_count)+".csv"),header=None)
        file_count+=1
    
    spectral_data=pd.DataFrame(spectral_data)