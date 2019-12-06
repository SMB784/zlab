'''
Created on Aug 12, 2019

@author: sean

Contains methods that:

1.) run spectrometer program (run_SX674Spectrometer) on
    precollected in local directories or data downloaded
    from teamdrive

2.) fourier filter input images (scanning temp or spectral)

3.) calculate fourier transform resolution trace for PCF
    probe
    
4.) make figs 2 & 3 for manuscript

Data files from Team Drive needed to run:


'''
########################## Import bolt-on modules ###########################
from Utilities.TeamDrive_DataDownload import *
from Utilities.TeamDrive_DataDownload import data_download
from Devices.SX674_Spectrometer import *
from Devices.SX674_Spectrometer import spectrum_read
from Devices.ScienceSurplus_Spectrometer import *
from Devices.ScienceSurplus_Spectrometer import Spectrum_Read
from Devices.Sony_DMK_23G618_Camera import *
from Devices.Sony_DMK_23G618_Camera import img_read
from Utilities.SplitVacancy_SpectralFit import *
from Utilities.SplitVacancy_SpectralFit import spectral_fit
########################## Import built-in modules ##########################

############################## Initializations ##############################
data_root_directory=Path(Path(os.getcwd())/'data/')
download_dir=data_download.Download(data_root_directory).download_data()

# 7-17-19 to 7-23-19
# calibration=[559.75,0.067417] #No binning
# calibration=[557.633,0.134624] #4x4 binning
# 11-05-19
calibration=[537.268697914187,0.14070300109619718] #4x4 binning
start=580
stop=630