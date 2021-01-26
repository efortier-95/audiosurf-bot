import cv2 as cv
from capture import WindowCapture
from keyboard import Keyboard
from math import hypot
from time import time
from vision import Vision


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
kb = Keyboard()

# Load trained cascade_block model
detect_block = cv.CascadeClassifier(r'cascade_block\cascade.xml')
# detect_spike = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

print('Start\n')

ship = (310, 375)
loop_time = time()
while True:

    targets = None

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Image detection
    detected_block = detect_block.detectMultiScale(screenshot)
    # detected_spike = detect_spike.detectMultiScale(screenshot)

    if len(detected_block) > 0:

        # Get center coordinates of detected objects and convert to screen positions
        blocks = vision.get_click_points(detected_block)

        for block in blocks:

            cv.line(screenshot, ship, block, (0, 255, 0), 2)

            tar_x, tar_y = block
            cur_x, cur_y = ship

            # Distance from object to ship
            dx = tar_x - cur_x
            dy = abs(tar_y - cur_y)

            draw_block = vision.draw_crosshairs(screenshot, blocks, (0, 255, 0))

            if 0 <= dy <= 50:
                if -10 <= dx <= 10:
                    kb.center()
                if dx < -10:
                    kb.left()
                if dx > 10:
                    kb.right()

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
