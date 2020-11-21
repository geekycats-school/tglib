from telegram import Telegram
import logging
import config
import tasks
import json
import os.path
from typing import Any, List, Callable


class Bot:
    def __init__(self, data_file):
        self._data_file = data_file
        if os.path.isfile(self._data_file):
            with open(self._data_file, "r") as savefile:
                self._stored_chats = json.load(savefile) or dict()
        else:
            self._stored_chats = dict()
        logging.info("Initialized")

    def save(self):
        with open(self._data_file, "w") as savefile:
            json.dump(self._stored_chats, savefile)
        logging.info("Saved")

    def handler(self, сhat_id_, text):
        self._chat_id = str(сhat_id_)
        if text.lstrip().startswith("/"):
            if text == "/new_task":
                task, answer = tasks.get_task()
                self._stored_chats[self._chat_id] = answer
                return task
        elif self._chat_id in self._stored_chats:
            if text == self._stored_chats[self._chat_id]:
                del self._stored_chats[self._chat_id]
                return config.TEXT_CORRECT_ANSWER
            else:
                return config.TEXT_INCORRECT_ANSWER
        return config.TEXT_NO_HANDLER


def main():
    cmd = {
        "commands": [{"command": "new_task", "description": "Generates a new task."}]
    }
    telegram = Telegram(config.TOKEN, cmd)
    bot = Bot(config.DATA_FILE)
    while True:
        try:
            chat_id, message = telegram.get_message()
            output = bot.handler(chat_id, message)
            telegram.send_message(chat_id, output)
        except TimeoutError:
            continue
        except telegram.TelegramError as e:
            logging.error(f"Exception occured\n{e}")
            continue
        except KeyboardInterrupt:
            bot.save()
            exit()


if __name__ == "__main__":
    main()
