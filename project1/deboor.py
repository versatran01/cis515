import numpy as np

def lerp(p, q, t):
    """
    Linear interpolation between two points p, q
    :param p:
    :param q:
    :param t: in [0, 1], when t = 0, returns p, t = 1, returns q
    :return: (1 - t) * p + t * q
    """
    assert 0 <= t <= 1
    return (1 - t) * p + t * q


def deboor_first(points, r=0.5, flip=False):
    points = np.array(points)
    if flip:
        points = np.flipud(points)
    d0, d1, d2, d3 = points
    b1_0 = d0
    b1_1 = d1
    b1_2 = lerp(d1, d2, 0.5)
    b2_1 = lerp(d2, d3, r)
    b1_3 = lerp(b1_2, b2_1, 0.5)
    bs = np.array([b1_0, b1_1, b1_2, b1_3])
    if flip:
        bs = np.flipud(bs)
    return bs

def deboor_second(points, r=0.5, flip=False):
    pass

class DeBoor:
    def __init__(self):
        pass
