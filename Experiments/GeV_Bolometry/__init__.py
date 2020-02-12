'''
Created on Aug 12, 2019

@author: sean

Contains methods that:
    
4.) make figs 2 & 3 for manuscript

Data files from Team Drive needed to run:


'''
########################## Import built-in modules ##########################
import os
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.ticker as ticker
from matplotlib.ticker import EngFormatter
############################## Initializations ##############################
data_root_directory=Path(Path(os.getcwd())/'data/')
write_directory=Path(Path(os.getcwd())/'Manuscript_Files/')