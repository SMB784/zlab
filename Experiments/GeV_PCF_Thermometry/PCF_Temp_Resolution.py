'''
Created on Oct 9, 2019

@author: sean
'''
from Experiments.GeV_PCF_Thermometry import *

wave_cal=[169.3,0.6413,-6.398e-5,-4.061e-9]

temp_cal=[599.6316,0.0078]

spectral_data=[]

for root,dirs,files in os.walk(download_dir,topdown=True):
    file_count=0

    for file in sorted(files,key=numerical_sort):
        files.sort(key=numerical_sort)
        input_spectrum=pd.read_csv(Path(Path(download_dir)/file),header=None).drop([1],axis=1)
        input_spectrum[[0]]=input_spectrum[[0]].apply(lambda x:wave_cal[0]+wave_cal[1]*x+wave_cal[2]*x**2+wave_cal[3]*x**3)
        input_spectrum.columns=[0,1]

        fit_data=spectral_fit.Fit(start,stop,input_spectrum).fit_spectrum()

        if(fit_data[2][0]==0):
            print("Fit invalid, skipped this entry")
            continue

        if(file_count==0):
            spectrum_data=np.transpose(fit_data[0])[0]
            spectrum_fit=np.transpose(fit_data[1])[0]
            fit_values=np.transpose(fit_data[2])
            file_count=1
        else:
            spectrum_data=np.c_[spectrum_data,np.transpose(fit_data[0])[1]]
            spectrum_fit=np.c_[spectrum_fit,np.transpose(fit_data[1])[1]]
            fit_values=np.c_[fit_values,np.transpose(fit_data[2])]

        print(os.path.join(root,file))

temp_values=(fit_values[0]-np.mean(fit_values[0]))/temp_cal[1]
time_values=np.arange(0.2,20.2,0.2)
print(temp_values)

temp_trace=pd.DataFrame(np.c_[time_values,temp_values])
spectrum_data=pd.DataFrame(spectrum_data)
spectrum_fit=pd.DataFrame(spectrum_fit)
fit_values=pd.DataFrame(np.transpose(fit_values))

temp_trace.to_csv(str(os.getcwd())+'/data/Imaging/wire_off_temp_trace.csv',index=None)

#0.66*np.sqrt(0.2)
#4
power_arr=[47,18,6.3,0.43]
std_arr=[0.77*np.sqrt(0.001)*1000,0.54*np.sqrt(0.02)*1000,0.72*np.sqrt(0.1)*1000,0.90*np.sqrt(1)*1000]

plt.scatter(power_arr,std_arr,s=200,color='b')
plt.scatter(4,0.66*np.sqrt(0.2)*1000,s=200,color='r')
plt.yscale('log')

plt.xlabel("Laser Power (mW)")
plt.ylabel("Temperature Sensitivity (mK/$\sqrt{Hz}$)")
plt.show()
