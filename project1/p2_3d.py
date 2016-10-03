import sys
import os
sys.path.append(os.path.abspath('..'))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from project1.bezier_builder import BezierBuilder3D

if __name__ == '__main__':
    # Initial setup
    fig = plt.figure(facecolor='white')
    ax_2d = fig.add_subplot(121)
    ax_3d = fig.add_subplot(122, projection='3d')
    ax_2d.set_aspect('equal')
    ax_3d.set_aspect('equal')

    # Create BezierBuilder
    bezier_builder = BezierBuilder3D(ax_2d, ax_3d)

    plt.show()
