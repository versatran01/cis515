import numpy as np
from project4.so3 import hat_R3_so3, vee_so3_R3, R3_exp_SO3
from math import exp, sin, cos, isclose


def SIM3_log_sim3(SIM3):
    """
    Logarithm map SIM3 -> sim3
    :param SIM3: 4x4 matrix
    :return: sim3, 4x4 matrix
    """
    pass


def SIM3_log_R7(SIM3):
    pass


def sim3_exp_R7(R7):
    """
    Exponential map R7 -> sim3 -> SIM3
    :param R7: 1x7 vector
    :return: SIM3, 4x4 matrix
    """
    s, a, b, c, x, y, z = R7
    w = [a, b, c]
    u = [x, y, z]
    # t = theta
    t2 = np.inner(w, w)
    t = np.sqrt(t2)
    t3 = t2 * t

    # pre-compute some coefficients
    cos_t = cos(t)
    sin_t = sin(t)
    I = np.eye(3)
    s2 = s * s
    e_s = exp(s)
    Omega = hat_R3_so3(w)
    Omega2 = np.dot(Omega, Omega)

    # Check whether we need to handle numerical issue
    s_close_0 = isclose(s, 0.0)
    t_close_0 = isclose(t, 0.0)

    # TODO: fix this for the case when both are close to 0
    if s_close_0:
        if t_close_0:
            # s = 0 and theta = 0
            V = I
        else:
            # s = 0 and theta != 0
            V = I + ((1 - cos_t) / t2) * Omega + ((t - sin_t) / t3) * Omega2
    else:
        A = (e_s - 1.0) / s

        if t_close_0:
            # s != 0 and theta = 0
            V = A * I
        else:
            # s !=0 and theta != 0
            s2_t2 = s2 + t2
            es_cos = e_s * cos_t
            es_sin = e_s * sin_t
            v2 = ((t * (1 - es_cos) + s * es_sin) / (t * s2_t2))
            v3a = A / t2
            v3b = es_sin / (t * s2_t2)
            v3c = s * (es_cos - 1) / (t2 * s2_t2)
            v3 = v3a - v3b - v3c
            V = A * I + v2 * Omega + v3 * Omega2

    # compute final matrix, lives in SIM3
    B = np.zeros((4, 4))
    B[:3, :3] = e_s * R3_exp_SO3(w)
    B[:3, 3] = np.dot(V, u)
    B[3, 3] = 1

    return B


def sim3_exp_SIM3(sim3):
    """
    exponential map sim3 -> SIM3
    :param sim3:
    :return:
    """
    return sim3_exp_R7(vee_sim3_R7(sim3))


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
