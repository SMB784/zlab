'''
Created on Feb 11, 2020

@author: sean
'''
from Experiments.GeV_Bolometry import *

################################# Data Import #################################

################################## Plot Setup #################################

fontsize=24
plt.rcParams.update({'font.size':fontsize})

grid=plt.GridSpec(2,2)

fig,ax=plt.subplots(figsize=(12,8))

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



###############################################################################
############################## Upper Right Plot ###############################
###############################################################################

UR_ax=fig.add_subplot(grid[0,1])



###############################################################################
############################## Lower Left Plot ################################
###############################################################################

LL_ax0=fig.add_subplot(grid[1,0])



###############################################################################
############################## Lower Right Plot ###############################
###############################################################################

LR_ax=fig.add_subplot(grid[1,1])



############################### Plot Export ###################################
plt.tight_layout()
plt.savefig(Path(write_directory/'Fig3.png'),bbox_inches='tight')
plt.show()