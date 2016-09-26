import numpy as np
import matplotlib.pyplot as plt


def subdivision(points, depth=6, t=0.5):
    curve = subdivision_rec(points, depth, t=t)
    curve_full = [points[0]] + curve + [points[-1]]
    return np.array(curve_full)


def subdivision_rec(points, depth, t=0.5):
    # make a copy of points since we will modify them later
    points = np.array(points)
    n = len(points)  # number of points
    d = len(points[0])  # dimension

    upper = np.zeros((n, d))
    lower = np.zeros_like(upper)

    m = n - 1
    for k in range(m):
        upper[k] = points[0]
        lower[k] = points[m - k]

        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i + 1]

    # add last point to ud and ld
    bm = points[0]
    upper[-1] = bm
    lower[-1] = bm
    # flip lower to ensure correct sequence
    lower = np.flipud(lower)

    if depth == 0:
        return [bm]
    return subdivision_rec(upper, depth - 1) + [bm] \
           + subdivision_rec(lower, depth - 1)


control_points = np.array([(0, 0), (0, 1), (1, 1), (1, 0)], float)
curve = subdivision(control_points, depth=8)
fig, ax = plt.subplots()
ax.set_xlim(-1, 1.5)
ax.set_ylim(-1, 1.5)
ax.plot(control_points[:, 0], control_points[:, 1])
print(len(curve))
ax.plot(curve[:, 0], curve[:, 1])
plt.show()
