import numpy as np
import matplotlib.pyplot as plt


def de_casteljau(points, t):
    points = np.array(points)
    n = len(points)
    m = n - 1
    for k in range(m):
        for i in range(m - k):
            points[i] = (1 - t) * points[i] + t * points[i+1]
    return points[0]


control_points = np.array([(0, 0), (0.25, 1), (1.25, 1), (1.5, 0)])
ts = np.linspace(0, 1, 100)
curve = np.zeros((len(ts), 2))
for i, t in enumerate(ts):
    curve[i] = de_casteljau(control_points, t)

fig, ax = plt.subplots()
ax.plot(control_points[:, 0], control_points[:, 1])
ax.plot(curve[:, 0], curve[:, 1])
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)
plt.show()
