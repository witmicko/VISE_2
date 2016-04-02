from threading import Thread

import cv2
import numpy as np
import time
import yaml
from easygui import *
import file_utils
import image_templates as templates
from template_matchers import match

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
            paused_time = time.time()
            self.left_click_dialog = True
            xx = self.is_click_inside_rect(x, y)
            if xx:
                choice = choicebox(msg='select template detected properly and ready to save as training data',
                                   choices=xx)
                led_or_analog = choicebox(msg='LED or analog?', choices=['LED', 'ANALOG'])
                self.training_data[choice] = {
                    'type': led_or_analog,
                    'roi': self.matches[choice]
                }
                print(choice)
            self.left_click_dialog = False
            self.paused_time += time.time() - paused_time


    def is_click_inside_rect(self, x, y):
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
        # runs main loop and camera
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

            self.draw_overlay()
            if GREY_MODE:
                backtorgb = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
                # dst = cv2.addWeighted(backtorgb, 0.7, self.overlay, 0.3, 0)
                dst = cv2.add(backtorgb, self.overlay)
            else:
                dst = cv2.addWeighted(self.img, 0.7, self.overlay, 0.3, 0)

            cv2.imshow('image', dst)
            key = cv2.waitKey(33) & 0xFF
            if key == ord('q'):
                file_utils.save_training_json(self.training_data)
                end = time.time()
                durr = end - self.start - self.paused_time
                print('durr',durr)
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

    def detect(self, image):
        # detects active templates within the image returns rectangle points starting at top left and going clockwise
        for name, t in self.templates.items():
            if t['active'] and name not in self.training_data:
                template = t['img']
                rec = match(image=image, template=template)
                self.matches[name] = rec

    def draw_overlay(self):
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
        return np.zeros((self.res_y, self.res_x, 3), np.uint8)


if __name__ == '__main__':
    training = Training()
    training.capture()
