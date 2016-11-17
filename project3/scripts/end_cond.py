import matplotlib.pyplot as plt
import numpy as np
from project3.bspline_builder import EndCondition
from project3.lu import lu_solve_tridiag, tridiag_from_udl


def curve_interp(points, end_cond):
    points = np.atleast_2d(np.array(points))
    assert len(points) >= 4

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


def make_deboor(X, d, d0, dN):
    n, c = np.shape(X)
    N = n - 1

    D = np.empty((N + 3, c))
    D[0] = X[0]
    D[1] = d0
    D[2:-2] = d
    D[-2] = dN
    D[-1] = X[-1]

    return D


def natural_end_cond(X):
    n, c = np.shape(X)
    N = n - 1  # number of Bezier curves
    a = N - 1  # size of A, min is 2

    # Assemble system
    u = np.ones(a - 1)
    A = tridiag_from_udl(u, np.ones(a) * 4, u)
    B = np.multiply(X[1:-1], 6)
    B[0] -= X[0]
    B[-1] -= X[-1]

    # Solve for deBoor control points
    d = lu_solve_tridiag(A, B, True)
    d0 = 2.0 / 3 * X[0] + 1.0 / 3 * d[0]
    dN = 1.0 / 3 * d[-1] + 2.0 / 3 * X[-1]

    # Assemble all deBoor control points
    D = make_deboor(X, d, d0, dN)

    return D


def quadratic_end_cond(X):
    n, c = np.shape(X)
    N = n - 1  # number of Bezier curves
    a = N - 1  # size of A, min is 2

    # Assemble system
    u = np.ones(a - 1)
    A = tridiag_from_udl(u, np.ones(a) * 4, u)
    A[0, 0] = 5
    A[-1, -1] = 5

    B = np.multiply(X[1:-1], 6)
    B[0] += X[1] - X[0]
    B[-1] += X[-2] - X[-1]

    # Solve for deBoor control points
    d = lu_solve_tridiag(A, B, True)
    d0 = d[0] + 2.0 / 3 * X[0] - 2.0 / 3 * X[1]
    dN = d[-1] + 2.0 / 3 * X[-1] - 2.0 / 3 * X[-2]

    D = make_deboor(X, d, d0, dN)
    return D


def bessel_end_cond():
    pass


def knot_end_cond():
    pass


points_x = [0, 0, 1, 1, 2]
points_y = [0, 1, 1, 0, 1]
s = 5

X = np.vstack((points_x[:s], points_y[:s])).T
D = quadratic_end_cond(X)
Dx, Dy = D.T

fig, ax = plt.subplots()
fig.set_facecolor('w')

ax.plot(points_x, points_y, 'o-')
ax.plot(Dx, Dy, 'o-')
ax.set_aspect('equal')
ax.grid(True)

plt.show()
