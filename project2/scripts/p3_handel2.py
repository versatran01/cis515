import matplotlib.pyplot as plt
import numpy as np
import os
from project2.haar import haar, haar_inv
from project2.scripts.plot_plf import plot_plf

data_dir = os.path.abspath('../data')
handel_file = os.path.join(data_dir, 'handel.csv')
u = np.loadtxt(handel_file)
n = int(np.log2(len(u)))
u = u[:2 ** n]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True)
fig.set_facecolor('w')

c = haar(u)
m = 2 ** (n - 1)
c[m:] = 0
u1 = haar_inv(c)

plot_plf(ax1, u)
plot_plf(ax2, u1)
plot_plf(ax3, u - u1)
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax1.set_ylabel('original')
ax2.set_ylabel('reconstructed')
ax3.set_ylabel('difference')
plt.setp(ax1.get_yticklabels(), visible=False)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)

fig.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
plt.show()
