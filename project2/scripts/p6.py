import os
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from scipy.misc import imresize

from haar_2d import haar2d

data_dir = os.path.abspath('../data')
image_file = os.path.join(data_dir, 'durer.png')

image = ndi.imread(image_file)
image = imresize(image, size=(512, 512))
image = np.array(image, float)

ks = range(4)
fig, axarr = plt.subplots(2, 2)
fig.set_facecolor('w')
axarr = np.ravel(axarr)

for i, ax in enumerate(axarr):
    k = ks[i]
    C = haar2d(image, k)
    ax.imshow(C, cmap=plt.cm.viridis)
    ax.set_title('k = ' + str(k))

for ax in axarr:
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_xticklabels(), visible=False)

plt.show()
