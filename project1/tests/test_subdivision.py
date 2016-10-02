import numpy as np
import matplotlib.pyplot as plt
from project1.bezier import (BezierDeCasteljau, BezierBernstein,
                             BezierSubdivision)

if __name__ == '__main__':
    points = np.array([[-4, 0], [-1, 4], [1, -4], [4, 0]], dtype=float)
    # points = np.array([[9, 0], [7, 3], [6, 4], [6, 6]], dtype=float)
    # points = np.array([[15, 0], [7, 10], [3, 4], [3, 6]], dtype=float)
    # points = np.array([[15, 0], [11, 5], [8, 6], [6, 6]], dtype=float)
    # points = np.array([[3, 0], [-1, 2], [-1, -4], [3, 6]], dtype=float)
    # points = np.array([[0, 0], [-4, 4], [-4, -12], [0, 0]], dtype=float)
    # points = np.array([[15, 0], [11, 5], [8, 6], [6, 6],
    #                    [12, -2], [9, -5], [6, -8], [2, -2]], dtype=float)
    fig, axarr = plt.subplots(2, 3)
    fig.set_facecolor('white')
    axarr = np.ravel(axarr)
    for i, ax in enumerate(axarr):
        depth = i + 1
        bezier = BezierSubdivision(depth=depth)
        curve = bezier.create_curve(points)
        ax.plot(points[:, 0], points[:, 1],
                ls='--', marker='+',
                markeredgewidth=2)
        ax.plot(curve[:, 0], curve[:, 1], marker='.')
        ax.set_aspect('equal')
        ax.set_title('divide: {}, points: {}'.format(depth, len(curve)))
        ax.margins(x=.1)
        ax.margins(y=.1)
    plt.show()
