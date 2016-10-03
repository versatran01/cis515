import numpy as np
from matplotlib.lines import Line2D

from project1.bezier_builder import BezierBuilder2D
from project1.deboor import deboor_to_bezier


class DeboorBuilder2D(BezierBuilder2D):
    def __init__(self, ax_2d):
        super(DeboorBuilder2D, self).__init__(ax_2d)

        # curves and their corresponding control points
        self.segments = []
        self.line_bezier_points_2d = []
        self.line_bezier_curve_2d = []
        self.bezier_points_style = {'linestyle': '--', 'marker': 'o'}

        self.last_point = False

    def create_curve(self, *args):
        """
        Given control points, build Bezier curve
        :param args: control points [x, y, z, ...]
        :return: Bezier curve
        """
        curve = self.bezier.create_curve(list(zip(*args)))
        return np.transpose(curve)

    def update_points_and_curve_2d(self):
        # Update de Boor control points
        self.line_points_2d.set_data(self.points_x, self.points_y)

        # Simply do nothing when segments is empty
        if len(self.segments) == 0:
            return

        # Update each segments
        for i, points in enumerate(self.line_bezier_points_2d):
            seg = self.segments[i]
            curve = self.line_bezier_curve_2d[i]
            points.set_data(seg[:, 0], seg[:, 1])
            curve.set_data(*self.create_curve(seg[:, 0], seg[:, 1]))

        # Create new segment when it is not the last point
        if not self.last_point:
            seg = self.segments[-1]
            bezier_points_2d = Line2D(seg[:, 0], seg[:, 1],
                                      **self.bezier_points_style)
            curve = self.create_curve(seg[:, 0], seg[:, 1])
            bezier_curve_2d = Line2D(curve[0], curve[1],
                                     **self.bezier_curve_style)
            self.line_bezier_curve_2d.append(
                self.ax_2d.add_line(bezier_curve_2d))
            self.line_bezier_points_2d.append(
                self.ax_2d.add_line(bezier_points_2d))

    def on_button_press(self, event):
        if event.inaxes != self.ax_2d:
            return
        if self.last_point:
            return

        # Add control point
        self.points_x.append(event.xdata)
        self.points_y.append(event.ydata)

        # Update segments, usually the last two are modified
        self.segments = deboor_to_bezier(
            list(zip(self.points_x, self.points_y)))
        self.update_points_and_curve_2d()
        
        self.canvas.draw()

    def on_key_press(self, event):
        """
        :param event:
        :return:
        """
        if event.key == ' ':
            self.last_point = True
            # TODO: maybe deboor stuff should be put into a class, since last
            # point only modifies the last two segments, we don't need to
            # calculate all the previous segments again
            self.segments = deboor_to_bezier(
                list(zip(self.points_x, self.points_y)), True)
            self.update_points_and_curve_2d()
        elif event.key == 'r':
            self.reset()

        self.canvas.draw()

    def reset(self):
        self.points_x = []
        self.points_y = []
        self.line_points_2d.set_data([], [])
        for points in self.line_bezier_points_2d:
            points.remove()
        for curve in self.line_bezier_curve_2d:
            curve.remove()
        self.line_bezier_curve_2d = []
        self.line_bezier_points_2d = []
        self.last_point = False
