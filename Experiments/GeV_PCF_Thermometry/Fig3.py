'''
Created on Feb 7, 2020

@author: sean
'''
'''
Created on Oct 1, 2019

@author: sean
'''
#################################################################################
############################# Import Declarations ###############################
#################################################################################

############################# Data import/analysis ##############################

import os
import numpy as np
import pandas as pd
from pathlib import Path

################################# Data plotting #################################

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches

############################## Import/Export Block ##############################

data_read_directory=str(os.getcwd())+'/data/Imaging/'
write_directory=str(os.getcwd())+'/Manuscript_Files/Rev1_Draft/'

#################################################################################
############################## Plot Setup Block #################################
#################################################################################

fontsize=24
markersize=200
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(1,2)

fig,ax=plt.subplots(figsize=(12,6))

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

norm=mpl.colors.Normalize(25,40)

burnt_orange='#ffa800'
burnt_magenta='#c85340'
burnt_violet='#800080'
charcoal='#000000'
flame_colors=[charcoal,burnt_orange,burnt_magenta,burnt_violet]

#################################################################################
################################ Left Plot #####################################
#################################################################################

diagram=mpl.image.imread(write_directory+'Fig3_a.png')

L_ax=fig.add_subplot(grid[0,0])

L_ax.xaxis.set_visible(False)
L_ax.yaxis.set_visible(False)
L_ax.spines['left'].set_visible(False)
L_ax.spines['right'].set_visible(False)
L_ax.spines['top'].set_visible(False)
L_ax.spines['bottom'].set_visible(False)
L_ax.xaxis.set_ticks([])
L_ax.yaxis.set_ticks([])

L_ax.imshow(diagram,aspect='auto')

L_ax.annotate('(a)',xy=(0.0125,0.925),xycoords='axes fraction')

#################################################################################
############################### Right Plot #####################################
#################################################################################

x_scan=pd.read_csv(Path(data_read_directory+'two_wire_x_scan.csv'),header=None).to_numpy()

R_ax=fig.add_subplot(grid[0,1])

R_ax.set_ylabel('$\delta x$ ($\mu m$)')
R_ax.set_xlabel('T ($\degree C$)')
R_ax.yaxis.set_ticks([0,300,600,895])
R_ax.set_yticklabels(['0','300','600','900'])
R_ax.set_ylim(-50,1000)
R_ax.set_xlim(27,39)
R_ax.xaxis.set_ticks([27,30,33,36,39])

for i in range(1,4):
    temp_trace=x_scan[:,i]+20
    R_ax.plot(temp_trace,x_scan[:,0],c=flame_colors[i],lw=10,solid_capstyle='round',zorder=5-i)
#     R_ax.scatter(temp_trace,x_scan[:,0],c=temp_trace,cmap='inferno',norm=norm,lw=3,zorder=5-i)


# 30 micron wire
R_ax.axhline(155,color='red',ls='dotted',lw=3,zorder=10)
R_ax.axhline(185,color='red',ls='dotted',lw=3,zorder=10)
 
# 15 micron wire
R_ax.axhline(787.5,color='blue',ls='dotted',lw=3,zorder=10)
R_ax.axhline(802.5,color='blue',ls='dotted',lw=3,zorder=10)

labels=['400 mA','375 mA','350 mA']
patchez=[patches.Patch(color=flame_colors[1],label=labels[0]),
       patches.Patch(color=flame_colors[2],label=labels[1]),
       patches.Patch(color=flame_colors[3],label=labels[2])]
 
R_ax.legend(handles=patchez,frameon=False,loc=(0.45,0.425))
    
R_ax.annotate('(b)',xy=(0.0125,0.925),xycoords='axes fraction')


############################### Plot Export ######################################
 
plt.tight_layout()
plt.savefig(write_directory+"Fig3_rev1.png",bbox_inches='tight',dpi=480)
plt.show()
