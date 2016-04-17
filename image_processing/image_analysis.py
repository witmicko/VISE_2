import cv2
import numpy as np


def detect_lines(img):
    """Hough line detection, returns list of parametric form lines"""
    (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
    return cv2.HoughLines(im_bw, 1, np.pi / 180, 190)


def detect_lines_p(img):
    """Finds line segments in a binary image using the probabilistic Hough transform."""
    (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
    return cv2.HoughLinesP(im_bw, 1, np.pi / 360.0, 90, minLineLength=180, maxLineGap=0)


def get_empty_img(res_x, res_y):
    """Returns empty image with the same size as current capture frame size"""
    return np.zeros((res_y, res_x, 3), np.uint8)