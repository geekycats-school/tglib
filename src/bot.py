import json
import tasks
import os.path
import config
import logging

class Bot:
    def __init__(self, data_file):
        self._data_file = data_file
        if os.path.isfile(self._data_file):
            with open(self._data_file, "r") as savefile:
                self._stored_chats = json.load(savefile) or dict()
        else:
            self._stored_chats = dict()
        logging.info("Initialized")

    def __del__(self):
        with open(self._data_file, "w") as savefile:
            json.dump(self._stored_chats, savefile)
        logging.info("Saved")

    def handle(self, сhat_id_, text):
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