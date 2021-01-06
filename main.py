import cv2 as cv
from time import time
from capture import WindowCapture
from vision import Vision

# Template matching methods
methods = {
    # Global max
    'CCOEFF': cv.TM_CCOEFF,
    'CCOEFF_NORMED': cv.TM_CCOEFF_NORMED,
    'CCORR': cv.TM_CCORR,
    'CCORR_NORMED': cv.TM_CCORR_NORMED,
    # Global min
    'SQDIFF': cv.TM_SQDIFF,
    'SQDIFF_NORMED': cv.TM_SQDIFF_NORMED
}


# Write data to image
def write_data(img, frames, detected):
    font = cv.FONT_HERSHEY_SIMPLEX

    # Bottom left corner of text
    threshold_location = (5, 15)
    blocks_location = (5, 35)
    frames_location = (425, 15)

    font_scale = 1 / 2

    # Colors for text
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (0, 0, 255)

    line_type = 2

    cv.putText(img, '60% Threshold', threshold_location, font, font_scale, white, line_type)
    cv.putText(img, f'Detected: {detected}', blocks_location, font, font_scale, green, line_type)
    cv.putText(img, f'FPS: {frames}', frames_location, font, font_scale, red, line_type)


# Initialization of classes
wincap = WindowCapture('Audiosurf 2')

#
vision = Vision(r'images\block_center.png', methods['CCOEFF_NORMED'])

print('Start\n')

blocks = 0
loop_time = time()
while True:

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Measure FPS and write on screen
    fps = str(int(1 / (time() - loop_time)))
    loop_time = time()
    write_data(screenshot, fps, blocks)

    # Display processed image
    points = vision.find(screenshot, 0.6, 'rectangles')

    # Add blocks to total
    if points:
        blocks += 1

    # Press 'q' with the output window focused to exit
    # Wait 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')
