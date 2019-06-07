from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from lmfit import Model
import os,re,io,sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import zipfile

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

data_root_directory=Path(Path(os.getcwd())/"data/")

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

def find_directory(path):
    for root,dirs,files in os.walk(Path(data_root_directory)):
        if(os.path.exists(path)):
            return True
    return False

def find_file(drive_URL):

    file_id = drive_URL.split("id=")[1]

    file_list = drive.ListFile({'q': '',\
                                'corpora': 'teamDrive',\
                                'teamDriveId': '0AC8KtsHsd3AhUk9PVA',\
                                'includeItemsFromAllDrives': True,\
                                'supportsAllDrives': True}).GetList() #"'root' in parents and trashed=false"
    
    for file in file_list:
        if(file['id']==file_id):
            return file
    return None

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs.sort(key=numerical_sort)
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('|->{}{}/'.format(indent, os.path.basename(root)))
        
def directory_select(directory):
    list_files(directory)
    directory_selection=input("Please enter a bottom-level directory for analysis: ")
    return directory_selection

def download_from_teamdrive(file):

    drive_file=drive.CreateFile(file)
    downloaded_file=Path(data_root_directory/file['title'])
    drive_file.GetContentFile(downloaded_file)

    if(drive_file['title'].split(".")[1]=='zip'):
        zip_ref=zipfile.ZipFile(downloaded_file,'r')
        zip_ref.extractall(data_root_directory)
        zip_ref.close()
        os.remove(downloaded_file)

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
