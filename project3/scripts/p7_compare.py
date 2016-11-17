import matplotlib.pyplot as plt
import numpy as np

from project3.bspline import (natural_end_cond, quadratic_end_cond,
                              bessel_end_cond, notaknot_end_cond)
from project1.deboor import deboor_to_bezier
from project1.bezier import BezierSubdivision

x = [0, 0, 1, 1, 2, 2]
y = [0, 1, 1, 0, 0, 1]

interp_funs = {'natural': natural_end_cond, 'quadratic': quadratic_end_cond,
               'bessel': bessel_end_cond, 'knot': notaknot_end_cond}

X = np.vstack((x, y)).T
X = np.array(X, float)

fig, ax = plt.subplots()
fig.set_facecolor('w')

bezier = BezierSubdivision()

ax.plot(x, y, 'k+-', markersize=10, linewidth=2, markeredgewidth=2)
colors = 'bgrc'

for i, (k, f) in enumerate(interp_funs.items()):
    D = f(X)
    ax.plot(D[:, 0], D[:, 1], '.--', color=colors[i], markersize=10)
    beziers = deboor_to_bezier(D, last_point=True)
    points = []
    for b in beziers:
        p = bezier.create_curve(b)
        points.append(p)
    points = np.vstack(points)
    ax.plot(points[:, 0], points[:, 1], colors[i], label=k)

ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
          ncol=4, mode="expand", borderaxespad=0.)
ax.set_aspect('equal')
ax.grid(True)
plt.show()
