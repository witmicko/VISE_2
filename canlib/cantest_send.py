#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
from _ctypes import pointer

from canlib import canlib_xl
import ctypes
import msvcrt
import time

if __name__ == "__main__":
    can = canlib_xl.candriver()
    can.open_driver()
    mask = can.get_channel_mask(hwtype=canlib_xl.devices['VN8950'])
    ok, phandle, pmask = can.open_port()
    # ok, phandle, pmask = can.open_port(user_name='VISE',
    #                                    access_mask=mask,
    #                                    bus_type=canlib_xl.XL_BUS_TYPE_CAN
    #                                    )

    # print(ok)
    ok = can.can_set_channel_bitrate(phandle, mask, 500000)
    # print ok, "ChannelBitrate"
    ok = can.get_appl_config()
    # print(ok, "appl config")
    ok = can.activate_channel(phandle)
    # print(ok, phandle)

    event_msg = canlib_xl.XLevent(0)
    event_msg.tag = canlib_xl.XL_TRANSMIT_MSG
    event_msg.tagData.msg.id = 0x04
    event_msg.tagData.msg.flags = 0
    event_msg.tagData.msg.data[0] = 0
    event_msg.tagData.msg.data[1] = 1
    event_msg.tagData.msg.data[2] = 2
    event_msg.tagData.msg.data[3] = 3
    event_msg.tagData.msg.data[4] = 4
    event_msg.tagData.msg.data[5] = 5
    event_msg.tagData.msg.data[6] = 6
    event_msg.tagData.msg.data[7] = 7
    event_msg.tagData.msg.dlc = 8

    # print event_list
    event_count = ctypes.c_ulong(1)
    # pi = pointer(event_count)
    ok = can.can_transmit(phandle, mask, event_count, event_msg)
    print(ok, event_msg)
    # ok = 1
    # loop = 1
    # while loop:
    #     if msvcrt.kbhit():
    #         loop = 0
    #     ok = 1
    #     while ok:
    #         time.sleep(0.1)
    #         event_count = ctypes.c_uint(1)
    #         ok = can.can_transmit(phandle, mask, event_count, event_msg)
    #         print(ok, event_msg)

    can.deactivate_channel(phandle, mask)
    can.close_port(phandle)
    can.close_driver()
