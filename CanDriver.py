import ctypes

from canlib import canlib_xl
from canlib.canlib_xl import candriver, get_device_id_by_type
from utils.file_utils import load_can_bus_json


class CanDriver:
    def __init__(self):
        settings = load_can_bus_json()
        if 'messages' not in settings:
            self.valid_setup = False
            print('error in CANbus.json, missing messages')

        else:
            self.valid_setup = True
            self.messages = settings['messages']
            self.can = candriver()
            self.can.open_driver()
            device_id = get_device_id_by_type(settings['device'])
            self.mask = self.can.get_channel_mask(hwtype=device_id)
            ok, self.phandle, pmask = self.can.open_port(user_name='VISE')
            print('open port: ', canlib_xl.xl_response_codes[str(ok)])

            ok = self.can.can_set_channel_bitrate(self.phandle, self.mask, settings['baud_rate']*1000)
            print('can_set_channel_bitrate: ', canlib_xl.xl_response_codes[str(ok)])

            ok = self.can.get_appl_config()
            print('get_appl_config: ', canlib_xl.xl_response_codes[str(ok[0])])
            ok = self.can.activate_channel(self.phandle)
            print('activate_channel: ', canlib_xl.xl_response_codes[str(ok)])

    def transmit_on_bus(self, message):
        event_count = ctypes.c_ulong(1)
        ok = self.can.can_transmit(self.phandle, self.mask, event_count, message)
        rec_string = self.can.get_event_string(message)
        print('transmit:', canlib_xl.xl_response_codes[str(ok)], ", msg:", rec_string)

    def transmit(self, name, value):
        tx_id = self.messages[name]['id']
        dlc   = self.messages[name]['dlc']
        msg = self.build_message(tx_id, value, dlc)
        self.transmit_on_bus(message=msg)
        print(name, value)


    def build_message(self, tx_id, data, dlc):
        event_msg = canlib_xl.XLevent(0)
        event_msg.tag = canlib_xl.XL_TRANSMIT_MSG
        event_msg.tagData.msg.id = tx_id
        event_msg.tagData.msg.flags = 0

        bytes = data.to_bytes(dlc, byteorder='big')
        for i in range(len(bytes)):
            event_msg.tagData.msg.data[i] = bytes[i]
        event_msg.tagData.msg.dlc = dlc
        return event_msg


    @staticmethod
    def get_test_message():
        event_msg = canlib_xl.XLevent(0)
        event_msg.tag = canlib_xl.XL_TRANSMIT_MSG
        event_msg.tagData.msg.id = 44
        event_msg.tagData.msg.flags = 0
        event_msg.tagData.msg.data[0] = 0
        event_msg.tagData.msg.data[1] = 0
        event_msg.tagData.msg.data[2] = 0
        event_msg.tagData.msg.data[3] = 0
        event_msg.tagData.msg.data[4] = 0
        event_msg.tagData.msg.data[5] = 0
        event_msg.tagData.msg.data[6] = 0
        event_msg.tagData.msg.data[7] = 0
        event_msg.tagData.msg.dlc = 8
        return event_msg


if __name__ == "__main__":
    can = CanDriver()
    if can.valid_setup:
        msg = can.get_test_message()
        can.transmit(msg)

    print()