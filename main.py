from capture import Capture
from bot import Bot


def main():
    cap = Capture('Audiosurf 2')
    bot = Bot()

    print('Bot Initialized')
    while True:
        screenshot = cap.get_screenshot()
        bot.hit_block(screenshot)
        bot.dodge_spike(screenshot)


if __name__ == "__main__":
    main()
    print('\nBot Terminated')
