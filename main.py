import cv2 as cv
from time import time
from window_capture import WindowCapture
from vision import Vision

# List window names and exit before capture
# WindowCapture.list_window_names()
# exit()

# Initialization of classes
wincap = WindowCapture()
# wincap = WindowCapture('Audiosurf 2')
vision = Vision(r'images\block_center.png')

print('Start\n')

loop_time = time()
while True:

    # Capture screenshot from window
    screenshot = wincap.get_screenshot()

    # Display processed image
    points = vision.find(screenshot, 0.6, 'points')

    # Measure fps
    passed_time = time() - loop_time
    fps = 1 / passed_time
    print(f'FPS: {fps:.2f}\n')
    loop_time = time()

    # Press 'q' with the output window focused to exit
    # Wait 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')
