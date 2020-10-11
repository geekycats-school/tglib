import requests
import json

TOKEN = ""
URL = "https://api.telegram.org/bot{token}/{method}"

def find_command(command_name: str, args: str) -> Function[str]:
    # /command arg1 arg2  
    pass

def parse_message():
    pass

def get_message(offset: int, limit: int = 1) -> Tuple[int, str]:
    # -> chat_id, text
    pass

def send_message(chat_id: int, text: str):
    data = {
        "chat_id": id,
        "text": text
    }
    p = requests.post(URL.format(token=TOKEN, method="sendMessage"), data=data)



