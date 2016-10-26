import numpy as np


def haar(u, normalize=False):
    """
    Compute the Haar transformation of a vector
    :param u: input vector
    :param normalize:
    :return: Haar coefficients of the input vector
    """
    return haar_step(u, -1, normalize=normalize)


def haar_inv(c, normalize=False):
    """
    Reconstruct a vector from its Haar coefficients
    :param c: Haar coefficients
    :param normalize:
    :return: original vector
    """
    return haar_inv_step(c, -1, normalize=normalize)


def haar_step(u, k, normalize=False):
    """
    Compute the Haar transformation of a vector k steps
    :param u: input vector
    :param k: number of steps, -1 means n steps
    :param normalize:
    :return: Haar coefficients of the input vector
    """
    n = int(np.log2(len(u)))

    assert 2 ** n == len(u)
    assert k <= n
    if k < 0:
        k = n

    # normalization factor
    d = np.sqrt(2.0) if normalize else 2.0

    # initialize
    c = np.array(u, copy=True)

    for j in range(k):
        # extract part of u to do average and diff
        m = n - j
        iu = 2 ** m  # indices of c for computing average and difference
        v = np.reshape(c[:iu], (-1, 2))
        mean = np.sum(v, axis=-1) / d
        diff = -np.diff(v) / d

        # update part of c with average and diff
        ic = int(iu / 2)
        c[:ic] = mean
        c[ic:iu] = np.ravel(diff)

    return c


def haar_inv_step(c, k, normalize=False):
    """
    Reconstruct a vector from its Haar coefficients
    :param c: Haar coefficients
    :param k: number of steps, -1 means n steps
    :param normalize:
    :return: original vector
    """
    n = int(np.log2(len(c)))

    assert 2 ** n == len(c)
    assert k <= n
    if k < 0:
        k = n

    # normalization factor
    d = np.sqrt(2.0) if normalize else 1.0

    # initialize
    u = np.array(c, copy=True)

    for j in range(k):
        # extract part of c to reverse average and diff
        ic = 2 ** (n - k + j)
        iu = ic * 2
        mean = u[:ic]
        diff = u[ic:iu]

        # restore part of u
        plus = (mean + diff) / d
        minus = (mean - diff) / d

        iu = ic * 2
        u[0:iu:2] = plus
        u[1:iu:2] = minus

    return u
