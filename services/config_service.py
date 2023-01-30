from dotenv import dotenv_values


class ConfigService:
    def __init__(self):
        self.config = dotenv_values()

    @property
    def telegram_api_id(self) -> int:
        return int(self.config["TELEGRAM_API_ID"])

    @property
    def telegram_api_hash(self) -> str:
        return self.config["TELEGRAM_API_HASH"]

    @property
    def telegram_phone(self) -> str:
        return self.config["TELEGRAM_PHONE"]
