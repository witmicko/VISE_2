"""
Holds list of current templates
"""
import cv2
LED_TEMPLATES = {
    'ABS':          {'active': True, 'file': 'abs.png'},
    'AIRBAG':       {'active': True, 'file': 'airbag.png'},
    'BRAKE':        {'active': True, 'file': 'parking_brake.png'},
    'BRAKE_WARN':   {'active': True, 'file': 'parking_brake_warn.png'},
    'ESP':          {'active': True, 'file': 'esp.png'},
    'ESP_OFF':      {'active': False, 'file': 'esp_off.png'},
    # 'FUEL':         {'active': False, 'file': 'fuel.png'},
    # 'GB_SPEED':     {'active': False, 'file': 'gear_speed.png'},
    # 'IND_LT':       {'active': False, 'file': 'ind_left.png'},
    # 'IND_RT':       {'active': False, 'file': 'ind_right.png'},
    'REVS':         {'active': False, 'file': 'revs.png'},
    'SPEED':        {'active': False, 'file': 'speed.png'}
    # 'WATER':        {'active': False, 'file': 'water.png'}
     }


def get_templates(grey=False):
    """
    Returns dict of templates as either gray or bgr colour space
    """
    templates = {}
    for name, t in LED_TEMPLATES.items():
        temp = {'active': t['active']}
        if grey:
            temp['img'] = cv2.cvtColor(cv2.imread('templates/' + t['file']), cv2.COLOR_BGR2GRAY)
        else:
            temp['img'] = cv2.imread('templates/' + t['file'])

        templates[name] = temp
    return templates

