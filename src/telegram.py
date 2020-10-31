import requests
from typing import Tuple
import os
import config

_offset = 0


class TelegramError(Exception):
    pass


def set_commands(commands: list):
    requests.post(
        config.URL.format(token=config.TOKEN, method="setMyCommands"), data=commands
    )


def get_message(offset: int = None, limit: int = 1) -> Tuple[int, str]:
    # -> chat_id, text
    global _offset
    if offset is None:
        offset = _offset
    params = {"offset": offset, "timeout": 60, "limit": limit}
    while True:
        resp = requests.get(
            config.URL.format(token=config.TOKEN, method="getUpdates"),
            params=params,
            timeout=60,
        )
        if resp.ok and resp.json()["ok"] == True:
            if len(resp.json()["result"]) == 1:
                result = resp.json()["result"][0]
                _offset = result["update_id"] + 1
                if "message" in result:
                    message = result["message"]
                else:
                    raise TelegramError(resp.text)
                try:
                    return message["chat"]["id"], message["text"]
                except KeyError:
                    return message["chat"]["id"], "None"
            elif len(resp.json()["result"]) == 0:
                continue
        else:
            raise TelegramError(resp.text)
        


def send_message(chat_id: int, text: str):
    data = {"chat_id": chat_id, "text": text}
    requests.post(
        config.URL.format(token=config.TOKEN, method="sendMessage"), data=data
    )
