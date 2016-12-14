import unittest
import numpy as np
import numpy.testing as nt
from project4.so3 import r3_exp_SO3, so3_exp_SO3, SO3_log_so3, SO3_log_r3


class TestSo3(unittest.TestCase):
    def setUp(self):
        self.R0 = np.eye(3)
        self.w0 = np.zeros(3)
        self.R1 = np.diag([1.0, -1, -1])
        self.w1 = np.array([np.pi, 0, 0])

    def test_so3_exp(self):
        nt.assert_array_almost_equal(r3_exp_SO3(self.w0), self.R0)
        nt.assert_array_almost_equal(r3_exp_SO3(self.w1), self.R1)

    def test_so3_log(self):
        nt.assert_array_almost_equal(SO3_log_r3(self.R0), self.w0)
        nt.assert_array_almost_equal(SO3_log_r3(self.R1), self.w1)

    def test_so3_exp_log(self):
        pass
