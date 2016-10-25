import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def SE2(theta, trans):
    T = np.eye(3)
    c = np.cos(theta)
    s = np.sin(theta)
    T[:2, :2] = np.array([[c, -s], [s, c]])
    T[:2, -1] = trans
    return T


def SE2_transform_points(SE2, points):
    R = SE2[:2, :2]
    t = SE2[:2, -1]
    return np.dot(points, R.T) + t


def center_of_rot(theta, trans):
    half_theta = theta / 2
    s = np.sin(half_theta)
    c = np.cos(half_theta)
    A = np.array([[s, -c], [c, s]])
    C = 0.5 / s * np.dot(A, trans)
    return C


def cog(points):
    return np.mean(points, axis=0)


fig, axarr = plt.subplots(2, 2)
fig.set_facecolor('w')
axarr = np.ravel(axarr)

translations = np.array([[1, 1],
                         [-1, 1],
                         [1, -1],
                         [-1, -1]], dtype=float)
theta = np.pi / 3

points = [[1, 0], [0, -0.4], [0, 0.4]]
for i, ax in enumerate(axarr):
    triangle = Polygon(points, fill=None)
    ax.add_patch(triangle)
    points = np.array(points, dtype=float)
    trans = translations[i]
    points_new = SE2_transform_points(SE2(theta, trans), points)
    triangle_new = Polygon(points_new, fill=None, linestyle='--')
    ax.add_patch(triangle_new)
    center = center_of_rot(theta, trans)
    ax.plot(center[0], center[1], marker='+', color='k', markersize=10,
            markeredgewidth=2)
    ax.set_title('translation = ' + np.array_str(trans))

    ax.grid(True)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
plt.show()
