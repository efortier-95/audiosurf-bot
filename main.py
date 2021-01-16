import cv2 as cv
from time import time, sleep
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
block = cv.CascadeClassifier(r'cascade_block\cascade.xml')
# spike = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

print('Start\n')

img_count = 0
loop_time = time()
while True:

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Image detection
    detect_block = block.detectMultiScale(screenshot)
    # detect_spike = spike.detectMultiScale(screenshot)

    # Draw detected results on image
    draw_block = vision.draw_rectangles(screenshot, detect_block, (0, 255, 0), 'Block')
    # draw_spike = vision.draw_rectangles(screenshot, detect_spike, (0, 0, 255))

    # Measure FPS
    fps = int(1 / (time() - loop_time))
    loop_time = time()

    # Write data on screen
    write_data(screenshot, fps)

    # Display image
    cv.imshow('Audiosurf 2 Image Detection', screenshot)

    # Take screenshots
    # cv.imwrite(fr'raw_images\right\right_{img_count}.jpg', screenshot)
    # sleep(0.2)
    # img_count += 1

    # Press 'q' with the output window focused to exit
    # Wait 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break

print('\nDone')
