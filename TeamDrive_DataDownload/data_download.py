'''
Created on Aug 9, 2019

@author: sean
'''
from TeamDrive_DataDownload import *

class Download:

    def __init__(self,root_dir):
        self.root_directory=root_dir
    
    def download_data(self):
        #drive_URL = "https://drive.google.com/open?id=1eR65LvN4WQiiEW5uGWzsY6CoNnzwoFn3"
        
        drive_URL=input("Please enter URL for TeamDrive data, or press ENTER to use existing data: ")
        
        print("Searching for data...")
        
        if(drive_URL==''):
            print("Existing data found in these directories:\r")
            return find_directory(self.root_directory,directory_select(self.root_directory))
        
        else: # searches for data on teamdrive according to input URL
            try:
                data=find_file(drive_URL) # returns the file metadata
                
                download_dir=Path(self.root_directory+data['title'].split('.')[0])# names directory after the name of the file to be downloaded
                
                if directory_exists(download_dir,self.root_directory)==False: # if directory with filename doesn't already exist, download file
                    print("Data located on TeamDrive, downloading data...")
                    download_from_teamdrive(data,self.root_directory) # downloads the file, creates directory named after downloaded file
                    print("Data downloaded from TeamDrive to following directories:\n")
                    return find_directory(directory_select(self.root_directory)) # returns path of user selected directory
                else:
                    print("Existing data from TeamDrive found in these directories:\n")
                    return find_directory(directory_select(self.root_directory)) # returns path of user selected directory
            except:
                print("File not found on TeamDrive.  Check URL and run program again")
                traceback.print_exc()
                sys.exit()