import win32api
import win32con
from time import sleep


# Virtual keyboard implementation
class Keyboard:

    def __init__(self):
        # Hex codes for key a and d
        self.a = 0x41
        self.d = 0x44

    def left(self):
        win32api.keybd_event(self.a, 0, 0, 0)
        sleep(0.1)
        win32api.keybd_event(self.a, 0, win32con.KEYEVENTF_KEYUP, 0)

    def right(self):
        win32api.keybd_event(self.d, 0, 0, 0)
        sleep(0.1)
        win32api.keybd_event(self.d, 0, win32con.KEYEVENTF_KEYUP, 0)

    def hold_left(self):
        self.center()
        win32api.keybd_event(self.a, 0, 0, 0)
        sleep(0.05)

    def hold_right(self):
        self.center()
        win32api.keybd_event(self.d, 0, 0, 0)
        sleep(0.05)

    def center(self):
        win32api.keybd_event(self.a, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(self.d, 0, win32con.KEYEVENTF_KEYUP, 0)
