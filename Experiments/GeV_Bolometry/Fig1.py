'''
Created on Feb 21, 2020

@author: sean
'''
from Experiments.GeV_Bolometry import *

################################# Data Import #################################
data_1=mpl.image.imread(str(Path(data_root_directory/'1.png')))
################################## Plot Setup #################################

fontsize=24
plt.rcParams.update({'font.size':fontsize})

fig,ax=plt.subplots(figsize=(12,6))

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

###############################################################################
############################### Center Plot ###################################
###############################################################################

C_ax=fig.add_subplot()

C_ax.xaxis.set_visible(False)
C_ax.yaxis.set_visible(False)
C_ax.spines['left'].set_visible(False)
C_ax.spines['right'].set_visible(False)
C_ax.spines['top'].set_visible(False)
C_ax.spines['bottom'].set_visible(False)
C_ax.xaxis.set_ticks([])
C_ax.yaxis.set_ticks([])

C_ax.imshow(data_1,aspect='auto')

C_ax.annotate('(a)',xy=(0.01,0.9),xycoords='axes fraction')
C_ax.annotate('(b)',xy=(0.4425,0.9),xycoords='axes fraction',c='white')

############################### Plot Export ###################################
plt.tight_layout()
plt.savefig(Path(write_directory/'Fig1.png'),bbox_inches='tight',dpi=480)
plt.show()