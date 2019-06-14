from SX674_Spectrometer import *

try:
    input_data=pd.read_csv(find_directory(Path(Path(data_directory)/save_directory)),header=None)
except:
    from SX674_Spectrometer import spectrum_read
    input_data=spectrum_read.spectral_data
    spectrum_read.spectral_data.to_csv(Path(Path(data_directory)\
                                            /(save_directory+processed_data_filename)),index=False,header=None)

lmodel=Model(lorentzianGaussianFit)

initial_fit=[[601.0,612,625],\
             [4.5,11,40],\
             [1,1,1],0]

temp_cal=[601.007,0.0078] # from center wavelength vs temp: [intercept, slope]

# lmodel.set_param_hint('c1',min=600,max=602)
lmodel.set_param_hint('c2',min=605,max=620)
lmodel.set_param_hint('c3',min=605,max=630)
        
lmodel.set_param_hint('w1',min=0)
lmodel.set_param_hint('w2',min=9,max=20)
lmodel.set_param_hint('w3',min=0,max=50)
                
params=lmodel.make_params(c1=initial_fit[0][0],w1=initial_fit[1][0],h1=initial_fit[2][0],\
                          c2=initial_fit[0][1],w2=initial_fit[1][1],h2=initial_fit[2][1],\
                          c3=initial_fit[0][2],w3=initial_fit[1][2],h3=initial_fit[2][2],\
                          o1=initial_fit[3])

fit_curves=input_data[0].to_numpy()
fit_values=[]
temp_values=[]

file_count=0


for i in range(1,len(input_data.columns)):

    result=lmodel.fit(input_data[i],params,x=input_data[0])
    print(result.best_values)

    fit_curves=np.c_[fit_curves,result.best_fit.to_numpy()]
    
    fit_values.append(findValue(result.best_values))
    
    temp_value=(findValue(result.best_values)[0]-temp_cal[0])/temp_cal[1]
    temp_values.append(temp_value)

#     plt.plot(input_data[0],input_data[i])
#     plt.plot(input_data[0],result.best_fit,ls='dashed')
#     if(file_count>2):
#         break
#     file_count+=1
# plt.show()

temp_stdev=np.std(np.transpose(temp_values)[1:len(np.transpose(temp_values))])

fit_curves=pd.DataFrame(fit_curves)
fit_values=pd.DataFrame(fit_values)
temp_values=pd.DataFrame(temp_values)

fit_curves.to_csv(Path(Path(data_directory)/(save_directory+"fit_curves.csv")),\
                       index=False,header=None)
fit_values.to_csv(Path(Path(data_directory)/(save_directory+"fit_values.csv")),\
                       index=False,header=None)
temp_values.to_csv(Path(Path(data_directory)/(save_directory+"temp_values.csv")),\
                       index=False,header=None)

