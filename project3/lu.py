import numpy as np
import scipy.linalg as la
from project3.ge import back_sub, forward_sub


def lu_solve(A, B, tridiag=False):
    # type: (object, object, object) -> object
    # To do this, first implement lu_factor and then use back_sub and
    # forward_sub to solve for X
    if tridiag:
        ab = banded_from_tridiag(A)
        m,n = np.shape(ab)

        # extract diagonals from the banded matrix
        du = ab[0, :] # upper diagonal of A padded with zero at end
        d = ab[1, :]  # diagonal of A
        dl = ab[2, :]  # lower diagonal of A padded with zero at front
        # allocate
        ddl = np.empty([n])
        ddl[0] = 0

        dd = np.empty([n])
        dd[0] = d[0]

        for i in range(1, n):
            ddl[i] = dl[i-1] / dd[i-1]
            dd[i] = d[i] - ddl[i] * du[i]

        L = np.diag([1]*n) + np.diag(ddl[1:], k=-1)
        U = np.diag(dd) + np.diag(du[1:], k=1)

        y = forward_sub(L, B, use_scipy=True)
        x = back_sub(U, y, use_scipy=False)

        return x



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

A = np.diag([-20, 5, 7], k=-1) + np.diag([5, 8, 2, 9]) + np.diag([-6, -5, -7], k=1)
ab = banded_from_tridiag(A)
x = lu_solve(A, [1, 1, 1, 1,], tridiag=True)
print(x)
