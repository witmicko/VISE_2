import cv2
import numpy as np

from geometry import get_point_at_circle


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
    # angles: 0, 22, 45, 67, 90, 112, 135,157, 180, 202, 225, 247, 270, 292, 315, 337
    # 0 to 180
    # pt_0 = get_point_at_circle(centre, r, 0)
    # put_angle_text(img, pt_0, 5, 10, '0')
    # pt_180 = get_point_at_circle(centre, r, 180)
    # put_angle_text(img, pt_180, -50, 10, '180')
    # line_blue_5(img, pt_0, pt_180)
    #
    # # 90 to 270
    # pt_90 = get_point_at_circle(centre, r, 90)
    # put_angle_text(img, pt_90, -30, -10, '90')
    # pt_270 = get_point_at_circle(centre, r, 270)
    # put_angle_text(img, pt_270, -50, 40, '270')
    # line_blue_5(img, pt_90, pt_270)
    #
    # # 135 to 315
    # pt_135 = get_point_at_circle(centre, r, 135)
    # put_angle_text(img, pt_135, -90, -0, '135')
    # pt_315 = get_point_at_circle(centre, r, 315)
    # put_angle_text(img, pt_315, 10, 20, '315')
    # line_blue_2(img, pt_135, pt_315)
    #
    # # 225 to 45
    # pt_225 = get_point_at_circle(centre, r, 225)
    # put_angle_text(img, pt_225, -95, 25, '225')
    # pt_45 = get_point_at_circle(centre, r, 45)
    # put_angle_text(img, pt_45, 10, 0, '45')
    # line_blue_2(img, pt_225, pt_45)
    
    # 22 to 202
    # pt_202 = get_point_at_circle(centre, r, 202)
    # put_angle_text(img, pt_202, -90, 10, '202')
    # pt_22 = get_point_at_circle(centre, r, 22)
    # put_angle_text(img, pt_22, 10, 0, '22')
    # line_blue_2(img, pt_202, pt_22)
    #
    # # 67 to 247
    # pt_247 = get_point_at_circle(centre, r, 247)
    # put_angle_text(img, pt_247, -60, 40, '247')
    # pt_67 = get_point_at_circle(centre, r, 67)
    # put_angle_text(img, pt_67, 10, 0, '67')
    # line_blue_2(img, pt_247, pt_67)
    #
    # # 112 to 292
    # pt_112 = get_point_at_circle(centre, r, 112)
    # put_angle_text(img, pt_112, -60, -15, '112')
    # pt_292 = get_point_at_circle(centre, r, 292)
    # put_angle_text(img, pt_292, 0, 40, '292')
    # line_blue_2(img, pt_112, pt_292)
    #
    # # 157 to 337
    # pt_157 = get_point_at_circle(centre, r, 157)
    # put_angle_text(img, pt_157, -90, -0, '157')
    # pt_337 = get_point_at_circle(centre, r, 337)
    # put_angle_text(img, pt_337, 10, 20, '337')
    # line_blue_2(img, pt_157, pt_337)

    draw_minutes(img, centre, r)


def draw_minutes(img, centre, r):
    range_22_5 = np.arange(0, 360, 22.5)
    for i in range_22_5:
        pt = get_point_at_circle(centre, r, i)
        # cv2.circle(img, pt, 2, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        line_blue_1(img, centre, pt)
        # cv2.putText(img, str(i), pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    range_11_25 = np.arange(0, 360, 11.25)
    for i in range_11_25:
        pt = get_point_at_circle(centre, r-50, i)
        # cv2.circle(img, pt, 2, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        line_blue_1(img, centre, pt)
        # cv2.putText(img, str(i), pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
