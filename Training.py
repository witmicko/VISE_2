from math import atan2
from threading import Thread

import cv2
import numpy as np
import time
import yaml
from easygui import *
import file_utils
import image_templates as templates
from angles import getAngleBetweenPoints
from template_matchers import match
from matplotlib import pyplot as plt
GREY_MODE = True
CAMERA = False


class Training:
    def __init__(self):
        self.frame_count = 0
        self.start = None
        self.paused_time = 0
        if CAMERA:
            self.config = yaml.load(open('cam_config.yaml', 'r'))['cap']
            self.res_x = self.config['res_x']
            self.res_y = self.config['res_y']
            self.cap = cv2.VideoCapture(0)
            self.setup_capture()
        else:
            self.cap = cv2.VideoCapture('Video 3.mp4')
            self.res_x = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.res_y = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.setup_window()

        self.training_data = file_utils.load_training_json()
        self.templates = templates.get_templates(GREY_MODE)
        self.paused = False

        self.overlay = self.get_empty_img()
        _, self.current_frame = self.cap.read()
        _, self.img = self.cap.read()

        # img = self.img[307:928, 41:656]
        #
        # # img = self.img[345:965, 1259:1908]
        # # edges = cv2.Canny(img, 1, 150, apertureSize=3)
        # lines = self.detect_lines(img)
        # for line in lines:
        #     print(line)
        #     rho, theta = line[0]
        #     a = np.cos(theta)
        #     b = np.sin(theta)
        #     x0 = a * rho
        #     y0 = b * rho
        #     x1 = int(x0 + 200 * (-b))
        #     y1 = int(y0 + 200 * (a))
        #     x2 = int(x0 - 200 * (-b))
        #     y2 = int(y0 - 200 * (a))
        #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        #
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # exit()

        self.matches = {}
        self.right_click_dialog = False
        self.left_click_dialog = False



    def setup_window(self):
        cv2.namedWindow('image', flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('image', 1200, 400)
        cv2.resizeWindow('image', 600, 400)
        cv2.setMouseCallback('image', self.on_mouse)

    def setup_capture(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.res_x)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.res_y)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.config['brightness'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, self.config['contrast'])
        self.cap.set(cv2.CAP_PROP_FOCUS, self.config['focus'])
        self.cap.set(cv2.CAP_PROP_GAIN, self.config['gain'])
        self.cap.set(cv2.CAP_PROP_SATURATION, self.config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, self.config['sharpness'])
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, self.config['white_balance'])
        self.cap.set(cv2.CAP_PROP_ZOOM, self.config['zoom'])

    def on_mouse(self, event, x, y, flags, param):
        # on right click show simple dialog to select active templates to search for
        if event == 2 and not self.right_click_dialog:

            paused_time = time.time()
            self.right_click_dialog = True
            choices = multchoicebox(msg='select templates',
                                    title='selector',
                                    preselect=-1,
                                    choices=self.templates.keys())
            for key in self.templates.keys():
                if choices is not None and key in choices:
                    self.templates[key]['active'] = True
                else:
                    self.templates[key]['active'] = False
            self.right_click_dialog = False
            self.paused_time += time.time() - paused_time

        # on left click:
        if event == 1 and not self.left_click_dialog:
            print(x, y)
            paused_time = time.time()
            self.left_click_dialog = True
            self.training_data_dialog(x, y)

            self.left_click_dialog = False
            self.paused_time += time.time() - paused_time

    def is_click_inside_rect(self, x, y):
        """Checks if click is inside of any matching template areas"""
        inside_of = []
        for m, rec in self.matches.items():
            if rec is not None:
                x_in = rec[0][0] <= x <= rec[1][0]
                y_in = rec[0][1] <= y <= rec[2][1]
                is_in = x_in and y_in
                print(is_in)
                if is_in:
                    inside_of.append(m)
        return inside_of

    def capture(self):
        """runs main loop and camera"""
        self.start = time.time()
        while self.cap.isOpened():
            if not self.paused:
                ret, frame = self.cap.read()
                self.frame_count += 1
                if GREY_MODE:
                    self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                else:
                    self.img = frame
                self.detect(image=self.img)

            # self.draw_overlay()
            if GREY_MODE:
                rgb = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
                # dst = cv2.addWeighted(backtorgb, 0.7, self.overlay, 0.3, 0)
                dst = cv2.add(rgb, self.overlay)
            else:
                dst = cv2.addWeighted(self.img, 0.7, self.overlay, 0.3, 0)


            img1 = self.img[307:928, 41:656]
            center = (int(img1.shape[0]/2), int(img1.shape[1]/2))
            lines2 = self.detect_lines_P(img1)
            if lines2 is not None :
                a, b, c = lines2.shape
                for i in range(a):
                    pt_A = (lines2[i][0][0], lines2[i][0][1])
                    pt_B = (lines2[i][0][2], lines2[i][0][3])
                    cv2.circle(dst, pt_A, 20, (0, 0, 255), 5) #RED
                    cv2.circle(dst, pt_B, 20, (0, 255, 0), 5) #GREEN

                    dist_A = np.math.hypot(pt_A[0] - center[0], pt_A[1] - center[1])
                    dist_B = np.math.hypot(pt_B[0] - center[0], pt_B[1] - center[1])
                    if dist_A < dist_B:
                        degs = getAngleBetweenPoints(pt_A, pt_B)
                    else:
                        degs = getAngleBetweenPoints(pt_B, pt_A)

                    if degs < 0:
                        degs += 360
                    print(degs)
                    if degs > 200:
                        pass

                    cv2.line(dst, pt_A, pt_B, (0, 0, 255), 3, cv2.LINE_AA)

            cv2.imshow('image', dst)
            key = cv2.waitKey(33) & 0xFF
            if key == ord('q'):
                file_utils.save_training_json(self.training_data)
                end = time.time()
                durr = end - self.start - self.paused_time
                print('durr', durr)
                print('paused time', self.paused_time)
                print('frames', self.frame_count)
                print('fps', self.frame_count / durr)
                break
            elif key == ord(' '):
                paused_time = time.time()
                self.paused = not self.paused
                print('paused', self.paused)
                self.paused_time += time.time() - paused_time

            elif key == ord('d'):
                print('detecting')
                self.detect(image=self.img)
        self.cap.release()
        cv2.destroyAllWindows()


    def detect_lines(self, img):
        (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
        return cv2.HoughLines(im_bw, 1, np.pi / 180, 190)

    def detect_lines_P(self, img):
        (thresh, im_bw) = cv2.threshold(img, 210, 250, cv2.THRESH_BINARY)
        # cv2.imshow('bw', im_bw)
        # key = cv2.waitKey(33) & 0xFF
        return cv2.HoughLinesP(im_bw, 1, np.pi / 360.0, 90, minLineLength=180, maxLineGap=0)
        


    def detect(self, image):
        """Detects active templates within the image and returns
            rectangle points starting at top left and going clockwise"""
        for name, t in self.templates.items():
            if t['active'] and name not in self.training_data:
                template = t['img']
                rec = match(image=image, template=template)
                self.matches[name] = rec

    def draw_overlay(self):
        """Draws overlay with detected templates and training data"""
        self.overlay = self.get_empty_img()
        drawn = []
        for name, data in self.training_data.items():
            rec = data['roi']
            cv2.rectangle(self.overlay, rec[0], rec[3], (0, 255, 255), 3)
            cv2.putText(img=self.overlay, org=rec[0], text=name,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                        color=(0, 255, 0), thickness=5)
            drawn.append(name)

        for name, rec in self.matches.items():
            if rec is not None and name not in drawn:
                cv2.rectangle(self.overlay, rec[0], rec[3], (0, 255, 255), 3)
                cv2.putText(img=self.overlay, org=rec[0], text=name,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                            color=(0, 0, 255), thickness=5)

    def get_empty_img(self):
        """Returns empty image with the same size as current capture frame size"""
        return np.zeros((self.res_y, self.res_x, 3), np.uint8)


    def training_data_dialog(self, x, y):
        xx = self.is_click_inside_rect(x, y)
        if xx:
            choice = choicebox(msg='select template detected properly and ready to save as training data',
                               choices=xx)
            led_or_analog = choicebox(msg='LED or analog?', choices=['LED', 'ANALOG'])
            match_rec = self.matches[choice]
            if 'LED' in led_or_analog:
                self.training_data[choice] = {
                    'type': led_or_analog,
                    'roi': match_rec
                }
            elif 'ANALOG' in led_or_analog:
                # numpy indexing [y1:y2, x1:x2]
                roi = self.img[345:965, 1259:1908]
                roi = self.img[match_rec[0][1]:match_rec[3][1], match_rec[0][0]:match_rec[3][0]]
                laplacian = cv2.Laplacian(roi, cv2.CV_64F)
                cv2.imshow('image', laplacian)
                cv2.waitKey(0)
                print(choice)



if __name__ == '__main__':
    training = Training()
    training.capture()
