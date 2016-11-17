import matplotlib.pyplot as plt
import numpy as np
from project3.bspline_builder import EndCondition
from project3.lu import lu_solve

points_x = [0, 1, 2]
points_y = [0, 2, 0]


def curve_interp(points, end_cond):
    n = len(points)
    N = n - 1

    if N < 4:
        raise NotImplementedError('N < 4')

    if end_cond == EndCondition.natural:
        interp_fun = natural_end_cond
    elif end_cond == EndCondition.quadratic:
        interp_fun = quadratic_end_cond
    elif end_cond == EndCondition.bessel:
        interp_fun = bessel_end_cond
    elif end_cond == EndCondition.knot:
        interp_fun = knot_end_cond
    else:
        raise ValueError("Unsupported end condition")

    return interp_fun(points)


def natural_end_cond(X):
    n = len(X)
    N = n - 1  # number of Bezier curves
    m = N - 1  # size of A

    A = np.diag(np.ones(m) * 4) + np.diag(np.ones(m - 1), 1) + np.diag(
        np.ones(m - 1), -1)


def quadratic_end_cond():
    pass


def bessel_end_cond():
    pass


def knot_end_cond():
    pass


fig, axarr = plt.subplots(2, 2)
fig.set_facecolor('w')

for ax in np.ravel(axarr):
    X = np.vstack((points_x, points_y)).T
    ax.plot(points_x, points_y, 'o-')
    ax.set_aspect('equal')
    ax.grid(True)

plt.show()
