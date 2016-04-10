from __future__ import print_function

from canlib import canlib_xl
# import canlib_xl
import ctypes
import msvcrt
import time

if __name__ == "__main__":

    canlib_xl.XL_TRANSMIT_MSG

    can = canlib_xl.candriver()
    can.open_driver()
    mask = can.get_channel_mask()
    ok, phandle, pmask = can.open_port()
    print(ok)
    # ok=can.can_set_channel_bitrate(phandle, mask, 500000)
    # print ok, "ChannelBitrate"
    ok = can.get_appl_config()
    print(ok, "appl config")
    ok = can.activate_channel(phandle)
    print(ok, phandle)
    event_list = canlib_xl.XLevent(0)
    print(event_list)
    event_count = ctypes.c_uint(1)
    print(event_count)
    ok = 1
    loop = 1
    while loop:
        if msvcrt.kbhit():
            loop = 0
        ok = 1
        while (ok):
            event_count = ctypes.c_uint(1)
            # print phandle, event_count
            ok = can.receive(phandle, event_count, event_list)
            time.sleep(0.001)

            # print ok, event_list

        rec_string = can.get_event_string(event_list)
        print(rec_string)
        # print ok, event_count, event_list

    can.deactivate_channel(phandle, mask)
    can.close_port(phandle)
    can.close_driver()
