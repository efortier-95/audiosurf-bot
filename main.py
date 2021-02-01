from capture import Capture
from bot import Bot


def main():
    cap = Capture('Audiosurf 2')
    bot = Bot()

    print('Bot Initialized')
    while True:
        screenshot = cap.get_screenshot()
        bot.dodge_spike(screenshot)
        bot.hit_block(screenshot)


if __name__ == "__main__":
    main()
