import cv2 as cv
from capture import Capture
from bot import Bot


def main(debug=False):
    cap = Capture('Audiosurf 2')
    bot = Bot()

    print('Bot Initialized')
    while True:
        screenshot = cap.get_screenshot()
        bot.hit_block(screenshot)
        bot.dodge_spike(screenshot)

        # Display detection window on debug mode
        if debug:
            cv.imshow('A2B', screenshot)

            k = cv.waitKey(1)
            if k == ord('q'):
                cv.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
