import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from project4.shape import torus

x, y, z = torus(2, 1, 100)

fig = plt.figure()
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_zlim(-3, 3)
ax1.plot_surface(x, y, z, rstride=10, cstride=10, color='k', edgecolors='w')
ax1.view_init(36, 26)
ax1.set_aspect('equal')
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_zlim(-3, 3)
ax2.plot_surface(x, y, z, rstride=5, cstride=5, color='k', edgecolors='w')
ax2.view_init(0, 0)
ax2.set_xticks([])
ax2.set_aspect('equal')
plt.show()
