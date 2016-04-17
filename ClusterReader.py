import time
import timeit

import yaml

from CanDriver import CanDriver
from image_processing.geometry import *
from image_processing import image_analysis as cv
from utils import file_utils

GREY_MODE = True
CAMERA    = False
LED_ON_BW_RATIO = 0.25

class ClusterReader:
    def __init__(self):
        can = CanDriver()
        self.can_bus = can if can.valid_setup else None

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
        self.current_state = self.build_initial_state()
        self.paused = False
        self.overlay = cv.get_empty_img(self.res_x, self.res_y)
        _, self.img = self.cap.read()

        self.right_click_dialog = False
        self.left_click_dialog = False

    def setup_window(self):
        # cv2.namedWindow('prev', flags=cv2.WINDOW_KEEPRATIO)
        # cv2.moveWindow('prev', 1200, 400)
        # cv2.resizeWindow('prev', 600, 400)
        cv2.namedWindow('image', flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow('image', 600, 200)
        # cv2.resizeWindow('image', 800)
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
            pass

        # on left click:
        if event == 1 and not self.left_click_dialog:
            pass


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
                # start = time.time()
                self.analyse()
                # end = time.time()
                # print('analysis time: ', end - start)
                self.draw_overlay()

            if GREY_MODE:
                rgb = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
                dst = cv2.add(rgb, self.overlay)
            else:
                dst = cv2.addWeighted(self.img, 0.7, self.overlay, 0.3, 0)
            y = 25
            for name, data in self.current_state.items():
                color = (0, 255, 0) if data else (0, 0, 255)
                txt = "{0}: {1}".format(name, data)
                cv2.putText(img=dst, org=(700, y), text=txt,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=color, thickness=2, lineType=cv2.LINE_AA)
                y += 30
            cv2.imshow('image', dst)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
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
            elif key == ord('a'):
                self.analyse()

        self.cap.release()
        cv2.destroyAllWindows()


    def draw_overlay(self):
        """Draws overlay with detected templates and training data"""
        self.overlay = cv.get_empty_img(self.res_x, self.res_y)
        for name, data in self.training_data.items():
            rec = data['roi']
            cv2.rectangle(self.overlay, rec[0], rec[3], (0, 255, 255), 3)
            cv2.putText(img=self.overlay, org=rec[0], text=name,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 255, 0), thickness=3, lineType=cv2.LINE_AA)

    def analyse(self):
        for name, data in self.training_data.items():
            roi = data['roi']
            img = self.img[roi[0][1]:roi[3][1], roi[0][0]:roi[3][0]]
            _, im_bw = cv2.threshold(img, 150, 250, cv2.THRESH_BINARY)
            value = 0
            # cv2.imshow('image1', img)
            # cv2.imshow('image2', im_bw)
            # key = cv2.waitKey(0) & 0xFF
            # if key == ord('q'):
            #     end = time.time()

            if data['type'] == 'LED':
                black = 0
                for x in np.nditer(im_bw):
                    y = int(x)
                    if y == 0:
                        black += 1
                total = im_bw.size
                white = total - black
                if white >= total * LED_ON_BW_RATIO:
                    value = 1
                else:
                    value = 0

            elif data['type'] == 'ANALOG':
                center = (int(img.shape[0] / 2), int(img.shape[1] / 2))
                lines = cv.detect_lines_p(im_bw)
                degs = get_line_degrees(lines, center)
                if degs is not None:
                    values_data = data['data']
                    xp = []
                    fp = []
                    kk = []
                    for d in values_data:
                        kk.append([d['degree'], d['value']])
                        xp.append(d['degree']*1.0)
                        fp.append(d['value']*1.0)
                    avg_deg = np.mean(degs)
                    interpolated = np.interp(avg_deg * 1.0, xp=xp, fp=fp, period=360)
                    value = int(interpolated * 1000) if name == 'REVS' else int(interpolated)
            self.current_state[name] = value
            self.can_bus.transmit(name, value)

    def build_initial_state(self):
        state = {}
        for name in self.training_data.keys():
            state[name] = False
        return state


if __name__ == '__main__':
    testing = ClusterReader()
    testing.capture()
