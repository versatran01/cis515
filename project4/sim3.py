import numpy as np
from project4.so3 import (R3_hat_so3, R3_exp_SO3, SO3_log_R3,
                          rand_R3_ism_so3)
from math import exp, sin, cos


def SIM3_log_sim3(SIM3):
    return R7_hat_sim3(SIM3_log_R7(SIM3))


def SIM3_log_R7(SIM3):
    """
    Logarithm map SIM3 -> sim3
    :param SIM3: 4x4 matrix
    :return: sim3, 4x4 matrix
    """
    assert SIM3[-1, -1] == 1

    s_R = SIM3[:3, :3]
    Vu = SIM3[:3, 3]
    # s2I this is supposed to be diagonal
    s2_I = np.dot(s_R, s_R.T)
    # extract s2 and take sqrt to get s = e^l
    # All diagonal elements should be the same, we just take the average
    s = np.sqrt(s2_I[0, 0])
    l = np.log(s)
    # Now we recover R and then we apply log map to get rotation vector
    R = s_R / s
    w = SO3_log_R3(R)
    # with s and w we can construct V
    V = sim3_exp_calc_V(l, w)
    u = np.dot(np.linalg.inv(V), Vu)

    return np.hstack((l, w, u))


def sim3_exp_calc_V(l, w):
    """
    Helper function that calculates V in sim3 exp map
    :param l: scalar, scale
    :param w: 1x3 vector
    :return: V, 3x3 matrix
    """
    # t = theta
    t2 = np.inner(w, w)
    t = np.sqrt(t2)
    t3 = t2 * t

    # pre-compute some coefficients
    cos_t = cos(t)
    sin_t = sin(t)
    I = np.eye(3)
    l2 = l * l
    e_s = exp(l)
    Omega = R3_hat_so3(w)
    Omega2 = np.dot(Omega, Omega)

    # Check whether we need to handle numerical issue
    s_close_0 = np.isclose(l, 0.0)
    t_close_0 = np.isclose(t, 0.0)

    if s_close_0:
        if t_close_0:
            # s = 0 and theta = 0
            # take the limit of theta -> 0 and s -> 0
            # V = I
            V = I + 0.5 * Omega + 1.0 / 6 * Omega2
        else:
            # s = 0 and theta != 0
            V = I + ((1 - cos_t) / t2) * Omega + ((t - sin_t) / t3) * Omega2
    else:
        A = (e_s - 1.0) / l

        if t_close_0:
            # s != 0 and theta = 0
            V = A * I
            # TODO: failed to take the limit of theta -> 0 for Omega2
            # V = A * I + (A + e_s) / s * Omega +
        else:
            # s !=0 and theta != 0
            s2_t2 = l2 + t2
            es_cos = e_s * cos_t
            es_sin = e_s * sin_t
            v2 = ((t * (1 - es_cos) + l * es_sin) / (t * s2_t2))
            v3a = A / t2
            v3b = es_sin / (t * s2_t2)
            v3c = l * (es_cos - 1) / (t2 * s2_t2)
            v3 = v3a - v3b - v3c
            V = A * I + v2 * Omega + v3 * Omega2

    return V


def R7_exp_SIM3(R7):
    """
    Exponential map R7 -> sim3 -> SIM3
    :param R7: 1x7 vector
    :return: SIM3, 4x4 matrix
    """
    s, a, b, c, x, y, z = R7
    w = [a, b, c]
    u = [x, y, z]

    V = sim3_exp_calc_V(s, w)

    # compute final matrix, lives in SIM3
    B = np.zeros((4, 4))
    B[:3, :3] = np.exp(s) * R3_exp_SO3(w)
    B[:3, 3] = np.dot(V, u)
    B[3, 3] = 1

    return B


def sim3_exp_SIM3(sim3):
    """
    exponential map sim3 -> SIM3
    :param sim3:
    :return:
    """
    return R7_exp_SIM3(sim3_vee_R7(sim3))


def R7_hat_sim3(R7):
    """
    hat map R7 -> sim3
    :param R7: 1x7 vector
    :return: sim3, 4x4 matrix
    """
    l, w, u = np.split(R7, [1, 4])
    A = np.zeros((4, 4))
    Omega = R3_hat_so3(w)
    A[:3, :3] = Omega + l * np.eye(3)
    A[:3, 3] = u
    return A


def sim3_vee_R7(sim3):
    """
    vee map sim3 -> R7
    :param sim3: 4x4 matrix
    :return: R7, 1x7 vector
    """
    v = np.array(
        [sim3[0, 0], sim3[2, 1], sim3[0, 2], sim3[1, 0], sim3[0, 3], sim3[1, 3],
         sim3[2, 3]], np.float)

    return v


def rand_R7_ism_sim3():
    """
    Uniform sampling of subspace of R7 that is isomorphic to sim3
    :return:
    """
    w = rand_R3_ism_so3()
    s = np.random.random()
    u = np.random.random(3)
    return np.hstack((s, w, u))


def SIM3_transform_points(SIM3, points):
    """
    Apply SIM3 to points
    :param SIM3: 4x4 matrix
    :param points: 3xn matrix
    :return: transformed points 3xn matrix
    """
    aR = SIM3[:3, :3]
    t = SIM3[:3, 3]
    pts = np.dot(points, aR.T) + t

    return pts


def SIM3_from_sRt(s, R, t):
    A = np.zeros((4, 4))
    A[:3, :3] = s * R
    A[:3, 3] = t
    A[3, 3] = 1
    return A
