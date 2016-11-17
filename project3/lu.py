import numpy as np
import scipy.linalg as la
from project3.ge import back_sub, forward_sub


def lu_solve(A, B, tridiag=True, use_scipy=True):
    """
    Solve systems of linear equations using LU decomposition
    This version currently assumes A is tridiagonal
    :param A:
    :param B:
    :param tridiag:
    :param use_scipy: True to use scipy.linalg.solve_triangular
    :return:
    """
    if not tridiag:
        raise NotImplementedError('General lu_solve is not implemented.')

    m, n = np.shape(A)
    # Extract diagonals
    c, b, a = banded_from_tridiag(A)

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


def lu_solve_scipy(A, B, tridiag=True):
    """
    Scipy version of lu_solve, handles both tridiagonal and general square
    matrices. Tridiagonal version is must faster, using
    scipy.linalg.solve_banded
    :param A:
    :param B:
    :param tridiag: True will use solve_banded
    :return:
    """
    n, _ = np.shape(A)
    if tridiag:
        ab = banded_from_tridiag(A)
        return la.solve_banded((1, 1), ab, B)

    return la.lu_solve(la.lu_factor(A), B)


def banded_from_tridiag(A):
    """
    Convert tridiagonal matrix to banded matrix
    :param A: MxM Tridiagonal matrix
    :return: Banded matrix of size 3xM
    """
    m, n = np.shape(A)
    if m != n:
        raise ValueError('A is not square matrix')

    ab = np.empty((3, m))
    # First row of ab is A off-diagonal by 1
    ab[0, 1:] = np.diag(A, 1)
    # Second row of ab is A diagonal
    ab[1] = np.diag(A)
    # Last row of ab is A off-diagonal by -1
    ab[-1, :-1] = np.diag(A, -1)

    # Pad 0s
    ab[0, 0] = 0
    ab[-1, -1] = 0

    return ab


def rand_tridiag(n):
    """
    Random tridiagonal matrix
    :param n: dimension of the matrix
    :return: A random tridiagonal matrix of size nxn
    """
    A = np.diag(np.random.random(n - 1), 1) + \
        np.diag(np.random.random(n)) + \
        np.diag(np.random.random(n - 1), -1)
    return A
