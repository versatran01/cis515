import unittest
import numpy as np
import numpy.testing as nt
from project3.ge import ge_solve


class TestGe(unittest.TestCase):
    def setUp(self):
        self.A0 = np.array([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], float)
        self.A1 = np.array([[1, 1, 1], [1, 1, 3], [2, 5, 8]], float)
        self.A2 = np.array([[0, 0, 1], [-2, 7, 2], [4, -6, 0]], float)
        self.B0 = np.array([5, -2, 9], float)
        self.B1 = np.array([1, 1, 1], float)
        self.B2 = np.array([1, 1, -1], float)
        self.X0 = np.array([1, 1, 2], float)
        self.X1 = np.array([4, -1, 0], float) / 3.0
        self.X2 = np.array([-0.8125, -0.375, 1])

        self.n_times = 50
        self.n_max = 8

    def test_ge_solve(self):
        X0 = ge_solve(self.A0, self.B0)
        nt.assert_array_equal(self.X0, X0.ravel())
        X1 = ge_solve(self.A1, self.B1)
        nt.assert_array_equal(self.X1, X1.ravel())
        X2 = ge_solve(self.A2, self.B2)
        nt.assert_array_equal(self.X2, X2.ravel())

    def test_ge_solve_random(self):
        for n in range(self.n_max):
            nX = 2 ** n
            A = np.random.random((nX, nX))
            X = np.random.random(nX)
            B = np.dot(A, X)

            Xge = ge_solve(A, B, use_scipy=False)
            nt.assert_array_almost_equal(X, Xge.ravel())

    def test_ge_solve_random_scipy(self):
        for n in range(self.n_max):
            nX = 2 ** n
            A = np.random.random((nX, nX))
            X = np.random.random(nX)
            B = np.dot(A, X)

            Xge = ge_solve(A, B, use_scipy=True)
            nt.assert_array_almost_equal(X, Xge.ravel())
