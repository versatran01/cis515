import numpy as np


def ge_solve(A, B):
    AB = np.hstack((A, B))
    ABr = gaussian_elimination(AB)


def gaussian_elimination(A, partial_pivot=True):
    """
    Gaussian elimination
    :param A:
    :param b:
    :param partial_pivot:
    :return:
    """
    assert np.ndim(A) == 2
    r, c = np.shape(A)
    assert r == c

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

        # Make pivot element 1
        pivot = A_k[0, 0]
        pivot_row = A_k[0] / pivot

        # Eliminate all variables below
        for j in range(1, r - k):
            A_k[j] -= pivot_row * A_k[j, 0]

    return A, pivlist


def back_substitution(A, B, pivlist):
    """

    :param A:
    :param b:
    :return:
    """
    pass


if __name__ == "__main__":
    A = np.array([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], float)
    # A = np.array([[1, 1, 1], [1, 1, 3], [2, 5, 8]], float)
    b = np.array([5, -2, 9], float)
    # b = np.array([1, 1, 1], float)
    Ae, be = gaussian_elimination(A)
    print(Ae)
