import logging
import numpy as np
from scipy.special import binom
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class Bezier:
    def __init__(self, num=100):
        self.num = num
        self.t = np.linspace(0, 1, num=num)

    def __call__(self, points):
        m = len(points)
        curve = np.zeros((self.num, 2))
        for k in range(m):
            curve += np.outer(Bernstein(m - 1, k)(self.t), points[k])
        return curve


class Bernstein:
    def __init__(self, n, k):
        self.n_choose_k = binom(n, k)
        self.n = n
        self.k = k

    def __call__(self, t):
        return self.n_choose_k * (t ** self.k) * ((1 - t) ** (self.n - self.k))


class BezierBuilder:
    def __init__(self, control_points):
        """
        :param control_points:
        :type control_points: Line2D
        """
        self.control_points = control_points
        self.xp = list(control_points.get_xdata())
        self.yp = list(control_points.get_ydata())
        self.canvas = control_points.figure.canvas
        self.ax = control_points.get_axes()

        # Event handler for mouse clicking
        self.cid_click = self.canvas.mpl_connect('button_press_event', self)

        # Create Bezier curve
        line_bezier = Line2D([], [],
                             color=control_points.get_markeredgecolor())
        self.bezier_curve = self.ax.add_line(line_bezier)

        self.bezier = Bezier(num=100)

    def __call__(self, event):
        """
        :param event:
        :type event: matplotlib.backend_bases.Event
        :return:
        """
        # Ignore clicks outside axes
        if event.inaxes != self.ax:
            return

        # Add control point
        self.xp.append(event.xdata)
        self.yp.append(event.ydata)
        self.control_points.set_data(self.xp, self.yp)

        # Rebuild Bezier curve and update canvas
        self.bezier_curve.set_data(*self.build_bezier())
        self.canvas.draw()

    def build_bezier(self):
        points = self.bezier(list(zip(self.xp, self.yp)))
        x, y = np.transpose(points)
        return x, y


if __name__ == '__main__':
    # Initial setup
    fig, ax = plt.subplots()

    line = Line2D([], [],
                  linestyle='--', marker='x', markeredgewidth=2)
    ax.add_line(line)
    # Create BezierBuilder
    bezier_builder = BezierBuilder(line)

    plt.show()
