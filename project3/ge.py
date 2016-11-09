import numpy as np


def gaussian_elimination(A, partial_pivot=True):
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
        pivot_row = A_k[0] / A_k[0, 0]

        # Eliminate all variables below
        for j in range(1, r - k):
            A_k[j] -= pivot_row * A_k[j, 0]

    return A
