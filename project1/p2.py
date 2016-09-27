from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier import (BezierBase, BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


class BezierType(Enum):
    Bernstein = 1
    DeCasteljau = 2
    Subdivision = 3


class BezierBuilder:
    def __init__(self, ax):
        """
        Key-bindings

            't' - toggle vertex markers on and off.
            '1, 2, 3' -
        """
        self.marker_on = True

        self.ax = ax
        control_points = Line2D([], [],
                                linestyle='--', marker='+',
                                markeredgewidth=2)
        self.line_control_points = self.ax.add_line(control_points)
        self.control_points_x = self.line_control_points.get_xdata()
        self.control_points_y = self.line_control_points.get_ydata()
        self.canvas = self.line_control_points.figure.canvas

        # Event handler for mouse clicking
        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)

        # Create Bezier curve
        bezier_curve = Line2D([], [],
                              color=self.line_control_points.get_markeredgecolor())
        self.line_bezier = self.ax.add_line(bezier_curve)

        self.bezier = BezierSubdivision()

    def on_key_press(self, event):
        """
        :param event:
        :return:
        """

        if event.key == 't':
            self.marker_on = not self.marker_on
            if self.marker_on:
                self.line_bezier.set_marker('.')
            else:
                self.line_bezier.set_marker("")

        self.canvas.draw()

    def on_button_press(self, event):
        """
        :param event:
        :return:
        """
        # Ignore clicks outside axes
        if event.inaxes != self.ax:
            return

        # Add control point
        self.control_points_x.append(event.xdata)
        self.control_points_y.append(event.ydata)
        self.line_control_points.set_data(self.control_points_x,
                                          self.control_points_y)

        # Rebuild Bezier curve and update canvas
        self.line_bezier.set_data(*self.build_bezier())
        self.canvas.draw()

    def build_bezier(self):
        points = self.bezier.create_curve(
            list(zip(self.control_points_x, self.control_points_y)))
        x, y = np.transpose(points)
        return x, y


if __name__ == '__main__':
    # Initial setup
    fig, ax = plt.subplots()

    # Create BezierBuilder
    bezier_builder = BezierBuilder(ax)

    plt.show()
