'''
Created on Sep 17, 2019

@author: sean
'''

from Devices.Trius_SX674_Camera import *


def fourierFilter(image,step,period):
    im_fft=fftpack.fft2(image)

#     plt.figure()
#     plt.imshow(image)

    N=len(image[0,:])
    print("N Samples per side: "+str(N))

    keep_fraction = period

    im_fft2 = im_fft.copy()
    r, c = im_fft2.shape

    fft=2.0/N*np.abs(im_fft2[0][0:N//2])

    im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0    

#     plt.figure()
#     plt.imshow(np.abs(im_fft2)[0:10,0:10])

    im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
    
    fft_filter=2.0/N*np.abs(im_fft2[0][0:N//2])

    image=pd.DataFrame(fftpack.ifft2(im_fft2).real)
    
#     plt.figure()
#     plt.imshow(image)   
    
    freq=np.linspace(0.0,1.0/(2.0*step),N//2)
    
    print(freq)
    plt.figure()
    plt.loglog(freq,fft,'r+')
    plt.loglog(freq,fft_filter,'b+')
    return image

image_input=pd.read_csv('<save directory>/<filename>.csv'\
                        ,header=None)\
                        .drop([0],axis=0).drop([0],axis=1).to_numpy()

stepsize=5.0

fourier=np.abs(fourierFilter(image_input,stepsize,.1)).to_numpy()

pd.DataFrame(fourier).to_csv('<save directory>/<filename>_Filtered.csv',index=False)

# fig, ax1=plt.subplots(figsize=(10,8),ncols=1)
#  
# ax1.tick_params(axis='x',labelsize=18)
# ax1.tick_params(axis='y',labelsize=18)
# ax1.set_xlabel('$\delta x (\mu m)$',fontsize=18)
# ax1.set_ylabel('$\delta y (\mu m)$',fontsize=18)
# heatmap=ax1.imshow(fourier,cmap='inferno',extent=[0,len(fourier[0,:])*stepsize,0,len(fourier[:,0])*stepsize])
# cbar=fig.colorbar(heatmap,ax=ax1)
# cbar.ax.tick_params(labelsize=18)
# 
# cbar.set_label('$\Delta T (K)$',size=18)
# 
# plt.show()
