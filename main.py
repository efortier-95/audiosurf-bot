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

# Initialization of classes
wincap = WindowCapture('Audiosurf 2')
vision = Vision()

# Load trained cascade model
cascade = cv.CascadeClassifier(r'cascade\cascade.xml')

print('Start\n')

img_count = 0
loop_time = time()
while True:

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Image detection
    rectangles = cascade.detectMultiScale(screenshot)

    # Draw detected results on image
    detection = vision.draw_rectangles(screenshot, rectangles)

    # Display image
    cv.imshow('Audiosurf 2 Image Detection', screenshot)

    # Measure FPS
    fps = int(1 / (time() - loop_time))
    loop_time = time()
    print(f'FPS: {fps}')

    # Take screenshots
    # cv.imwrite(fr'screenshots\{img_count}.jpg', screenshot)
    # sleep(0.5)
    # img_count += 1

    # Press 'q' with the output window focused to exit
    # Wait 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break

print('\nDone')
