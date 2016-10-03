from __future__ import (print_function, division)
import sys
import os
sys.path.append(os.path.abspath('..'))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier_builder import BezierBuilder2D
from project1.bezier import (BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


def deboor_to_bezier(points, last_point=False):
    b_points = []
    d_points = np.array(points)
    num_dp = len(d_points)
    segments = []
    for i in range(len(d_points)):

        curr_point = d_points[i]
        if i == 0 or i == 1:
            b_points.append(curr_point)
        if i == 2:
            b_points.append((d_points[i - 1] + curr_point) / 2)
        if i == 3:
            b_points.append(
                d_points[i - 2] / 4.0 + 7 * d_points[i - 1] / 12.0 + curr_point / 6.0)
            segments.append(b_points[:4])

        if i >= 4 and last_point:
            if num_dp == 5:
                b_points.pop()
                b_points.append(((d_points[i - 1] + d_points[i - 2]) / 2.0 +
                                 b_points[-1]) / 2.0)
                b_points.append(b_points[-1])
                b_points.append((d_points[i - 1] + d_points[i - 2]) / 2)
                b_points.append(d_points[num_dp - 2])
                b_points.append(d_points[num_dp - 1])
                segments.pop()
                segments.append(b_points[:4])
                segments.append(b_points[-4:])

                break

            if num_dp == 6:
                j = num_dp - 2
                b_points.append(b_points[-1])
                b_points.append(d_points[j - 1] / 3 + 2 * d_points[j - 2] / 3)
                b_points.append(d_points[j - 2] / 3 + 2 * d_points[j - 1] / 3)
                b_points.append(
                    ((d_points[j] + d_points[j - 1]) / 2 + b_points[-1]) / 2)
                b_points.append(b_points[-1])
                b_points.append((d_points[j] + d_points[j - 1]) / 2)
                b_points.append(d_points[num_dp - 2])
                b_points.append(d_points[num_dp - 1])

                segments.append(b_points[:4])
                segments.append(b_points[-8:-4])
                segments.append(b_points[-4:])
                break

            if i < (num_dp - 2):
                b_points.append(b_points[-1])
                b_points.append(d_points[i - 1] / 3 + 2 * d_points[i - 2] / 3)
                b_points.append(d_points[i - 2] / 3 + 2 * d_points[i - 1] / 3)
                b_points.append(d_points[i - 2] / 6 + 4 * d_points[
                    i - 1] / 6 + curr_point / 6)
                segments.append(b_points[-4:])

            elif num_dp >= 7:
                j = num_dp - 1
                b_points.append(b_points[-1])
                b_points.append(2 * d_points[j - 3] / 3 + d_points[j - 2] / 3)
                b_points.append(2 * d_points[j - 2] / 3 + d_points[j - 3] / 3)
                b_points.append(
                    1 * d_points[j - 3] / 6 + 7 * d_points[j - 2] / 12 + 1 *
                    d_points[j - 1] / 4)
                b_points.append(b_points[-1])
                b_points.append((d_points[j - 2] + d_points[j - 1]) / 2)
                b_points.append(d_points[j - 1])
                b_points.append(d_points[j])
                segments.append(b_points[-8:-4])
                segments.append(b_points[-4:])
                break

        elif i >= 4:
            b_points.append(b_points[-1])
            b_points.append(d_points[i - 1] / 3 + 2 * d_points[i - 2] / 3)
            b_points.append(d_points[i - 2] / 3 + 2 * d_points[i - 1] / 3)
            b_points.append(d_points[i - 2] / 6 + 4 * d_points[i - 1] / 6 + curr_point / 6)
            segments.append(b_points[-4:])

    return np.array(b_points), np.array(segments)


class DeboorBuilder:
    def __init__(self, ax_2d):
        self.ax_2d = ax_2d
        self.canvas = self.ax_2d.figure.canvas

        self.control_points_style_deboor = {'marker': '+', 'linestyle': '--',
                                            'markeredgewidth': 2, 'color': 'm'}
        points_2d_deboor = Line2D([], [], **self.control_points_style_deboor)
        self.line_points_2d_deboor = self.ax_2d.add_line(points_2d_deboor)

        # deboor control points
        self.xp = []
        self.yp = []

        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)

        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)
        # bezier control points
        self.xp_bez = []
        self.yp_bez = []

        #segments
        self.segments = []

        self.control_points_style_bezier = {'marker': '+', 'linestyle': '-',
                                            'markeredgewidth': 2, 'color': 'b'}
        points_2d_bezier = Line2D([], [], **self.control_points_style_bezier)
        self.line_points_2d_bezier = self.ax_2d.add_line(points_2d_bezier)

        # Bezier curve stuff
        self.bezier_curve_style = {'color': 'r'}
        bezier_curve_2d = Line2D([], [], **self.bezier_curve_style)
        self.line_bezier_2d = []
        self.line_bezier_2d.append(self.ax_2d.add_line(bezier_curve_2d))

        self.marker_on = False
        self.last_point = False

        # Bezier curve method
        self.bezier = BezierSubdivision()
        self.bezier_type = 3
        self.num = 256
        self.depth = 6

    def create_curve(self, *args):
        """
        Given control points, build Bezier curve
        :param args: control points [x, y, z, ...]
        :return: Bezier curve
        """
        curve = self.bezier.create_curve(list(zip(*args)))
        return np.transpose(curve)

    def update_points_and_curve_2d(self):
        self.line_points_2d_deboor.set_data(self.xp, self.yp)
        self.line_points_2d_bezier.set_data(self.xp_bez, self.yp_bez)
        if len(self.segments) == 0:
            return

        if self.last_point and len(self.segments) != 4:
            self.line_bezier_2d.pop(-3)
            # print (self.segments)

        for line, seg in zip(self.line_bezier_2d, self.segments[:-1]):
            if self.last_point:
                print(line)
                print(seg)
            line.set_data(*self.create_curve(seg[:, 0], seg[:, 1]))

        seg = self.segments[-1]
        if self.last_point:
            self.line_bezier_2d[-1].set_data(*self.create_curve(seg[:, 0], seg[:, 1]))
            self.ax_2d.lines[-3].remove()
        else:
            new_curve = self.create_curve(seg[:, 0], seg[:, 1])
            bezier_curve_2d = Line2D(new_curve[0], new_curve[1], **self.bezier_curve_style)
            self.line_bezier_2d.append(self.ax_2d.add_line(bezier_curve_2d))

    def on_button_press(self, event):

        if event.inaxes != self.ax_2d:
            return
        if self.last_point:
            return

        self.xp.append(event.xdata)
        self.yp.append(event.ydata)
        bezier_points, self.segments = deboor_to_bezier(list(zip(self.xp, self.yp)))
        bezier_points = bezier_points.transpose()
        #self.segments = deboor_to_bezier(list(zip(self.xp, self.yp)))
        self.xp_bez = bezier_points[0]
        self.yp_bez = bezier_points[1]
        #
        #
        self.update_points_and_curve_2d()
        self.canvas.draw()

    def on_key_press(self, event):
        """
        :param event:
        :return:
        """
        if event.key == ' ':
            self.last_point = True
            bezier_points, self.segments = deboor_to_bezier(list(zip(self.xp, self.yp)), True)
            bezier_points = bezier_points.transpose()
            self.xp_bez = bezier_points[0]
            self.yp_bez = bezier_points[1]
            self.update_points_and_curve_2d()
            self.canvas.draw()

if __name__ == '__main__':
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    # Create DeboorBuilder
    deboor_builder = DeboorBuilder(ax)

    plt.show()
