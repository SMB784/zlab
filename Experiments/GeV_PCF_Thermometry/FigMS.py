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
from matplotlib.collections import LineCollection
from matplotlib.ticker import EngFormatter

############################## Import/Export Block ##############################

data_read_directory=str(os.getcwd())+'/data/Imaging/'
write_directory=str(os.getcwd())+'/Manuscript_Files/Rev1_Draft/'

############################# Temperature Conversion ############################

wire_image=mpl.image.imread(data_read_directory+'wire_grid_segment.png')

wavelength20C=600.8838564550902
slope=0.0078
initial_temp=20
stepsize=5.0

avg_wavelength_10300=pd.read_csv(Path(data_read_directory+'data_ave_wave_10300_Filtered.csv'),header=None).drop([0])
std_wavelength_10300=pd.read_csv(Path(data_read_directory+'data_std_wave_10300.csv'),header=None).drop([0])
avg_wavelength_10500=pd.read_csv(Path(data_read_directory+'data_ave_wave_10500_Filtered.csv'),header=None).drop([0])
std_wavelength_10500=pd.read_csv(Path(data_read_directory+'data_std_wave_10500.csv'),header=None).drop([0])
avg_wavelength_10700=pd.read_csv(Path(data_read_directory+'data_ave_wave_10700_Filtered.csv'),header=None).drop([0])
std_wavelength_10700=pd.read_csv(Path(data_read_directory+'data_std_wave_10700.csv'),header=None).drop([0])

avg_temp_10300=(avg_wavelength_10300-wavelength20C)/slope+initial_temp
std_temp_10300=std_wavelength_10300/slope
avg_temp_10500=(avg_wavelength_10500-wavelength20C)/slope+initial_temp
std_temp_10500=std_wavelength_10500/slope
avg_temp_10700=(avg_wavelength_10700-wavelength20C)/slope+initial_temp
std_temp_10700=std_wavelength_10700/slope

avg_temp_10300=avg_temp_10300.to_numpy()
std_temp_10300=std_temp_10300.to_numpy()
avg_temp_10500=avg_temp_10500.to_numpy()
std_temp_10500=std_temp_10500.to_numpy()
avg_temp_10700=avg_temp_10700.to_numpy()
std_temp_10700=std_temp_10700.to_numpy()

# print(str(np.mean(avg_temp_10700))+", "+str(np.mean(avg_temp_10500))+", "+str(np.mean(avg_temp_10300)))

z_temp=pd.read_csv(Path(data_read_directory+'z_temp.csv'),header=None).drop(0)
z_temp=z_temp.to_numpy()[24:49,:].astype(float) #5900(index 24) to 10700(index 49)
z_temp[:,0]=(np.abs(z_temp[:,0]-10700.0))/10.0 #rescales the z axis to start at zero

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

norm=mpl.colors.Normalize(40,50)
norm_inset_cbar=mpl.colors.Normalize(0,2)

#################################################################################
################################# Left Plot #####################################
#################################################################################

diagram=mpl.image.imread(write_directory+'FigMS_sub.png')

L_ax=fig.add_subplot(grid[0,0])

L_ax.xaxis.set_visible(False)
L_ax.yaxis.set_visible(False)
L_ax.spines['left'].set_visible(False)
L_ax.spines['right'].set_visible(False)
L_ax.spines['top'].set_visible(False)
L_ax.spines['bottom'].set_visible(False)
L_ax.xaxis.set_ticks([])
L_ax.yaxis.set_ticks([])

L_inset=L_ax.inset_axes([0.657,0.013,0.333,0.333])
L_inset.imshow(wire_image,extent=[0,100,0,100],aspect='auto')
L_inset.xaxis.set_ticks([])
L_inset.yaxis.set_ticks([])

L_ax.imshow(diagram,aspect='auto')

#################################################################################
################################# Right Plot ####################################
#################################################################################

R_ax=fig.add_subplot(grid[0,1])

R_ax.tick_params(axis='x')
R_ax.tick_params(axis='y')
R_ax.set_xlabel('$\delta x$ ($\mu m$)')
R_ax.xaxis.set_ticks([0,100,200,300,400,495])
R_ax.set_xticklabels(['0','100','200','300','400','500'])
R_ax.set_ylabel('$\delta y$ ($\mu m$)')

heatmap=R_ax.imshow(avg_temp_10700,cmap='inferno',norm=norm,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')

cax = R_ax.inset_axes([0.725,0.7,0.05,0.233]) 
cbar_inset=fig.colorbar(heatmap,cax=cax, orientation='vertical')
cbar=fig.colorbar(heatmap,ax=R_ax,cax=cax)
cbar.set_label('T ($\degree C$)')

norm_inset=mpl.colors.Normalize(48.75,50.75)
LR_inset=R_ax.inset_axes([0.0,0.0,0.333,0.333])
LR_inset.imshow(avg_temp_10700,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')
LR_inset.set_xlim(300,400)
LR_inset.set_ylim(175,275)
LR_inset.xaxis.set_ticks_position('top')
LR_inset.yaxis.set_ticks_position('right')
LR_inset.xaxis.set_ticks([325,375])
LR_inset.yaxis.set_ticks([200,250])
LR_inset.set_xticklabels(['25','75'])
LR_inset.set_yticklabels(['25','75'])
LR_inset.tick_params(axis='x', colors='black')
LR_inset.tick_params(axis='y', colors='black')

subheatmap=LR_inset.imshow(avg_temp_10700,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')
cbar_inset_ax = R_ax.inset_axes([0.50,0.055,0.05,0.238]) 
cbar_inset=fig.colorbar(subheatmap,cax=cbar_inset_ax, orientation='vertical')
cbar_inset.set_ticks([48.75,49.75,50.75])
cbar_inset.ax.set_yticklabels(['0', '1', '2'])
cbar_inset.ax.tick_params(colors='black')
cbar_inset.set_label('$\delta T$ ($\degree C$)',color='black')

R_ax.indicate_inset_zoom(LR_inset,lw=3,ls='dashed',edgecolor='black',alpha=1)

############################### Plot Export ######################################

plt.tight_layout()
plt.savefig(write_directory+"FigMS.png",bbox_inches='tight')
plt.show()