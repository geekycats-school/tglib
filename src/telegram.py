import requests
from typing import Tuple

class Telegram:
    
    _URL = "https://api.telegram.org/bot{token}/{method}"

    class TelegramError(Exception):
        pass

    class Message:
        def __init__(self, message: dict):
            pass

    
    def __init__(self, token: str, commands: dict, offset=0, limit=1):
        self._token = token
        self._offset = offset
        self._limit = limit
        resp = requests.post(
            self._URL.format(token=self._token, method="setMyCommands"), json=commands
        )
        if not resp.ok:
            raise TelegramError("Can't bind commands")
        

    def get_message(self) -> Message:
        # -> chat_id, text
        params = {"offset": self._offset, "timeout": 60, "limit": self._limit}
        while True:
            resp = requests.get(
                self._URL.format(token=self._token, method="getUpdates"),
                params=params,
                timeout=60,
            )
            if resp.ok and resp.json()["ok"] == True:
                if len(resp.json()["result"]) == 1:
                    result = resp.json()["result"][0]
                    self._offset = result["update_id"] + 1
                    if "message" in result:
                        message = result["message"]
                    else:
                        raise TelegramError(resp.text)
                    id = str(message["chat"]["id"])
                    try:
                        return id, message["text"]
                    except KeyError:
                        return id, "None"
                elif len(resp.json()["result"]) == 0:
                    continue
            else:
                raise TelegramError(resp.text)
            

    def send_message(self, chat_id: str, text: str):
        data = {"chat_id": chat_id, "text": text}
        requests.post(
            self._URL.format(token=self._token, method="sendMessage"), data=data
        )