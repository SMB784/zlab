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
write_directory=str(os.getcwd())+'/Manuscript_Files/'

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

grid=plt.GridSpec(3,2)

fig,ax=plt.subplots(figsize=(12,16))

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
############################## Upper Left Plot ##################################
#################################################################################

UL_ax=fig.add_subplot(grid[0,0])

# adds dummy value 0 to end of data @ delta z=500
# to make tick labels line up right
z_temp=np.flip(np.append(np.flip(z_temp,axis=0),[[500.0,0.0,0.0]],axis=0),axis=0)

UL_ax.set_xlabel('$\delta z (\mu m)$')
UL_ax.set_ylabel('$T (\degree C)$')
UL_ax.set_xlim(-25,500)
UL_ax.xaxis.set_ticks([0,100,200,300,400,500])
UL_ax.set_xticklabels(['0','100','200','300','400','500'])
UL_ax.set_ylim(34.25,46.5)
UL_ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(3))

heatmap=UL_ax.scatter(z_temp[:,0],z_temp[:,1],c=z_temp[:,1],cmap='inferno',norm=norm,s=markersize,zorder=2)

error_norm = mpl.colors.Normalize(vmin=40, vmax=50)
error_mapper=mpl.cm.ScalarMappable(norm=error_norm,cmap='inferno')
error_color=np.array([error_mapper.to_rgba(v) for v in z_temp[:,1]])

for i in range(0,len(z_temp[:,1])):
    UL_ax.errorbar(z_temp[i,0],z_temp[i,1],z_temp[i,2],capsize=5,markeredgewidth=3,lw=3,linestyle="None",color=error_color[i],zorder=1)

cax = UL_ax.inset_axes([0.65,0.666,0.05,0.233]) 
cbar_inset=fig.colorbar(heatmap,cax=cax, orientation='vertical')
cbar=fig.colorbar(heatmap,ax=UL_ax,cax=cax)
cbar.set_label('$T (\degree C)$')

UL_inset=UL_ax.inset_axes([0.0,0.0,0.333,0.333])
UL_inset.imshow(wire_image,extent=[0,100,0,100],aspect='auto')
UL_inset.xaxis.set_ticks_position('top')
UL_inset.yaxis.set_ticks_position('right')
UL_inset.xaxis.set_label_position('top')
UL_inset.yaxis.set_label_position('right')
UL_inset.xaxis.set_ticks([25,75])
UL_inset.yaxis.set_ticks([25,75])
UL_inset.set_xlabel('$d_x (\mu m)$')
UL_inset.set_ylabel('$d_y (\mu m)$')

x_trace = patches.Rectangle((25,0),0,100,lw=4,ls='dotted',edgecolor='yellow',facecolor='none',zorder=20)
y_trace = patches.Rectangle((0,25),100,0,lw=4,ls='dotted',edgecolor='yellow',facecolor='none',zorder=20)
UL_inset.add_patch(x_trace)
UL_inset.add_patch(y_trace)

UL_ax.annotate('(a)',xy=(0.01,0.90),xycoords='axes fraction')
# UL_ax.annotate('(b)',xy=(0.04,0.655),xycoords='axes fraction')
# UL_ax.annotate('(c)',xy=(0.0775,0.595),xycoords='axes fraction')
# UL_ax.annotate('(d)',xy=(0.115,0.535),xycoords='axes fraction')

#################################################################################
############################## Upper Right Plot #################################
#################################################################################

UR_ax=fig.add_subplot(grid[0,1])

UR_ax.tick_params(axis='x')
UR_ax.tick_params(axis='y')
UR_ax.set_xlabel('$\delta x (\mu m)$')
UR_ax.xaxis.set_ticks([0,100,200,300,400,495])
UR_ax.set_xticklabels(['0','100','200','300','400','500'])
UR_ax.set_ylabel('$\delta y (\mu m)$')

heatmap=UR_ax.imshow(avg_temp_10700,cmap='inferno',norm=norm,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')

norm_inset=mpl.colors.Normalize(48.75,50.75)
UR_inset=UR_ax.inset_axes([0.0,0.0,0.333,0.333])
UR_inset.imshow(avg_temp_10700,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')
UR_inset.set_xlim(300,400)
UR_inset.set_ylim(175,275)
UR_inset.xaxis.set_ticks_position('top')
UR_inset.yaxis.set_ticks_position('right')
UR_inset.xaxis.set_ticks([325,375])
UR_inset.yaxis.set_ticks([200,250])
UR_inset.set_xticklabels(['25','75'])
UR_inset.set_yticklabels(['25','75'])
UR_inset.tick_params(axis='x', colors='black')
UR_inset.tick_params(axis='y', colors='black')

subheatmap=UR_inset.imshow(avg_temp_10700,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10700[0,:])*stepsize,0,len(avg_temp_10700[:,0])*stepsize],aspect='auto')
cbar_inset_ax = UR_ax.inset_axes([0.50,0.05,0.05,0.233]) 
cbar_inset=fig.colorbar(subheatmap,cax=cbar_inset_ax, orientation='vertical')
cbar_inset.set_ticks([48.75,49.75,50.75])
cbar_inset.ax.set_yticklabels(['0', '1', '2'])
cbar_inset.ax.tick_params(colors='black')
cbar_inset.set_label('$\delta T (\degree C)$',color='black')

UR_ax.indicate_inset_zoom(UR_inset,lw=3,ls='dashed',edgecolor='black',alpha=1)

line = patches.Rectangle((475,0),0,500,lw=3,edgecolor='black',facecolor='none',ls='dotted')
UR_ax.add_patch(line)

UR_ax.annotate('(b)',xy=(0.01,0.90),xycoords='axes fraction',color='white')

#################################################################################
############################# Middle Left Plot ##################################
#################################################################################

ML_ax=fig.add_subplot(grid[1,0])

ML_ax.tick_params(axis='x')
ML_ax.tick_params(axis='y')
ML_ax.set_xlabel('$\delta x (\mu m)$')
ML_ax.set_ylabel('$\delta y (\mu m)$')

heatmap=ML_ax.imshow(avg_temp_10500,cmap='inferno',norm=norm,extent=[0,len(avg_temp_10500[0,:])*stepsize,0,len(avg_temp_10500[:,0])*stepsize],aspect='auto')

norm_inset=mpl.colors.Normalize(45.5,47.5) # 44 48
ML_inset=ML_ax.inset_axes([0.0,0.0,0.333,0.333])
ML_inset.imshow(avg_temp_10500,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10500[0,:])*stepsize,0,len(avg_temp_10500[:,0])*stepsize],aspect='auto')
ML_inset.set_xlim(290,390)
ML_inset.set_ylim(345,445)
ML_inset.xaxis.set_ticks_position('top')
ML_inset.yaxis.set_ticks_position('right')
ML_inset.xaxis.set_ticks([325,375])
ML_inset.yaxis.set_ticks([375,425])
ML_inset.set_xticklabels(['25','75'])
ML_inset.set_yticklabels(['25','75'])
ML_inset.tick_params(axis='x', colors='white')
ML_inset.tick_params(axis='y', colors='white')

ML_ax.indicate_inset_zoom(ML_inset,lw=3,ls='dashed',edgecolor='white',alpha=1)

ML_ax.annotate('(c)',xy=(0.01,0.90),xycoords='axes fraction',color='white')

#################################################################################
############################# Middle Right Plot #################################
#################################################################################

MR_ax=fig.add_subplot(grid[1,1])

MR_ax.tick_params(axis='x')
MR_ax.tick_params(axis='y')
MR_ax.set_xlabel('$\delta x (\mu m)$')
MR_ax.xaxis.set_ticks([0,100,200,300,400,495])
MR_ax.set_xticklabels(['0','100','200','300','400','500'])
MR_ax.set_ylabel('$\delta y (\mu m)$')

heatmap=MR_ax.imshow(avg_temp_10300,cmap='inferno',norm=norm,extent=[0,len(avg_temp_10300[0,:])*stepsize,0,len(avg_temp_10300[:,0])*stepsize],aspect='auto')

norm_inset=mpl.colors.Normalize(43,45)
norm_inset_cbar=mpl.colors.Normalize(0,2)
MR_inset=MR_ax.inset_axes([0.0,0.0,0.333,0.333])
MR_inset.imshow(avg_temp_10300,cmap='gray',norm=norm_inset,extent=[0,len(avg_temp_10300[0,:])*stepsize,0,len(avg_temp_10300[:,0])*stepsize],aspect='auto')
MR_inset.set_xlim(245,345)
MR_inset.set_ylim(345,445)
MR_inset.xaxis.set_ticks_position('top')
MR_inset.yaxis.set_ticks_position('right')
MR_inset.xaxis.set_ticks([275,325])
MR_inset.yaxis.set_ticks([375,425])
MR_inset.set_xticklabels(['25','75'])
MR_inset.set_yticklabels(['25','75'])
MR_inset.tick_params(axis='x', colors='white')
MR_inset.tick_params(axis='y', colors='white')

MR_ax.indicate_inset_zoom(MR_inset,lw=3,ls='dashed',edgecolor='white',alpha=1)

MR_ax.annotate('(d)',xy=(0.01,0.90),xycoords='axes fraction',color='white')

#################################################################################
############################## Lower Left Plot ##################################
#################################################################################

subgrid=mpl.gridspec.GridSpecFromSubplotSpec(3,1,subplot_spec=grid[4],hspace=0.1)

# x trace: y,x=60,78:98 and y trace: y,x=45:65,85
avg_temp_10300_window=np.arange(0,50,5)
avg_temp_10300_window=np.transpose(np.c_[avg_temp_10300_window,avg_temp_10300[73,56:66],avg_temp_10300[72:82,52]]) # x,y trace
# x trace: y,x=80,79:99 and y trace: y,x=75:95,85
avg_temp_10500_window=(np.arange(0,50,5))
avg_temp_10500_window=np.transpose(np.c_[avg_temp_10500_window,avg_temp_10500[73,64:74],avg_temp_10500[73:83,64]]) # x,y trace
# x trace: y,x= , :  and y trace: y,x= : , 
avg_temp_10700_window=(np.arange(0,50,5))
avg_temp_10700_window=np.transpose(np.c_[avg_temp_10700_window,avg_temp_10700[38,69:79],avg_temp_10700[37:47,94]]) # x,y trace

LL_ax1=fig.add_subplot(subgrid[2,0])
LL_ax1.plot(avg_temp_10300_window[0],avg_temp_10300_window[1],color='b',lw=3)
LL_ax1.plot(avg_temp_10300_window[0],avg_temp_10300_window[2],color='b',ls='dashed',lw=3)
LL_ax1.set_xlabel('$d_{x,y} (\mu m)$')
LL_ax1.set_ylabel('')
LL_ax1.set_ylim(42.4,42.8)

LL_ax2=fig.add_subplot(subgrid[1,0])
LL_ax2.plot(avg_temp_10500_window[0],avg_temp_10500_window[1],color='g',lw=3)
LL_ax2.plot(avg_temp_10500_window[0],avg_temp_10500_window[2],color='g',ls='dashed',lw=3)
LL_ax2.set_xlabel('')
LL_ax2.set_xticks([])
LL_ax2.set_ylabel('$T (\degree C)$')
LL_ax2.set_ylim(45.4,45.9)

LL_ax3=fig.add_subplot(subgrid[0,0])
LL_ax3.plot(avg_temp_10700_window[0],avg_temp_10700_window[1],color='r',lw=3)
LL_ax3.plot(avg_temp_10700_window[0],avg_temp_10700_window[2],color='r',ls='dashed',lw=3)
LL_ax3.set_xlabel('')
LL_ax3.set_xticks([])
LL_ax3.set_ylabel('')
LL_ax3.set_ylim(49.3,50.3)


# LL_ax.set_yscale('log')

LL_ax3.annotate('(e)',xy=(0.01,0.70),xycoords='axes fraction')

#################################################################################
############################## Lower Right Plot #################################
#################################################################################

LR_ax1=fig.add_subplot(grid[2,1])
LR_ax2 = LR_ax1.twiny()

avg_temp_10700_trace=np.arange(0,len(avg_temp_10700[:,95])*5,5)/52
avg_temp_10700_trace=np.transpose(np.c_[avg_temp_10700_trace,avg_temp_10700[:,95]])

riemann_array=[[0],[0]]
for i in range(0,10):
    riemann_array[0].append(i+1)
    riemann_array[1].append(np.mean(avg_temp_10700_trace[1,7+10*i:7+10*i+10]))
riemann_array=np.asarray(riemann_array)

LR_ax1.plot(avg_temp_10700_trace[0],avg_temp_10700_trace[1],color='purple',lw=3,zorder=10)
LR_ax1.bar(riemann_array[0],riemann_array[1],color='orange',align='center')

LR_ax1.set_xlabel('Wire Number')
LR_ax1.set_ylabel('$T (\degree C)$')
LR_ax1.set_ylim(46,51)
LR_ax1.set_xlim(0.5,9.5)
LR_ax1.set_xticks(np.arange(1,10,2))

LR_ax2.set_xlabel('$\delta y (\mu m)$',labelpad=10)
LR_ax2.set_xticks(np.arange(0,600,100)) #600 cuz drops last entry
LR_ax2.set_xticklabels(np.arange(0,600,100))

LR_ax1.annotate('(f)',xy=(0.01,0.90),xycoords='axes fraction')

############################### Plot Export ######################################

plt.tight_layout()
plt.savefig(write_directory+"Fig3.png",bbox_inches='tight')
plt.show()
