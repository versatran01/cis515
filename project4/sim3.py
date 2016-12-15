import numpy as np
from project4.so3 import hat_R3_so3, vee_so3_R3
from math import exp, sin, cos


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
    l, a, b, c, x, y, z = r7
    l2 = l * l
    theta2 = a ** 2 + b ** 2 + c ** 2  # compute theta
    theta = np.sqrt(theta2)
    theta3 = theta2 * theta
    Omega = hat_R3_so3([a, b, c])  # compute omega matrix
    Omega2 = np.dot(Omega, Omega)

    W = np.array([x, y, z])
    I = np.eye(3)
    e_l = exp(l)
    cos_th = cos(theta)
    sin_th = sin(theta)
    l2_theta2 = l2 + theta2

    if np.isclose(l, 0.0) and np.isclose(theta, 0.0):
        # both lambda = 0 and theta = 0
        V = I
        e_gamma = e_l * I

    elif not np.isclose(l, 0.0) and np.isclose(theta, 0.0):
        # lambda != 0 and theta = 0
        V = ((e_l - 1) / l) * I
        e_gamma = e_l * I

    elif np.isclose(l, 0.0) and not np.isclose(theta, 0.0):
        # lambda = 0 and theta != 0
        V = I + ((1 - cos_th) / theta2) * Omega \
            + ((theta - sin_th) / theta3) * Omega2
        e_gamma = e_l * (I + (sin_th / theta) * Omega
                         + ((1 - cos_th) / theta2) * Omega2)

    elif not np.isclose(l, 0.0) and not np.isclose(theta, 0.0):
        # lambda != 0 and theta != 0

        v_1 = ((e_l - 1) / l) * I

        v_2 = ((theta * (1 - e_l * cos_th) + e_l * l * sin_th) / (
            theta * l2_theta2)) * Omega

        v_3a = (e_l - 1) / (l * theta2)

        v_3b = e_l * sin_th / (theta * l2_theta2)

        v_3c = l * (e_l * cos_th - 1) / (theta2 * l2_theta2)

        v_3 = (v_3a - v_3b - v_3c) * Omega2

        V = v_1 + v_2 + v_3

        e_gamma = e_l * (I + (sin_th / theta) * Omega
                         + ((1 - cos_th) / theta2) * Omega2)

    # compute final matrix, lives in SIM3
    B = np.zeros([4, 4])
    B[:3, :3] = e_gamma
    B[:3, 3] = np.dot(V, W)
    B[3, 3] = 1

    return B


def sim3_exp_R7(R7):
    pass


def hat_R7_sim3(R7):
    """
    hat map R7 -> sim3
    :param R7: 1x7 vector
    :return: sim3, 4x4 matrix
    """
    l, w, u = np.split(R7, [1, 4])
    A = np.zeros((4, 4))
    Omega = hat_R3_so3(w)
    A[:3, :3] = Omega + l * np.eye(3)
    A[:3, 3] = u
    return A


def vee_sim3_R7(sim3):
    """
    vee map sim3 -> R7
    :param sim3: 4x4 matrix
    :return: R7, 1x7 vector
    """
    v = np.array(
        [sim3[0, 0], sim3[2, 1], sim3[0, 2], sim3[1, 0], sim3[0, 3], sim3[1, 3],
         sim3[2, 3]], np.float)

    return v


if __name__ == '__main__':
    r7 = np.arange(1, 8)
    print(hat_R7_sim3(r7))
