from dotenv import dotenv_values


class ConfigService:
    def __init__(self):
        self.config = dotenv_values()

    def get_telegram_api_id(self) -> int:
        return int(self.config["TELEGRAM_API_ID"])

    def get_telegram_api_hash(self) -> str:
        return self.config["TELEGRAM_API_HASH"]

    def get_telegram_phone(self) -> str:
        return self.config["TELEGRAM_PHONE"]
