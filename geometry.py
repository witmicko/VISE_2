from math import *

import cv2
import numpy as np


def get_angle_between_points(origin, end):
    x_diff = end[0] - origin[0]
    y_diff = origin[1] - end[1]
    deg = degrees(atan2(y_diff, x_diff))
    if deg < 0:
        deg += 360
    return deg


def get_point_at_circle(centre, r, angle):
    x = int(centre[0] + r * cos(np.deg2rad(angle)))
    y = int(centre[1] - r * sin(np.deg2rad(angle)))
    return x, y


def get_line_degrees(lines, match_rec, center, img=None):
    if lines is not None:
        degs = []
        a, b, c = lines.shape
        for i in range(a):
            pt_a = (lines[i][0][0] + match_rec[0][0], lines[i][0][1] + match_rec[0][1])
            pt_b = (lines[i][0][2] + match_rec[0][0], lines[i][0][3] + match_rec[0][1])

            dist_a = np.math.hypot(pt_a[0] - center[0], pt_a[1] - center[1])
            dist_b = np.math.hypot(pt_b[0] - center[0], pt_b[1] - center[1])
            # todo check which points to use
            if dist_a < dist_b:
                # deg = get_angle_between_points(pt_a, pt_b)
                deg = get_angle_between_points(center, pt_b)
            else:
                # deg = get_angle_between_points(pt_b, pt_a)
                deg = get_angle_between_points(center, pt_a)

            # degs.append(int(deg))
            degs.append(deg)
            if img is not None:
                cv2.line(img, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.line(img, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
        return degs

def get_line_degrees_2(lines, center, img=None):
    if lines is not None:
        degs = []
        a, b, c = lines.shape
        for i in range(a):
            pt_a = (lines[i][0][0], lines[i][0][1])
            pt_b = (lines[i][0][2], lines[i][0][3])

            dist_a = np.math.hypot(pt_a[0] - center[0], pt_a[1] - center[1])
            dist_b = np.math.hypot(pt_b[0] - center[0], pt_b[1] - center[1])
            # todo check which points to use
            if dist_a < dist_b:
                # deg = get_angle_between_points(pt_a, pt_b)
                deg = get_angle_between_points(center, pt_b)
            else:
                # deg = get_angle_between_points(pt_b, pt_a)
                deg = get_angle_between_points(center, pt_a)
            deg = (deg + 90) % 360
            degs.append(int(deg))
            if img is not None:
                cv2.line(img, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.line(img, pt_a, pt_b, (0, 0, 255), 3, cv2.LINE_AA)
        return degs