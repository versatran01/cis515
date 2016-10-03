import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Line3D
from project1.bezier import (BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


class BezierBuilder2D(object):
    def __init__(self, ax_2d):
        self.marker_on = False

        self.ax_2d = ax_2d
        self.canvas = self.ax_2d.figure.canvas

        # Bezier control points in 2D
        self.control_points_style = {'marker': '+', 'linestyle': '--',
                                     'markeredgewidth': 2, 'color': 'm'}
        points_2d = Line2D([], [], **self.control_points_style)
        self.line_points_2d = self.ax_2d.add_line(points_2d)
        self.points_x = []
        self.points_y = []

        # Bezier curve in 2D
        self.bezier_curve_style = {'color': 'b'}
        bezier_curve_2d = Line2D([], [], **self.bezier_curve_style)
        self.line_bezier_2d = self.ax_2d.add_line(bezier_curve_2d)

        # Bezier curve method
        self.bezier = BezierSubdivision()
        self.bezier_type = 3
        self.num = 256
        self.divide = 6

        # Event handler for mouse clicking
        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)

    def create_curve(self, *args):
        """
        Given control points, build Bezier curve
        :param args: control points [x, y, z, ...]
        :return: Bezier curve
        """
        curve = self.bezier.create_curve(list(zip(*args)))
        return np.transpose(curve)

    def reset(self):
        self.points_x = []
        self.points_y = []
        self.line_bezier_2d.set_data([], [])
        self.line_points_2d.set_data([], [])

    def update_points_and_curve_2d(self):
        self.line_points_2d.set_data(self.points_x, self.points_y)
        self.line_bezier_2d.set_data(
            *self.create_curve(self.points_x, self.points_y))

    def on_button_press(self, event):
        # Ignore clicks outside axes
        if event.inaxes != self.ax_2d:
            return

        # Add control point
        self.points_x.append(event.xdata)
        self.points_y.append(event.ydata)

        # Build Bezier curve 2d
        self.update_points_and_curve_2d()

        # Draw canvas
        self.canvas.draw()

    def on_key_press(self, event):
        if event.key == 't':
            self.marker_on = not self.marker_on
            if self.marker_on:
                marker = '.'
            else:
                marker = ''
            self.set_curve_marker(marker)
        elif event.key == 'r':
            self.reset()

        self.canvas.draw()

    def set_curve_marker(self, marker):
        self.line_bezier_2d.set_marker(marker)


class BezierBuilder3D(BezierBuilder2D):
    def __init__(self, ax_2d, ax_3d):
        super(BezierBuilder3D, self).__init__(ax_2d)
        # super().__init__(ax_2d)

        self.ax_3d = ax_3d

        # Bezier control points in 3D
        points_3d = Line3D([], [], [], **self.control_points_style)
        self.line_points_3d = self.ax_3d.add_line(points_3d)
        self.points_z = []

        # Bezier curve in 3D
        bezier_curve_3d = Line3D([], [], [], **self.bezier_curve_style)
        self.line_bezier_3d = self.ax_3d.add_line(bezier_curve_3d)

        # Stuff related to specify z
        self.press_xy = None
        circle = plt.Circle((0, 0), radius=0, facecolor='none', edgecolor='b')
        self.patch_circle = self.ax_2d.add_patch(circle)
        self.background_2d = None

        # Event handler for motion and release
        self.cid_button_release = self.canvas.mpl_connect(
            'button_release_event', self.on_button_release)
        self.cid_motion_notify = self.canvas.mpl_connect('motion_notify_event',
                                                         self.on_motion_notify)

    def on_motion_notify(self, event):
        if self.press_xy is None:
            return
        if event.inaxes != self.ax_2d:
            return

        x_press, y_press = self.press_xy
        self.patch_circle.center = x_press, y_press
        # Z of this point is the radius of the circle
        r = np.hypot(event.xdata - x_press, event.ydata - y_press)
        self.patch_circle.radius = r

        # Speed update drawing (only draw the circle)
        self.canvas.restore_region(self.background_2d)
        self.ax_2d.draw_artist(self.patch_circle)
        #self.canvas.blit(self.ax_2d.bbox)


    def on_button_release(self, event):
        if event.inaxes != self.ax_2d:
            return
        if self.press_xy is None:
            return

        self.press_xy = None
        self.background_2d = None

        self.points_z.append(self.patch_circle.radius)
        self.patch_circle.radius = 0

        self.update_points_and_curve_3d()

        # Draw 3d control points and also 3d Bezier curve
        self.canvas.draw()

    def set_curve_marker(self, marker):
        super(BezierBuilder3D, self).set_curve_marker(marker)

        self.line_bezier_3d.set_marker(marker)

    def on_button_press(self, event):
        # Ignore clicks outside axes
        if event.inaxes != self.ax_2d:
            return

        # Call super class method to handle drawing in 2d
        super(BezierBuilder3D, self).on_button_press(event)
        # super().on_button_press(event)

        # Remember where we pressed
        self.press_xy = event.xdata, event.ydata
        # Save background
        self.background_2d = self.canvas.copy_from_bbox(self.ax_2d.bbox)

    def reset(self):
        super(BezierBuilder3D, self).reset()

        self.points_z = []
        self.update_line3d(self.line_points_3d, [], [], [])
        self.update_line3d(self.line_bezier_3d, [], [], [])

    def update_points_and_curve_3d(self):
        self.update_line3d(self.line_points_3d,
                           self.points_x,
                           self.points_y,
                           self.points_z)
        self.update_line3d(self.line_bezier_3d,
                           *self.create_curve(self.points_x,
                                              self.points_y,
                                              self.points_z))

    @staticmethod
    def update_line3d(line_3d, *args):
        x, y, z = args
        line_3d.set_data(np.array(x), np.array(y))
        line_3d.set_3d_properties(np.array(z))
