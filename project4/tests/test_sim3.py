import unittest
import numpy as np
import numpy.testing as nt
from project4.sim3 import sim3_exp_SIM3, vee_sim3_R7, hat_R7_sim3
from scipy.linalg import expm
from project4.so3 import R3_exp_SO3


class TestSim3(unittest.TestCase):
    def setUp(self):
        self.B1 = np.array([[1., 0., 0., 1.],  # theta = 0 and lambda = 1
                            [0., 1., 0., 1.],
                            [0., 0., 1., 1.],
                            [0., 0., 0., 0.]], dtype=float)

        self.B2 = np.array([[0., 0., 0., 1.],  # theta = 0 and lambda = 0
                            [0., 0., 0., 2.],
                            [0., 0., 0., 1.],
                            [0., 0., 0., 0.]], dtype=float)

        self.B3 = np.array([[0., -0.1, 0., 1.],  # theta != 0 and lambda = 0
                            [0.1, 0., 0., 2.],
                            [0., 0., 0., 1.],
                            [0., 0., 0., 0.]], dtype=float)

        self.B4 = np.array([[1., -0.1, .01, 1.],  # theta != 0 and lambda != 0
                            [0.1, 1., -.01, 2.],
                            [-.01, .01, 1., 1.],
                            [0., 0., 0., 0.]], dtype=float)

        self.e_B1 = expm(self.B1)
        self.e_B2 = expm(self.B2)
        self.e_B3 = expm(self.B3)
        self.e_B4 = expm(self.B4)

    def test_sim3_exp_SIM3(self):
       # nt.assert_almost_equal(sim3_exp_SIM3(self.B1), self.e_B1, decimal=2)
       # nt.assert_almost_equal(sim3_exp_SIM3(self.B2), self.e_B2, decimal=2)
        nt.assert_almost_equal(sim3_exp_SIM3(self.B3), self.e_B3, decimal=3)
        #nt.assert_almost_equal(sim3_exp_SIM3(self.B4), self.e_B4, decimal=2)

    def test_vee_sim3_R7(self):
        pass

    def test_hat_R7_sim3(self):
        pass
