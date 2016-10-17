import numpy as np
from project2.haar import haar, haar_inv


def haar2d(A):
    """

    :param A:
    :return:
    """
    r, c = np.shape(A)

    B = np.empty_like(A)
    for i in range(r):
        B[i] = haar(A[i])

    BT = np.transpose(B)
    CT = np.empty_like(BT)
    for i in range(c):
        CT[i] = haar(BT[i])

    return np.transpose(CT)


def haar_inv2d(C):
    """

    :param C:
    :return:
    """
    r, c = np.shape(C)

    CT = np.transpose(C)
    BT = np.empty_like(CT)
    for i in range(c):
        BT[i] = haar_inv(CT[i])

    B = np.transpose(BT)
    A = np.empty_like(B)
    for i in range(r):
        A[i] = haar_inv(B[i])

    return A


def haar2d_n(M):
    return M


def haar_inv2d_n(M):
    return M
