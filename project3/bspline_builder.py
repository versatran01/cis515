from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from project1.bezier import BezierSubdivision
from project1.deboor import deboor_to_bezier
from project3.bspline import EndCondition, curve_interp


class BuilderState(Enum):
    """
    State of the interactive window
    """
    add = 1
    delete = 2
    move = 3
    view = 4


class BsplineBuilder2D(object):
    def __init__(self, ax_2d):
        self.ax_2d = ax_2d
        self.canvas = self.ax_2d.figure.canvas
        # Default to add new points
        self.state = BuilderState.add

        # End condition
        self.end_cond = EndCondition.natural

        # Use subdivison algorithm to create bezier points
        self.bezier = BezierSubdivision()

        # Data points
        self.x = []
        self.y = []
        self.points_style = {'marker': '+', 'linestyle': '-.',
                             'markeredgewidth': 2, 'color': 'k',
                             'markersize': 10}
        points_2d = Line2D([], [], **self.points_style)
        self.line_points_2d = self.ax_2d.add_line(points_2d)

        # DeBoor points
        self.deboor_style = {'marker': '.', 'linestyle': '--',
                             'markersize': 10, 'color': 'b'}
        deboor_2d = Line2D([], [], **self.deboor_style)
        self.line_deboor_2d = self.ax_2d.add_line(deboor_2d)

        # Bspline points
        self.bspline_style = {'linestyle': '-', 'color': 'b', 'linewidth': 2}
        bspline_2d = Line2D([], [], **self.bspline_style)
        self.line_bspline_2d = self.ax_2d.add_line(bspline_2d)

        # Callbacks
        self.cid_button_press = self.canvas.mpl_connect('button_press_event',
                                                        self.on_button_press)
        self.cid_key_press = self.canvas.mpl_connect('key_press_event',
                                                     self.on_key_press)

    def add_points(self, event):
        # Add control point
        self.x.append(event.xdata)
        self.y.append(event.ydata)

        self.update_lines()

        self.ax_2d.set_title('add point [{0}]: ({1:.2f}, {2:.2f})'.format(
            self.n_points, event.xdata, event.ydata))

    @property
    def n_points(self):
        return len(self.x)

    def create_deboor(self):
        X = np.vstack((self.x, self.y)).T
        D = curve_interp(X, self.end_cond)
        return D

    def create_bspline(self, D):
        B = deboor_to_bezier(D, last_point=True)
        P = []
        for b in B:
            p = self.bezier.create_curve(b)
            P.append(p)
        return np.vstack(P)

    def update_lines(self):
        self.line_points_2d.set_data(self.x, self.y)

        n = self.n_points
        if n < 2:
            self.line_deboor_2d.set_data([], [])
            self.line_bspline_2d.set_data([], [])
        elif n == 2:
            # If we only have two points, just draw a straight line
            self.line_deboor_2d.set_data(self.x, self.y)
            self.line_bspline_2d.set_data(self.x, self.y)
        else:
            # Create deboor control points
            D = self.create_deboor()
            self.line_deboor_2d.set_data(D[:, 0], D[:, 1])
            P = self.create_bspline(D)
            self.line_bspline_2d.set_data(P[:, 0], P[:, 1])

    def reset(self):
        self.x = []
        self.y = []
        self.line_points_2d.set_data([], [])
        self.line_deboor_2d.set_data([], [])
        self.ax_2d.set_title('reset, press [a] to start adding points')

    def undo_add(self):
        if len(self.x) == 0:
            self.ax_2d.set_title('no points to remove.')
            return

        n = len(self.x)
        x = self.x.pop()
        y = self.y.pop()

        self.ax_2d.set_title(
            'remove point [{0}]: ({1:.2f}, {2:.2f})'.format(n, x, y))

        self.update_lines()

    def on_button_press(self, event):
        # Ignore clicks outside axes
        if event.inaxes != self.ax_2d:
            return

        if self.state == BuilderState.view:
            # Do nothing when we are only viewing
            return
        elif self.state == BuilderState.add:
            self.add_points(event)
        elif self.state == BuilderState.delete:
            pass
        elif self.state == BuilderState.move:
            pass

        # Draw canvas
        self.canvas.draw()

    def on_key_press(self, event):
        if event.key == 't':
            # toggle points
            raise NotImplementedError('t is not implemented')
        elif event.key == 'r':
            self.reset()
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
        elif event.key == 'p':
            # show control polygon
            raise NotImplementedError('p is not implemented')
        else:
            self.ax_2d.set_title('key: {} is not supported'.format(event.key))

        self.canvas.draw()


if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Create BezierBuilder
    bspline_builder = BsplineBuilder2D(ax)

    plt.show()
