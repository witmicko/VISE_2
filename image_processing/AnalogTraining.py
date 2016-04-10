import cv2
from easygui import integerbox

from image_processing.geometry import get_angle_between_points


class AnalogTraining:
    def __init__(self, match_rec, img):
        self.match_rec = match_rec
        self.img = img.copy()
        self.roi = img[match_rec[0][1]:match_rec[3][1], match_rec[0][0]:match_rec[3][0]]
        self.center = (int(self.roi.shape[0] / 2) + match_rec[0][0], int(self.roi.shape[1] / 2) + match_rec[0][1])
        self.training_data = []

    def run(self):
        cv2.namedWindow('ANALOG', flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('ANALOG', 1200, 400)
        cv2.resizeWindow('ANALOG', 1280, 720)
        cv2.setMouseCallback('ANALOG', self.on_mouse)
        x_offset = 0
        y_offset = 0
        while True:
            image = self.img.copy()
            text = 'Press "e" to exit and save, "r" to reset current data'
            cv2.putText(image, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 5, cv2.LINE_AA)
            h = 150
            for t in self.training_data:
                txt = "deg {0}, value: {1}".format(t['degree'], t['value'])
                cv2.putText(image, txt, (100, h), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 5, cv2.LINE_AA)
                h += 50

            cv2.imshow('ANALOG', image)
            key = cv2.waitKey(33) & 0xFF
            if key == ord('e'):
                break
            elif key == ord('r'):
                self.training_data = []

        cv2.destroyWindow('ANALOG')
        return self.training_data

    def on_mouse(self, event, x, y, flags, param):
        # deg = get_angle_between_points(self.center, (x, y))
        # print(deg)
        if event == cv2.EVENT_LBUTTONDOWN:
            deg = int(get_angle_between_points(self.center, (x, y)))
            deg_plus_90 = (deg + 90)%360
            i = integerbox(msg="enter value", title='analog trainer', lowerbound=0, upperbound=9999)
            self.training_data.append({'degree': deg_plus_90, 'value': i})



