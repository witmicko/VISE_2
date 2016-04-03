from math import *
import numpy as np


def get_angle_between_points(origin, end):
    x_diff = end[0] - origin[0]
    y_diff = origin[1] - end[1]

    return degrees(atan2(y_diff, x_diff))


def get_point_at_circle(centre, r, angle):
    x = int(centre[0] + r * cos(np.deg2rad(angle)))
    y = int(centre[1] - r * sin(np.deg2rad(angle)))
    return x,y
