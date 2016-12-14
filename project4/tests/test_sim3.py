import unittest
import numpy as np
import numpy.testing as nt
from project4.sim3 import sim3_exp_SIM3, vee_sim3_R7, hat_R7_sim3

class TestSim3(unittest.TestCase):

    def setUp(self):
        self.R0 = np.eye(3)
        self.w0 = np.zeros(3)
        self.R1 = np.diag([1.0, -1, -1])
        self.w1 = np.array([np.pi, 0, 0])

    def test_sim3_exp_SIM3(self):
        # put in testing code

    def test_vee_sim3_R7(self):
        # put in testing code

    def test_hat_R7_sim3(self):
        # put in testing code





