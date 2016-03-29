import tkinter

import cv2
import yaml

import templates


class Training:
    def __init__(self):
        self.templates = templates.t
        self.cap = cv2.VideoCapture(0)
        # self.cap = cv2.VideoCapture('Video 3.mp4')
        self.method = cv2.TM_SQDIFF_NORMED
        self.gui_root = tkinter.Tk()
        self.gui_root.wm_state('iconic')
        self.paused = False
        self.setup_window()
        self.setup_capture()
        _, self.img = self.cap.read()
        self.matches = yaml.load(open('training.yaml', 'r'))
        print()

    def setup_window(self):
        cv2.namedWindow('image', flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('image', 1200, 400)
        cv2.resizeWindow('image', 600, 400)
        cv2.setMouseCallback('image', self.onmouse)

        # d = MyDialog(self.gui_root)
        # self.gui_root.wait_window(d.top)

    def setup_capture(self):
        config = yaml.load(open('cam_config.yaml', 'r'))['cap']
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config['res_x'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['res_y'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS,   config['brightness'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS,   config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST,     config['contrast'])
        self.cap.set(cv2.CAP_PROP_FOCUS,        config['focus'])
        self.cap.set(cv2.CAP_PROP_GAIN,         config['gain'])
        self.cap.set(cv2.CAP_PROP_SATURATION,   config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS,    config['sharpness'])
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, config['white_balance'])
        self.cap.set(cv2.CAP_PROP_ZOOM,         config['zoom'])

    def onmouse(self, event, x, y, flags, param):
        pass



    def capture(self):
        while self.cap.isOpened():
            if not self.paused:
                ret, self.img = self.cap.read()
                # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                self.detect()

            cv2.imshow('image', self.img)
            key = cv2.waitKey(33) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                self.paused = not self.paused
                print('paused', self.paused)

            elif key == ord('d'):
                print('detecting')
                self.detect()

        self.cap.release()
        yaml.dump(self.matches, open('training.yaml', 'w'), default_flow_style=False)
        cv2.destroyAllWindows()

    def detect(self):
        for t, name in self.templates.items():
                # Apply template Matching
                template = cv2.imread('templates/' + t)
                # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                # template = cv2.Canny(template, 50, 200)
                w, h = template.shape[:2]

                res = cv2.matchTemplate(self.img, template, self.method)
                res_2 = cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
                # print(res_2)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_2)
                # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if self.method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)

                if max_val == 1:
                    # print(t, 'max_val', max_val)
                    # cv2.circle(img=img, center=min_loc, radius=20, color=(255, 255, 255), thickness=10, lineType=8, shift=0)
                    rec = (top_left, (bottom_right[0],top_left[1]), (top_left[0], bottom_right[1]),bottom_right)
                    self.matches[name]=rec
                    cv2.rectangle(self.img, top_left, bottom_right, 255, 2)

                    cv2.putText(img=self.img, org=top_left, text=name, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                                color=(0, 0, 255), thickness=5)


if __name__ == '__main__':
    training = Training()
    training.capture()