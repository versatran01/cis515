import matplotlib.pyplot as plt
import numpy as np
import os
from project2.haar import haar_step
from project2.scripts.plot_plf import plot_plf

data_dir = os.path.abspath('../data')
handel_file = os.path.join(data_dir, 'handel.csv')
u = np.loadtxt(handel_file)
n = int(np.log2(len(u)))
u = u[:2 ** n]

nk = 4
ks = range(nk)
fig, axarr = plt.subplots(nk, 1, sharex=True, sharey=True)
fig.set_facecolor('w')

for i, ax in enumerate(axarr):
    k = ks[i]
    c = haar_step(u, k)
    plot_plf(ax, c)
    ax.grid(True)
    ax.set_ylabel('k = ' + str(k))
    plt.setp(ax.get_yticklabels(), visible=False)

fig.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
plt.show()
