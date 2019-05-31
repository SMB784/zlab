from SX674_Spectrometer import *
from SX674_Spectrometer import spectrum_read as input_data

lmodel=Model(doubleLorentzianFit)

# lmodel.set_param_hint('c1',min=595,max=605)
lmodel.set_param_hint('c2',min=610,max=620)
lmodel.set_param_hint('c3',min=615,max=630)
        
lmodel.set_param_hint('w1',min=0)
lmodel.set_param_hint('w2',min=0)
lmodel.set_param_hint('w3',min=0,max=50)
                
params=lmodel.make_params(c1=initial_fit[0][0],w1=initial_fit[1][0],h1=initial_fit[2][0],\
                          c2=initial_fit[0][1],w2=initial_fit[1][1],h2=initial_fit[2][1],\
                          c3=initial_fit[0][2],w3=initial_fit[1][2],h3=initial_fit[2][2],\
                          o1=initial_fit[3])

fit_values=[]
for i in range(1,len(input_data.spectral_data.columns)):
    result=lmodel.fit(input_data.spectral_data[i],params,x=input_data.spectral_data[0])
    fit_values.append(findValue(result.best_values)[0]-75128.49624473446)
#     plt.plot(input_data.spectral_data[0],input_data.spectral_data[i])
#     plt.plot(input_data.spectral_data[0],result.best_fit)
    print(result.best_values)

print(np.std(np.transpose(fit_values)))
