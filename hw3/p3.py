import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def SO2(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]])


def SO2_transform_points(SO2, points):
    return np.dot(points, np.transpose(SO2))


def cog(points):
    return np.mean(points, axis=0)


fig, axarr = plt.subplots(2, 2)
fig.set_facecolor('w')
axarr = np.ravel(axarr)

theta_div = np.array([6, 4, 3, 2])

points = [[1, 0], [0, -0.4], [0, 0.4]]
for i, ax in enumerate(axarr):
    theta = np.pi / theta_div[i]
    triangle = Polygon(points, fill=None)
    ax.add_patch(triangle)
    points = np.array(points, dtype=float)
    points_new = SO2_transform_points(SO2(theta), points)
    triangle_new = Polygon(points_new, fill=None, linestyle='--')
    ax.add_patch(triangle_new)
    ax.set_title('theta = pi / ' + np.array_str(theta_div[i]))

    ax.grid(True)
    ax.set_xlim(-1, 1.5)
    ax.set_ylim(-1, 1.5)
    ax.set_aspect('equal')
plt.show()
