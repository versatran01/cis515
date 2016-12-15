import unittest
import numpy as np
import numpy.testing as nt
from project4.sim3 import (R7_exp_SIM3, SIM3_log_R7, sim3_vee_R7, R7_hat_sim3,
                           rand_R7_ism_sim3, sim3_exp_SIM3)
from scipy.linalg import expm
from project4.tests.test_so3 import TestExpmLogm


class TestSim3(TestExpmLogm):
    def setUp(self):
        # theta = 0, lambda != 0
        self.r1 = np.array([5, 0, 0, 0, 3, 2, 1.0])
        # theta = 0, lambda = 0
        self.r2 = np.array([0, 0, 0, 0, 1, 4, 9.0])
        # theta != 0, lambda = 0
        self.r3 = np.array([0, 0.1, 0.2, 0.3, 5, 4, 3])
        # theta != 0, lambda = != 0
        self.r4 = np.array([3, 1, 0.1, 0.01, 1, 2, 9])

    def test_sim3_exp_edge(self):
        B1 = R7_hat_sim3(self.r1)
        nt.assert_almost_equal(expm(B1), sim3_exp_SIM3(B1))

        B2 = R7_hat_sim3(self.r2)
        nt.assert_almost_equal(expm(B2), sim3_exp_SIM3(B2))

        B3 = R7_hat_sim3(self.r3)
        nt.assert_almost_equal(expm(B3), sim3_exp_SIM3(B3))

        B4 = R7_hat_sim3(self.r4)
        nt.assert_almost_equal(expm(B4), sim3_exp_SIM3(B4))

    def test_hat_vee_random(self):
        self.random_hat_vee(rand_R7_ism_sim3, R7_hat_sim3, sim3_vee_R7)

    def test_sim3_exp_log_random(self):
        self.random_expm_logm(rand_R7_ism_sim3, R7_exp_SIM3, SIM3_log_R7)
