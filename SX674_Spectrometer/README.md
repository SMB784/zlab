# Installation instructions:
-----

## 1. Install Anaconda
- #### WINDOWS:
  - ###### open powershell as administrator from start menu under anaconda folder
  - ###### enter the following command into powershell: conda install numpy scipy matplotlib pandas pathlib astropy && conda install -c conda-forge pydrive lmfit
- #### LINUX:
  - ###### open terminal
  - ###### enter the following command into terminal prompt: conda install numpy scipy matplotlib pandas pathlib astropy && conda install -c conda-forge pydrive lmfit
## 2. Install Java
## 3. Install Eclipse
- #### Install Java development environment
- #### Configure PyDev
  - ###### Start eclipse
  - ###### Click Help
  - ###### Select Install New Software
  - ###### Click Add
  - ###### Enter the following URL into Location bar, then hit Add: http://www.pydev.org/updates
  - ###### Hit Select All, then hit Next and accept all license agreements, then hit Finish
- #### Create a new PyDev project (File -> New Project -> Other -> PyDev -> PyDev Project)
  - ###### Give arbitrary name
  - ###### Configure interpreter (choose First in Path)
  - ###### Select Open Perspective (remember your decision)
- #### Configure EGit for github integration (follow this video: https://www.youtube.com/watch?v=ptK9-CNms98)
- #### Configure PyDrive (follow steps here: https://pythonhosted.org/PyDrive/quickstart.html)
  - ###### Save client_secrets.json in */git/zlab/SX674_Spectrometer directory
  - ###### Run patcher to fix files.py with the following command: 
  ```
  patch -u $HOME/miniconda3/lib/python3.7/site-packages/pydrive/files.py -i $HOME/git/zlab/SX674_Spectrometer/files_fix.patch
  ```
  - ###### Run program
