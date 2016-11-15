import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from enum import Enum


class BuilderState(Enum):
    add = 1
    delete = 2
    move = 3
    view = 4


class Bspline(object):
    def __init__(self):
        pass


class BsplineBuilder2D(object):
    def __init__(self, ax_2d):
        self.ax_2d = ax_2d
        self.canvas = self.ax_2d.figure.canvas
        # default to add new points
        self.state = BuilderState.add

        self.points_x = []
        self.points_y = []
        self.history = []

        self.points_2d_style = {'marker': '+', 'linestyle': '-',
                                'markeredgewidth': 2, 'color': 'b'}
        points_2d = Line2D(self.points_x, self.points_y, **self.points_2d_style)
        self.line_points_2d = self.ax_2d.add_line(points_2d)

        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)

    def on_button_press(self, event):
        # Ignore clicks outside axes
        if event.inaxes != self.ax_2d:
            return

        if self.state == BuilderState.view:
            return

        if self.state == BuilderState.add:
            # Add control point
            self.points_x.append(event.xdata)
            self.points_y.append(event.ydata)

            self.line_points_2d.set_data(self.points_x, self.points_y)

            n = len(self.points_x)
            self.ax_2d.set_title('add point [{0}]: ({1:.2f}, {2:.2f})'.format(
                n, event.xdata, event.ydata))
        elif self.state == BuilderState.delete:
            pass
        elif self.state == BuilderState.move:
            pass

        # Draw canvas
        self.canvas.draw()

    def on_key_press(self, event):
        if event.key == 't':
            raise NotImplementedError('t is not implemented')
        elif event.key == 'r':
            self.reset()
            self.ax_2d.set_title('reset, press [a] to start adding points')
        elif event.key == 'u':
            # TODO: change this to generic undo/redo action by restoring states
            self.undo_add()
        elif event.key == 'a':
            self.state = BuilderState.add
            self.ax_2d.set_title('click to add new points')
        elif event.key == 'd':
            self.state = BuilderState.delete
            self.ax_2d.set_title('click on a point to delete')
        elif event.key == 'm':
            self.state = BuilderState.move
            self.ax_2d.set_title('drag a point to move')
        elif event.key == 'v':
            self.state = BuilderState.view
            self.ax_2d.set_title('view only')
        else:
            self.ax_2d.set_title('key: {} is not supported'.format(event.key))

        self.canvas.draw()

    def reset(self):
        self.points_x = []
        self.points_y = []
        self.line_points_2d.set_data(self.points_x, self.points_y)

    def undo_add(self):
        if len(self.points_x) == 0:
            self.ax_2d.set_title('no points to remove.')
            return

        n = len(self.points_x)
        x = self.points_x.pop()
        y = self.points_y.pop()
        self.line_points_2d.set_data(self.points_x, self.points_y)

        self.ax_2d.set_title(
            'remove point [{0}]: ({1:.2f}, {2:.2f})'.format(n, x, y))


if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Create BezierBuilder
    bspline_builder = BsplineBuilder2D(ax)

    plt.show()
