import telegram
import logging
import config
import tasks
import json
from typing import Any, List, Callable

_stored_chats = dict()  # chat_id answer
commands = [{"command": "new_task", "description": "Generates a new task."}]


def init():
    telegram.set_commands(commands)

    
def save():
    savefile = open("stored_chats.json", "w")
    json.dump(_stored_chats, savefile)
    savefile.close()
    logging.info("Saved")
    exit()

    
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

if __name__ == "__main__":
    main() 