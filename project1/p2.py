import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier import (BezierBase, BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


class BezierBuilder:
    def __init__(self, control_points, bezier):
        """
        :param control_points:
        :type control_points: Line2D
        :param bezier:
        :type bezier: BezierBase
        """
        self.control_points = control_points
        self.xp = list(control_points.get_xdata())
        self.yp = list(control_points.get_ydata())
        self.canvas = control_points.figure.canvas
        self.ax = control_points.axes

        # Event handler for mouse clicking
        self.cid_click = self.canvas.mpl_connect('button_press_event', self)

        # Create Bezier curve
        line_bezier = Line2D([], [],
                             color=control_points.get_markeredgecolor())
        self.bezier_curve = self.ax.add_line(line_bezier)

        self.bezier = bezier

    def __call__(self, event):
        """
        :param event:
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
        points = self.bezier.create_curve(list(zip(self.xp, self.yp)))
        x, y = np.transpose(points)
        return x, y


if __name__ == '__main__':
    # Initial setup
    fig, ax = plt.subplots()

    line = Line2D([], [],
                  linestyle='--', marker='+', markeredgewidth=2)
    ax.add_line(line)

    bezier = BezierSubdivision()
    # bezier = BezierDeCasteljau()
    # bezier = BezierBernstein()
    # Create BezierBuilder
    bezier_builder = BezierBuilder(line, bezier)

    plt.show()
