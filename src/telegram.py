import requests
from typing import Tuple
import os

TOKEN = os.environ["BOT_TOKEN"]
URL = "https://api.telegram.org/bot{token}/{method}"
_offset = 0


class TelegramError(Exception):
    pass


def get_message(offset: int = None, limit: int = 1) -> Tuple[int, str]:
    # -> chat_id, text
    global _offset
    if offset is None:
        offset = _offset
    params = {"offset": offset, "timeout": 60, "limit": limit}
    resp = requests.get(
        URL.format(token=TOKEN, method="getUpdates"), params=params, timeout=60
    )
    if resp.ok and resp.json()["ok"] == True and len(resp.json()["result"]) == 1:
        result = resp.json()["result"][0]
        _offset = result["update_id"] + 1
        if "message" in result:
            message = result["message"]
        else:
            raise TelegramError(resp.text)
        return message["chat"]["id"], message["text"]
    else:
        raise TelegramError(resp.text)


def send_message(chat_id: int, text: str):
    data = {"chat_id": chat_id, "text": text}
    requests.post(URL.format(token=TOKEN, method="sendMessage"), data=data)
