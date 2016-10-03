import numpy as np
import matplotlib.pyplot as plt


def lerp(p, q, t):
    """
    Linear interpolation between two points p, q
    :param p:
    :param q:
    :param t: in [0, 1], when t = 0, returns p, t = 1, returns q
    :return: (1 - t) * p + t * q
    """
    assert 0 <= t <= 1
    return (1 - t) * p + t * q


def deboor_1st(points, t=0.5, flip=False):
    """
    Given 4 points, generates the 1st/last Bezier segment
    :param points: 4 de Boor control points
    :param t: interpolation value of the next segment, can only be 1/2 or 1/3
    :param flip: flip points if True, to handle backwards
    :return:
    """
    points = np.array(points)
    if flip:
        points = np.flipud(points)
    d0, d1, d2, d3 = points
    b1_0 = d0
    b1_1 = d1
    b1_2 = lerp(d1, d2, 0.5)
    b2_1 = lerp(d2, d3, t)
    b1_3 = lerp(b1_2, b2_1, 0.5)
    bs = np.array([b1_0, b1_1, b1_2, b1_3])
    if flip:
        bs = np.flipud(bs)
    return bs


def deboor_2nd(points, t=0.5, flip=False):
    """
    Given 4 points, generates the 2nd/2nd-to-last Bezier segment
    :param points: 4 de Boor control points
    :param t: interpolation value of the next segment, can only be 1/2 or 1/3
    :param flip: flip points if True, to handle backwards
    :return:
    """
    points = np.array(points)
    if flip:
        points = np.flipud(points)
    d1, d2, d3, d4 = points
    b1_2 = lerp(d1, d2, 0.5)
    b2_1 = lerp(d2, d3, 1.0 / 3)
    b2_0 = lerp(b1_2, b2_1, 0.5)
    b2_2 = lerp(d2, d3, 2.0 / 3)
    b3_1 = lerp(d3, d4, t)
    b2_3 = lerp(b2_2, b3_1, 0.5)
    bs = np.array([b2_0, b2_1, b2_2, b2_3])
    if flip:
        bs = np.flipud(bs)
    return bs


def deboor_ith(points):
    """
    Given 4 points, generates the ith Bezier segment
    :param points: 4 de Boor control points
    :return:
    """
    dim1, di, di1, di2 = points
    bi_0 = (dim1 + 4 * di + di1) / 6.0
    bi_1 = lerp(di, di1, 1.0 / 3)
    bi_2 = lerp(di, di1, 2.0 / 3)
    bi_3 = (di + 4 * di1 + di2) / 6.0
    return np.array([bi_0, bi_1, bi_2, bi_3])


def deboor_to_bezier(points, last_point=False):
    """
    Convert de Boor control points to list of Bezier control points
    Given N de Boor control points, this function will return N-3 segments of
    Bezier control points. Each segment consists of 4 Bezier control points.
    When N is less then 4, returns empty list.
    :param points: de Boor control points
    :param last_point: indicate whether this is the last control points
    :return: segments of bezier control points
    """
    points = np.array(points)

    w = 4  # points in window
    m = w - 1  # degree of bezier curve
    n = len(points)
    if n < w:
        return []

    segments = []
    # We will have n - m segments given n points
    for i in range(n - m):
        points_w = points[i:i + w]
        if i == 0:
            bs = deboor_1st(points_w, t=1.0 / 3)
        elif i == 1:
            bs = deboor_2nd(points_w, t=1.0 / 3)
        else:
            bs = deboor_ith(points_w)
        segments.append(bs)

    # fix segments when last point
    if last_point:
        if n == 5:
            # Modify both segments
            segments[0] = deboor_1st(points[:w], t=0.5)
            segments[1] = deboor_1st(points[1:1 + w], t=0.5, flip=True)
        if n == 6:
            # Modify last two segments
            segments[1] = deboor_2nd(points[1:1 + w], t=0.5)
            segments[2] = deboor_1st(points[2:2 + w], t=1 / 3.0, flip=True)
        if n >= 7:
            # Modify last two segments
            segments[-2] = deboor_2nd(points[-w - 1:-1], t=1 / 3.0, flip=True)
            segments[-1] = deboor_1st(points[-w:], t=1 / 3.0, flip=True)

    return segments


class DeBoor:
    def __init__(self):
        pass


def deboor_to_bezier_old(points, last_point=False):
    b_points = []
    d_points = np.array(points)
    num_dp = len(d_points)
    segments = []
    for i in range(len(d_points)):

        curr_point = d_points[i]
        if i == 0 or i == 1:
            b_points.append(curr_point)
        if i == 2:
            b_points.append((d_points[i - 1] + curr_point) / 2)
        if i == 3:
            b_points.append(
                d_points[i - 2] / 4.0 + 7 * d_points[
                    i - 1] / 12.0 + curr_point / 6.0)
            segments.append(b_points[:4])

        if i >= 4 and last_point:
            if num_dp == 5:
                b_points.pop()
                b_points.append(((d_points[i - 1] + d_points[i - 2]) / 2.0 +
                                 b_points[-1]) / 2.0)
                b_points.append(b_points[-1])
                b_points.append((d_points[i - 1] + d_points[i - 2]) / 2)
                b_points.append(d_points[num_dp - 2])
                b_points.append(d_points[num_dp - 1])
                segments.pop()
                segments.append(b_points[:4])
                segments.append(b_points[-4:])

                break

            if num_dp == 6:
                j = num_dp - 2
                b_points.append(b_points[-1])
                b_points.append(d_points[j - 1] / 3 + 2 * d_points[j - 2] / 3)
                b_points.append(d_points[j - 2] / 3 + 2 * d_points[j - 1] / 3)
                b_points.append(
                    ((d_points[j] + d_points[j - 1]) / 2 + b_points[-1]) / 2)
                b_points.append(b_points[-1])
                b_points.append((d_points[j] + d_points[j - 1]) / 2)
                b_points.append(d_points[num_dp - 2])
                b_points.append(d_points[num_dp - 1])
                segments.pop()
                segments.append(b_points[:4])
                segments.append(b_points[-8:-4])
                segments.append(b_points[-4:])
                break

            if i < (num_dp - 2):
                b_points.append(b_points[-1])
                b_points.append(d_points[i - 1] / 3 + 2 * d_points[i - 2] / 3)
                b_points.append(d_points[i - 2] / 3 + 2 * d_points[i - 1] / 3)
                b_points.append(d_points[i - 2] / 6 + 4 * d_points[
                    i - 1] / 6 + curr_point / 6)
                segments.append(b_points[-4:])

            elif num_dp >= 7:
                j = num_dp - 1
                b_points.append(b_points[-1])
                b_points.append(2 * d_points[j - 3] / 3 + d_points[j - 2] / 3)
                b_points.append(2 * d_points[j - 2] / 3 + d_points[j - 3] / 3)
                b_points.append(
                    1 * d_points[j - 3] / 6 + 7 * d_points[j - 2] / 12 + 1 *
                    d_points[j - 1] / 4)
                b_points.append(b_points[-1])
                b_points.append((d_points[j - 2] + d_points[j - 1]) / 2)
                b_points.append(d_points[j - 1])
                b_points.append(d_points[j])
                segments.append(b_points[-8:-4])
                segments.append(b_points[-4:])
                break

        elif i >= 4:
            b_points.append(b_points[-1])
            b_points.append(d_points[i - 1] / 3 + 2 * d_points[i - 2] / 3)
            b_points.append(d_points[i - 2] / 3 + 2 * d_points[i - 1] / 3)
            b_points.append(
                d_points[i - 2] / 6 + 4 * d_points[i - 1] / 6 + curr_point / 6)
            segments.append(b_points[-4:])

    return np.array(b_points), np.array(segments)


if __name__ == '__main__':
    dpoints = np.array(
        [[0, 0], [0, 1], [1, 1], [1, 0], [2, 0], [2, 1], [3, 1], [3, 0],
         [4, 0]],
        float)
    bpoints = deboor_to_bezier(dpoints[:6], True)
    fig, ax = plt.subplots()
    ax.plot(dpoints[:, 0], dpoints[:, 1], '-+')
    for b in bpoints:
        plt.plot(b[:, 0], b[:, 1], linewidth=2)
    ax.margins(x=.1, y=.1)
    ax.set_aspect('equal')
    plt.show()
