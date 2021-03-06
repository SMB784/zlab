'''
Created on Nov 16, 2019

@author: sean
'''
from Experiments.GeV_PCF_Thermometry import *

# spectrum=Spectrum_Read.Spectrum('/home/sean/git/zlab/Experiments/GeV_PCF_Thermometry/data/11-12-19/air/50_ms_filter_1-0/SN1398 2019-11-12, 11-18-31.5, A.csv').read_spectrum().to_numpy()

save_dir='processed_data'
spectral_data=[]

temp_cal=[599.6316,0.0078]

if directory_exists(Path(download_dir),save_dir)==True:
    print("Processed data already exists!")
else:
    exclude = set([save_dir])
    for root,dirs,files in os.walk(download_dir,topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        file_count=0

        for file in sorted(files,key=numerical_sort):
            files.sort(key=numerical_sort)

            input_spectrum=Spectrum_Read.Spectrum(Path(download_dir)/file).read_spectrum()
            fit_data=spectral_fit.Fit(start,stop,input_spectrum).fit_spectrum()

            if(fit_data[3][0]==0):
                print("Fit invalid, skipped this entry")
                file_count+=1
                plt.plot(input_spectrum[0],input_spectrum[1])
                plt.show()
                continue

            if(file_count==0):
                raw_spectra=np.transpose(fit_data[0])[0]
                spectrum_data=np.transpose(fit_data[1])[0]
                spectrum_fit=np.transpose(fit_data[2])[0]
                fit_values=np.transpose(fit_data[3])
            else:
                raw_spectra=np.c_[raw_spectra,np.transpose(fit_data[0])[1]]
                spectrum_data=np.c_[spectrum_data,np.transpose(fit_data[1])[1]]
                spectrum_fit=np.c_[spectrum_fit,np.transpose(fit_data[2])[1]]
                fit_values=np.c_[fit_values,np.transpose(fit_data[3])]

            if(file_count%100==0):
                print(os.path.join(root,file))

            file_count+=1

        break

    print(np.mean(fit_values[0])/temp_cal[1])
    temp_values=pd.DataFrame((fit_values[0]-np.min(fit_values[0]))/temp_cal[1])
    raw_spectra=pd.DataFrame(raw_spectra)
    spectrum_data=pd.DataFrame(spectrum_data)
    spectrum_fit=pd.DataFrame(spectrum_fit)
    fit_values=pd.DataFrame(np.transpose(fit_values))

    print(np.std(temp_values))

    # Comment out the block below to suppress data saving

    os.mkdir(Path(Path(download_dir)/save_dir))

    raw_spectra.to_csv(Path(Path(download_dir)/(save_dir+'/raw_spectra.csv')),index=False,header=None)
    spectrum_data.to_csv(Path(Path(download_dir)/(save_dir+'/spectrum_data.csv')),index=False,header=None)
    spectrum_fit.to_csv(Path(Path(download_dir)/(save_dir+'/spectrum_fit.csv')),index=False,header=None)
    fit_values.to_csv(Path(Path(download_dir)/(save_dir+'/fit_values.csv')),index=False,header=None)
    temp_values.to_csv(Path(Path(download_dir)/(save_dir+'/temp_values.csv')),index=False,header=None)

print("Done reading data!")
