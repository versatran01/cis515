import numpy as np
from warnings import warn
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D
from project1.bezier import (BezierBase, BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


def update_line3d(line_3d, *args):
    x, y, z = args
    line_3d.set_data(np.array(x), np.array(y))
    line_3d.set_3d_properties(np.array(z))


class BezierBuilder:
    def __init__(self, ax_2d, ax_3d):
        """
        Key-bindings

            't' - toggle vertex markers on and off.
            '1, 2, 3' - Switch between different Bezier type
                        1 - Bernstein
                        2 - DeCasteljau
                        3 - Subdivision
        """
        self.marker_on = False

        points_style = {'marker': '+', 'linestyle': '--', 'markeredgewidth': 2}
        # 2d plot
        self.ax_2d = ax_2d
        points_2d = Line2D([], [], **points_style)
        self.line_points_2d = self.ax_2d.add_line(points_2d)
        self.points_x = self.line_points_2d.get_xdata()
        self.points_y = self.line_points_2d.get_ydata()
        self.canvas = self.ax_2d.figure.canvas

        # 3d plot
        self.ax_3d = ax_3d
        points_3d = Line3D([], [], [], **points_style)
        self.line_points_3d = self.ax_3d.add_line(points_3d)
        self.points_z = []

        # Specify Z
        self.press_xy = None
        circle = plt.Circle((0, 0), radius=0, facecolor='none', edgecolor='b')
        self.patch_circle = self.ax_2d.add_patch(circle)
        self.background_2d = None

        # Event handler for mouse clicking
        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_button_release = self.canvas.mpl_connect(
            'button_release_event',
            self.on_button_release)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)
        self.cid_motion_notify = self.canvas.mpl_connect('motion_notify_event',
                                                         self.on_motion_notify)

        # Create Bezier curve
        bezier_curve_2d = Line2D([], [])
        bezier_curve_3d = Line3D([], [], [])
        self.line_bezier_2d = self.ax_2d.add_line(bezier_curve_2d)
        self.line_bezier_3d = self.ax_3d.add_line(bezier_curve_3d)
        self.bezier = BezierSubdivision()

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
        self.canvas.update()
        self.canvas.flush_events()

    def on_button_release(self, event):
        if event.inaxes != self.ax_2d:
            return
        if self.press_xy is None:
            return

        self.press_xy = None
        self.background_2d = None

        self.points_z.append(self.patch_circle.radius)
        self.patch_circle.radius = 0

        # Draw 3d control points and also 3d Bezier curve
        update_line3d(self.line_points_3d,
                      self.points_x,
                      self.points_y,
                      self.points_z)
        update_line3d(self.line_bezier_3d,
                      *self.build_bezier(self.points_x,
                                         self.points_y,
                                         self.points_z))
        self.canvas.draw()

    def on_key_press(self, event):
        """
        :param event:
        :return:
        """
        pass

    def on_button_press(self, event):
        """
        :param event:
        :return:
        """
        # Ignore clicks outside axes
        if event.inaxes != self.ax_2d:
            return

        # Add control point
        self.points_x.append(event.xdata)
        self.points_y.append(event.ydata)
        self.line_points_2d.set_data(self.points_x, self.points_y)

        # Remember where we pressed
        self.press_xy = event.xdata, event.ydata

        # Rebuild Bezier curve 2d and update canvas 2d
        curve_2d_x, curve_2d_y = self.build_bezier(self.points_x, self.points_y)
        self.line_bezier_2d.set_data(curve_2d_x, curve_2d_y)

        # Draw canvas
        self.canvas.draw()
        # Save background
        self.background_2d = self.canvas.copy_from_bbox(self.ax_2d.bbox)

    def build_bezier(self, *args):
        points = self.bezier.create_curve(list(zip(*args)))
        return np.transpose(points)


if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax_2d = fig.add_subplot(121)
    ax_3d = fig.add_subplot(122, projection='3d')
    ax_2d.set_aspect('equal')
    ax_3d.set_aspect('equal')

    # Create BezierBuilder
    bezier_builder = BezierBuilder(ax_2d, ax_3d)

    plt.show()
