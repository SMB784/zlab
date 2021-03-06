'''
Created on Aug 9, 2019

@author: sean

The data_download module in this utility used to download data from the
team drive when given an appropriate team drive URL.

Required inputs:  root directory where data is to be downloaded
Returned outputs: directory of downloaded data

Example usage:

from Utilities.TeamDrive_DataDownload import *
from Utilities.TeamDrive_DataDownload import data_download

data_root_directory=/home/
download_dir=data_download.Download(data_root_directory).download_data()
'''
import os,re,io,sys,zipfile,traceback
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def directory_exists(root_directory,dir_name):
    try:
        for root,dirs,files in os.walk(Path(root_directory)):
            dirs.sort(key=numerical_sort)
            if(os.path.isdir(Path(root_directory)/dir_name)):
                return True
        return False
    except:
        traceback.print_exc()
        return False

def directory_select(directory):
    list_files(directory)
    directory_selection=input("Please enter a bottom-level directory for analysis: ")
    return directory_selection

def download_from_teamdrive(file,root_directory):

    drive_file=drive.CreateFile(file)
    downloaded_file=Path(Path(root_directory)/file['title'])
    drive_file.GetContentFile(downloaded_file)

    if(drive_file['title'].split(".")[1]=='zip'):
        zip_ref=zipfile.ZipFile(downloaded_file,'r')
        zip_ref.extractall(root_directory)
        zip_ref.close()
        os.remove(downloaded_file)

def find_directory(root_dir,select_dir):
    for root,dirs,files in os.walk(root_dir):
        dirs.sort(key=numerical_sort)
        dir_path=os.path.join(root,select_dir)
        if(os.path.exists(dir_path)):
            return dir_path
    return None

def find_file(drive_URL):
    try:
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
    except:
        traceback.print_exc()
        return None

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        dirs.sort(key=numerical_sort)
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('|->{}{}'.format(indent, os.path.basename(root)))

def numerical_sort(value):
    numbers=re.compile(r'(\d+)')
    parts=numbers.split(value)
    parts[1::2]=map(int,parts[1::2])
    return parts

################### Credentials and Authentication block ####################
try:
    # Find location of TeamDrive_DataDownload directory containing auth files
    auth_path=Path('/')
    for root, dirs, files in os.walk('../..'):
        for name in dirs:
            if name.endswith('TeamDrive_DataDownload'):
                auth_path=Path(os.path.abspath(os.path.join(root,name)))
    
    # Authenticate using auth_path defined above
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = auth_path/'client_secrets.json'
    gauth=GoogleAuth()
    gauth.LoadCredentialsFile(auth_path/'credentials.txt')
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
    gauth.SaveCredentialsFile(auth_path/'credentials.txt')
    drive=GoogleDrive(gauth)
except:
    traceback.print_exc()