import numpy as np
from project4.so3 import hat_R3_so3, vee_so3_R3


def SIM3_log_sim3(SIM3):
    """
    Logarithm map SIM3 -> sim3
    :param SIM3: 4x4 matrix
    :return: sim3, 4x4 matrix
    """
    pass


def SIM3_log_R7(SIM3):
    pass


def sim3_exp_SIM3(sim3):
    """
    Exponential map sim3 -> SIM3
    :param sim3: 4x4 matrix
    :return: SIM3, 4x4 matrix
    """
    r7 = vee_sim3_R7(sim3)  # get r7 representation
    lmda = r7[0]
    theta = (r7[1]**2 + r7[2]**2 + r7[3]**2)**0.5  # compute theta

    if lmda != 0 and theta  == 0:




    pass


def sim3_exp_R7(R7):
    pass


def hat_R7_sim3(R7):
    """

    :param R7: 1x7 vector
    :return: sim3, 4x4 matrix
    """
    A = np.array([[R7[0], -R7[3], R7[2], R7[5]],
                 [R7[3], R7[0], -R7[1], R7[6]],
                 [-R7[2], R7[1], R7[0], R7[7]],
                 [0, 0, 0, 0]], np.float)

    return A
    pass


def vee_sim3_R7(sim3):
    """

    :param sim3: 4x4 matrix
    :return: R7, 1x7 vector
    """
    v = np.array([sim3[0, 0], sim3[2, 1], sim3[0, 2], sim3[1, 0], sim3[0, 3], sim3[1, 3], sim3[2, 3]], np.float)

    return v

    pass
