import telegram
import logging


def main():
    while True:
        try:
            chat_id, message = telegram.get_message()
        except TimeoutError:
            continue
        except telegram.TelegramError as e:
            logging.error(f"Exception occured\n{e}")
            continue
        parser = telegram.get_message_parser(chat_id, message)
        telegram.send_message(chat_id, parser(message))

main()