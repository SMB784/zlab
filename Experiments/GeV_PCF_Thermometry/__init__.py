'''
Created on Aug 12, 2019

@author: sean

Imports and initializations go here

'''
########################## Import bolt-on modules ###########################
from Utilities.TeamDrive_DataDownload import *
from Utilities.TeamDrive_DataDownload import data_download
from Devices.SX674_Spectrometer import *
from Devices.SX674_Spectrometer import spectrum_read
from Utilities.SplitVacancy_SpectralFit import *
from Utilities.SplitVacancy_SpectralFit import spectral_fit
########################## Import built-in modules ##########################

############################## Initializations ##############################
data_root_directory=Path(Path(os.getcwd())/'data/')
download_dir=data_download.Download(data_root_directory).download_data()

# calibration=[543.741,0.068256] #No binning
calibration=[543.26,0.13497] #4x4 binning
start=585
stop=673