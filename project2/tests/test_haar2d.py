import unittest
import numpy as np
import numpy.testing as nt
from project2.haar_2d import haar2d, haar_inv2d


class TestHaar2d(unittest.TestCase):
    def setUp(self):
        self.A = np.array([[64, 2, 3, 61, 60, 6, 7, 57],
                           [9, 55, 54, 12, 13, 51, 50, 16],
                           [17, 47, 46, 20, 21, 43, 42, 24],
                           [40, 26, 27, 37, 36, 30, 31, 33],
                           [32, 34, 35, 29, 28, 38, 39, 25],
                           [41, 23, 22, 44, 45, 19, 18, 48],
                           [49, 15, 14, 52, 53, 11, 10, 56],
                           [8, 58, 59, 5, 4, 62, 63, 1.0]])
        self.C = np.array([[32.5, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 4, -4, 4, -4],
                           [0, 0, 0, 0, 4, -4, 4, -4],
                           [0, 0, 0.5, 0.5, 27, -25, 23, -21],
                           [0, 0, -0.5, - 0.5, -11, 9, -7, 5],
                           [0, 0, 0.5, 0.5, -5, 7, -9, 11],
                           [0, 0, -0.5, -0.5, 21, -23, 25, -27]])

    def test_haar2d(self):
        nt.assert_array_almost_equal(haar2d(self.A), self.C)

    def test_haar_inv2d(self):
        pass
        nt.assert_array_almost_equal(haar_inv2d(self.C), self.A)
