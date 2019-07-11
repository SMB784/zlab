from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from pathlib import Path
from scipy import stats
from scipy import fftpack
from scipy.integrate import simps
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

save_directory='processed_data/'
processed_data_filename='spectral_data.csv'


GeV=601
tolerance=0.2

calibration=[543.26,0.13497] #4x4 binning
# calibration=[543.741,0.068256] #No binning

initial_fit=[]

temp_cal=[] # from center wavelength vs temp: [intercept, slope]

numbers=re.compile(r'(\d+)')

def find_directory(directory):
    for root,dirs,files in os.walk(Path(data_root_directory)):
        dirs.sort(key=numerical_sort)
        dir_path=os.path.join(root,directory)
        if(os.path.exists(dir_path)):
            print("\n"+str(dir_path)+" directory found\n")
            return dir_path
    return None

def directory_exists(path):
    try:
        for root,dirs,files in os.walk(Path(data_root_directory)):
            dirs.sort(key=numerical_sort)
            if(os.path.isdir(path)):
                return True
        return False
    except:
        return False

def find_file(drive_URL):

    file_id = drive_URL.split("id=")[1]

    file_list = drive.ListFile({'q': '',\
                                'corpora': 'teamDrive',\
                                'teamDriveId': '0AC8KtsHsd3AhUk9PVA',\
                                'includeItemsFromAllDrives': True,\
                                'supportsAllDrives': True}).GetList()
    
    for file in file_list:
        if(file['id']==file_id):
            return file
    return None

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs.sort(key=numerical_sort)
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('|->{}{}'.format(indent, os.path.basename(root)))
        
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
    loc=[]
    y_window=[]
    for i in range(0,len(df.columns)-2):

        vals=df[i].values
        baseline=np.mean(df[i].values[0:150])
        maximum=np.max(vals)
        trigger=(maximum-baseline)/2
        vals=vals-baseline
        
        try:
            y_min=np.min(np.argwhere(vals>=trigger))
            y_window.append(np.min(np.argwhere(vals[y_min:len(vals)]<=trigger)))
        except ValueError:  #raised if `y` is empty.
            y_min=0
            y_window.append(0)
        loc.append(y_min)
    return [y_window,loc]

def doubleLorentzianFit(x,c1,c2,\
                w1,w2,\
                h1,h2,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +o1

def lorentzianGaussianFit(x,c1,c2,\
                          w1,w2,\
                          h1,h2,\
                          o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c2)**2/(2*w2**2))\
           +o1

def tripleLorentzianFit(x,c1,c2,c3,\
                w1,w2,w3,\
                h1,h2,h3,\
                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(np.pi*w3)*(w3**2/((x-c3)**2+w3**2))\
           +o1

def lorentzianDoubleGaussianFit(x,c1,c2,c3,\
                                w1,w2,w3,\
                                h1,h2,h3,\
                                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c2)**2/(2*w2**2))\
           +h3/(w2*np.sqrt(2*np.pi))*np.exp(-(x-c3)**2/(2*w3**2))\
           +o1

def doubleLorentzianGaussianFit(x,c1,c2,c3,\
                                w1,w2,w3,\
                                h1,h2,h3,\
                                o1):
    return h1/(np.pi*w1)*(w1**2/((x-c1)**2+w1**2))\
           +h2/(np.pi*w2)*(w2**2/((x-c2)**2+w2**2))\
           +h3/(w3*np.sqrt(2*np.pi))*np.exp(-(x-c3)**2/(2*w3**2))\
           +o1

def findValue(bestValues): #input is dictionary output from result.best_values
    center_FWHM=[]
    for key, value in bestValues.items():
        if np.isclose(a=value,b=GeV,atol=tolerance*10):
                center_FWHM.append(value) # center wavelength
                widthKey='w'+re.findall(r'\d+',key)[0]
                center_FWHM.append(2*bestValues[widthKey]) # width
    return center_FWHM

#drive_URL = "https://drive.google.com/open?id=1eR65LvN4WQiiEW5uGWzsY6CoNnzwoFn3"

data_directory=''

drive_URL=input("Please enter URL for TeamDrive data, or press ENTER to use existing data: ")

print("Searching for data...")

if(drive_URL==''):
    print("Existing data found in these directories:\n")
    data_directory=find_directory(directory_select(data_root_directory))
else:

    find_file=find_file(drive_URL)
    
    try:
        download_dir=Path(data_root_directory/find_file['title'].split('.')[0])# names directory after the name of the file to be downloaded
        
        if directory_exists(download_dir)==False: # if directory with filename doesn't already exist, download file
            print("Data located on TeamDrive, downloading data...")
            download_from_teamdrive(find_file) # downloads the file, creates directory named after downloaded file
            print("Data downloaded from TeamDrive to following directories:\n")
            data_directory=find_directory(directory_select(data_root_directory)) # returns path of user selected directory
        else:
            print("Existing data from TeamDrive found in these directories:\n")
            data_directory=find_directory(directory_select(data_root_directory))
    except Exception:
        print("File not found on TeamDrive.  Check URL and run program again")
        print(Exception)
        sys.exit()