import cv2 as cv
from time import time
from capture import WindowCapture
from vision import Vision
from hsv import HSVFilter

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

# HSV filtered block
# hsv_filter = HSVFilter()


# Write data to image
def write_data(img, frames, detected):
    font = cv.FONT_HERSHEY_SIMPLEX

    # Bottom left corner of text
    blocks_location = (5, 15)
    frames_location = (425, 15)

    font_scale = 1 / 2

    # Colors for text
    white = (255, 255, 255)
    green = (0, 255, 0)

    line_type = 2

    cv.putText(img, f'Detected: {detected}', blocks_location, font, font_scale, green, line_type)
    cv.putText(img, f'FPS: {frames}', frames_location, font, font_scale, white, line_type)


# Initialization of classes
wincap = WindowCapture('Audiosurf 2')
vision = Vision(r'images\block_center.png', methods['CCOEFF_NORMED'])

# Create trackbar window
vision.init_control_gui()

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

    # Preprocess image to highlight object
    # processed_img = vision.apply_hsv_filter(screenshot, hsv_filter)

    # Image detection
    rectangles = vision.find(screenshot, 0.6)

    # Draw detection results to image
    output = vision.draw_rectangles(screenshot, rectangles)

    # Display processed image
    cv.imshow('Audiosurf 2 Image Detection', output)

    # Add blocks to total
    if len(rectangles) > 0:
        blocks += 1

    # Press 'q' with the output window focused to exit
    # Wait 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')
