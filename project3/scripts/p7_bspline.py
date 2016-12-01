import matplotlib.pyplot as plt
from project3.bspline_builder import BsplineBuilder2D

if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Create BezierBuilder
    bspline_builder = BsplineBuilder2D(ax)

    plt.show()
