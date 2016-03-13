import cv2
import atexit
import yaml

from subprocess import call, check_output


class CameraSettings:
    def __init__(self, captureObject):
        self.cap = captureObject
        self.setup_capture()

    def setup_capture(self):
        config = yaml.load(open('cam_config.yaml', 'r'))['cap']
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, config['brightness'])
        self.cap.set(cv2.CAP_PROP_CONTRAST, config['contrast'])
        self.cap.set(cv2.CAP_PROP_FOCUS, config['focus'])
        self.cap.set(cv2.CAP_PROP_GAIN, config['gain'])
        self.cap.set(cv2.CAP_PROP_SATURATION, config['saturation'])
        self.cap.set(cv2.CAP_PROP_SHARPNESS, config['sharpness'])
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, config['white_balance'])
        self.cap.set(cv2.CAP_PROP_ZOOM, config['zoom'])

    def getFocus(self):
        return int(cap.get(cv2.CAP_PROP_FOCUS))

    def getContrast(self):
        return int(cap.get(cv2.CAP_PROP_CONTRAST))

    def getBrightness(self):
        return int(cap.get(cv2.CAP_PROP_BRIGHTNESS))

    def getSaturation(self):
        return int(cap.get(cv2.CAP_PROP_SATURATION))

    def getHue(self):
        return int(cap.get(cv2.CAP_PROP_HUE))

    def getGain(self):
        return int(cap.get(cv2.CAP_PROP_GAIN))

    def getWhiteBalance(self):
        return int(cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V))

    def setFocus(self, arg):
        self.cap.set(cv2.CAP_PROP_FOCUS, arg)

    def setContrast(self, arg):
        self.cap.set(cv2.CAP_PROP_CONTRAST, arg)

    def setBrightness(self, arg):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, arg)

    def setSaturation(self, arg):
        self.cap.set(cv2.CAP_PROP_SATURATION, arg)

    def setHue(self, arg):
        self.cap.set(cv2.CAP_PROP_HUE, arg)

    def setGain(self, arg):
        self.cap.set(cv2.CAP_PROP_GAIN, arg)

    def setWhiteBalance(self, arg):
        self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, arg)

    def get_zoom(self):
        return self.cap.get(cv2.CAP_PROP_ZOOM)

    def set_zoom(self, arg):
        self.cap.set(cv2.CAP_PROP_ZOOM, arg)

    def get_sharpness(self):
        return self.cap.get(cv2.CAP_PROP_SHARPNESS)

    def set_sharpness(self, arg):
        self.cap.set(cv2.CAP_PROP_SHARPNESS, arg)

    def get_exposure(self):
        return self.cap.get(cv2.CAP_PROP_EXPOSURE)

    def set_exposure(self, arg):
        self.cap.set(cv2.CAP_PROP_EXPOSURE, arg)

    def save(self):
        settings = {
            'cap': {
                'contrast': self.getContrast(),
                'brightness': self.getBrightness(),
                'saturation': self.getSaturation(),
                'exposure': self.get_exposure(),
                'gain': self.getGain(),
                'white_balance': self.getWhiteBalance(),
                'focus': self.getFocus(),
                'zoom': self.get_zoom(),
                'sharpness': self.get_sharpness()
            }
        }
        stream = open('cam_config.yaml', 'w')
        yaml.dump(settings, stream, default_flow_style=False)
        print(yaml.dump(settings))

    def trackbar(self, windowName, trackbarName, callback, start=128, max=255):
        cv2.namedWindow(windowName)
        cv2.createTrackbar(trackbarName, windowName, start, max, callback)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    camSettings = CameraSettings(cap)
    # atexit.register(camSettings.save)

    camSettings.trackbar("window", "brightness", camSettings.setBrightness, camSettings.getBrightness())
    camSettings.trackbar("window", "contrast", camSettings.setContrast, camSettings.getContrast())
    camSettings.trackbar("window", "exposure", camSettings.set_exposure, start=128)
    camSettings.trackbar("window", "focus", camSettings.setFocus, camSettings.getFocus())
    camSettings.trackbar("window", "gain", camSettings.setGain, camSettings.getGain())
    camSettings.trackbar("window", "saturation", camSettings.setSaturation, camSettings.getSaturation())
    camSettings.trackbar("window", "sharpness", camSettings.set_sharpness, start=128)
    camSettings.trackbar("window", "white balance", camSettings.setWhiteBalance, camSettings.getWhiteBalance())
    camSettings.trackbar("window", "zoom", camSettings.set_zoom, start=100, max=500)

    while camSettings.cap.isOpened:
        _, image = camSettings.cap.read()
        cv2.imshow("window2", image)
        print(cap.get(cv2.CAP_PROP_SATURATION))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camSettings.save()
            break
cap.release()
cv2.destroyAllWindows()
