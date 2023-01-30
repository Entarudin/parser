from telethon.sync import TelegramClient


class TelethonWrapper:
    def __init__(self, phone: str, api_id: int, api_hash: str):
        self.__phone = phone
        self.__api_id = api_id
        self.__api_hash = api_hash

    def get_client(self) -> TelegramClient:
        client = TelegramClient(
            self.__phone,
            self.__api_id,
            self.__api_hash
        )
        client.start()
        return client
