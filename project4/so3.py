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
    b2, c2, d2 = np.diag(S) + 1.0


def hat_map3(w):
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


def vee_map3(so3):
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


def so3_exp_r3(w):
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

    if np.isclose(theta2, 0.0):
        # When theta^2 is close to 0, we take the limit of exponential map
        # with theta -> 0
        A = 1.0
        B = 0.5
    else:
        A = np.sin(theta) / theta
        B = (1 - np.cos(theta)) / theta2

    I = np.eye(3)
    wx = hat_map3(w)
    wx2 = np.dot(wx, wx)

    R = I + A * wx + B * wx2

    return R


def so3_exp_so3(so3):
    """
    Exponential map so3 -> SO3
    :param so3: so3, 3x3 skew-symmetric matrix
    :return: SO3, 3x3 special orthogonal matrix
    """
    return so3_exp_r3(vee_map3(so3))


def SO3_log(SO3):
    """
    Logarithm map SO3 -> so3
    :param SO3:
    :return:
    """
    c = (np.trace(SO3) - 1.0) / 2.0
