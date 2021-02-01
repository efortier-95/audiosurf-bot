import win32api
import win32con


class Keyboard:

    def __init__(self):
        self.a = 0x41
        self.d = 0x44

    def hold_left(self):
        win32api.keybd_event(self.a, 0, 0, 0)

    def hold_right(self):
        win32api.keybd_event(self.d, 0, 0, 0)

    def center(self):
        win32api.keybd_event(self.a, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(self.d, 0, win32con.KEYEVENTF_KEYUP, 0)
