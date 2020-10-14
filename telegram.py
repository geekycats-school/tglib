import requests
import json
import tasks
from typing import List, Callable, Tuple

TOKEN = "1360917608:AAGB4YtRDmIi7ywCMFb6IILGswf0wHCx-r0"
URL = "https://api.telegram.org/bot{token}/{method}"
_stored_chats = dict() #chat_id function


class TelegramError(Exception):
    pass


def get_command_parser(chat_id: int, command_name: str, *args: List[str]) -> Callable[[], str]:
    # /command arg1 arg2  
    if command_name == "new_task":
        task, answer = tasks.get_task()
        _stored_chats[chat_id] = lambda s: "Right!" if s.strip() == answer else "That isn't a right answer."
        return lambda *args: task 

def get_message_parser(chat_id: int,  text: str) -> Callable[[],str]:
    if text.lstrip().startswith("/"):
        get_command_parser(chat_id, *text.split())
    elif chat_id in _stored_chats:
        return _stored_chats['chat_id']
    else:
        return lambda s: "No handler for your request"  
      

def get_message(offset: List[int] = [], limit: int = 1) -> Tuple[int, str]:
    # -> chat_id, text
    params = {
        "offset" : offset[0] if len(offset) == 1 else 0,
        "timeout" : 60
    }
    resp = requests.get(URL.format(token=TOKEN, method="getUpdates"), params=params, timeout=60)
    if resp.ok and resp.json()['ok'] == True and len(resp.json()['result']) == 1:
        result = resp.json()['result'][0]
        offset[0] = result['update_id'] + 1
        message = result['message']
        return message['chat']['id'], message['text']
    else:
        raise TelegramError(resp.text)


def send_message(chat_id: int, text: str):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(URL.format(token=TOKEN, method="sendMessage"), data=data)



