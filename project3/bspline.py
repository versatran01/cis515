import numpy as np
from enum import Enum
from project3.lu import tridiag_from_udl, lu_solve_tridiag
from project1.deboor import deboor_to_bezier


class EndCondition(Enum):
    """
    End condition of a bspline
    """
    natural = 1
    quadratic = 2
    bessel = 3
    notaknot = 4


def deboor_to_bspline(D, bezier):
    """
    First convert deboor control points to list of 4 bezier control points
    Then use Bezier class to create bezier curve from each bezier segment
    Stack them together to get final bspline
    :param D: deBoor control points, nxm array
    :param bezier: class of Bezier that has create_curve method
    :return:
    """
    B = deboor_to_bezier(D, last_point=True)
    P = []
    for b in B:
        p = bezier.create_curve(b)
        P.append(p)
    return np.vstack(P)


def curve_interp(points, end_cond):
    """
    Interpolate data points using bspline by generating deBoor control points
    :param points: n points, nxm array
    :param end_cond:
    :return: deBoor control points, (n+d)xm array
    """
    points = np.atleast_2d(np.array(points))
    if len(points) < 3:
        raise ValueError('Not enough points')

    if end_cond == EndCondition.natural:
        interp_fun = natural_end_cond
    elif end_cond == EndCondition.quadratic:
        interp_fun = quadratic_end_cond
    elif end_cond == EndCondition.bessel:
        interp_fun = bessel_end_cond
    elif end_cond == EndCondition.notaknot:
        interp_fun = notaknot_end_cond
    else:
        raise ValueError("Unsupported end condition")

    return interp_fun(points)


def make_deboor(X, d, d0, dN):
    """
    Helper function to make deBoor control points
    :param X:
    :param d: d_1 to d_N-1
    :param d0:
    :param dN:
    :return:
    """
    n, c = np.shape(X)

    D = np.empty((n + 2, c))
    D[0] = X[0]
    D[1] = d0
    D[2:-2] = d
    D[-2] = dN
    D[-1] = X[-1]

    return D


def make_interp_lhs(m, c=None):
    """
    Create lhs of interpolation system
    :param m: size of the system
    :param c: A[0,0] = A[-1,-1] = c
    :return:
    """
    u = np.ones(m - 1)
    A = tridiag_from_udl(u, np.ones(m) * 4, u)
    if c is not None:
        A[0, 0] = c
        A[-1, -1] = c
    return A


def natural_end_cond(X):
    n, c = np.shape(X)

    # Assemble system
    A = make_interp_lhs(n - 2)
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

    # Assemble system
    A = make_interp_lhs(n - 2, 5)
    B = np.multiply(X[1:-1], 6)
    B[0] += X[1] - X[0]
    B[-1] += X[-2] - X[-1]

    # Solve for deBoor control points
    d = lu_solve_tridiag(A, B, True)
    d0 = d[0] + 2.0 / 3 * X[0] - 2.0 / 3 * X[1]
    dN = d[-1] + 2.0 / 3 * X[-1] - 2.0 / 3 * X[-2]

    D = make_deboor(X, d, d0, dN)
    return D


def bessel_end_cond(X):
    n, c = np.shape(X)

    # Assemble system
    A = make_interp_lhs(n - 2, 7.0 / 2)
    d0 = 1.0 / 2 * X[0] + 2.0 / 3 * X[1] - 1.0 / 6 * X[2]
    dN = -1.0 / 6 * X[-3] + 2.0 / 3 * X[-2] + 1.0 / 2 * X[-1]

    B = np.multiply(X[1:-1], 6)
    B[0] -= 3.0 / 2 * d0
    B[-1] -= 3.0 / 2 * dN

    d = lu_solve_tridiag(A, B, True)
    D = make_deboor(X, d, d0, dN)
    return D


def notaknot_end_cond(X):
    n, c = np.shape(X)
    # N = n - 1

    d1 = -1.0 / 6 * (X[0] + X[2]) + 4.0 / 3 * X[1]
    dNm1 = -1.0 / 6 * (X[-3] + X[-1]) + 4.0 / 3 * X[-2]
    if n == 3:
        # N = 2, dNm1 = d1
        d0 = 7.0 / 18 * (X[0] + X[2]) + 8.0 / 9 * X[1] - 2.0 / 3 * d1
        d2 = d0
        D = np.vstack((X[0], d0, d1, d2, X[-1]))
    elif n == 4:
        # N = 3, dNm1 = d2
        d2 = dNm1
        d0 = 7.0 / 18 * (X[0] + X[2]) + 8.0 / 9 * X[1] - 2.0 / 3 * d2
        d3 = 7.0 / 18 * (X[1] + X[3]) + 8.0 / 9 * X[2] - 2.0 / 3 * d1
        D = np.vstack((X[0], d0, d1, d2, d3, X[-1]))
    elif n == 5:
        # N = 4, dNm1 = d3
        d3 = dNm1
        d2 = 3.0 / 2 * X[2] - 1.0 / 4 * (d1 + d3)
        d0 = 7.0 / 18 * (X[0] + X[2]) + 8.0 / 9 * X[1] - 2.0 / 3 * d2
        d4 = 7.0 / 18 * (X[2] + X[4]) + 8.0 / 9 * X[3] - 2.0 / 3 * d2
        D = np.vstack((X[0], d0, d1, d2, d3, d4, X[-1]))
    elif n >= 6:
        A = make_interp_lhs(n - 4)
        B = np.multiply(X[2:-2], 6)
        B[0] -= d1
        B[-1] -= dNm1
        d = lu_solve_tridiag(A, B, True)

        d0 = 7.0 / 18 * (X[0] + X[2]) + 8.0 / 9 * X[1] - 2.0 / 3 * d[0]
        dN = 7.0 / 18 * (X[-3] + X[-1]) + 8.0 / 9 * X[-2] - 2.0 / 3 * d[-1]

        D = np.vstack((X[0], d0, d1, d, dNm1, dN, X[-1]))
    else:
        raise ValueError('n = {}'.format(n))

    return D
