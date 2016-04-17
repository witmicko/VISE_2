import cv2
import numpy as np

from image_processing.geometry import get_point_at_circle


def put_angle_text(img, point, offset_x, offset_y, text):
    cv2.putText(img, text,
                (point[0] + offset_x, point[1] + offset_y),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 5, cv2.LINE_AA)


def line_blue_1(img, start, end):
    cv2.line(img, start, end, (255, 0, 0), 1, lineType=cv2.LINE_AA)


def line_blue_2(img, start, end):
    cv2.line(img, start, end, (255, 0, 0), 2, lineType=cv2.LINE_AA)


def line_blue_5(img, start, end):
    cv2.line(img, start, end, (255, 0, 0), 5, lineType=cv2.LINE_AA)


def draw_degree_scale(img, centre, x1, x2):
    r = int((x2 - x1) / 2)
    cv2.circle(img, centre, r, (255, 0, 0), 10, lineType=cv2.LINE_AA)
    draw_minutes(img, centre, r)


def draw_minutes(img, centre, r):
    range_22_5 = np.arange(0, 360, 22.5)
    for i in range_22_5:
        pt = get_point_at_circle(centre, r, i)
        line_blue_1(img, centre, pt)

    range_11_25 = np.arange(0, 360, 11.25)
    for i in range_11_25:
        pt = get_point_at_circle(centre, r-50, i)
        line_blue_1(img, centre, pt)
