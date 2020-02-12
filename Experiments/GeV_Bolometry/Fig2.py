'''
Created on Feb 11, 2020

@author: sean
'''

from Experiments.GeV_Bolometry import *

################################# Data Import #################################
data_2_a=np.transpose(pd.read_csv(Path(data_root_directory/'2a.csv'),dtype=float,skiprows=1,header=None).to_numpy())[:,0:100]
data_2_b=np.transpose(pd.read_csv(Path(data_root_directory/'2b.csv'),dtype=float,skiprows=1,header=None).to_numpy())[:,701:801]
data_2_c=np.transpose(pd.read_csv(Path(data_root_directory/'2c.csv'),dtype=float,skiprows=1,usecols=[0,1,4,5,8,9],header=None).dropna(axis=0,how='any').to_numpy())
data_2_e=np.transpose(pd.read_csv(Path(data_root_directory/'2e.csv'),dtype=float,skiprows=1,nrows=8,header=None).to_numpy())
data_2_f=np.transpose(pd.read_csv(Path(data_root_directory/'2f.csv'),dtype=float,skiprows=1,header=None).to_numpy())
################################## Plot Setup #################################
fontsize=24
markersize=150
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
###############################################################################
############################## Upper Left Plot ################################
###############################################################################

UL_ax=fig.add_subplot(grid[0,0])

UL_ax.plot(data_2_a[0],data_2_a[1],lw=4,c='b',zorder=5)
UL_ax.plot(data_2_a[0],data_2_a[2],lw=4,c='g',zorder=4)
UL_ax.plot(data_2_a[0],data_2_a[3],lw=4,c='r',zorder=3)

UL_ax.set_ylabel('PL Amplitude (a. u.)')
UL_ax.set_xlabel('$\lambda_c$ (nm)')
UL_ax.xaxis.set_ticks([580,600,620,640])
UL_ax.set_xticklabels(['580','600','620','640'])
UL_ax.yaxis.set_ticks([5000,30000,55000])
UL_ax.yaxis.set_major_formatter(EngFormatter())
UL_ax.set_ylim(1,60000)

labels=['21$\degree$C','28$\degree$C','44$\degree$C']
handles=UL_ax.get_legend_handles_labels()
UL_ax.legend(handles,labels=labels,frameon=False,loc='upper right')

UL_ax.annotate('(a)',xy=(0.0125,0.9125),xycoords='axes fraction')

###############################################################################
############################## Upper Right Plot ###############################
###############################################################################

UR_ax=fig.add_subplot(grid[0,1])

UR_ax.plot(data_2_b[0],data_2_b[1],lw=7,c='green',ls='dotted', zorder=6)
UR_ax.plot(data_2_b[0],data_2_b[2],lw=4,c='red',zorder=2)
UR_ax.plot(data_2_b[0],data_2_b[3],lw=4,c='red',ls='dashed',zorder=3)
UR_ax.plot(data_2_b[0],data_2_b[4],lw=4,c='blue',zorder=4)
UR_ax.plot(data_2_b[0],data_2_b[5],lw=4,c='blue',ls='dashed',zorder=5)

UR_ax.set_ylabel('PL Amplitude (a. u.)')
UR_ax.set_xlabel('$\lambda_c$ (nm)')
UR_ax.xaxis.set_ticks([580,600,620,640])
UR_ax.set_xticklabels(['580','600','620','640'])
UR_ax.yaxis.set_ticks([5000,30000,55000])
UR_ax.yaxis.set_major_formatter(EngFormatter())
UR_ax.set_ylim(-2500,70000)

UR_ax.axvline(607,color='black',ls='dashed',lw=5,zorder=10)

UR_ax.annotate('(b)',xy=(0.0125,0.9125),xycoords='axes fraction')

###############################################################################
############################# Middle Left Plot ################################
###############################################################################

ML_ax=fig.add_subplot(grid[1,0])

data_2_c_fit=[(np.polyfit(data_2_c[0],data_2_c[1],deg=1)[1]+data_2_c[0]*np.polyfit(data_2_c[0],data_2_c[1],deg=1)[0]),
              (np.polyfit(data_2_c[2],data_2_c[3],deg=1)[1]+data_2_c[2]*np.polyfit(data_2_c[2],data_2_c[3],deg=1)[0]),
              (np.polyfit(data_2_c[4],data_2_c[5],deg=1)[1]+data_2_c[4]*np.polyfit(data_2_c[4],data_2_c[5],deg=1)[0])]

labels=[str(np.polyfit(data_2_c[0],data_2_c[1],deg=1)[0].astype(int)),
        str(np.polyfit(data_2_c[2],data_2_c[3],deg=1)[0].astype(int)),
        str(np.polyfit(data_2_c[4],data_2_c[5],deg=1)[0].astype(int))]

ML_ax.scatter(data_2_c[0],data_2_c[1],c='red',lw=3,edgecolors='black',s=markersize,zorder=5)
ML_ax.plot(data_2_c[0],data_2_c_fit[0],lw=4,c='red',zorder=4)
ML_ax.scatter(data_2_c[2],data_2_c[3],c='green',lw=3,edgecolors='black',s=markersize,zorder=3)
ML_ax.plot(data_2_c[2],data_2_c_fit[1],lw=4,c='green',zorder=2)
ML_ax.scatter(data_2_c[4],data_2_c[5],c='blue',lw=3,edgecolors='black',s=markersize,zorder=1)
ML_ax.plot(data_2_c[4],data_2_c_fit[2],lw=4,c='blue',zorder=0)

ML_ax.set_ylabel('T ($\degree$C)')
ML_ax.set_xlabel('PL Ratio (a.u.)')
ML_ax.set_xlim(.995,1.075)
ML_ax.xaxis.set_ticks([1.0,1.035,1.07])

handles=ML_ax.get_legend_handles_labels()
ML_ax.legend(handles,labels=labels,frameon=False,title='Slope:',loc='lower right')

ML_ax.annotate('(c)',xy=(0.0125,0.9125),xycoords='axes fraction')

###############################################################################
############################# Middle Right Plot ###############################
###############################################################################

diagram=mpl.image.imread(str(Path(data_root_directory/'2d.png')))

MR_ax=fig.add_subplot(grid[1,1])

MR_ax.xaxis.set_visible(False)
MR_ax.yaxis.set_visible(False)
MR_ax.spines['left'].set_visible(False)
MR_ax.spines['right'].set_visible(False)
MR_ax.spines['top'].set_visible(False)
MR_ax.spines['bottom'].set_visible(False)
MR_ax.xaxis.set_ticks([])
MR_ax.yaxis.set_ticks([])

MR_ax.imshow(diagram,aspect='auto')

MR_ax.annotate('(d)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

###############################################################################
############################## Lower Left Plot ################################
###############################################################################

LL_ax=fig.add_subplot(grid[2,0])

labels=['1','2','3']

LL_ax.scatter(data_2_e[0],data_2_e[2],c='red',lw=3,edgecolors='black',s=markersize,zorder=3)
LL_ax.plot(data_2_e[0],data_2_e[2],lw=4,c='red',zorder=2)
LL_ax.scatter(data_2_e[0],data_2_e[3],c='green',lw=3,edgecolors='black',s=markersize,zorder=1)
LL_ax.plot(data_2_e[0],data_2_e[3],lw=4,c='green',zorder=0)
LL_ax.scatter(data_2_e[0],data_2_e[1],c='blue',lw=3,edgecolors='black',s=markersize,zorder=5)
LL_ax.plot(data_2_e[0],data_2_e[1],lw=4,c='blue',zorder=4)

LL_ax.set_ylabel('PL Ratio (a.u.)')
LL_ax.set_xlabel('T ($\degree$C)')
LL_ax.set_ylim(0.53,0.65)
LL_ax.xaxis.set_ticks([20,30,40])

handles=LL_ax.get_legend_handles_labels()
LL_ax.legend(handles,labels=labels,frameon=False,loc='lower right')

LL_ax.annotate('(e)',xy=(0.0125,0.9125),xycoords='axes fraction')

###############################################################################
############################## Lower Right Plot ###############################
###############################################################################

LR_ax=fig.add_subplot(grid[2,1])

LR_ax.set_ylabel('PL Ratio (a.u.)')
LR_ax.set_xlabel('Frame Number')
LR_ax.plot(data_2_f[0],data_2_f[1],lw=3,c='black')
LR_ax.set_ylim(1.0325,1.0365)
LR_ax.xaxis.set_ticks([0,15,30,45])

LR_ax.annotate('(f)',xy=(0.0125,0.9125),xycoords='axes fraction')

############################### Plot Export ###################################
plt.tight_layout()
plt.savefig(Path(write_directory/'Fig2.png'),bbox_inches='tight')
plt.show()
