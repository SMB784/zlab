from SX674_Spectrometer import *

try:
    input_data=pd.read_csv(find_directory(Path(Path(data_directory)/save_directory)),header=None)
except:
    from SX674_Spectrometer import spectrum_read
    input_data=spectrum_read.spectral_data
    spectrum_read.spectral_data.to_csv(Path(Path(data_directory)\
                                            /(save_directory+processed_data_filename)),index=False,header=None)
