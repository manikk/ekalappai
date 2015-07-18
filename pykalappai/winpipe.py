# -*- coding: utf-8 -*-
__author__ = 'manikk'
#shamelessly copied from url http://www.cs.unc.edu/~gb/blog/2007/11/16/sending-key-events-to-pygame-programs/

from ctypes import *

PUL = POINTER(c_ulong)
class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time",c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]

KEYEVENTF_KEYUP = 0x2
KEYEVENTF_UNICODE = 0x4
KEYEVENTF_SCANCODE = 0x8
MAPVK_VK_TO_VSC = 0

def SendKeyPress(key):    
    i = Input()
    i.type = 1
    extra = c_ulong(0)
    pextra = pointer(extra)
    #vk = windll.user32.VkKeyScanW(ord(key))    
    #sc = windll.user32.MapVirtualKeyW(vk&0xff, MAPVK_VK_TO_VSC)    
    i.ii.ki.wVk = 0
    #i.ii.ki.wScan = sc
    i.ii.ki.wScan = ord(key)
    #i.ii.ki.dwFlags = KEYEVENTF_SCANCODE
    i.ii.ki.dwFlags = KEYEVENTF_UNICODE
    i.ii.ki.time = 0
    i.ii.ki.dwExtraInfo = pextra
    windll.user32.SendInput(1, byref(i), sizeof(i))

def SendKeyRelease(key):
    i = Input()
    i.type = 1
    extra = c_ulong(0)
    pextra = pointer(extra)
    vk = windll.user32.VkKeyScanW(ord(key))
    sc = windll.user32.MapVirtualKeyW(vk&0xff, MAPVK_VK_TO_VSC)
    i.ii.ki.wVk = 0
    i.ii.ki.wScan = sc
    i.ii.ki.time = 0
    i.ii.ki.dwExtraInfo = pextra
    i.ii.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    windll.user32.SendInput(1, byref(i), sizeof(i))

def PressKey(hexKeyCode):
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, pointer(extra) )
    x = Input( c_ulong(1), ii_ )
    windll.user32.SendInput(1, pointer(x), sizeof(x))

def SendBackSpace():
    PressKey(0x08)