import unittest
import numpy as np
import numpy.testing as nt
from project2.haar import haar, haar_inv


class TestHaar(unittest.TestCase):
    def setUp(self):
        self.u = np.array([31, 29, 23, 17, -6, -8, -2, -4])
        self.c = np.array([10, 15, 5, -2, 1, 3, 1, 1])

    def test_haar(self):
        nt.assert_array_almost_equal(haar(self.u), self.c)

    def test_haar_inv(self):
        nt.assert_array_almost_equal(haar_inv(self.c), self.u)
