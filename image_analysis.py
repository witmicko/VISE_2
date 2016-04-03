import cv2
import numpy as np


def detect_lines(img):
    (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
    return cv2.HoughLines(im_bw, 1, np.pi / 180, 190)


def detect_lines_P(img):
    (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
    # cv2.imshow('bw', im_bw)
    # key = cv2.waitKey(33) & 0xFF
    return cv2.HoughLinesP(im_bw, 1, np.pi / 360.0, 90, minLineLength=180, maxLineGap=0)