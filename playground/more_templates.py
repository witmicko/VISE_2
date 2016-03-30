import numpy as np
import cv2

cap = cv2.VideoCapture('Video 3.mp4')
templates = ['abs.png',
             # 'airbag_1.png',
             # 'esp.png',
             # 'esp_off.png',
             # 'fuel.png',
             # 'gear_speed.png',
             # 'ind_left.png',
             # 'ind_right.png',
             # 'parking_brake.png',
             # 'parking_brake_warn.png',
             # 'rev.png',
             # 'water.png'
             ]

# template = cv2.imread('abs_2.png', 0)
# w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED',
# 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
methods = ['cv2.TM_CCOEFF']

while (cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    method = eval('cv2.TM_SQDIFF')
    for t in templates:
        # Apply template Matching
        template = cv2.imread('templates/'+t)
        # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # template = cv2.Canny(template, 50, 200)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(gray, template, method)
        # res_2 = cv2.normalize(res,res,0,1,cv2.NORM_MINMAX,-1)
        # print(res_2)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        print(t, 'max_val', max_val)
        if max_val > 0.0:
            cv2.rectangle(gray, top_left, bottom_right, 255, 2)
            cv2.putText(img=gray, org=top_left, text=t, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255))
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
