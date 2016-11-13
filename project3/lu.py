import numpy as np
import scipy.linalg as la


def lu_solve(A, B, tridiag=True, use_scipy=False):
    if use_scipy:
        return lu_solve_scipy(A, B, tridiag=tridiag)

    # Our implementation here

    return None


def lu_solve_scipy(A, B, tridiag=True):
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

    ab = np.zeros((3, m))
    ab[0, 1:] = np.diag(A, 1)
    ab[1] = np.diag(A)
    ab[-1, :-1] = np.diag(A, -1)

    return ab


if __name__ == '__main__':
    A = np.reshape(np.arange(16), (4, 4))
    print(A)
    ab = banded_from_tridiag(A)
    print(ab)
