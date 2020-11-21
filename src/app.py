from telegram import Telegram
from bot import Bot
from typing import Any, List, Callable
import logging
import config


def main():
    cmd = {
        "commands": [{"command": "new_task", "description": "Generates a new task."}]
    }
    telegram = Telegram(config.TOKEN, cmd)
    bot = Bot(config.DATA_FILE)
    while True:
        try:
            chat_id, message = telegram.get_message()
            output = bot.handle(chat_id, message)
            telegram.send_message(chat_id, output)
        except TimeoutError:
            continue
        except telegram.TelegramError as e:
            logging.error(f"Exception occured\n{e}")
            continue
        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    main()
