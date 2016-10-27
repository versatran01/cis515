import matplotlib.pyplot as plt
import numpy as np
from project2.scripts.plot_plf import plot_plf
from project2.haar import haar

u0 = np.array([31, 29, 23, 17, -6, -8, -2, -4])
u1 = np.array([0, 2, 4, 6, 6, 4, 2, 1, -1, -2, -4, -6, -6, -4, -2, 0])
u = [u0, u1]
w = np.tile(u1, 8)

fig1, axarr = plt.subplots(1, 2)
fig1.set_facecolor('white')
axarr = np.ravel(axarr)
for i, ax in enumerate(axarr):
    c = haar(u[i])
    plot_plf(ax, c)
    ax.grid(True)
    ax.margins(0.1)
    ax.set_xlabel('u = ' + np.array_str(u[i]))
    ax.set_title('c = ' + np.array_str(c))

fig2 = plt.figure(facecolor='white')
ax = fig2.add_subplot(111)
ax.grid(True)
ax.margins(x=0.02, y=0.1)
plot_plf(ax, haar(w))

plt.show()
