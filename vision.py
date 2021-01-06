import cv2 as cv
import numpy as np

'''
OpenCV Doc:
- Object Detection: https://docs.opencv.org/4.5.1/df/dfb/group__imgproc__object.html
- Flags: https://docs.opencv.org/3.4/d8/d6a/group__imgcodecs__flags.html
- Template Matching Example: https://docs.opencv.org/4.5.1/d4/dc6/tutorial_py_template_matching.html
'''


class Vision:

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

    def find(self, haystack_img, threshold=0.5, debug_mode=None):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Searching for all locations of object
        # Global max >= threshold
        # Global min <= threshold
        locations = np.where(result >= threshold)

        # Convert locations to (x, y) tuples
        locations = list(zip(*locations[::-1]))

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
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        # Draw rectangles around all matched locations
        points = []
        if len(rectangles):

            # Add block to total
            self.blocks += 1

            # Rectangle parameters
            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            # Marker parameters
            marker_color = (0, 255, 0)
            marker_type = cv.MARKER_CROSS

            # Loop over locations and draw rectangles
            for (x, y, w, h) in rectangles:

                # Marker center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)

                # Save the points
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Determine box positions
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)

                    # Draw rectangle
                    cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
                elif debug_mode == 'points':
                    cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        if debug_mode:
            cv.imshow('Audiosurf Image Detection', haystack_img)

        return points
