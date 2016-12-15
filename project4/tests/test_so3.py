import unittest
import numpy as np
import numpy.testing as nt
from project4.so3 import R3_exp_SO3, SO3_log_R3, hat_R3_so3, vee_so3_R3
from scipy.linalg import expm, logm


class TestExpmLogm(unittest.TestCase):
    def setUp(self):
        self.n_times = 10

    def random_expm(self, rand_fun, expm_fun, hat_fun):
        for n in range(self.n_times):
            r = rand_fun()
            rx = hat_fun(r)
            exp_r = expm_fun(rx)
            nt.assert_array_equal(expm(rx), exp_r)

    def random_logm(self, rand_fun, logm_fun):
        for n in range(self.n_times):
            R = rand_fun()
            log_R = logm_fun(R)
            nt.assert_array_almost_equal(logm(R), log_R)

    def random_expm_logm(self):
        pass

    def random_hat_vee(self):
        pass


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

    def test_hat_vee_random(self):
        for n in range(self.n_times):
            r3 = np.random.random(3)
            so3 = hat_R3_so3(r3)
            nt.assert_array_equal(r3, vee_so3_R3(so3))
