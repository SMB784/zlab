'''
Created on Aug 9, 2019

@author: sean
'''
import os,re,io,sys,zipfile
from pathlib import Path
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

data_root_directory=Path(Path(os.getcwd())/"data/")
save_directory='processed_data/'
processed_data_filename='spectral_data.csv'

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