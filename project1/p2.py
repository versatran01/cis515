import numpy as np
from warnings import warn
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier import (BezierBase, BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


class BezierBuilder:
    def __init__(self, ax):
        """
        Key-bindings

            't' - toggle vertex markers on and off.
            '1, 2, 3' - Switch between different Bezier type
                        1 - Bernstein
                        2 - DeCasteljau
                        3 - Subdivision
        """
        self.marker_on = False

        self.ax = ax
        control_points = Line2D([], [],
                                linestyle='--', marker='+', color='m',
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
                              color='b')
        self.line_bezier = self.ax.add_line(bezier_curve)

        # Number of points/depth
        self.depth = 6
        self.num = 2 ** (self.depth + 1)

        # Bezier type, default to subdivision
        self.bezier_type = 3
        self.bezier = BezierSubdivision(depth=self.depth)
        self.ax.set_title('Subdivision')

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
        elif event.key == '+':
            raise NotImplementedError
        elif event.key == '-':
            raise NotImplementedError
        else:
            try:
                bezier_type = int(event.key)
                # only redraw if it's a different type
                if bezier_type > 3:
                    warn("not a valid bezier type")
                elif bezier_type != self.bezier_type:
                    if bezier_type == 1:
                        self.bezier = BezierBernstein(num=self.num)
                        self.line_bezier.set_color('r')
                        self.ax.set_title('Bernstein')
                    elif bezier_type == 2:
                        self.bezier = BezierDeCasteljau(num=self.num)
                        self.line_bezier.set_color('g')
                        self.ax.set_title('DeCasteljau')
                    elif bezier_type == 3:
                        self.bezier = BezierSubdivision(depth=self.depth)
                        self.line_bezier.set_color('b')
                        self.ax.set_title('Subdivision')
                    else:
                        pass

                    self.bezier_type = bezier_type
                    if len(self.control_points_x) > 0:
                        self.line_bezier.set_data(*self.build_bezier())

            except ValueError:
                pass

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
