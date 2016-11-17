import matplotlib.pyplot as plt
import numpy as np

from project3.bspline import (natural_end_cond, quadratic_end_cond,
                              bessel_end_cond, knot_end_cond)
from project1.deboor import deboor_to_bezier
from project1.bezier import BezierSubdivision

x = [0, 0, 1, 1, 2, 2]
y = [0, 1, 1, 0, 1, 0]

interp_funs = {'natural': natural_end_cond, 'quadratic': quadratic_end_cond,
               'bessel': bessel_end_cond, 'knot': knot_end_cond}

X = np.vstack((x, y)).T
X = np.array(X, float)
D1 = natural_end_cond(X)
D2 = quadratic_end_cond(X)
D3 = bessel_end_cond(X)

fig, ax = plt.subplots()
fig.set_facecolor('w')

bezier = BezierSubdivision()
ax.plot(x, y, 'bo-')
colors = 'grmc'
for i, (k, f) in enumerate(interp_funs.items()):
    D = f(X)
    ax.plot(D[:, 0], D[:, 1], 'o-')
    beziers = deboor_to_bezier(D, last_point=True)
    for b in beziers:
        points = bezier.create_curve(b)
        ax.plot(points[:, 0], points[:, 1], colors[i])

ax.set_aspect('equal')
ax.grid(True)
plt.show()
