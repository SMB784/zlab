'''
Created on Feb 11, 2020

@author: sean
'''
from Experiments.GeV_Bolometry import *

################################# Data Import #################################
data_3_a=mpl.image.imread(str(Path(data_root_directory/'3a.png')))
data_3_b=np.transpose(pd.read_csv(Path(data_root_directory/'3c.csv'),header=None).to_numpy())
data_3_c=np.transpose(pd.read_csv(Path(data_root_directory/'3c.csv'),header=None).to_numpy())
################################## Plot Setup #################################

fontsize=24
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(1,3)

fig,ax=plt.subplots(figsize=(18,6))

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

###############################################################################
################################# Left Plot ###################################
###############################################################################

L_ax=fig.add_subplot(grid[0,0])

L_ax.xaxis.set_visible(False)
L_ax.yaxis.set_visible(False)
L_ax.spines['left'].set_visible(False)
L_ax.spines['right'].set_visible(False)
L_ax.spines['top'].set_visible(False)
L_ax.spines['bottom'].set_visible(False)
L_ax.xaxis.set_ticks([])
L_ax.yaxis.set_ticks([])

L_ax.imshow(data_3_a,aspect='auto')

L_ax.annotate('(a)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

###############################################################################
################################ Middle Plot ##################################
###############################################################################

def bivariate_gaussian(x_input,y_input):
    sigma_x=166.4544
    sigma_y=209.2569
    mean_x=1374.1
    mean_y=843.0
    A=10000
    
    biv_gauss=A/(2*np.pi*mean_x*mean_y)*np.exp(-0.5*(((x_input-mean_x)/sigma_x)**2+((y_input-mean_y)/sigma_y)**2))
    
    return biv_gauss

M_ax=fig.add_subplot(grid[0,1])

x=np.linspace(900,1800,900,dtype=float)
y=np.linspace(500,1100,600,dtype=float)

X,Y=np.meshgrid(x,y)

Z=bivariate_gaussian(X,Y)

x=np.rint(data_3_c[1,:])
y=np.rint(data_3_c[0,:])
z=data_3_c[2,:]

powermap=M_ax.imshow(Z,origin='lower',clim=(np.max(Z)*0.8,np.max(Z)),extent=[900,1800,500,1100],aspect='auto')
M_ax.set_xlim(900,1800)
M_ax.set_ylim(1100,500)
M_ax.xaxis.set_ticks([900,1200,1500,1800])
M_ax.yaxis.set_ticks([1100,900,700,500])
M_ax.yaxis.set_ticklabels(['500','700','900','1100'])
M_ax.set_xlabel('X Pixels')
M_ax.set_ylabel('Y Pixels')

cax = M_ax.inset_axes([0.025,0.05,0.05,0.233]) 
cbar=fig.colorbar(powermap,ax=M_ax,cax=cax)
cbar.set_label('$P_{L} (\mu W)$',c='white')
cbar.ax.set_yticklabels(['1.1','1.2','1.3'],c='white')

M_ax.annotate('(b)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

###############################################################################
################################ Right Plot ###################################
###############################################################################

R_ax=fig.add_subplot(grid[0,2])

x=np.rint(data_3_c[1,:])
y=np.rint(data_3_c[0,:])
z=data_3_c[2,:]/100

X,Y=np.linspace(x.min(), x.max(), 900), np.linspace(y.min(), y.max(), 600)
X,Y=np.meshgrid(X,Y)
Z=np.nan_to_num(interpolate.griddata((x,y),z,(X,Y),method='cubic'),nan=1.0)

pabsmap=R_ax.imshow(Z,vmin=z.min(),vmax=z.max(),cmap='inferno',extent=[900,1800,500,1100],aspect='auto')
R_ax.scatter(x[0:len(x)-4],y[0:len(y)-4],c='red',marker=(5,2),s=125,lw=3)
R_ax.set_ylim(1100,500)
R_ax.set_xlim(900,1800)
R_ax.xaxis.set_ticks([900,1200,1500,1800])
R_ax.yaxis.set_ticks([1100,900,700,500])
R_ax.yaxis.set_ticklabels(['500','700','900','1100'])
R_ax.set_xlabel('X Pixels')
R_ax.set_ylabel('Y Pixels')

cax = R_ax.inset_axes([0.025,0.05,0.05,0.233]) 
cbar=fig.colorbar(pabsmap,ax=R_ax,cax=cax)
cbar.set_label('$P_{abs} (nW)$',c='white')
cbar.ax.set_yticklabels(['75','50','25'],c='white')

R_ax.annotate('(c)',xy=(0.0125,0.9125),xycoords='axes fraction',c='white')

############################### Plot Export ###################################
plt.tight_layout()
plt.savefig(Path(write_directory/'Fig3.png'),bbox_inches='tight')
plt.show()