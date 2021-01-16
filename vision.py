import cv2 as cv
import numpy as np
from hsv import HSVFilter
from edge import EdgeFilter


class Vision:

    # Constants
    TRACKBAR_WINDOW = 'Trackbars'

    # Properties
    needle_img = None
    needle_w = 0
    needdle_h = 0
    method = None

    # Constructor
    def __init__(self, needle_img_path=None, method=cv.TM_CCOEFF_NORMED):
        if needle_img_path:
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

        # Total cascade_block detected
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

    # Match keypoints in needle image against the template
    def match_keypoints(self, original_img, patch_size=32):

        # Minimum number of detections for match
        min_match_count = 5

        # Number of features on needle and template raw_images
        orb = cv.ORB_create(edgeThreshold=0, patchSize=patch_size)
        keypoints_needle, descriptors_needle = orb.detectAndCompute(self.needle_img, None)
        orb2 = cv.ORB_create(edgeThreshold=0, patchSize=patch_size, nfeatures=2000)
        keypoints_haystack, descriptors_haystack = orb2.detectAndCompute(original_img, None)

        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                            table_number=6,
                            key_size=12,
                            multi_probe_level=1)

        search_params = dict(checks=50)

        try:
            flann = cv.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors_needle, descriptors_haystack, k=2)
        except cv.error:
            return None, None, [], [], None

        # Store all the good matches as per Lowe's ratio test.
        good = []
        points = []

        # Look at distance to determine match
        for pair in matches:
            if len(pair) == 2:
                if pair[0].distance < 0.7 * pair[1].distance:
                    good.append(pair[0])

        # If matches are more than threshold, return value
        if len(good) > min_match_count:
            print('match %03d, kp %03d' % (len(good), len(keypoints_needle)))
            for match in good:
                points.append(keypoints_haystack[match.trainIdx].pt)
            # print(points)

        return keypoints_needle, keypoints_haystack, good, points

    # Find average of all matched keypoints in template image
    @staticmethod
    def centroid(point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]

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
    def draw_rectangles(haystack_img, rectangles, color, text):

        font_scale = 0.5
        line_type = 2

        for (x, y, w, h) in rectangles:

            # Determine box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            # Draw rectangle
            cv.rectangle(haystack_img, top_left, bottom_right, color, line_type)

            # Text overlay
            cv.putText(haystack_img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, font_scale, color, line_type)

        return haystack_img

    # Draw crosshairs on image from list of [x, y] positions
    @staticmethod
    def draw_crosshairs(haystack_img, points, color):

        # Marker parameters
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), color, marker_type)

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

        # Trackbars for edge creation
        cv.createTrackbar('KernelSize', self.TRACKBAR_WINDOW, 1, 30, nothing)
        cv.createTrackbar('ErodeIter', self.TRACKBAR_WINDOW, 1, 5, nothing)
        cv.createTrackbar('DilateIter', self.TRACKBAR_WINDOW, 1, 5, nothing)
        cv.createTrackbar('Canny1', self.TRACKBAR_WINDOW, 0, 200, nothing)
        cv.createTrackbar('Canny2', self.TRACKBAR_WINDOW, 0, 500, nothing)

        # Default value for Canny edge
        cv.setTrackbarPos('KernelSize', self.TRACKBAR_WINDOW, 5)
        cv.setTrackbarPos('Canny1', self.TRACKBAR_WINDOW, 100)
        cv.setTrackbarPos('Canny2', self.TRACKBAR_WINDOW, 200)

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

    # Return Canny edge filter based on GUI controls
    def get_edge_filter_from_controls(self):

        # Get current positions of all trackbars
        edge_filter = EdgeFilter()
        edge_filter.kernelSize = cv.getTrackbarPos('KernelSize', self.TRACKBAR_WINDOW)
        edge_filter.erodeIter = cv.getTrackbarPos('ErodeIter', self.TRACKBAR_WINDOW)
        edge_filter.dilateIter = cv.getTrackbarPos('DilateIter', self.TRACKBAR_WINDOW)
        edge_filter.canny1 = cv.getTrackbarPos('Canny1', self.TRACKBAR_WINDOW)
        edge_filter.canny2 = cv.getTrackbarPos('Canny2', self.TRACKBAR_WINDOW)
        return edge_filter

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

    # Apply Canny edge filter
    def apply_edge_filter(self, original_img, edge_filter=None):

        # If no filter given, use filter values from GUI controls
        if not edge_filter:
            edge_filter = self.get_edge_filter_from_controls()

        kernel = np.ones((edge_filter.kernelSize, edge_filter.kernelSize), np.uint8)
        eroded_img = cv.erode(original_img, kernel, iterations=edge_filter.erodeIter)
        dilated_img = cv.dilate(eroded_img, kernel, iterations=edge_filter.dilateIter)

        # Canny edge detection
        result = cv.Canny(dilated_img, edge_filter.canny1, edge_filter.canny2)

        # Convert single channel image back to BGR
        img = cv.cvtColor(result, cv.COLOR_GRAY2BGR)

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
