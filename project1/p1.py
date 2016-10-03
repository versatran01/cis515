import os
import sys

sys.path.append(os.path.abspath('..'))

import matplotlib.pyplot as plt
from project1.deboor_builder import DeboorBuilder2D

if __name__ == '__main__':
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    # Create DeboorBuilder
    deboor_builder = DeboorBuilder2D(ax)

    plt.show()
