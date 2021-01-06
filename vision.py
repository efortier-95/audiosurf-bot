import cv2 as cv
import numpy as np
from hsv import HSVFilter

'''
OpenCV Doc:
- Object Detection: https://docs.opencv.org/4.5.1/df/dfb/group__imgproc__object.html
- Flags: https://docs.opencv.org/3.4/d8/d6a/group__imgcodecs__flags.html
- Template Matching Example: https://docs.opencv.org/4.5.1/d4/dc6/tutorial_py_template_matching.html
'''


class Vision:

    # Constants
    TRACKBAR_WINDOW = 'Trackbars'

    # Properties
    needle_img = None
    needle_w = 0
    needdle_h = 0
    method = None

    # Constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # Load image to match
        # Flag -1 for original
        # Flag 17 for 1/2 size color
        # Flag 33 for 1/4 size color
        self.needle_img = cv.imread(needle_img_path, 17)

        # Needle image dimensions
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # Compare template against image
        self.method = method

        # Total block detected
        self.blocks = 0

    def find(self, haystack_img, threshold=0.5, max_results=10):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Searching for all locations of object
        # Global max >= threshold
        # Global min <= threshold
        locations = np.where(result >= threshold)

        # Convert locations to (x, y) tuples
        locations = list(zip(*locations[::-1]))

        # Return reshaped array if no result found
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # List of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [
                int(loc[0]),
                int(loc[1]),
                self.needle_w,
                self.needle_h
            ]
            rectangles.append(rect)
            rectangles.append(rect)

        # Group overlapping rectangles
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        # Cap number of results to improve performance
        if len(rectangles) > max_results:
            print('Warning: Too many results. Raise max result limit')
            rectangles = rectangles[:max_results]

        return rectangles

    @staticmethod
    def get_click_points(rectangles):

        # Draw rectangles around all matched locations
        points = []

        # Loop over locations and draw rectangles
        for (x, y, w, h) in rectangles:

            # Marker center position
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)

            # Save the points
            points.append((center_x, center_y))

        return points

    # Draw rectangles on image from list of [x, y, w, h] positions
    @staticmethod
    def draw_rectangles(haystack_img, rectangles):

        # BGR colors
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:

            # Determine box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            # Draw rectangle
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

        return haystack_img

    # Draw crosshairs on image from list of [x, y] positions
    @staticmethod
    def draw_crosshairs(haystack_img, points):

        # Marker parameters
        marker_color = (0, 255, 0)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    # Create GUI window for adjusting HSV
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # Required callback for createTrackbar
        def nothing(position):
            pass

        # Trackbars for bracketing
        # HSV scale - H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)

        # Default value for max HSV
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # Controls for saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    # Return HSV filter based on GUI controls
    def get_hsv_filter_from_controls(self):

        # Get current positions of all trackbars
        hsv_filter = HSVFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)

        return hsv_filter

    # Apply HSV filter
    def apply_hsv_filter(self, original_img, hsv_filter=None):

        # Convert image to HSV
        hsv = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)

        # If no filter given, use filter values from GUI controls
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # Adjust saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

        # Apply thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # Convert back to BGR for display
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    # Apply adjustments to HSV channel
    @staticmethod
    def shift_channel(c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
