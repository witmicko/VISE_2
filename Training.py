import time
import image_processing.image_templates as templates
from image_processing.template_matchers import match
from image_processing.AnalogTraining    import AnalogTraining
from image_processing.geometry          import *
from image_processing import image_analysis as cv
import yaml
from easygui import *

from utils import file_utils

GREY_MODE = True
CAMERA    = False


class Training:
    def __init__(self):
        cv2.setUseOptimized(True)
        self.frame_count = 0
        self.start = None
        self.paused_time = 0
        if CAMERA:
            self.config = yaml.load(open('settings/cam_config.yaml', 'r'))['cap']
            self.res_x = self.config['res_x']
            self.res_y = self.config['res_y']
            self.cap = cv2.VideoCapture(0)
            self.setup_capture()
        else:
            self.cap = cv2.VideoCapture('Video 4.mp4')
            self.res_x = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.res_y = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.setup_window()

        self.training_data = file_utils.load_training_json()
        self.templates = templates.get_templates(GREY_MODE)
        self.paused = False

        self.overlay = cv.get_empty_img(self.res_x, self.res_y)
        _, self.img = self.cap.read()

        self.matches = {}
        self.right_click_dialog = False
        self.left_click_dialog = False

    def setup_window(self):
        cv2.namedWindow('image', flags=cv2.WINDOW_KEEPRATIO)
        cv2.setMouseCallback('image', self.on_mouse_main)

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

    def on_mouse_main(self, event, x, y, flags, param):
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
                    if key in self.matches.keys():
                        self.matches.pop(key)

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
        analytics_time = []
        while self.cap.isOpened():
            if not self.paused:
                ret, frame = self.cap.read()
                self.frame_count += 1
                if GREY_MODE:
                    self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                else:
                    self.img = frame
                start = time.time()
                self.detect(image=self.img)
                end = time.time()
                analytics_time.append(end - start)
                # print('analysis time: ', end - start)

            self.draw_overlay()
            if GREY_MODE:
                rgb = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
                dst = cv2.add(rgb, self.overlay)
            else:
                dst = cv2.addWeighted(self.img, 0.7, self.overlay, 0.3, 0)

            cv2.imshow('image', dst)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print('Average analytics time per frame: ', np.mean(analytics_time) * 1000)
                file_utils.save_training_json(self.training_data)
                end = time.time()
                durr = end - self.start - self.paused_time
                print('Frames processed', self.frame_count)
                print('FPS', self.frame_count / durr)
                print('Time per frame: ', (durr * 1000) / self.frame_count)
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
        """
        Detects active templates within the image,
        returns rectangle points starting at top left and going clockwise
        :param image:
        :return:
        """
        for name, t in self.templates.items():
            if t['active'] and name not in self.training_data:
                template = t['img']
                rec = match(image=image, template=template)
                self.matches[name] = rec

    def draw_overlay(self):
        """
        Draws overlay with detected templates and training data
        :return:
        """
        self.overlay = cv.get_empty_img(self.res_x, self.res_y)
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

    def training_data_dialog(self, x, y):
        """
        Shows the dialog when user clicks inside of a detected element
        :param x:
        :param y:
        :return:
        """
        xx = self.is_click_inside_rect(x, y)
        if xx:
            choice = choicebox(msg='select template detected properly and ready to save as training data', choices=xx)
            led_or_analog = choicebox(msg='LED or analog?', choices=['LED', 'ANALOG'])
            if choice is not None and led_or_analog is not None:
                match_rec = self.matches[choice]
                if 'LED' in led_or_analog:
                    self.training_data[choice] = {
                        'type': led_or_analog,
                        'roi': match_rec
                    }
                elif 'ANALOG' in led_or_analog:
                    self.paused = True
                    data = AnalogTraining(match_rec, self.img).run()
                    self.training_data[choice] = {
                        'type': led_or_analog,
                        'roi': match_rec,
                        'data': data
                    }
                    self.paused = False

if __name__ == '__main__':
    training = Training()
    training.capture()
