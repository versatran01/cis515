import numpy as np
from scipy.special import binom


class BezierBase:
    def create_curve(self, points):
        raise NotImplementedError


def bernstein(n, k, t):
    return binom(n, k) * (t ** k) * ((1 - t) ** (n - k))


class BezierBernstein(BezierBase):
    def __init__(self, num=256):
        """
        :param num: number of samples for the entire curve
        """
        self.num = num
        self.ts = np.linspace(0, 1, num)

    def create_curve(self, points):
        n = len(points)
        d = len(points[0])
        m = n - 1

        curve = np.zeros((self.num, d))
        for k in range(n):
            curve += np.outer(bernstein(m, k, self.ts), points[k])
        return curve


def de_casteljau(points, t):
    n = len(points)  # number of control points
    m = n - 1  # polynomial degree
    for k in range(m):
        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i + 1]
    return points[0]


class BezierDeCasteljau(BezierBase):
    def __init__(self, num=256):
        self.num = num
        self.ts = np.linspace(0, 1, num)

    def create_curve(self, points):
        points = np.array(points, float)
        curve = np.zeros((self.num, 2))
        for i, t in enumerate(self.ts):
            curve[i] = de_casteljau(points, t)
        return curve


def subdivision(points, depth=6, t=0.5):
    curve = subdivision_rec(points, depth, t=t)
    curve_full = [points[0]] + curve + [points[-1]]
    return np.array(curve_full)


def subdivision_rec(points, depth, t=0.5):
    """
    Recursive version of the subdivision algorithm
    :param points: control points
    :param depth:
    :param t:
    :return:
    """
    # make a copy of points since we will modify them later
    points = np.array(points)
    n = len(points)  # number of points
    d = len(points[0])  # dimension
    m = n - 1  # degree of polynomial

    upper = np.zeros((n, d))
    lower = np.zeros_like(upper)

    for k in range(m):
        upper[k] = points[0]
        lower[k] = points[m - k]

        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i + 1]

    # add last point to ud and ld
    bm = points[0]
    upper[-1] = bm
    lower[-1] = bm
    # flip lower to ensure correct sequence
    lower = np.flipud(lower)

    if depth == 0:
        return [bm]
    return subdivision_rec(upper, depth - 1) + [bm] \
           + subdivision_rec(lower, depth - 1)


class BezierSubdivision(BezierBase):
    def __init__(self, depth=7):
        self.depth = depth

    def create_curve(self, points):
        points = np.array(points)
        curve = subdivision(points, self.depth)
        return curve
