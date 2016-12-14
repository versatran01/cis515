import numpy as np


def torus(R, r, n=50):
    """
    Make a torus
    :param R: distance from the center of the tube to the center of the torus
    :param r: radius of the tube
    :param n: number of points
    :return: (x, y, z) each has dimension n x n
    """
    theta = np.linspace(0, 2. * np.pi, n)
    phi = np.linspace(0, 2. * np.pi, n)
    theta, phi = np.meshgrid(theta, phi)
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    return x, y, z
