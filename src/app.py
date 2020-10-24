import telegram
import logging
import tasks
from typing import Any, List, Callable

commands = [{"command": "new_task", "description": "Generates a new task."}]
_stored_chats = dict()  # chat_id answer


def init():
    telegram.set_commands(commands)


def handler(chat_id, text):
    if text.lstrip().startswith("/"):
        if text == "/new_task":
            task, answer = tasks.get_task()
            _stored_chats[chat_id] = answer
            return task
        else:
            return "No handler for your request."
    elif chat_id in _stored_chats:
        return check_answer(chat_id, text)
    else:
        return "no handler for your request"


def check_answer(chat_id: int, text: str) -> str:
    if _stored_chats[chat_id] == text:
        del _stored_chats[chat_id]
        return "Correct"
    else:
        return "Wrong"


def get_command_parser(
    chat_id: int, command_name: str, *args: List[str]
) -> Callable[[Any], str]:
    if command_name == "/new_task":
        task, answer = tasks.get_task()
        _stored_chats[chat_id] = answer
        return lambda s: task
    else:
        raise telegram.TelegramError


def get_message_parser(chat_id: int, text: str) -> Callable[[str], str]:
    if text.lstrip().startswith("/"):
        return get_command_parser(chat_id, *text.split())
    elif chat_id in _stored_chats:
        return check_answer(chat_id, text)
    else:
        return lambda s: "No handler for your request"


def main():
    init()
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


if __name__ == "__main__":
    main()
