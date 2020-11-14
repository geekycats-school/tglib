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





def check_answer(chat_id: int, text: str) -> str:
    if _stored_chats[chat_id] == text:
        del _stored_chats[chat_id]
        return config.TEXT_CORRECT_ANSWER
    else:
        return config.TEXT_INCORRECT_ANSWER


def handler(chat_id, text):
    if text.lstrip().startswith("/"):
        if text == "/new_task":
            task, answer = tasks.get_task()
            _stored_chats[chat_id] = answer
            return task
    elif chat_id in _stored_chats:
        return check_answer(chat_id, text)
    return config.TEXT_NO_HANDLER


def main():
    init()
    cmd = {"commands": [{"command": "new_task", "description": "Generates a new task."}]}
    telegram = Telegram(config.TOKEN, cmd)
    while True:
        try:
            chat_id, message = telegram.get_message()
            output = handler(chat_id, message)
            telegram.send_message(chat_id, output)
        except TimeoutError:
            continue
        except telegram.TelegramError as e:
            logging.error(f"Exception occured\n{e}")
            continue
        except KeyboardInterrupt:
            save()
            exit()


if __name__ == "__main__":
    main()
