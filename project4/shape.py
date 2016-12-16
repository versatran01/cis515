import numpy as np
from collections import namedtuple

Shape = namedtuple('Shape', ['size', 'data'])


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


def flatten_grid(x, y, z):
    """
    Given x, y, z grid data of size mxn, make a list of point of size (mxn)x3
    """
    size = np.shape(x)
    xf = np.ravel(x)
    yf = np.ravel(y)
    zf = np.ravel(z)
    data = np.vstack((xf, yf, zf)).T
    return Shape(size=size, data=data)


def restore_grid(data, size):
    """
    Given data and size, restore original grid
    :param data: 3x(mxn) points
    :param size: tuple of original grid shape
    :return: x, y, z grid data of size mxn
    """
    x, y, z = data.T
    return np.reshape(x, size), np.reshape(y, size), np.reshape(z, size)
