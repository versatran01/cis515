import unittest
import numpy as np
from random import randint
import numpy.testing as nt
from project2.haar import haar, haar_inv, haar_step, haar_inv_step


class TestHaar(unittest.TestCase):
    def setUp(self):
        self.u = np.array([31, 29, 23, 17, -6, -8, -2, -4])
        self.c = np.array([10, 15, 5, -2, 1, 3, 1, 1])
        self.c2 = np.array([30, 20, -7, -3, 1, 3, 1, 1])
        self.c1 = np.array([25, -5, 5, - 2, 1, 3, 1, 1])
        self.c0 = np.array([10, 15, 5, -2, 1, 3, 1, 1])

        self.n_times = 50
        self.n_max = 8

    def test_haar(self):
        nt.assert_array_almost_equal(haar(self.u), self.c)

    def test_haar_inv(self):
        nt.assert_array_almost_equal(haar_inv(self.c), self.u)

    def test_haar_step(self):
        nt.assert_array_almost_equal(haar_step(self.u, 0), self.u)
        nt.assert_array_almost_equal(haar_step(self.u, 1), self.c2)
        nt.assert_array_almost_equal(haar_step(self.u, 2), self.c1)
        nt.assert_array_almost_equal(haar_step(self.u, 3), self.c0)

    def test_haar_inv_step(self):
        nt.assert_array_almost_equal(haar_inv_step(self.u, 0), self.u)
        nt.assert_array_almost_equal(haar_inv_step(self.c2, 1), self.u)
        nt.assert_array_almost_equal(haar_inv_step(self.c1, 2), self.u)
        nt.assert_array_almost_equal(haar_inv_step(self.c0, 3), self.u)

    def test_haar_random(self):
        for i in range(self.n_times):
            n = randint(1, self.n_max)
            u = np.random.random(2 ** n)
            nt.assert_array_almost_equal(haar_inv(haar(u)), u)

    def test_haar_step_random(self):
        for i in range(self.n_times):
            n = randint(1, self.n_max)
            k = randint(1, n)
            u = np.random.random(2 ** n)
            nt.assert_array_almost_equal(haar_inv_step(haar_step(u, k), k), u)
