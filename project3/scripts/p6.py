import matplotlib.pyplot as plt
import numpy as np
from project3.ge import ge_solve
from project3.lu import lu_solve_tridiag, rand_tridiag
import time

sizes = range(2, 300)
iters = range(50)
times = np.zeros((3, len(sizes)))
for n in sizes:
    A = rand_tridiag(n)
    X = np.random.random([n, 1])
    B = np.dot(A, X)
    dt_ge = 0
    dt_lu = 0
    for i in iters:
        # time the ge_solve function
        t0 = time.time()
        ge_solve(A, B, use_scipy=False)
        dt_ge += (time.time() - t0) * 100

        # time the lu_solve function
        t0 = time.time()
        lu_solve_tridiag(A, B)
        dt_lu += (time.time() - t0) * 100

    times[0, n - 2] = dt_ge / len(iters)
    times[1, n - 2] = dt_lu / len(iters)
    print(n)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Average Computation Time vs. Matrix Size')
ax.set_xlabel('Matrix Size')
ax.set_ylabel('Time [ms]')

ax.plot(sizes, times[0], color="blue", linewidth=2.5, linestyle="-",
        label="gaussian elimination")
ax.plot(sizes, times[1], color="red", linewidth=2.5, linestyle="-",
        label="lu factorization")
plt.legend(loc='upper left')
plt.grid()
plt.show()
