'''
Created on Aug 12, 2019

@author: sean
'''

import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from scipy.integrate import simps

data_root_directory=Path(Path(os.getcwd())/'data/')

start=558
stop=673

data_dir=data_download.Download(data_root_directory).download_data()
save_dir='processed_data'
processed_data_filename='/spectral_data.csv'

# calibration=[543.741,0.068256] #No binning

calibration=[543.26,0.13497] #4x4 binning

        spectral_data=[]
        
        if directory_exists(Path(download_dir),save_dir)==True:
            print("Processed data already exists!")
        else:
        
            exclude = set([save_dir])
            for root,dirs,files in os.walk(download_dir,topdown=True):
                dirs[:] = [d for d in dirs if d not in exclude]
        
                file_count=0
            
                for file in sorted(files,key=numerical_sort): 
                    files.sort(key=numerical_sort)
                    
                    spectrum=image_read.Image(Path(download_dir)/file).read_image()
        
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
        
                    # Comment out the block below to suppress plotting
                    if(file_count==0):
                        plt.figure(1)
                        plt.plot(wavelength,normalized_amplitude,color='red')
                        plt.figure(2)
                        plot_image(spectrum)
        
            # Comment out the block below to suppress data saving
                    file_count+=1
            os.mkdir(Path(Path(download_dir)/save_dir))
            spectral_data=pd.DataFrame(spectral_data)
            spectral_data.to_csv(Path(Path(download_dir)/(save_dir+processed_data_filename)),index=False,header=None)
        
        print("Done reading data!")

from Devices.SX674_Spectrometer import *

try:
    input_data=pd.read_csv(find_directory(Path(Path(data_directory)\
                                               /(save_directory+processed_data_filename))),\
                                               header=None)
except:
    from SX674_Spectrometer import spectrum_read
    
    input_data=spectrum_read.spectral_data
    spectrum_read.spectral_data.to_csv(Path(Path(data_directory)\
                                            /(save_directory+processed_data_filename)),\
                                            index=False,header=None)

                temp_cal=[599.6316,0.0078] # from center wavelength vs temp: [intercept, slope]
        fit_values=[]
        temp_values=[]
        
                for i in range(1,len(self.spectrum.columns)):

        
            fit_curves=np.c_[fit_curves,result.best_fit]
            
            fit_values.append(findValue(result.best_values))
            
            temp_value=(findValue(result.best_values)[0]-temp_cal[0])/temp_cal[1]
            temp_values.append(temp_value)
        
        #     # Comment out this code block to suppress plotting data
        #     plt.plot(wavelength,normalized_amplitude)
        #     plt.plot(wavelength,result.best_fit,ls='dashed')
        #     if(file_count==0):
        #         break
        # 
        #     file_count+=1
        # plt.show()
        
        # Comment out this block to suppress data writing to disk
        temp_stdev=np.std(np.transpose(temp_values)[1:len(np.transpose(temp_values))])
        print(temp_stdev)
        
        fit_curves=pd.DataFrame(fit_curves)
        fit_values=pd.DataFrame(fit_values)
        temp_values=pd.DataFrame(temp_values)
        
        fit_curves.to_csv(Path(Path(data_directory)/(save_directory+"fit_curves.csv")),\
                               index=False,header=None)
        fit_values.to_csv(Path(Path(data_directory)/(save_directory+"fit_values.csv")),\
                               index=False,header=None)
        temp_values.to_csv(Path(Path(data_directory)/(save_directory+"fit_temp_values.csv")),\
                               index=False,header=None)
