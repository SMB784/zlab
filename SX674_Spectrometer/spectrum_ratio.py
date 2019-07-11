from SX674_Spectrometer import *

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

start=575
stop=673
crit=607
tolerance=0.3

temp_cal=temp_cal=[1.11286585,-0.00144068]
temp_values=[]

for i in range(1,len(input_data.columns)):

    lambdaStartIndex=input_data[input_data[[0]].apply(np.isclose,b=start,atol=tolerance).any(1)].index.tolist()[0]
    lambdaStopIndex=input_data[input_data[[0]].apply(np.isclose,b=stop,atol=tolerance).any(1)].index.tolist()[0]
    lambdaCritIndex=input_data[input_data[[0]].apply(np.isclose,b=crit,atol=tolerance).any(1)].index.tolist()[0]

    wavelength=input_data.iloc[lambdaStartIndex:lambdaStopIndex,0].to_numpy()
    amplitude=input_data.iloc[lambdaStartIndex:lambdaStopIndex,i].to_numpy()
    normalized_amplitude=(amplitude-amplitude.min())/(amplitude.max()-amplitude.min())
        
    wavelength_left=input_data[[0]].iloc[lambdaStartIndex:lambdaCritIndex,0].to_numpy()
    wavelength_right=input_data[[0]].iloc[lambdaCritIndex:lambdaStopIndex,0].to_numpy()

    normalized_left=normalized_amplitude[0:len(wavelength_left)]
    normalized_right=normalized_amplitude[len(wavelength_left):len(wavelength)]
    
    I_left=simps(normalized_left,wavelength_left)
    I_right=simps(normalized_right,wavelength_right)
    ratio=I_left/I_right
    temp_values.append((ratio-temp_cal[0])/temp_cal[1])

temp_values=temp_values-np.min(temp_values)
print(np.std(temp_values))
temp_values=pd.DataFrame(temp_values)

temp_values.to_csv(Path(Path(data_directory)/(save_directory+"ratio_temp_values.csv")),\
                       index=False,header=None)