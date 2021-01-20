import cv2 as cv
import numpy as np


class Vision:

    # Convert [x, y, w, h] to [x, y] center positions
    @staticmethod
    def get_click_points(rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points

    # Return image with rectangles drawn from [x, y, w, h]
    @staticmethod
    def draw_rectangles(haystack_img, rectangles, color, name):

        for (x, y, w, h) in rectangles:

            # Rectangle positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            # Draw rectangle and with name overlay
            cv.rectangle(haystack_img, top_left, bottom_right, color, 2)
            cv.putText(haystack_img, name, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return haystack_img

    # Return image with click points drawn as crosshairs
    @staticmethod
    def draw_crosshairs(haystack_img, points, color, name):

        marker_type = cv.MARKER_TILTED_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), color, marker_type, 10, 2)
            cv.putText(haystack_img, name, (center_x - 35, center_y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return haystack_img

    # Find average of all matched keypoints on image
    @staticmethod
    def centroid(point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]
