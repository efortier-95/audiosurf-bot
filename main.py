import win32api
import win32con
import cv2 as cv
from time import time, sleep
from capture import WindowCapture
from math import sqrt
from vision import Vision


# Hex codes for key a and d
a = 0x41
d = 0x44


def press(key):
    win32api.keybd_event(key, 0, 0, 0)
    sleep(.15)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def hold(key):
    win32api.keybd_event(key, 0, 0, 0)
    sleep(0.05)


def release(key):
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def ordered_targets(objects):

    pos_x, pos_y = win32api.GetCursorPos()

    def distance(pos):
        dist = sqrt((pos[0] - pos_x)**2 + (pos[1] - pos_y)**2)
        return dist

    objects.sort(key=distance)

    return objects


# Write to capture screen
def write_data(img, frames):

    # Bottom left corner of text
    fps_loc = (525, 15)

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    white = (255, 255, 255)
    line_type = 2

    cv.putText(img, f'FPS: {frames}', fps_loc, font, font_scale, white, line_type)


# Initialization of classes
wincap = WindowCapture('Audiosurf 2')
vision = Vision()

# Load trained cascade_block model
detect_block = cv.CascadeClassifier(r'cascade_block\cascade.xml')
# detect_spike = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

print('Start\n')

loop_time = time()
while True:

    targets = None

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Image detection
    block = detect_block.detectMultiScale(screenshot)
    # spike = detect_spike.detectMultiScale(screenshot)

    # Draw detected results on image
    # draw_block = vision.draw_rectangles(screenshot, block, (0, 255, 0), 'Block')
    # draw_spike = vision.draw_rectangles(screenshot, spike, (0, 0, 255), 'Spike')

    if len(block) > 0:

        positions = []

        # Get center coordinates of detected objects and convert to screen positions
        targets = vision.get_click_points(block)
        for target in targets:
            position = wincap.get_screen_position(target)
            positions.append(position)

        # Sort object from ships by distance
        positions = ordered_targets(positions)

        # Coordinates of closest object
        closest = positions[0]
        tar_x = closest[0]
        tar_y = closest[1]

        # Coordinates of ship
        cur_x, cur_y = win32api.GetCursorPos()

        # Distance x and y from ship to nearest object
        dx = tar_x - cur_x
        dy = abs(tar_y - cur_y)

        draw_block = vision.draw_crosshairs(screenshot, targets, (0, 255, 0), f'({dx}, {dy})')

        if dy < 50:
            if -5 <= dx <= 5:
                release(a)
                release(d)
            if dx < -5:
                press(a)
            if dx > 5:
                press(d)

    # Measure FPS
    fps = int(1 / (time() - loop_time))
    loop_time = time()

    # Write data on screen
    write_data(screenshot, fps)

    # Display image
    cv.imshow('Audiosurf 2 Image Detection', screenshot)

    # Press 'q' on capture screen to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('\nDone')
