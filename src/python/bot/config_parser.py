import os


class ConfigParser:
    @staticmethod
    def parse_bot_token():
        token = os.getenv("TG_TOKEN")
        if token is None:
            raise KeyError("Telegram bot token is not set")

        return token
