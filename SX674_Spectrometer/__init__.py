from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from lmfit import Model
import os,re,io
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth=GoogleAuth()

gauth.LoadCredentialsFile("credentials.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("credentials.txt")

drive=GoogleDrive(gauth)

download_dir=Path(Path(os.getcwd())/"data/")

drive_URL = "https://drive.google.com/open?id=1eR65LvN4WQiiEW5uGWzsY6CoNnzwoFn3"


data_root_directory='/home/sean/Desktop/5-29-19/NewSpectrometer/' # data directory goes here
sub_folder='27000uW_250ms_NoBin/' # data subfolder goes here
save_folder='spectralData/'

GeV=601
tolerance=0.2

baseline=800.0 # No Binning
# baseline=1100.0 # 4x4 Binning
trigger=1.2
gate=10

# calibration=[543.26,0.13497] #4x4 binning
calibration=[543.741,0.068256] #No binning

initial_fit=[[601.0,612,625],\
             [4.5,11,40],\
             [1,1,1],0]

temp_cal=[0,0.008] # from center wavelength vs temp: [intercept, slope]

numbers=re.compile(r'(\d+)')


def download_from_teamdrive():

    
    file_id = drive_URL.split("id=")[1]

    file_list = drive.ListFile({'q': '',\
                                'corpora': 'teamDrive',\
                                'teamDriveId': '0AC8KtsHsd3AhUk9PVA',\
                                'includeTeamDriveItems': True,\
                                'supportsTeamDrives': 'true'}).GetList() #"'root' in parents and trashed=false"

    for file in file_list:
        if(file['id']==file_id):
            drive_file=drive.CreateFile(file)
            print(drive_file.GetPermissions())
            drive_file.GetContentFile(Path(download_dir/file['title']))

download_from_teamdrive() # delete before finalizing merge

def numerical_sort(value):
    parts=numbers.split(value)
    parts[1::2]=map(int,parts[1::2])
    return parts

def find_max_window(df):
    rollingArray=df[0:len(df[0])].rolling(window=gate).mean()[gate-1:len(df[0])]
    loc=[]
    y_window=[]
    for i in range(0,len(df.columns)):
        vals=rollingArray[i].values
        try:
            y=np.min(np.argwhere(vals>=baseline*trigger))
            y_window.append(np.min(np.argwhere(vals[y:len(vals)]<=baseline*trigger)))
        except:
            y=0
            y_window.append(0)
        loc.append(y)
    return [np.max(y_window),loc]

def tripleLorentzianFit(x,c1,c2,c3,\
                w1,w2,w3,\
                h1,h2,h3,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(np.pi*w3)*(w3**2/((x-c3)**2+w3**2))\
           +o1
           
def doubleLorentzianFit(x,c1,c2,\
                w1,w2,\
                h1,h2,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +o1

def findValue(bestValues): #input is dictionary output from result.best_values
    center_FWHM=[]
    for key, value in bestValues.items():
        if np.isclose(a=value,b=GeV,atol=tolerance*20):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
    return center_FWHM
