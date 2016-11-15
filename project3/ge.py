import numpy as np
import scipy.linalg as la


def ge_solve(A, B, use_scipy=False):
    """
    Solve AX=B using gaussian elimination with partial pivoting
    :param A: MxM matrix
    :param B: MxP matrix
    :param use_scipy:
    :return: MxP matrix X such that AX=B, X will have the same dimension as B
    """
    A = np.asarray(A, float)
    B = np.asarray(B, float)

    squeeze = False
    if np.ndim(B) == 1:
        B = np.atleast_2d(B).T
        squeeze = True

    mA, nA = np.shape(A)
    mB, nB = np.shape(B)

    if mA != mB:
        raise ValueError("Incompatible dimension, number of equations do not "
                         "match: {} != {}.".format(mA, mB))

    if mA != nA:
        raise ValueError("Incompatible dimension, A is not square matrix")

    AB = np.hstack((A, B))
    ABr = gauss_elim(AB)
    Ar, Br = np.split(ABr, [nA], axis=1)
    X = back_sub(Ar, Br, use_scipy=use_scipy)

    return np.squeeze(X) if squeeze else X


def gauss_elim(A, partial_pivot=True):
    """
    Gaussian elimination
    :param A: MxN matrix
    :param partial_pivot: True to use partial pivot
    :return:
    """
    assert np.ndim(A) == 2
    r, c = np.shape(A)

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

        # Make pivot element 1
        pivot = A_k[0, 0]
        pivot_row = A_k[0] / pivot

        # Eliminate all variables below
        for j in range(1, r - k):
            if A_k[j, 0] != 0:
                A_k[j] -= pivot_row * A_k[j, 0]

    return A


def is_triu(M):
    """
    Check if matrix is upper triangular
    """
    return np.array_equal(M, np.triu(M))


def is_tril(M):
    """
    Check if matrix is lower triangular
    """
    return np.array_equal(M, np.tril(M))


def back_sub(A, B, use_scipy=False):
    """
    Back substitution of a triangular system AX = B
    :param A: MxM matrix
    :param B: MxP matrix
    :param use_scipy: if True use scipy.linalg.solve_triangular
    :return: MxP matrix X such that AX=B
    """
    if not is_triu(A):
        raise ValueError("A is not upper triangular")

    if use_scipy:
        return la.solve_triangular(A, B)

    A = np.asarray(A, float)
    B = np.asarray(B, float)
    X = np.empty_like(B)

    mA, nA = np.shape(A)

    # TODO: Fix this, failed when B has more than 1 column
    X[-1] = B[-1] / A[-1, -1]
    for i in reversed(range(mA - 1)):
        ax = np.dot(A[i, i + 1:], X[i + 1:])
        X[i] = (B[i] - np.sum(ax, axis=0)) / A[i, i]

    return X


def forward_sub(A, B, use_scipy=False):
    """
    Forward substitution of a triangular system AX = B
    :param A: MxM lower triangular matrix
    :param B: MxP matrix
    :param use_scipy: if True use scipy.linalg.solve_triangular
    :return: MxP matrix X such that AX=B
    """
    if not is_tril(A):
        raise ValueError("A is not lower triangular")

    if use_scipy:
        return la.solve_triangular(A, B, lower=True)

        # TODO: add our own forward-substitution code


def rand_square(n):
    """
    Random square matrix
    :param n:
    :return:
    """
    return np.random.random((n, n))
