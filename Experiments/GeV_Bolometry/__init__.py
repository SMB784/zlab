'''
Created on Aug 12, 2019

@author: sean

Contains methods that:
    
4.) make figs 2 & 3 for manuscript

Data files from Team Drive needed to run:


'''
########################## Import bolt-on modules ###########################
from Utilities.TeamDrive_DataDownload import *
from Utilities.TeamDrive_DataDownload import data_download
########################## Import built-in modules ##########################

############################## Initializations ##############################
data_root_directory=Path(Path(os.getcwd())/'data/')
download_dir=data_download.Download(data_root_directory).download_data()