import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier_builder import BezierBuilder2D
from project1.bezier import (BezierBernstein, BezierDeCasteljau,
                             BezierSubdivision)


class DeboorBuilder:
    def __init__(self, deboor_points):
        self.ax = ax
        self.deboor_points = deboor_points
        self.xp = list(deboor_points.get_xdata())
        self.yp = list(deboor_points.get_ydata())
        self.canvas = deboor_points.figure.canvas
        self.ax = deboor_points.axes
        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)
        self.xp_bez = list()
        self.yp_bez = list()
        self.pnt_cnt = 0
        self.cnt = 0
        self.last_point = False
        self.marker_on = False
        self.bezier_poly = Line2D([], [], linestyle='-', marker='o',
                                  markeredgewidth=2)
        self.line_bezier_poly = self.ax.add_line(self.bezier_poly)
        self.control_points = list()
        self.segments = list()
        self.seg_count = 0

        # Bezier curve stuff
        self.bezier_curve_style = {'color': 'r'}
        bezier_curve_2d = Line2D([], [], **self.bezier_curve_style)
        self.line_bezier_2d = self.ax.add_line(bezier_curve_2d)

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
        # self.line_points_2d.set_data(self.xp_bez, self.yp_bez)
        self.line_bezier_2d.set_data(
            *self.create_curve(self.xp_bez, self.yp_bez))

    def on_button_press(self, event):

        if event.inaxes != self.ax:
            return
        self.xp.append(event.xdata)
        self.yp.append(event.ydata)
        self.deboor_points.set_data(self.xp, self.yp)
        self.calcBezierControlPoints()
        self.bezier_poly.set_data(self.xp_bez, self.yp_bez)
        self.canvas.draw()

    def on_key_press(self, event):
        """
        :param event:
        :return:
        """
        if event.key == ' ':
            self.last_point = True

            if self.pnt_cnt >= 7:
                for i in range(0, 5):
                    self.xp_bez.pop()
                    self.yp_bez.pop()

                old_segment = self.segments.pop()
                self.cnt -= 5
                old_segment.pop()
                self.xp_bez.append(
                    self.xp[self.pnt_cnt - 4] / 6 + 7 * self.xp[
                        self.pnt_cnt - 3] / 12 + self.xp[self.pnt_cnt - 2] / 4)
                self.yp_bez.append(
                    self.yp[self.pnt_cnt - 4] / 6 + 7 * self.yp[
                        self.pnt_cnt - 3] / 12 + self.yp[self.pnt_cnt - 2] / 4)
                old_segment.append(
                    [self.xp_bez[self.cnt], self.yp_bez[self.cnt]])
                self.segments.append(old_segment)
                self.xp_bez.append(
                    self.xp[self.pnt_cnt - 4] / 6 + 7 * self.xp[
                        self.pnt_cnt - 3] / 12 + self.xp[self.pnt_cnt - 2] / 4)
                self.yp_bez.append(
                    self.yp[self.pnt_cnt - 4] / 6 + 7 * self.yp[
                        self.pnt_cnt - 3] / 12 + self.yp[self.pnt_cnt - 2] / 4)
                self.xp_bez.append(
                    (self.xp[self.pnt_cnt - 3] + self.xp[self.pnt_cnt - 2]) / 2)
                self.yp_bez.append(
                    (self.yp[self.pnt_cnt - 3] + self.yp[self.pnt_cnt - 2]) / 2)
                self.xp_bez.append(self.xp[self.pnt_cnt - 2])
                self.yp_bez.append(self.yp[self.pnt_cnt - 2])
                self.xp_bez.append(self.xp[self.pnt_cnt - 1])
                self.yp_bez.append(self.yp[self.pnt_cnt - 1])

                new_segment = list()
                for i in range(self.cnt + 1, self.cnt + 5):
                    new_segment.append([self.xp_bez[i], self.yp_bez[i]])

                self.segments.append(new_segment)

            elif self.pnt_cnt == 5 or self.pnt_cnt == 6:
                for i in range(0, 5):
                    self.xp_bez.pop()
                    self.yp_bez.pop()

                self.segments.pop()
                first_segment = self.segments.pop()
                first_segment.pop()

                new_point_x = (self.xp[self.pnt_cnt - 3] / 2 + self.xp[
                    self.pnt_cnt - 2] / 2 + first_segment[2][0]) / 2
                new_point_y = (self.yp[self.pnt_cnt - 3] / 2 + self.yp[
                    self.pnt_cnt - 2] / 2 + first_segment[2][1]) / 2
                first_segment.append([new_point_x, new_point_y])
                self.xp_bez.append(new_point_x)
                self.yp_bez.append(new_point_y)
                self.xp_bez.append(new_point_x)
                self.yp_bez.append(new_point_y)

                self.xp_bez.append(self.xp[self.pnt_cnt - 3] / 2 + self.xp[
                    self.pnt_cnt - 2] / 2)
                self.yp_bez.append(self.yp[self.pnt_cnt - 3] / 2 + self.yp[
                    self.pnt_cnt - 2] / 2)

                self.xp_bez.append(self.xp[self.pnt_cnt - 2])
                self.yp_bez.append(self.yp[self.pnt_cnt - 2])

                self.xp_bez.append(self.xp[self.pnt_cnt - 1])
                self.yp_bez.append(self.yp[self.pnt_cnt - 1])

                second_segment = list()
                for i in range(self.cnt - 4, self.cnt):
                    second_segment.append([self.xp_bez[i], self.yp_bez[i]])

                self.segments.append(first_segment)
                self.segments.append(second_segment)

            self.bezier_poly.set_data(self.xp_bez, self.yp_bez)
            self.update_points_and_curve_2d()
            self.canvas.draw()
            print self.segments

    def calcBezierControlPoints(self):

        self.pnt_cnt += 1

        if self.seg_count == 0:
            if self.pnt_cnt == 1 or self.pnt_cnt == 2:
                self.xp_bez.append(self.xp[self.pnt_cnt - 1])
                self.yp_bez.append(self.yp[self.pnt_cnt - 1])
            elif self.pnt_cnt == 3:
                self.xp_bez.append((self.xp[1] + self.xp[2]) / 2)
                self.yp_bez.append((self.yp[1] + self.yp[2]) / 2)
            else:
                self.xp_bez.append(
                    self.xp[self.pnt_cnt - 3] / 4 + 7 * self.xp[
                        self.pnt_cnt - 2] / 12 + self.xp[self.pnt_cnt - 1] / 6)
                self.yp_bez.append(
                    self.yp[self.pnt_cnt - 3] / 4 + 7 * self.yp[
                        self.pnt_cnt - 2] / 12 + self.yp[self.pnt_cnt - 1] / 6)
                new_segment = list()

                for i in range(self.cnt, self.cnt + 4):
                    new_segment.append([self.xp_bez[i], self.yp_bez[i]])
                self.segments.append(new_segment)
                print self.segments
                self.seg_count += 1
                self.cnt += 4

        else:
            self.xp_bez.append(self.xp_bez[self.cnt - 1])
            self.yp_bez.append(self.yp_bez[self.cnt - 1])
            self.xp_bez.append(self.xp[self.pnt_cnt - 2] / 3 + 2 * self.xp[
                self.pnt_cnt - 3] / 3)
            self.yp_bez.append(self.yp[self.pnt_cnt - 2] / 3 + 2 * self.yp[
                self.pnt_cnt - 3] / 3)
            self.xp_bez.append(self.xp[self.pnt_cnt - 3] / 3 + 2 * self.xp[
                self.pnt_cnt - 2] / 3)
            self.yp_bez.append(self.yp[self.pnt_cnt - 3] / 3 + 2 * self.yp[
                self.pnt_cnt - 2] / 3)
            self.xp_bez.append(
                self.xp[self.pnt_cnt - 3] / 6 + 4 * self.xp[
                    self.pnt_cnt - 2] / 6 + self.xp[self.pnt_cnt - 1] / 6)
            self.yp_bez.append(
                self.yp[self.pnt_cnt - 3] / 6 + 4 * self.yp[
                    self.pnt_cnt - 2] / 6 + self.yp[self.pnt_cnt - 1] / 6)
            new_segment = list()
            for i in range(self.cnt, self.cnt + 4):
                new_segment.append([self.xp_bez[i], self.yp_bez[i]])
            self.segments.append(new_segment)
            self.cnt += 4
            print self.segments[self.seg_count]
            self.seg_count += 1
        self.update_points_and_curve_2d()


if __name__ == '__main__':
    # Initial setup
    fig, ax = plt.subplots()

    line = Line2D([], [],
                  linestyle='--', marker='+', markeredgewidth=2)
    ax.add_line(line)

    deboor_builder = DeboorBuilder(line)

    plt.show()
