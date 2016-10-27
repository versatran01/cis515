import os
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from scipy.misc import imresize

from project2.haar_2d import haar2d, haar_inv2d

data_dir = os.path.abspath('../data')
image_file = os.path.join(data_dir, 'durer.png')

image = ndi.imread(image_file)
image = imresize(image, size=(512, 512))
image = np.array(image, float)

# image = image[:512]
# pad = np.ones((512, 3)) * 50
# image = np.concatenate((image, pad), axis=1)

fig, axarr = plt.subplots(2, 2)
fig.set_facecolor('w')
axarr = np.ravel(axarr)

image_haar = haar2d(image)
image_recon = haar_inv2d(image_haar)
image_diff = image - image_recon
axarr[0].imshow(image, cmap=plt.cm.gray)
axarr[0].set_title('durer original')
axarr[1].imshow(image_haar, cmap=plt.cm.viridis)
axarr[1].set_title('durer haar')
axarr[2].imshow(image_recon, cmap=plt.cm.gray)
axarr[2].set_title('durer reconstructed')
axarr[3].imshow(image_diff, cmap=plt.cm.viridis)
axarr[3].set_title('difference orig. and recon.')
for ax in axarr:
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_xticklabels(), visible=False)
plt.show()
