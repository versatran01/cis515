import matplotlib.pyplot as plt
import numpy as np


def make_plf(u):
    y = np.hstack((u, u[-1]))
    m = np.size(y)
    x = np.linspace(0, 1, m)
    return x, y


def plot_plf(ax, u):
    x, y = make_plf(u)
    ax.step(x, y, where='post')


if __name__ == '__main__':

    u0 = np.array([1, 2])
    u1 = np.array([1, 2, 3, 4])
    u2 = np.array([2.4, 2.2, 2.15, 2.05, 6.8, 2.8, 1.1, 1.3])
    u3 = np.array([0, 2, 4, 6, 6, 4, 2, 1, -1, -2, -4, -6, -6, -4, -2, 0])
    u = [u0, u1, u2, u3]

    fig1, axarr = plt.subplots(2, 2)
    fig1.set_facecolor('white')
    axarr = np.ravel(axarr)
    for i, ax in enumerate(axarr):
        plot_plf(ax, u[i])
        ax.margins(0.1)
        ax.grid(True)
        ax.set_title(np.array_str(u[i], precision=1))

    fig2, ax = plt.subplots()
    fig2.set_facecolor('white')
    plot_plf(ax, np.tile(u3, 8))
    ax.margins(0.1)
    ax.grid(True)
    ax.set_title(np.array_str(u3) + " * 8")

    plt.show()

