'''
Created on Aug 20, 2019

@author: sean
'''
from Devices.Max10_Counting_Board import *
import numpy as np
import time
from conda.base.context import channel_alias_validation

filename='/home/sean/Desktop/test'

channel_counts={'n0':192,'n1':193,'n2':196,'n3':208,\
                'n12':197,'n23':212,'n13':209,'n123':213}

start_time=time.time()
channels=['n2','n3','n23']

with open('/home/sean/Desktop/test','rb') as f:
    data=np.frombuffer(f.read(),dtype=np.uint8)

    coincidence=np.count_nonzero(data==channel_counts[channels[2]])
    channel_b=np.count_nonzero(data==channel_counts[channels[0]])+coincidence
    channel_a=np.count_nonzero(data==channel_counts[channels[1]])+coincidence

    g2=len(data)*coincidence/(channel_a*channel_b)

    end_time=time.time()

    print(len(data))

    print('Channel A: '+str(channel_a))
    print('Channel B: '+str(channel_b))
    print('Coincidence: '+str(coincidence))
    print('G2: '+str(g2))
    print()
    print("Execution Time: "+str(end_time-start_time))
