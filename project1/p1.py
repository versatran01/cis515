import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class DeboorBuilder:

    def __init__(self, deboor_points):
        self.ax = ax
        self.deboor_points = deboor_points
        self.xp = list(deboor_points.get_xdata())
        self.yp = list(deboor_points.get_ydata())
        self.canvas = deboor_points.figure.canvas
        self.ax = deboor_points.axes
        self.cid_button_press = self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.xp_bez = list()
        self.yp_bez = list()
        self.pnt_cnt = 0
        self.cnt = 0
        self.last_point = False
        self.marker_on = False
        self.bezier_poly = Line2D([], [], linestyle='-', marker='o', markeredgewidth=2)
        self.line_bezier_poly = self.ax.add_line(self.bezier_poly)
        self.control_points = list()
        self.segments = list()
        self.seg_count = 0

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

            for i in range(0, 5):
                self.xp_bez.pop()
                self.yp_bez.pop()

            old_segment = self.segments.pop()
            self.cnt -= 5
            old_segment.pop()
            self.xp_bez.append(self.xp[self.pnt_cnt - 4] / 6 + 7 * self.xp[self.pnt_cnt - 3] / 12 + self.xp[self.pnt_cnt - 2] / 4)
            self.yp_bez.append(self.yp[self.pnt_cnt - 4] / 6 + 7 * self.yp[self.pnt_cnt - 3] / 12 + self.yp[self.pnt_cnt - 2] / 4)
            old_segment.append([self.xp_bez[self.cnt], self.yp_bez[self.cnt]])
            self.segments.append(old_segment)
            self.xp_bez.append(self.xp[self.pnt_cnt - 4] / 6 + 7 * self.xp[self.pnt_cnt - 3] / 12 + self.xp[self.pnt_cnt - 2] / 4)
            self.yp_bez.append(self.yp[self.pnt_cnt - 4] / 6 + 7 * self.yp[self.pnt_cnt - 3] / 12 + self.yp[self.pnt_cnt - 2] / 4)
            self.xp_bez.append((self.xp[self.pnt_cnt - 3] + self.xp[self.pnt_cnt - 2]) / 2)
            self.yp_bez.append((self.yp[self.pnt_cnt - 3] + self.yp[self.pnt_cnt - 2]) / 2)
            self.xp_bez.append(self.xp[self.pnt_cnt - 2])
            self.yp_bez.append(self.yp[self.pnt_cnt - 2])
            self.xp_bez.append(self.xp[self.pnt_cnt - 1])
            self.yp_bez.append(self.yp[self.pnt_cnt - 1])

            new_segment = list()
            for i in range(self.cnt+1, self.cnt+5):
                new_segment.append([self.xp_bez[i], self.yp_bez[i]])

            self.segments.append(new_segment)


        self.bezier_poly.set_data(self.xp_bez, self.yp_bez)
        self.canvas.draw()
        print self.segments
    def calcBezierControlPoints(self):

        self.pnt_cnt += 1

        if self.seg_count == 0:
            if self.pnt_cnt == 1 or self.pnt_cnt == 2:
                self.xp_bez.append(self.xp[self.pnt_cnt-1])
                self.yp_bez.append(self.yp[self.pnt_cnt-1])
            elif self.pnt_cnt == 3:
                self.xp_bez.append((self.xp[1] + self.xp[2])/2)
                self.yp_bez.append((self.yp[1] + self.yp[2])/2)
            else:
                self.xp_bez.append(self.xp[self.pnt_cnt-3]/4 + 7*self.xp[self.pnt_cnt-2]/12 + self.xp[self.pnt_cnt-1]/6)
                self.yp_bez.append(self.yp[self.pnt_cnt-3]/4 + 7*self.yp[self.pnt_cnt-2]/12 + self.yp[self.pnt_cnt-1]/6)
                new_segment = list()

                for i in range(self.cnt, self.cnt+4):
                    new_segment.append([self.xp_bez[i], self.yp_bez[i]])
                self.segments.append(new_segment)
                print self.segments
                self.seg_count += 1
                self.cnt += 4

        else:
            self.xp_bez.append(self.xp_bez[self.cnt - 1])
            self.yp_bez.append(self.yp_bez[self.cnt - 1])
            self.xp_bez.append(self.xp[self.pnt_cnt - 2] / 3 + 2 * self.xp[self.pnt_cnt - 3] / 3)
            self.yp_bez.append(self.yp[self.pnt_cnt - 2] / 3 + 2 * self.yp[self.pnt_cnt - 3] / 3)
            self.xp_bez.append(self.xp[self.pnt_cnt - 3] / 3 + 2 * self.xp[self.pnt_cnt - 2] / 3)
            self.yp_bez.append(self.yp[self.pnt_cnt - 3] / 3 + 2 * self.yp[self.pnt_cnt - 2] / 3)
            self.xp_bez.append(self.xp[self.pnt_cnt - 3] / 6 + 4 * self.xp[self.pnt_cnt - 2] / 6 + self.xp[self.pnt_cnt - 1] / 6)
            self.yp_bez.append(self.yp[self.pnt_cnt - 3] / 6 + 4 * self.yp[self.pnt_cnt - 2] / 6 + self.yp[self.pnt_cnt - 1] / 6)
            new_segment = list()
            for i in range(self.cnt, self.cnt+4):
                new_segment.append([self.xp_bez[i], self.yp_bez[i]])
            self.segments.append(new_segment)
            self.cnt += 4
            print self.segments[self.seg_count]
            self.seg_count += 1









            # self.xp_bez.append((self.xp_bez[self.pnt_cnt-1] + self.xp_bez[self.pnt_cnt-2])/2)
            # self.yp_bez.append((self.yp_bez[self.pnt_cnt-1] + self.yp_bez[self.pnt_cnt - 2]) / 2)
            # self.xp_bez.insert(self.pnt_cnt-1, (self.xp_bez[self.pnt_cnt-2] + self.xp_bez[self.pnt_cnt-1])/2)
            # self.yp_bez.insert(self.pnt_cnt-1, (self.yp_bez[self.pnt_cnt-2] + self.yp_bez[self.pnt_cnt - 1]) / 2)
            #print self.xp_bez
            #print self.yp_bez





if __name__ == '__main__':
    # Initial setup
    fig, ax = plt.subplots()

    line = Line2D([], [],
                  linestyle='--', marker='+', markeredgewidth=2)
    ax.add_line(line)

    deboor_builder = DeboorBuilder(line)

    plt.show()