import matplotlib.pyplot as plt
import numpy as np

from project3.bspline import (natural_end_cond, quadratic_end_cond,
                              bessel_end_cond, notaknot_end_cond)
from project1.deboor import deboor_to_bezier
from project1.bezier import BezierSubdivision

x = [0, 0, 1, 1, 2, 2]
y = [0, 1, 1, 0, 0, 1]

interp_funs = {'natural': natural_end_cond, 'quadratic': quadratic_end_cond,
               'bessel': bessel_end_cond, 'not-a-knot': notaknot_end_cond}
point_style = {'color': 'k', 'linestyle': '-.', 'markersize': 10,
               'linewidth': 1, 'markeredgewidth': 2, 'marker': '+'}
deboor_style = {'linestyle': '--', 'marker': '.', 'markersize': 10}
bezier_style = {'linewidth': 2}

# Make X n-by-2
X = np.vstack((x, y)).T
X = np.array(X, float)

# Plots
fig1, ax1 = plt.subplots()
fig1.set_facecolor('w')
fig2, axarr = plt.subplots(2, 2, sharex=True, sharey=True)
fig2.set_facecolor('w')

bezier = BezierSubdivision()

ax1.plot(x, y, **point_style)

colors = 'bgrc'

for i, ((k, f), ax) in enumerate(zip(interp_funs.items(), axarr.ravel())):
    D = f(X)
    ax.plot(x, y, **point_style)
    ax.set_title(k)
    ax.plot(D[:, 0], D[:, 1], color=colors[i], **deboor_style)
    ax1.plot(D[:, 0], D[:, 1], color=colors[i], **deboor_style)

    beziers = deboor_to_bezier(D, last_point=True)
    points = []
    for b in beziers:
        p = bezier.create_curve(b)
        points.append(p)
    points = np.vstack(points)

    ax.plot(points[:, 0], points[:, 1], colors[i], label=k, **bezier_style)
    ax1.plot(points[:, 0], points[:, 1], colors[i], label=k, **bezier_style)
    ax.grid(True)

ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
ax1.set_aspect('equal')
ax1.grid(True)
plt.show()
