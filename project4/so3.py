import numpy as np


def skew_sqrt(R):
    """
    Solve for U
    U = [[0,    -d,     c],
         [d,    0,      -b],
         [-c,   b,      0]]
    such that U^2 = S = (R - I)/2, where
    S = [[b^2 - 1,  bc,         bd      ],
         [bc,       c^2 - 1,    cd      ],
         [bd,       cd,         d^2 - 1 ]]
    :param R: rotation matrix
    :return:
    """
    R = np.array(R, dtype=float)
    I = np.eye(3)
    S = (R - I) / 2.0
    SI = S + I
    # SI is a matrix with [b^2, c^2, d^2] along the diagonal
    bcd2 = np.diag(SI)
    # Get the maximum value for [b62, c^2, d^2], which is guaranteed to be
    # nonzero
    ind = np.argmax(bcd2)
    k = np.sqrt(bcd2[ind])
    # k has to be positive
    assert k > 0
    bcd = SI[ind] / k
    return hat_R3_so3(bcd)


def hat_R3_so3(w):
    """
    Hat operator R3 -> so(3)
    Create skew symmetric matrix [v]x from vector v
    https://en.wikipedia.org/wiki/Skew-symmetric_matrix
    http://mathworld.wolfram.com/AntisymmetricMatrix.html
    :param w: R3, 1x3 vector
    :return: so(3), 3x3 skew-symmetric matrix
    """
    wx, wy, wz = w
    return np.array([[0, -wz, wy],
                     [wz, 0, -wx],
                     [-wy, wx, 0]], np.float)


def vee_so3_R3(so3):
    """
    Vee operator so(3) -> R3
    :param so3: so(3), 3x3 skew-symmetric matrix
    :return: R3, 1x3 vector
    """
    assert np.ndim(so3) == 2 and np.shape(so3) == (3, 3)

    wx = -so3[1, 2]
    wy = so3[0, 2]
    wz = -so3[0, 1]

    return np.array([wx, wy, wz])


def R3_exp_SO3(w):
    """
    Exponential map R3 -> so3 -> SO3
    [R3  -> so3]    w_x = hat_map(w)
    [so3 -> SO3]    exp(w) = I + A * w_x + B * w_x^2
                    A = sin(theta) / theta
                    B = (1 - cos(theta)) / theta^2
    :param w: R3, 1x3 vector
    :return: SO3, 3x3 special orthogonal matrix
    """
    theta2 = np.inner(w, w)
    theta = np.sqrt(theta2)
    I = np.eye(3)

    if theta == 0.0:
        return I

    if np.isclose(theta, 0.0):
        # When cos(theta) -> 1, theta -> 0, we take the limit of
        # exponential map with theta -> 0
        # Note we could omit the case when theta = 0 since this handles it
        A = 1.0
        B = 0.5
    else:
        A = np.sin(theta) / theta
        B = (1 - np.cos(theta)) / theta2

    wx = hat_R3_so3(w)
    wx2 = np.dot(wx, wx)

    R = I + A * wx + B * wx2

    return R


def so3_exp_SO3(so3):
    """
    Exponential map so3 -> SO3
    :param so3: so3, 3x3 skew-symmetric matrix
    :return: SO3, 3x3 special orthogonal matrix
    """
    return R3_exp_SO3(vee_so3_R3(so3))


def SO3_log_so3(SO3):
    """
    Logarithm map SO3 -> so3
    :param SO3:
    :return: so3, 3x3 skew-symmetric matrix
    """
    R = np.array(SO3, dtype=float)
    # cos(theta)
    cos_t = (np.trace(R) - 1.0) / 2.0
    theta = np.arccos(cos_t)

    if cos_t == 1.0:
        # case R = I, cos(theta) = 1, w = [0, 0, 0]
        return np.zeros((3, 3))
    elif np.isclose(theta, np.pi):
        # case R != I, tr(R) = -1, cos(theta) = -1, theta = pi
        return skew_sqrt(R) * np.pi
    else:
        # case R != I, tr(R) != -1
        # wx = theta / sin(theta) * (R - R^T)
        # arccos guarantees that theta is between 0 to pi
        if np.isclose(theta, 0.0):
            # theta is close to 0, take limit of theta -> 0
            k = 1.0 / 2
        else:
            k = theta / (np.sin(theta) * 2.0)
        return k * (R - R.T)


def SO3_log_R3(SO3):
    """
    :param SO3:
    :return:
    """
    return vee_so3_R3(SO3_log_so3(SO3))
