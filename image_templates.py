import cv2
LED_TEMPLATES = {
    'ABS':          {'active': False, 'file': 'abs.png'},
    'AIRBAG':       {'active': False, 'file': 'airbag_1.png'},
    'BRAKE':        {'active': False, 'file': 'parking_brake.png'},
    'BRAKE_WARN':   {'active': False, 'file': 'parking_brake_warn.png'},
    'ESP':          {'active': False, 'file': 'esp.png'},
    'ESP_OFF':      {'active': False, 'file': 'esp_off.png'},
    'FUEL':         {'active': False, 'file': 'fuel.png'},
    'GB_SPEED':     {'active': False, 'file': 'gear_speed.png'},
    'IND_LT':       {'active': False, 'file': 'ind_left.png'},
    'IND_RT':       {'active': False, 'file': 'ind_right.png'},
    'REVS':         {'active': False, 'file': 'rev.png'},
    'WATER':        {'active': False, 'file': 'water.png'}
     }


def get_templates(grey=False):
    templates = {}
    for name, t in LED_TEMPLATES.items():
        if grey:
            templates[name] = cv2.cvtColor(cv2.imread('templates/' + t['file']), cv2.COLOR_BGR2GRAY)
        else:
            templates[name] = cv2.imread('templates/' + t['file'])
    return templates

