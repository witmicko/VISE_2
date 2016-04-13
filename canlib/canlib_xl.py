# from __future__ import print_function
from _ctypes import POINTER
from builtins import range
from builtins import object
import ctypes

XLuint64 = ctypes.c_ulonglong
XLaccess = XLuint64
XLstatus = ctypes.c_short
XLporthandle = ctypes.c_long

XL_ACTIVATE_RESET_CLOCK = 8
XL_HWTYPE_NONE = 0
XL_HWTYPE_VIRTUAL = 1
XL_HWTYPE_CANCARDXL = 15
XL_HWTYPE_CANCASEXL = 21

XL_BUS_TYPE_NONE = 0
XL_BUS_TYPE_CAN = 1

XL_INTERFACE_VERSION = 3

XL_INVALID_PORTHANDLE = -1

XL_ACTIVATE_NONE = 0
XL_ACTIVATE_RESET_CLOCK = 8

XLeventtag = ctypes.c_ubyte
MAX_MSG_LEN = 8

XL_NO_COMMAND = 0
XL_RECEIVE_MSG = 1
XL_CHIP_STATE = 4
XL_TRANSCEIVER = 6
XL_TIMER = 8
XL_TRANSMIT_MSG = 10
XL_SYNC_PULSE = 11
XL_APPLICATION_NOTIFICATION = 15

# //for LIN we have special events
XL_LIN_MSG = 20
XL_LIN_ERRMSG = 21
XL_LIN_SYNCERR = 22
XL_LIN_NOANS = 23
XL_LIN_WAKEUP = 24
XL_LIN_SLEEP = 25
XL_LIN_CRCINFO = 26

# // for D/A IO bus
XL_RECEIVE_DAIO_DATA = 32


class s_xl_can_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong),
                ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort),
                ("res1", XLuint64),
                ("data", ctypes.c_ubyte * MAX_MSG_LEN)]


class s_xl_chip_state(ctypes.Structure):
    _fields_ = [("busStatus", ctypes.c_ubyte),
                ("txErrorCounter", ctypes.c_ubyte),
                ("rxErrorCounter", ctypes.c_ubyte),
                ("chipStatte", ctypes.c_ubyte),
                ("flags", ctypes.c_uint)]


class s_xl_lin_crc_info(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("flags", ctypes.c_ubyte)]


class s_xl_lin_wake_up(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]


class s_xl_lin_no_ans(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte)]  #


class s_xl_lin_sleep(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]


class s_xl_lin_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("dlc", ctypes.c_ubyte),
                ("flags", ctypes.c_ushort),
                ("data", ctypes.c_ubyte * 8),
                ("crc", ctypes.c_ubyte)]


class s_xl_lin_msg_api(ctypes.Union):
    _fields_ = [("s_xl_lin_msg", s_xl_lin_msg),
                ("s_xl_lin_no_ans", s_xl_lin_no_ans),
                ("s_xl_lin_wake_up", s_xl_lin_wake_up),
                ("s_xl_lin_sleep", s_xl_lin_sleep),
                ("s_xl_lin_crc_info", s_xl_lin_crc_info)]


class s_xl_sync_pulse(ctypes.Structure):
    _fields_ = [("pulseCode", ctypes.c_ubyte),
                ("time", XLuint64)]


class s_xl_daio_data(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_ubyte),
                ("timestamp_correction", ctypes.c_uint),
                ("mask_digital", ctypes.c_ubyte),
                ("value_digital", ctypes.c_ubyte),
                ("mask_analog", ctypes.c_ubyte),
                ("reserved", ctypes.c_ubyte),
                ("value_analog", ctypes.c_ubyte * 4),
                ("pwm_frequency", ctypes.c_uint),
                ("pwm_value", ctypes.c_ubyte),
                ("reserved1", ctypes.c_uint),
                ("reserved2", ctypes.c_uint)]


class s_xl_transceiver(ctypes.Structure):
    _fields_ = [("event_reason", ctypes.c_ubyte),
                ("is_present", ctypes.c_ubyte)]


class s_xl_tag_data(ctypes.Union):
    _fields_ = [("msg", s_xl_can_msg),
                ("chipState", s_xl_chip_state),
                ("linMsgApi", s_xl_lin_msg_api),
                ("syncPulse", s_xl_sync_pulse),
                ("daioData", s_xl_daio_data),
                ("transceiver", s_xl_transceiver)]


class s_xl_event(ctypes.Structure):
    _fields_ = [("tag", XLeventtag),
                ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort),
                ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort),
                ("timeStamp", XLuint64),
                ("tagData", s_xl_tag_data)]


XLevent = s_xl_event

xl_response_codes ={
    '0': "XL_SUCCESS",
    '10': "XL_ERR_QUEUE_IS_EMPTY",
    '11': "XL_ERR_QUEUE_IS_FULL",
    '12': "XL_ERR_TX_NOT_POSSIBLE",
    '14': "XL_ERR_NO_LICENSE",
    '101': "XL_ERR_WRONG_PARAMETER",
    '111': "XL_ERR_INVALID_CHAN_INDEX",
    '112': "XL_ERR_INVALID_ACCESS",
    '113': "XL_ERR_PORT_IS_OFFLINE",
    '116': "XL_ERR_CHAN_IS_ONLINE",
    '117': "XL_ERR_NOT_IMPLEMENTED",
    '118': "XL_ERR_INVALID_PORT",
    '120': "XL_ERR_HW_NOT_READY",
    '121': "XL_ERR_CMD_TIMEOUT",
    '129': "XL_ERR_HW_NOT_PRESENT",
    '158': "XL_ERR_INIT_ACCESS_MISSING",
    '201': "XL_ERR_CANNOT_OPEN_DRIVER",
    '202': "XL_ERR_WRONG_BUS_TYPE",
    '203': "XL_ERR_DLL_NOT_FOUND",
    '204': "XL_ERR_INVALID_CHANNEL_MASK",
    '205': "XL_ERR_NOT_SUPPORTED",
    '255': "XL_ERROR"
}

class candriver(object):
    def __init__(self):
        self.candll = ctypes.windll.LoadLibrary("vxlapi64.dll")

    def open_driver(self):
        ok = self.candll.xlOpenDriver()
        return ok

    def get_appl_config(self, appname="xlCANcontrol", channel=0, bustype=XL_BUS_TYPE_CAN):
        app_name = ctypes.c_char_p(appname.encode())
        app_channel = ctypes.c_uint(channel)
        p_hw_type = ctypes.pointer(ctypes.c_uint())
        p_hw_index = ctypes.pointer(ctypes.c_uint())
        p_hw_channel = ctypes.pointer(ctypes.c_uint())
        bus_type = ctypes.c_uint(bustype)
        ok = self.candll.xlGetApplConfig(app_name, app_channel, p_hw_type, p_hw_index, p_hw_channel, bus_type)
        return ok, p_hw_type.contents, p_hw_index.contents, p_hw_channel.contents

    def set_appl_config(self, appname, appchannel, hwtype, hwindex, hwchannel, bustype):
        self.candll.xlSetApplConfig.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint,
                                                ctypes.c_uint, ctypes.c_uint]
        ok = self.candll.xlSetApplConfig(appname, appchannel, hwtype, hwindex, hwchannel, bustype)
        return ok

    def get_channel_index(self, hw_type=XL_HWTYPE_CANCARDXL, hw_index=0, hw_channel=0):
        self.candll.xlGetChannelIndex.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        channel_index = self.candll.xlGetChannelIndex(hw_type, hw_index, hw_channel)
        return channel_index

    def get_channel_mask(self,
                         hwtype=XL_HWTYPE_CANCARDXL,
                         hwindex=0,
                         hwchannel=0):
        self.candll.xlGetChannelMask.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        mask = self.candll.xlGetChannelMask(hwtype, hwindex, hwchannel)
        return ctypes.c_ulonglong(mask)

    def open_port(self,
                  port_handle=XLporthandle(XL_INVALID_PORTHANDLE),
                  user_name="xlCANcontrol",
                  access_mask=XLaccess(1),
                  permission_mask=XLaccess(1),
                  rx_queue_size=256,
                  interface_version=XL_INTERFACE_VERSION,
                  bus_type=XL_BUS_TYPE_CAN):
        self.candll.xlOpenPort.argtypes = [ctypes.POINTER(XLporthandle),
                                           ctypes.c_char_p,
                                           XLaccess,
                                           ctypes.POINTER(XLaccess),
                                           ctypes.c_uint,
                                           ctypes.c_uint,
                                           ctypes.c_uint]
        ok = self.candll.xlOpenPort(port_handle,
                                    user_name.encode(),
                                    access_mask,
                                    permission_mask,
                                    rx_queue_size,
                                    interface_version,
                                    bus_type)
        return ok, port_handle, permission_mask

    def activate_channel(self, port_handle,
                         access_mask=XLaccess(1),
                         bustype=XL_BUS_TYPE_CAN,
                         flags=XL_ACTIVATE_RESET_CLOCK):
        self.candll.xlActivateChannel.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        ok = self.candll.xlActivateChannel(port_handle, access_mask, bustype, flags)
        return ok

    def close_driver(self):
        ok = self.candll.xlCloseDriver()
        return ok

    def deactivate_channel(self, port_handle=XLporthandle(XL_INVALID_PORTHANDLE), access_mask=XLaccess(1)):
        self.candll.xlDeactivateChannel.argtypes = [XLporthandle, XLaccess]
        ok = self.candll.xlDeactivateChannel(port_handle, access_mask)
        return ok

    def close_port(self, port_handle=XLporthandle(XL_INVALID_PORTHANDLE)):
        self.candll.xlClosePort.argtypes = [XLporthandle]
        ok = self.candll.xlClosePort(port_handle)
        return ok

    def receive(self, port_handle, event_count, event_list):
        self.candll.xlReceive.argtypes = [XLporthandle, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(XLevent)]
        ok = self.candll.xlReceive(port_handle, ctypes.byref(event_count), ctypes.byref(event_list))
        return ok

    def get_event_string(self, ev):
        self.candll.xlGetEventString.argtypes = [ctypes.POINTER(XLevent)]
        self.candll.xlGetEventString.restype = ctypes.c_char_p
        rec_string = self.candll.xlGetEventString(ctypes.pointer(ev))
        return rec_string

    def can_set_channel_bitrate(self, port_handle, amask, bitrate):
        self.candll.xlCanSetChannelBitrate.argtypes = [XLporthandle, XLaccess, ctypes.c_ulong]
        ok = self.candll.xlCanSetChannelBitrate(port_handle, amask, ctypes.c_ulong(bitrate))
        return ok

    def can_transmit(self, port_handle, amask, message_count, p_messages):
        self.candll.xlCanTransmit.argtypes = [XLporthandle,
                                              XLaccess,
                                              POINTER(ctypes.c_uint),
                                              ctypes.c_void_p]
        ok = self.candll.xlCanTransmit(port_handle,
                                       amask,
                                       ctypes.byref(message_count),
                                       ctypes.byref(p_messages))
        return ok

    def get_error_string(self, err):
        self.candll.xlGetErrorString.argtypes = [XLstatus]
        self.candll.xlGetErrorString.restype = ctypes.c_char_p
        err_string = self.candll.xlGetErrorString(err)
        return str(err_string)


def get_device_id_by_type(device_type):
    return devices[device_type]


devices = {
    'NONE': 0,
    'VIRTUAL': 1,
    'CANCARDX': 2,
    'CANAC2PCI': 6,
    'CANCARDY': 12,
    'CANCARDXL': 15,
    'CANCASEXL': 21,
    'CANCASEXL_LOG_OBSOLETE': 23,
    'CANBOARDXL': 25,
    'CANBOARDXL_PXI': 27,
    'VN2600': 29,
    'VN2610': 29,
    'VN3300': 37,
    'VN3600': 39,
    'VN7600': 41,
    'CANCARDXLE': 43,
    'VN8900': 45,
    'VN8950': 47,
    'VN2640': 53,
    'VN1610': 55,
    'VN1630': 57,
    'VN1640': 59,
    'VN8970': 61,
    'VN1611': 63,
    'VN5610': 65,
    'VN7570': 67,
    'IPCLIENT': 69,
    'IPSERVER': 71,
    'VX1121': 73,
    'VX1131': 75,
    'VT6204': 77,
    'XL_MAX_HWTYPE': 81}

def get_device_id_by_type(device_type):
    return devices[device_type]