import cv2
import yaml
from easygui import *

import file_utils
import image_templates as templates
from gui.CvDialog import CvDialog
# from gui.my_dialogs import LeftClickDialog, RightClickDialog
from template_matchers import match

GREY_MODE = True
class Training:
    def __init__(self):
        self.templates = templates.get_templates(GREY_MODE)

        self.cap = cv2.VideoCapture('Video 3.mp4')
        self.paused = False
        self.setup_window()
        self.setup_capture()
        _, self.img = self.cap.read()
        self.matches = file_utils.load_training_json()
        self.matches['break'] = [(50, 50), (100, 50), (50, 100), (100, 100)]
        self.right_click_dialog = False;
        self.left_click_dialog = False;

    def setup_window(self):
        cv2.namedWindow('image', flags=cv2.WINDOW_KEEPRATIO)
        # cv2.moveWindow('image', 1200, 400)
        # cv2.resizeWindow('image', 600, 400)
        cv2.setMouseCallback('image', self.on_mouse)

    def setup_capture(self):
        config = yaml.load(open('cam_config.yaml', 'r'))['cap']
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['res_x'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['res_y'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, config['contrast'])
        self.cap.set(cv2.CAP_PROP_FOCUS, config['focus'])
        self.cap.set(cv2.CAP_PROP_GAIN, config['gain'])
        self.cap.set(cv2.CAP_PROP_SATURATION, config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, config['sharpness'])
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, config['white_balance'])
        self.cap.set(cv2.CAP_PROP_ZOOM, config['zoom'])

    def on_mouse(self, event, x, y, flags, param):
        if event == 2 and not self.right_click_dialog:
            choices = multchoicebox(msg='select templates',
                                    title='selector',
                                    preselect=-1,
                                    choices=self.templates.keys())

            for key in self.templates.keys():
                if choices is not None and key in choices:
                    self.templates[key]['active'] = True
                else:
                    self.templates[key]['active'] = False

        if event == 1 and not self.left_click_dialog:
            print(event, x, y, flags, param)
            # d = MyDialog(self.gui_root)
            # self.gui_root.wait_window(d.top)
        pass

    def capture(self):
        while self.cap.isOpened():
            if not self.paused:
                ret, frame = self.cap.read()
                if GREY_MODE:
                    self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                else:
                    self.img = frame
                self.detect(image=self.img)

            cv2.imshow('image', self.img)
            key = cv2.waitKey(33) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                self.paused = not self.paused
                print('paused', self.paused)

            elif key == ord('d'):
                print('detecting')
                self.detect(image=self.img)
        self.cap.release()
        cv2.destroyAllWindows()

    def detect(self, image):
        for name, t in self.templates.items():
            if t['active']:
                template = t['img']
                rec = match(image=image, template=template)
                if rec is not None:
                    cv2.rectangle(self.img, rec[0], rec[3], 255, 2)
                    cv2.putText(img=self.img, org=rec[0], text=name,
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2,
                                color=(0, 0, 255),
                                thickness=5)


if __name__ == '__main__':
    training = Training()
    training.capture()
