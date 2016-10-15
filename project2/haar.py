import numpy as np


def haar(u):
    """
    Compute the Haar transformation of a vector
    :param u: input vector
    :return: Haar coefficients of the input vector
    """
    return haar_step(u, -1)


def haar_inv(c):
    """
    Reconstruct a vector from its Haar coefficients
    :param c: Haar coefficients
    :return: original vector
    """
    return haar_inv_step(c, -1)


def haar_step(u, k):
    """
    Compute the Haar transformation of a vector k steps
    :param u: input vector
    :param k: number of steps, -1 means n steps
    :return: Haar coefficients of the input vector
    """
    n = int(np.log2(len(u)))

    assert k <= n
    if k < 0:
        k = n

    # initialize
    c = np.array(u, copy=True)

    for j in range(k):
        # extract part of u to do average and diff
        m = n - j
        iu = 2 ** m
        v = np.reshape(c[:iu], (-1, 2))
        mean = np.mean(v, axis=-1)
        diff = -np.diff(v) / 2.0

        # update part of c with average and diff
        ic = int(iu / 2)
        c[:ic] = mean
        c[ic:(ic * 2)] = np.ravel(diff)

    return c


def haar_inv_step(c, k):
    """
    Reconstruct a vector from its Haar coefficients
    :param c: Haar coefficients
    :param k: number of steps, -1 means n steps
    :return: original vector
    """
    n = int(np.log2(len(c)))

    assert k <= n
    if k < 0:
        k = n

    # initialize
    u = np.array(c, copy=True)

    for j in range(k):
        # extract part of c to reverse average and diff
        ic = 2 ** j
        mean = u[:ic]
        diff = u[ic:(ic * 2)]

        # restore part of u
        plus = mean + diff
        minus = mean - diff

        iu = ic * 2
        u[0:iu:2] = plus
        u[1:iu:2] = minus

    return u
