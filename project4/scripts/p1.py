import numpy as np
import matplotlib.pyplot as plt
from project4.interp_sim import interp_sim3
from mpl_toolkits.mplot3d import Axes3D
from project4.shape import torus, flatten_grid, restore_grid
from project4.sim3 import (R7_exp_SIM3, SIM3_transform_points, SIM3_from_sRt,
                           SIM3_log_R7)
from project4.so3 import R3_exp_SO3

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

R1 = R3_exp_SO3(w1 * t1)
R2 = R3_exp_SO3(w2 * t2)
SIM3_1 = SIM3_from_sRt(s1, R1, u1)
SIM3_2 = SIM3_from_sRt(s2, R2, u2)
sim3_1 = SIM3_log_R7(SIM3_1)
sim3_2 = SIM3_log_R7(SIM3_2)

sim3s = interp_sim3(sim3_1, sim3_2, n=n)

X, Y, Z = torus(0.5, 0.1)
shape = flatten_grid(X, Y, Z)

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, projection='3d')

cmi = np.array(np.linspace(0, 255, n), int)
for sim3, c in zip(sim3s, cmi):
    SIM3 = R7_exp_SIM3(sim3)
    data_transformed = SIM3_transform_points(SIM3, shape.data)
    Xs, Ys, Zs = restore_grid(data_transformed, shape.size)
    ax.plot_wireframe(Xs, Ys, Zs, rstride=5, cstride=5, color=plt.cm.jet(c))

plt.show()
