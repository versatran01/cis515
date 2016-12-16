import numpy as np


def linspace_vec(v1, v2, n=100):
    """
    vector version of linspace
    """
    L = []
    for a, b in zip(v1, v2):
        l = np.linspace(a, b, num=n)
        L.append(l)
    return np.array(L)


def interp_sim3(sim1, sim2, n=100):
    """
    Linear interpolation in sim3
    """
    return linspace_vec(sim1, sim2, n=n)
