import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from project1.bezier import BezierSubdivision
from project3.bspline import curve_interp, EndCondition, deboor_to_bspline
from project4.shape import torus, flatten_grid, restore_grid
from project4.sim3 import R7_exp_SIM3, SIM3_transform_points

t = np.array([0, 0.16, 0.25, 0.5, 0.5, 0, 1.5]) * np.pi
w = np.array([[0, 0, 0],
              [1, 0, 0],
              [0, 0.5, 0.5],
              [0, 0, 1],
              [1, 0, 0],
              [1, 0, 0],
              [1, 1, 1]])
u = np.array([[0, 0, 0],
              [2, 1, 1],
              [2, 2, 1],
              [3, 3, 1],
              [3, 3, 1],
              [3, 0, 1],
              [0, 1, 0]])
s = np.array([0.25, 1, 2, 0.5, 1, 3, 1])

wt = (w.T * t).T
s = np.atleast_2d(s).T

bezier = BezierSubdivision(divide=2)
sims = np.hstack((s, w, u))
D = curve_interp(sims, EndCondition.natural)
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
