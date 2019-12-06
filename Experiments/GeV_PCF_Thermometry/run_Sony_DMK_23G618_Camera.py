'''
Created on Dec 6, 2019

@author: sean
'''
from Experiments.GeV_PCF_Thermometry import *

save_dir='processed_data'
image_data=[]

if directory_exists(Path(download_dir),save_dir)==True:
    print("Processed data already exists!")
else:
    exclude = set([save_dir])
    for root,dirs,files in os.walk(download_dir,topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        file_count=0

        for file in sorted(files,key=numerical_sort):
            files.sort(key=numerical_sort)
            
            if(file_count==0):
                input_image=img_read.Image(Path(download_dir)/file).read_image()
            else:
                input_image+=img_read.Image(Path(download_dir)/file).read_image()
            file_count+=1

    output_image=pd.DataFrame(input_image/file_count)
    
    os.mkdir(Path(Path(download_dir)/save_dir))
    output_image.to_csv(Path(Path(download_dir)/(save_dir+'/frame_averaged_image.csv')),index=False,header=None)

print("Done reading data!")