import numpy as np
import scipy.linalg as la


def lu_solve(A, B, tridiag=False):
    pass


def lu_solve_scipy(A, B, tridiag=False):
    """
    Scipy version of lu_solve
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
    :param A: Tridiagonal matrix
    :return: Banded matrix
    """
    m, n = np.shape(A)
    if m != n:
        raise ValueError('A is not square matrix')

    ab = np.empty((3, m))
    ab[0, 1:] = np.diag(A, 1)
    ab[1] = np.diag(A)
    ab[-1, :-1] = np.diag(A, -1)

    # Pad 0s
    ab[0, 0] = 0
    ab[-1, -1] = 0

    return ab
