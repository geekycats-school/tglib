import telegram
import logging
import tasks
from typing import Any, List, Callable

_stored_chats = dict()  # chat_id function


def check_answer(chat_id: int, text: str) -> Callable[[], str]:
    _, answer = tasks.get_task()
    if text == answer:
        return _stored_chats.pop(chat_id)
    else:
        return _stored_chats[chat_id]


def get_command_parser(chat_id: int, command_name: str, *args: List[str]) -> Callable[[Any], str]:
    # /command arg1 arg2  
    if command_name == "/new_task":
        task, answer = tasks.get_task()
        _stored_chats[chat_id] = lambda s: "correct" if s.strip() == answer else "WRONG"
        return lambda *args: task
    else:
        raise telegram.TelegramError


def get_message_parser(chat_id: int, text: str) -> Callable[[], str]:
    if text.lstrip().startswith("/"):
        return get_command_parser(chat_id, *text.split())
    elif chat_id in _stored_chats:
        return check_answer(chat_id, text)
        # return _stored_chats.pop(chat_id)
    else:
        return lambda s: "No handler for your request"


def main():
    while True:
        try:
            chat_id, message = telegram.get_message()
            parser = get_message_parser(chat_id, message)
            telegram.send_message(chat_id, parser(message))
        except TimeoutError:
            continue
        except telegram.TelegramError as e:
            logging.error(f"Exception occured\n{e}")
            continue


if __name__ == "__main__":
    main()