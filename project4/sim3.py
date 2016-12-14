import numpy as np
from project4.so3 import hat_R3_so3, vee_so3_R3
from math import exp, cos, sin


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
    lmda, a, b, c, x, y, z = r7
    theta = (a ** 2 + b ** 2 + c ** 2) ** 0.5  # compute theta
    omega = hat_R3_so3([a, b, c])  # compute omega matrix

    W = np.array([x, y, z])

    if np.isclose(lmda, 0.0) and np.isclose(theta, 0.0):  # both lambda = 0 and theta = 0
        V = np.eye(3)
        e_gamma = exp(lmda) * np.eye(3)

    elif not np.isclose(lmda, 0.0) and np.isclose(theta, 0.0):  # lambda != 0 and theta = 0
        V = ((exp(lmda) - 1) / lmda) * np.eye(3)
        e_gamma = exp(lmda) * np.eye(3)

    elif np.isclose(lmda, 0.0) and not np.isclose(theta, 0.0):  # lambda = 0 and theta != 0
        V = np.eye(3) + ((1 - np.cos(theta)) / (theta ** 2)) * omega
        + ((theta - np.sin(theta)) / (theta ** 3)) * omega * omega

        e_gamma = exp(lmda) * (
            np.eye(3) + (np.sin(theta) / theta) * omega + ((1 - np.cos(theta)) / (theta ** 2)) * omega * omega)

    elif not np.isclose(lmda, 0.0) and not np.isclose(theta, 0.0):  # lambda != 0 and theta != 0

        v_1 = ((exp(lmda) - 1) / lmda) * np.eye(3)

        v_2 = ((theta * (1 - exp(lmda) * cos(theta)) + exp(lmda) * lmda * sin(theta)) / (
            theta * (lmda ** 2 + theta ** 2))) * omega

        v_3a = (exp(lmda) - 1) / (lmda * theta ** 2)

        v_3b = exp(lmda) * sin(theta) / (theta * (lmda ** 2 + theta ** 2))

        v_3c = lmda * (exp(lmda) * cos(theta) - 1) / (theta ** 2 * (lmda ** 2 + theta ** 2))

        v_3 = (v_3a - v_3b - v_3c) * omega * omega

        V = v_1 + v_2 + v_3
        e_gamma = exp(lmda) * (
            np.eye(3) + (sin(theta) / theta) * omega + (
                (1 - cos(theta)) / theta ** 2) * omega * omega)  # now compute the final matrix in SIM3


    B = np.zeros([4, 4])
    B[:3, :3] = e_gamma
    B[:3, 3] = np.dot(V, W)
    B[3, 3] = 1

    return B


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
