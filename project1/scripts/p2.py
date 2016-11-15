import sys
import os

import matplotlib.pyplot as plt
from project1.bezier_builder import BezierBuilder2D

sys.path.append(os.path.abspath('..'))

if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Create BezierBuilder
    bezier_builder = BezierBuilder2D(ax)

    plt.show()
