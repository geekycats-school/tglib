import os

TOKEN = os.environ["BOT_TOKEN"]
URL = "https://api.telegram.org/bot{token}/{method}"
TEXT_CORRECT_ANSWER = "Right!"
TEXT_INCORRECT_ANSWER = "This isn't a right answer."
TEXT_NO_HANDLER = "No handler for your request"
