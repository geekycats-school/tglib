import os

TOKEN = os.environ["BOT_TOKEN"]
URL = "https://api.telegram.org/bot{token}/{method}"
TEXT_CORRECT_ANSWER = "Correct"
TEXT_INCORRECT_ANSWER = "Wrong"
TEXT_NO_HANDLER = "No handler for your request"
DATA_FILE = "stored_chats.json"
