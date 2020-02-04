'''
Created on Feb 4, 2020

@author: Sean
'''
from Experiments.GeV_PCF_Thermometry import *

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

            input_spectrum=SpectrumRead.Spectrum(Path(download_dir)/file).read_spectrum()
            fit_data=spectral_fit.Fit(start,stop,input_spectrum).fit_spectrum()

            if(fit_data[2][0]==0):
                print("Fit invalid, skipped this entry")
                file_count+=1
                plt.plot(input_spectrum[0],input_spectrum[1])
                plt.show()
                continue

            if(file_count==0):
                spectrum_data=np.transpose(fit_data[0])[0]
                spectrum_fit=np.transpose(fit_data[1])[0]
                fit_values=np.transpose(fit_data[2])
            else:
                spectrum_data=np.c_[spectrum_data,np.transpose(fit_data[0])[1]]
                spectrum_fit=np.c_[spectrum_fit,np.transpose(fit_data[1])[1]]
                fit_values=np.c_[fit_values,np.transpose(fit_data[2])]

            if(file_count%100==0):
                print(os.path.join(root,file))

            file_count+=1

        break

    print(np.mean(fit_values[0])/temp_cal[1])
    temp_values=pd.DataFrame((fit_values[0]-np.min(fit_values[0]))/temp_cal[1])
    spectrum_data=pd.DataFrame(spectrum_data)
    spectrum_fit=pd.DataFrame(spectrum_fit)
    fit_values=pd.DataFrame(np.transpose(fit_values))

    print(np.std(temp_values))

    # Comment out the block below to suppress data saving

    os.mkdir(Path(Path(download_dir)/save_dir))

    spectrum_data.to_csv(Path(Path(download_dir)/(save_dir+'/spectrum_data.csv')),index=False,header=None)
    spectrum_fit.to_csv(Path(Path(download_dir)/(save_dir+'/spectrum_fit.csv')),index=False,header=None)
    fit_values.to_csv(Path(Path(download_dir)/(save_dir+'/fit_values.csv')),index=False,header=None)
    temp_values.to_csv(Path(Path(download_dir)/(save_dir+'/temp_values.csv')),index=False,header=None)

print("Done reading data!")
