import numpy as np
from project2.haar_2d import haar_inv2d

C = np.array([[1212, -306, -146, -54, -24, -68, -40, 4],
              [30, 36, -90, -2, 8, -20, 8, -4],
              [-50, -10, -20, -24, 0, 72, -16, -16],
              [82, 38, -24, 68, 48, -64, 32, 8],
              [8, 8, -32, 16, -48, -48, -16, 16],
              [20, 20, -56, -16, -16, 32, -16, -16],
              [-8, 8, -48, 0, -16, -16, -16, -16],
              [44, 36, 0, 8, 80, -16, -16, 0]])

print(haar_inv2d(C))
