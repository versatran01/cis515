import numpy as np
from scipy.special import binom


class BezierBase:
    def create_curve(self, points):
        """
        Interface for generating Bezier curve
        :param points: control points
        """
        raise NotImplementedError


def bernstein(n, k, t):
    """
    Bernstein polynomial value at t
    """
    return binom(n, k) * (t ** k) * ((1 - t) ** (n - k))


class BezierBernstein(BezierBase):
    def __init__(self, num=256):
        """
        :param num: number of samples
        """
        self.num = num
        self.ts = np.linspace(0, 1, num)

    def create_curve(self, points):
        """
        Creating Bezier curve using Bernstein polynomials
        :param points: control points
        :return: points on Bezier curve
        """
        n = len(points)
        d = len(points[0])
        m = n - 1

        curve = np.zeros((self.num, d))
        for k in range(n):
            curve += np.outer(bernstein(m, k, self.ts), points[k])
        return curve


def de_casteljau(points, t):
    """
    De Casteljau algorithm
    :param points: control points
    :param t: interpolation value
    :return: interpolated point on Bezier curve
    """
    n = len(points)  # number of control points
    m = n - 1  # polynomial degree
    for k in range(m):
        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i + 1]
    return points[0]


class BezierDeCasteljau(BezierBase):
    def __init__(self, num=256):
        """
        :param num: number of samples
        """
        self.num = num
        self.ts = np.linspace(0, 1, num)

    def create_curve(self, points):
        """
        Creating Bezier curve using De Casteljau algorithm
        :param points: control points
        :return: points on Bezier curve
        """
        points = np.array(points, float)
        curve = np.empty((self.num, len(points[0])))
        for i, t in enumerate(self.ts):
            curve[i] = de_casteljau(points, t)
        return curve


def subdivision(points, divide=6, t=0.5):
    """
    Subdivision version of De Casteljau algorithm
    :param points: control points
    :param divide: number of times the algorithm divide
    :param t: where to divide default is 0.5
    :return: all control points as numpy.array
    """
    curve = subdiv_rec(points, divide, t)
    curve_full = curve + [points[-1]]  # Add the last point
    curve_full = np.vstack(curve_full)
    return np.array(curve_full)


def subdiv_rec(points, divide, t):
    """
    Recursive version of the subdivision algorithm
    :param points: control points
    :param divide: number of times this step divides
    :param t: where to divide
    :return: list of control points
    """
    # make a copy of points since we will modify them later
    points = np.array(points)
    if divide == 0:
        # The last point is repeated so we don't add it here
        return [points[:-1]]

    n = len(points)  # number of points
    d = len(points[0])  # dimension
    m = n - 1  # degree of polynomial

    ud = np.empty((n, d))
    ld = np.empty_like(ud)

    for k in range(m):
        ud[k] = points[0]
        # To ensure correct sequence, ld are assembled backwards
        ld[m - k] = points[m - k]

        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i + 1]

    # add last point to ud and ld
    ud[-1] = points[0]
    ld[0] = points[0]

    return subdiv_rec(ud, divide - 1, t) + subdiv_rec(ld, divide - 1, t)


class BezierSubdivision(BezierBase):
    def __init__(self, divide=6):
        """
        :param divide: number of times to subdivide
        """
        self.divide = divide

    def create_curve(self, points):
        """
        Creating Bezier curve using subdivision algorithm
        :param points: control points
        :return: points on Bezier curve
        """
        points = np.array(points)
        curve = subdivision(points, self.divide)
        return curve
