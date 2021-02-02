import win32ui
import win32gui
import win32con
import numpy as np


class Capture:

    def __init__(self, window_name=None):

        if window_name is None:
            # Capture whole window if Audiosurf 2 not found
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window not found: {window_name}')

        # Capture region
        self.w = 600
        self.h = 500

        # Offset pixels from (0, 0)
        self.offset_x = 650
        self.offset_y = 200

    def get_screenshot(self):
        """Capture game screenshot"""

        # Get window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # Set screen offset arguments
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.offset_x, self.offset_y), win32con.SRCCOPY)

        # Save screeshot to bitmap format
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Remove alpha channel to use img with opencv
        img = img[..., :3]

        # Make image contiguous
        img = np.ascontiguousarray(img)
        return img
