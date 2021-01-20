import cv2 as cv
from capture import WindowCapture
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

# Load trained cascade_block model
detect_block = cv.CascadeClassifier(r'cascade_block\cascade.xml')
# detect_spike = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

print('Start\n')

img_count = 0
loop_time = time()
while True:

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Image detection
    block = detect_block.detectMultiScale(screenshot)
    # spike = detect_spike.detectMultiScale(screenshot)

    # Draw detected results on image
    # draw_block = vision.draw_rectangles(screenshot, block, (0, 255, 0), 'Block')
    # draw_spike = vision.draw_rectangles(screenshot, spike, (0, 0, 255), 'Spike')

    if len(block) > 0:

        targets = vision.get_click_points(block)
        target = wincap.get_screen_position(targets[0])

        x = target[0]
        y = target[1]

        crosshair = vision.draw_crosshairs(screenshot, targets, (0, 255, 0), f'({x}, {y})')

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
