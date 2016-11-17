import numpy as np
import scipy.linalg as la
from project3.ge import back_sub, forward_sub
from numpy.random import random


def lu_solve_tridiag(A, B, use_scipy=True):
    """
    Solve systems of linear equations using LU decomposition
    This version currently assumes A is tridiagonal
    """
    m, n = np.shape(A)
    # Extract diagonals
    c, b, a = banded3_from_tridiag(A)

    # allocate
    # off diagonal of L
    ddL = np.empty(n)
    ddL[0] = 0

    # diagonal of U
    dU = np.empty(n)
    dU[0] = b[0]

    for i in range(1, n):
        ddL[i] = a[i - 1] / dU[i - 1]
        dU[i] = b[i] - ddL[i] * c[i]

    L = np.eye(n) + np.diag(ddL[1:], k=-1)
    U = np.diag(dU) + np.diag(c[1:], k=1)

    W = forward_sub(L, B, use_scipy=use_scipy)
    X = back_sub(U, W, use_scipy=use_scipy)

    return X


def lu_solve_scipy(A, B):
    """
    Scipy version of lu_solve, handles both tridiagonal and general square
    matrices. Tridiagonal version is must faster, using
    scipy.linalg.solve_banded
    """
    return la.lu_solve(la.lu_factor(A), B)


def solve_tridiag(A, B):
    """
    Solve tridiagonal system
    """
    ab = banded3_from_tridiag(A)
    return la.solve_banded((1, 1), ab, B)


def solve_banded3(Ab, B):
    """
    Solve banded matrix with width 3
    """
    return la.solve_banded((1, 1), Ab, B)


def banded3_from_udl(u, d, l):
    """
    Banded matrix from upper, diagonal and lower
    """
    n = len(d)

    ab = np.empty((3, n))
    # First row of ab is A off-diagonal by 1
    ab[0, 1:] = u
    # Second row of ab is A diagonal
    ab[1] = d
    # Last row of ab is A off-diagonal by -1
    ab[-1, :-1] = l

    # Pad 0s
    ab[0, 0] = 0
    ab[-1, -1] = 0

    return ab


def banded3_from_tridiag(A):
    """
    Convert tridiagonal matrix to banded matrix
    :param A: MxM Tridiagonal matrix
    :return: Banded matrix of size 3xM
    """
    m, n = np.shape(A)
    if m != n:
        raise ValueError('A is not square matrix')

    ab = banded3_from_udl(np.diag(A, 1), np.diag(A), np.diag(A, -1))

    return ab


def tridiag_from_udl(u, d, l):
    """
    Tridiagonal matrix from upper, diagonal and lower
    """
    return np.diag(u, 1) + np.diag(d) + np.diag(l, -1)


def rand_tridiag(n):
    """
    Random tridiagonal matrix
    :param n: dimension of the matrix
    :return: A random tridiagonal matrix of size nxn
    """
    return tridiag_from_udl(random(n - 1), random(n), random(n - 1))
