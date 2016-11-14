import matplotlib.pyplot as plt
import numpy as np
from haar import haar_step
from scripts.plot_plf import plot_plf

u = np.array([0, 2, 4, 6, 6, 4, 2, 1, -1, -2, -4, -6, -6, -4, -2, 0])
w = np.tile(u, 8)
ks = range(8)

fig, axarr = plt.subplots(len(ks), 1, sharex=True, sharey=True)
fig.set_facecolor('white')
axarr = np.ravel(axarr)

for i, ax in enumerate(axarr):
    k = ks[i]
    c = haar_step(w, k)
    plot_plf(ax, c)
    ax.grid(True)
    ax.margins(x=0.02, y=0.1)
    ax.set_ylabel('k = ' + str(k))
    plt.setp(ax.get_yticklabels(), visible=False)

fig.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

plt.show()
