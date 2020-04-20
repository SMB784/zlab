'''
Created on Feb 11, 2020

@author: sean
'''
from Experiments.GeV_Bolometry import *

################################# Data Import #################################
data_3_a=mpl.image.imread(str(Path(data_root_directory/'3a.png')))
data_3_b=np.transpose(pd.read_csv(Path(data_root_directory/'3d.csv'),header=None).to_numpy())
data_3_c=np.transpose(pd.read_csv(Path(data_root_directory/'3c.csv'),header=None).to_numpy())
data_3_d=np.transpose(pd.read_csv(Path(data_root_directory/'3d.csv'),header=None).to_numpy())
################################## Plot Setup #################################

fontsize=24
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(2,2)

fig,ax=plt.subplots(figsize=(12,10))

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

UL_ax.xaxis.set_visible(False)
UL_ax.yaxis.set_visible(False)
UL_ax.spines['left'].set_visible(False)
UL_ax.spines['right'].set_visible(False)
UL_ax.spines['top'].set_visible(False)
UL_ax.spines['bottom'].set_visible(False)
UL_ax.xaxis.set_ticks([])
UL_ax.yaxis.set_ticks([])

UL_ax.imshow(data_3_a,aspect='auto')

UL_ax.annotate('(a)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

###############################################################################
############################# Upper Right Plot ################################
###############################################################################

def bivariate_gaussian(x_input,y_input):
    sigma_x=166.4544
    sigma_y=209.2569
    mean_x=1374.1
    mean_y=843.0
    A=10000
    
    biv_gauss=A/(2*np.pi*mean_x*mean_y)*np.exp(-0.5*(((x_input-mean_x)/sigma_x)**2+((y_input-mean_y)/sigma_y)**2))
    
    return biv_gauss

UR_ax=fig.add_subplot(grid[0,1])

x=np.linspace(900,1800,900,dtype=float)
y=np.linspace(500,1100,600,dtype=float)

x_temp=np.rint(data_3_c[1,:])
y_temp=np.rint(data_3_c[0,:])

X,Y=np.meshgrid(x,y)

Z=bivariate_gaussian(X,Y)

x=np.rint(data_3_d[1,:])
y=np.rint(data_3_d[0,:])
z=data_3_d[2,:]

powermap=UR_ax.imshow(Z,origin='lower',clim=(np.max(Z)*0.8,np.max(Z)),extent=[900,1800,500,1100],aspect='auto')
UR_ax.scatter(x_temp[0:len(x_temp)-4],y_temp[0:len(y_temp)-4],c='red',marker=(5,2),s=125,lw=3)
UR_ax.set_xlim(900,1800)
UR_ax.set_ylim(1100,500)
UR_ax.xaxis.set_ticks([900,1200,1500,1800])
UR_ax.yaxis.set_ticks([1100,900,700,500])
UR_ax.yaxis.set_ticklabels(['500','700','900','1100'])
UR_ax.set_xlabel('X Pixels')
UR_ax.set_ylabel('Y Pixels')

cax = UR_ax.inset_axes([0.025,0.1,0.05,0.233]) 
cbar=fig.colorbar(powermap,ax=UR_ax,cax=cax)
cbar.set_label('$P_{L} (\mu W)$',c='white')
cbar.ax.set_yticklabels(['<1.0','1.2','1.4'],c='white')

UR_ax.annotate('(b)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

###############################################################################
############################# Lower Right Plot ################################
###############################################################################

LL_ax=fig.add_subplot(grid[1,0])

z_temp=data_3_c[4,:]

X_temp,Y_temp=np.linspace(x_temp.min(), x_temp.max(), 900), np.linspace(y_temp.min(), y_temp.max(), 600)
X_temp,Y_temp=np.meshgrid(X_temp,Y_temp)
Z_temp=np.nan_to_num(interpolate.griddata((x_temp,y_temp),z_temp,(X_temp,Y_temp),method='linear'),nan=1.0)

trelmap=LL_ax.imshow(Z_temp,vmin=25,vmax=100,cmap='inferno',extent=[900,1800,500,1100],aspect='auto')
LL_ax.scatter(x_temp[0:len(x_temp)-4],y_temp[0:len(y_temp)-4],c='red',marker=(5,2),s=125,lw=3)
LL_ax.set_ylim(1100,500)
LL_ax.set_xlim(900,1800)
LL_ax.xaxis.set_ticks([900,1200,1500,1800])
LL_ax.yaxis.set_ticks([1100,900,700,500])
LL_ax.yaxis.set_ticklabels(['500','700','900','1100'])
LL_ax.set_xlabel('X Pixels')
LL_ax.set_ylabel('Y Pixels')

cax = LL_ax.inset_axes([0.025,0.1,0.05,0.233]) 
cbar_heat=fig.colorbar(trelmap,ax=LL_ax,cax=cax)
cbar_heat.set_label('$\delta T (\degree C)$',c='white')
cbar_heat.ax.set_yticklabels([25,100],c='white')

LL_ax.annotate('(c)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')


###############################################################################
############################# Lower Right Plot ################################
###############################################################################

LR_ax=fig.add_subplot(grid[1,1])

x=np.rint(data_3_d[1,:])
y=np.rint(data_3_d[0,:])
z=data_3_d[2,:]/100

X,Y=np.linspace(x.min(), x.max(), 900), np.linspace(y.min(), y.max(), 600)
X,Y=np.meshgrid(X,Y)
Z=np.nan_to_num(interpolate.griddata((x,y),z,(X,Y),method='cubic'),nan=1.0)

pabsmap=LR_ax.imshow(Z,vmin=0.2*z.max(),vmax=z.max(),extent=[900,1800,500,1100],aspect='auto')
LR_ax.scatter(x[0:len(x)-4],y[0:len(y)-4],c='red',marker=(5,2),s=125,lw=3)
LR_ax.set_ylim(1100,500)
LR_ax.set_xlim(900,1800)
LR_ax.xaxis.set_ticks([900,1200,1500,1800])
LR_ax.yaxis.set_ticks([1100,900,700,500])
LR_ax.yaxis.set_ticklabels(['500','700','900','1100'])
LR_ax.set_xlabel('X Pixels')
LR_ax.set_ylabel('Y Pixels')

cax = LR_ax.inset_axes([0.025,0.1,0.05,0.233]) 
cbar_power=fig.colorbar(pabsmap,ax=LR_ax,cax=cax)
cbar_power.set_label('$P_{abs} (nW)$',c='white')
cbar_power.ax.set_yticklabels(['25','50','75'],c='white')

LR_ax.annotate('(d)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

############################### Plot Export ###################################
plt.tight_layout()
plt.savefig(Path(write_directory/'Fig3.png'),bbox_inches='tight')
plt.show()