import numpy as np
from project2.haar import haar_step, haar, haar_inv, haar_inv_step


def haar2d(A, k=-1, normalize=False):
    """

    :param A:
    :return:
    """
    r, c = np.shape(A)

    B = np.empty_like(A)
    for i in range(r):
        B[i] = haar_step(A[i], k=k, normalize=normalize)

    BT = np.transpose(B)
    CT = np.empty_like(BT)
    for i in range(c):
        CT[i] = haar_step(BT[i], k=k, normalize=normalize)

    return np.transpose(CT)


def haar_inv2d(C, k=-1, normalize=False):
    """

    :param C:
    :return:
    """
    r, c = np.shape(C)

    CT = np.transpose(C)
    BT = np.empty_like(CT)
    for i in range(c):
        BT[i] = haar_inv_step(CT[i], k=k, normalize=normalize)

    B = np.transpose(BT)
    A = np.empty_like(B)
    for i in range(r):
        A[i] = haar_inv_step(B[i], k=k, normalize=normalize)

    return A


def haar2d_n(A):
    """

    :param A:
    :return:
    """
    return haar2d(A, normalize=True)


def haar_inv2d_n(C):
    """

    :param C:
    :return:
    """
    return haar_inv2d(C, normalize=True)
