import cv2

methods = [
    cv2.TM_CCOEFF,
    cv2.TM_CCOEFF_NORMED,
    cv2.TM_CCORR,
    cv2.TM_CCORR_NORMED,
    cv2.TM_SQDIFF,
    cv2.TM_SQDIFF_NORMED
]


def match(image=None, template=None, method=cv2.TM_SQDIFF_NORMED):
    w, h = template.shape[:2]
    res = cv2.matchTemplate(image, template, method)

    res_2 = cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_2)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if min_val == 0:
        rec = (top_left, (bottom_right[0], top_left[1]), (top_left[0], bottom_right[1]), bottom_right)
        return rec

# def match_2(image=None,template=None, method=cv2.TM_SQDIFF_NORMED):
