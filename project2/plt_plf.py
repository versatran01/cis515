import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111)


# u = np.array([0, 2, 4, 6, 6, 4, 2, 1, -1, -2, -4, -6, -6, -4, -2, 0])
u = np.array([1, 2, 3, 4, 5])
m = np.size(u)
x = np.linspace(0, 1, m)
ax.step(x, u)
ax.set_xlim(-0.1, 1.1)
plt.show()

