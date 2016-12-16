import numpy as np
import matplotlib.pyplot as plt
from project4.interp_sim import interp_sim3
from mpl_toolkits.mplot3d import Axes3D
from project4.shape import torus, flatten_grid, restore_grid
from project4.sim3 import R7_exp_SIM3, SIM3_transform_points

x, y, z = torus(2, 1, 100)

n = 10

t1 = 0.0
t2 = np.pi / 2
w1 = np.zeros(3)
w2 = np.ones(3)
u1 = np.zeros(3)
u2 = np.ones(3) * 3
s1 = 0.5
s2 = 1.0

sim1 = np.hstack((s1, w1 * t1, u1))
sim2 = np.hstack((s2, w2 * t2, u2))

sims = interp_sim3(sim1, sim2, n=n)

X, Y, Z = torus(0.5, 0.1)
shape = flatten_grid(X, Y, Z)

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, projection='3d')

for sim3 in sims.T:
    SIM3 = R7_exp_SIM3(sim3)
    data_transformed = SIM3_transform_points(SIM3, shape.data)
    Xs, Ys, Zs = restore_grid(data_transformed, shape.size)
    ax.plot_wireframe(Xs, Ys, Zs, rstride=5, cstride=5)

plt.show()
