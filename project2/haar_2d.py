import numpy as np
from project2.haar import haar, haar_inv


def haar2d(M):
    r, c = np.shape(M)

    B = np.empty_like(M)
    for i in range(r):
        B[i] = haar(M[i])

    BT = np.transpose(B)
    CT = np.empty_like(BT)
    for i in range(c):
        CT[i] = haar(BT[i])

    return np.transpose(CT)


def haar_inv2d(M):
    return M


def haar2d_n(M):
    return M


def haar_inv2d_n(M):
    return M


if __name__ == '__main__':
    M = np.array([[64, 2, 3, 61, 60, 6, 7, 57],
                  [9, 55, 54, 12, 13, 51, 50, 16],
                  [17, 47, 46, 20, 21, 43, 42, 24],
                  [40, 26, 27, 37, 36, 30, 31, 33],
                  [32, 34, 35, 29, 28, 38, 39, 25],
                  [41, 23, 22, 44, 45, 19, 18, 48],
                  [49, 15, 14, 52, 53, 11, 10, 56],
                  [8, 58, 59, 5, 4, 62, 63, 1]], float)

    print(haar2d(M))
