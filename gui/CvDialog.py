import cv2


class CvDialog:
    def __init__(self, templates):
        window_name = 'template select'
        window = cv2.namedWindow(window_name)

        for name, t in templates.items():
            cv2.createTrackbar(name, window_name, t['active'], 1)
