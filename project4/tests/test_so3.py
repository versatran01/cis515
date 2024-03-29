import unittest
import numpy as np
import numpy.testing as nt
from project4.so3 import (R3_exp_SO3, SO3_log_R3, R3_hat_so3, so3_vee_R3,
                          rand_R3_ism_so3)


class TestExpmLogm(unittest.TestCase):
    n_times = 50

    def random_expm_logm(self, rand_fun, expm_fun, logm_fun):
        for n in range(self.n_times):
            r = rand_fun()
            R = expm_fun(r)
            r0 = logm_fun(R)
            nt.assert_array_almost_equal(r, r0)

    def random_hat_vee(self, rand_fun, hat_fun, vee_fun):
        for n in range(self.n_times):
            r = rand_fun()
            nt.assert_array_equal(r, vee_fun(hat_fun(r)))


class TestSo3(TestExpmLogm):
    def setUp(self):
        self.R0 = np.eye(3)
        self.w0 = np.zeros(3)
        self.R1 = np.diag([1.0, -1, -1])
        self.w1 = np.array([np.pi, 0, 0])

        self.w2 = np.ones(3)
        self.w3 = -np.ones(3)
        self.w4 = np.ones(3) * np.pi / 2
        self.w5 = np.ones(3) * np.pi / 4
        self.w6 = np.ones(3) * 1e-10

    def test_so3_exp_edge(self):
        nt.assert_array_almost_equal(R3_exp_SO3(self.w0), self.R0)
        nt.assert_array_almost_equal(R3_exp_SO3(self.w1), self.R1)

    def test_so3_log_edge(self):
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

        R6 = R3_exp_SO3(self.w6)
        nt.assert_array_almost_equal(SO3_log_R3(R6), self.w6)

    def test_so3_hat_vee_random(self):
        self.random_hat_vee(rand_R3_ism_so3, R3_hat_so3, so3_vee_R3)

    def test_so3_exp_log_random(self):
        self.random_expm_logm(rand_R3_ism_so3, R3_exp_SO3, SO3_log_R3)
