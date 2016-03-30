import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('vlcsnap.png')
templates = {'abs.png': 'ABS',
             'airbag_1.png': 'AIRBAG',
             'esp.png': 'ESP',
             'esp_off.png': 'ESP_OFF',
             'fuel.png': 'FUEL',
             'gear_speed.png': 'GB_SPEED',
             'ind_left.png': 'IND_LT',
             'ind_right.png': 'IND_RT',
             'parking_brake.png': 'BRAKE',
             'parking_brake_warn.png': 'BRAKE_WARN',
             'rev.png': 'REVS',
             'water.png': 'WATER'
             }

methods = ['cv2.TM_CCOEFF_NORMED']

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
method = eval('cv2.TM_SQDIFF_NORMED')
for t, name in templates.items():
    # Apply template Matching
    template = cv2.imread('templates/' + t)
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # template = cv2.Canny(template, 50, 200)
    w, h = template.shape[:2]

    res = cv2.matchTemplate(img, template, method)
    res_2 = cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
    # print(res_2)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if max_val <= 1:
        print(t, 'max_val', max_val)
        # cv2.circle(img=img, center=min_loc, radius=20, color=(255, 255, 255), thickness=10, lineType=8, shift=0)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)

        cv2.putText(img=img, org=top_left, text=name, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(255, 255, 255))

cv2.imshow('frame', img)
k = cv2.waitKey(0)
if k == 27:  # wait for ESC key to exit
    cv2.destroyAllWindows()

# cv2.destroyAllWindows()
