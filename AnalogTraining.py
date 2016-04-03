import cv2

from geometry import get_line_degrees
import image_analysis as cv
import gui.drawers as ui


def some_name(match_rec, img):
    roi = img[match_rec[0][1]:match_rec[3][1], match_rec[0][0]:match_rec[3][0]]
    center = (int(roi.shape[0] / 2) + match_rec[0][0], int(roi.shape[1] / 2) + match_rec[0][1])
    lines = cv.detect_lines_p(roi)
    degs = get_line_degrees(lines, match_rec, center)
    x_offset = 0
    y_offset = 0
    while True:
        image = img.copy()
        center = (int(roi.shape[0] / 2) + match_rec[0][0] + x_offset, int(roi.shape[1] / 2) + match_rec[0][1] + y_offset)
        ui.draw_degree_scale(image, center, match_rec[0][0], match_rec[3][0])
        cv2.namedWindow('ANALOG', flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('ANALOG', 1200, 400)
        cv2.resizeWindow('ANALOG', 600, 400)
        cv2.setMouseCallback('ANALOG', on_mouse_anal)
        cv2.imshow('ANALOG', image)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('w'):
            y_offset -= 1
        elif key == ord('s'):
            y_offset += 1
        elif key == ord('a'):
            x_offset -= 1
        elif key == ord('d'):
            x_offset += 1

    cv2.destroyWindow('ANALOG')



def on_mouse_anal(event, x, y, flags, param):
    pass