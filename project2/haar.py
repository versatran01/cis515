import numpy as np


def haar(u):
    """
    Compute the Haar transformation of a vector
    :param u: input vector
    :return: Haar coefficients of the input vector
    """
    l = len(u)
    n = int(np.log2(l))
    # initialize
    c = u

    for j in range(n):
        # extract part of u to do average and diff
        m = n - j
        iu = 2 ** m
        v = np.reshape(u[:iu], (-1, 2))
        mean = np.mean(v, axis=-1)
        diff = -np.diff(v) / 2.0

        # update part of c with average and diff
        ic = int(iu / 2)
        c[:ic] = mean
        c[ic:(ic * 2)] = np.ravel(diff)

    return c


def haar_inv(c):
    """
    Reconstruct a vector from its Haar coefficients
    :param c: Haar coefficients
    :return: original vector
    """
    l = len(c)
    n = int(np.log2(l))
    # initialize
    u = c

    for j in range(n):
        # extract part of c to reverse average and diff
        ic = 2 ** j
        mean = c[:ic]
        diff = c[ic:(ic * 2)]

        # restore part of u
        plus = mean + diff
        minus = mean - diff

        iu = ic * 2
        u[0:iu:2] = plus
        u[1:iu:2] = minus

    return u


def haar_step(u, k):
    return u


def haar_inv_step(v, k):
    return v
