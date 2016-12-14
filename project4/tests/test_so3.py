import unittest
import numpy as np
import numpy.testing as nt
from project4.so3 import R3_exp_SO3, so3_exp_SO3, SO3_log_so3, SO3_log_R3


class TestSo3(unittest.TestCase):
    def setUp(self):
        self.R0 = np.eye(3)
        self.w0 = np.zeros(3)
        self.R1 = np.diag([1.0, -1, -1])
        self.w1 = np.array([np.pi, 0, 0])

        self.w2 = np.ones(3)
        self.w3 = -np.ones(3)
        self.w4 = np.ones(3) * np.pi / 2
        self.w5 = np.ones(3) * np.pi / 4

        self.n_times = 10

    def test_so3_exp(self):
        nt.assert_array_almost_equal(R3_exp_SO3(self.w0), self.R0)
        nt.assert_array_almost_equal(R3_exp_SO3(self.w1), self.R1)

    def test_so3_log(self):
        nt.assert_array_almost_equal(SO3_log_R3(self.R0), self.w0)
        nt.assert_array_almost_equal(SO3_log_R3(self.R1), self.w1)

    def test_so3_exp_log(self):
        R2 = R3_exp_SO3(self.w2)
        nt.assert_array_almost_equal(SO3_log_R3(R2), self.w2)

        R3 = R3_exp_SO3(self.w3)
        nt.assert_array_almost_equal(SO3_log_R3(R3), self.w3)

        R4 = R3_exp_SO3(self.w4)
        nt.assert_array_almost_equal(SO3_log_R3(R4), self.w4)

        R5 = R3_exp_SO3(self.w5)
        nt.assert_array_almost_equal(SO3_log_R3(R5), self.w5)

    def test_so3_exp_log_random(self):
        for n in range(self.n_times):
            w = np.random.random(3)
            wn = np.sqrt(np.inner(w, w))
            w /= wn * np.pi
            w0 = SO3_log_R3(R3_exp_SO3(w))
            nt.assert_array_almost_equal(w, w0)
