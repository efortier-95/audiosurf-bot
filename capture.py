import win32ui
import win32gui
import win32con
import numpy as np


class WindowCapture:

    # Properties
    w = 0
    h = 0
    offset_x = 600
    offset_y = 200
    hwnd = None

    # Constructor
    def __init__(self, window_name=None):

        if window_name is None:
            # Capture whole window if Audiosurf 2 not found
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            # Found Audiosurf 2 window
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window not found: {window_name}')

        # Screen dimensions
        self.w = 500
        self.h = 600

        # Offset pixels
        # x = 700, y = 150 for center region
        self.offset_x = 700
        self.offset_y = 150

    # Capture window screenshot
    def get_screenshot(self):

        # Get window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        # Set 4th argument for screen offset
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.offset_x, self.offset_y), win32con.SRCCOPY)

        # Save screeshot to bitmap file
        # dataBitMap.SaveBitmapFile(cDC, r'captures\debug.bmp')
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

    # Find names of all active windows
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(winEnumHandler, None)

    # Translate pixel position on screenshot to window position
    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y
