from Devices.Trius_SX674_Camera import image_read
import Devices.Trius_SX674_Camera
from Utilities.TeamDrive_DataDownload import *
import Utilities.TeamDrive_DataDownload
import pandas as pd
import numpy as np

root_dir='/home/sean/git/zlab/Experiments/SPDC/data/SPDC_Interference/'
dark_dir='dark'

spdc_crosses=Devices.Trius_SX674_Camera.image_read.Image(root_dir,dark_dir).calculate_dark_frame()
# spdc_crosses=pd.read_csv(data_root_directory,header=None).to_numpy()

Devices.Trius_SX674_Camera.plot_image(spdc_crosses)

pd.DataFrame(spdc_crosses).to_csv(root_dir+'SPDC_interference_B.csv',index=False,header=None)