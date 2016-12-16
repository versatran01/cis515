import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from project1.bezier import BezierSubdivision
from project3.bspline import curve_interp, EndCondition, deboor_to_bspline
from project4.shape import torus, flatten_grid, restore_grid
from project4.sim3 import (R7_exp_SIM3, SIM3_transform_points, SIM3_from_sRt,
                           SIM3_log_R7)
from project4.so3 import R3_exp_SO3

T = np.array([0, 0.16, 0.25, 0.5, 0.5, 0, 1.5]) * np.pi
W = np.array([[0, 0, 0],
              [1, 0, 0],
              [0, 0.5, 0.5],
              [0, 0, 1],
              [1, 0, 0],
              [1, 0, 0],
              [1, 1, 1]])
U = np.array([[0, 0, 0],
              [2, 1, 1],
              [2, 2, 1],
              [3, 3, 1],
              [3, 3, 1],
              [3, 0, 1],
              [0, 1, 0]])
S = np.array([0.25, 1, 2, 0.5, 1, 3, 1])

sim3s = []
for t, w, u, s in zip(T, W, U, S):
    R = R3_exp_SO3(w * t)
    SIM3 = SIM3_from_sRt(s, R, u)
    sim3s.append(SIM3_log_R7(SIM3))

bezier = BezierSubdivision(divide=2)
D = curve_interp(sim3s, EndCondition.natural)
B = deboor_to_bspline(D, bezier)
n = len(B)

X, Y, Z = torus(0.2, 0.02)
shape = flatten_grid(X, Y, Z)

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, projection='3d')

cmi = np.array(np.linspace(0, 255, n), int)
for sim3, c in zip(B, cmi):
    SIM3 = R7_exp_SIM3(sim3)
    data_transformed = SIM3_transform_points(SIM3, shape.data)
    Xs, Ys, Zs = restore_grid(data_transformed, shape.size)
    ax.plot_wireframe(Xs, Ys, Zs, rstride=10, cstride=10, color=plt.cm.jet(c))

plt.show()
