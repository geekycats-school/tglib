import os

TOKEN = os.environ["BOT_TOKEN"]
URL = "https://api.telegram.org/bot{token}/{method}"
TEXT_CORRECT_ANSWER = {"en": "Correct", "ru": "Правильно"}
TEXT_INCORRECT_ANSWER = {"en": "Wrong", "ru": "Неправильно"}
TEXT_NO_HANDLER = "No handler for your request"
