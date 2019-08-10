'''
Created on Aug 9, 2019

@author: sean
'''
from TeamDrive_DataDownload import *

class Download:
    def __init__(self,root,save,filename):
        self.root_directory=root
        self.save_directory=save
        self.processed_data_filename=filename
    
    #drive_URL = "https://drive.google.com/open?id=1eR65LvN4WQiiEW5uGWzsY6CoNnzwoFn3"
    data_directory=''
    
    drive_URL=input("Please enter URL for TeamDrive data, or press ENTER to use existing data: ")
    
    print("Searching for data...")
    
    if(drive_URL==''):
        data_root_directory=\
            set_root_directory(\
            '/home/sean/git/zlab/SX674_Spectrometer/data/')
        print("Existing data found in these directories:\r")
    
        data_directory=find_directory(\
                        directory_select(\
                        data_root_directory))
    
    else:
        find_file=find_file(drive_URL)
        
        try:
            download_dir=Path(data_root_directory+find_file['title'].split('.')[0])# names directory after the name of the file to be downloaded
            
            if directory_exists(download_dir)==False: # if directory with filename doesn't already exist, download file
                print("Data located on TeamDrive, downloading data...")
                download_from_teamdrive(find_file) # downloads the file, creates directory named after downloaded file
                print("Data downloaded from TeamDrive to following directories:\n")
                data_directory=find_directory(directory_select(data_root_directory)) # returns path of user selected directory
            else:
                print("Existing data from TeamDrive found in these directories:\n")
                data_directory=find_directory(directory_select(data_root_directory))
        except:
            print("File not found on TeamDrive.  Check URL and run program again")
            traceback.print_exc()
            sys.exit()