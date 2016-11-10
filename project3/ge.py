import numpy as np
import scipy.linalg as la


def ge_solve(A, B, fast=False):
    """
    Solve AX=B using gaussian elimination with partial pivoting
    :param A: MxM matrix
    :param B: MxP matrix
    :return: MxP matrix X such that AX=B
    """
    A = np.asarray(A, float)
    B = np.asarray(B, float)

    if np.ndim(B) == 1:
        B = np.atleast_2d(B).T

    mA, nA = np.shape(A)
    mB, nB = np.shape(B)

    if mA != mB:
        raise ValueError("incompatible dimension, number of equations do not "
                         "match: {} != {}.".format(mA, mB))

    if mA != nA:
        raise ValueError("incompatible dimension, A is not square matrix")

    AB = np.hstack((A, B))
    ABr, pivlist = gauss_elim(AB)
    Ar, Br = np.split(ABr, [nA], axis=1)
    X = back_sub(Ar, Br, fast=fast)
    return X


def gauss_elim(A, partial_pivot=True):
    """
    Gaussian elimination
    :param A: MxN matrix
    :param partial_pivot: True to use partial pivot
    :return:
    """
    assert np.ndim(A) == 2
    r, c = np.shape(A)

    pivlist = np.arange(r)

    for k in range(r - 1):
        # Working on the kth subsystem
        A_k = A[k:, k:]

        # row i is the pivot row
        if partial_pivot:
            # maximum abs value
            i = np.argmax(np.abs(A_k[:, 0]))
        else:
            # first non-zero value
            i = np.argmax(np.where(A_k[:, 0] != 0))[0]

        # and it cannot be zero, otherwise matrix is singular
        assert A_k[i, 0] != 0

        # Swap row 1 with row i of A_k
        if i != 0:
            A_k[[0, i]] = A_k[[i, 0]]
            pivlist[k] = k + i
            pivlist[k + i] = k

        # Make pivot element 1
        pivot = A_k[0, 0]
        pivot_row = A_k[0] / pivot

        # Eliminate all variables below
        for j in range(1, r - k):
            A_k[j] -= pivot_row * A_k[j, 0]

    return A, pivlist


def is_triu(M):
    """
    Check if matrix is upper triangular
    """
    return np.array_equal(M, np.triu(M))


def back_sub(A, B, fast=False):
    """
    Back substitution of a triangular system AX = B
    :param A: MxM matrix
    :param B: MxP matrix
    :param fast: if True use scipy.linalg.solve_triangular
    :return: MxP matrix X such that AX=B
    """
    if not is_triu(A):
        raise ValueError("A is not upper triangular")

    if fast:
        return la.solve_triangular(A, B)

    A = np.asarray(A, float)
    B = np.asarray(B, float)
    X = np.empty_like(B)

    mA, nA = np.shape(A)

    X[-1] = B[-1] / A[-1, -1]
    for i in reversed(range(mA - 1)):
        ax = np.dot(A[i, i + 1:], X[i + 1:])
        X[i] = (B[i] - np.sum(ax, axis=0)) / A[i, i]

    return X


if __name__ == "__main__":
    # A = np.array([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], float)
    # A = np.array([[1, 1, 1], [1, 1, 3], [2, 5, 8]], float)
    A = np.array([[0, 0, 1], [-2, 7, 2], [4, -6, 0]], float)
    # B = np.array([5, -2, 9], float)
    # B = np.array([1, 1, 1], float)
    B = np.array([1, 1, -1], float)
    X = ge_solve(A, B, fast=False)
    Xf = ge_solve(A, B, fast=True)
    print(Xf)
    print(X)
