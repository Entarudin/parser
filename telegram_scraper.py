from typing import Optional
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from constants import (
    UNIQUE_KEYWORDS,
    VULNERABILITIES_KEYWORDS,
    ATTACKS_KEYWORDS,
    INCIDENTS_KEYWORDS,
    THREATS_KEYWORDS
)
from models import Threat
import re


class TelegramScraper:
    def __init__(self, client: Optional[TelegramClient]):
        self.client = client

    def scrape_channels(self, channels_names: list[str]) -> list[Threat]:
        result = []
        for item in channels_names:
            result += self.scrape_channel(item)
        return result

    def scrape_channel(self, channel_name: str) -> list[Threat]:
        result = []

        channel_entity = self.client.get_entity(channel_name)

        offset_id = 0
        limit = 100
        total_messages = 0
        total_count_limit = 0

        while True:
            history_posts = self.client(GetHistoryRequest(
                peer=channel_entity,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

            if not history_posts.messages:
                break

            messages = history_posts.messages

            for message in messages:
                if self._is_part_in_list(str(message.message), UNIQUE_KEYWORDS):
                    message_id = message.id
                    threat = Threat()
                    threat.source = self._get_link_on_channel_message(channel_name, message_id)
                    threat.type = self._get_type_threat_by_description(message.message)
                    threat.description = self._fix_many_spaces_with_hhtp_clck(message.message)
                    threat.date_publication = message.date
                    result.append(threat)

            offset_id = messages[len(messages) - 1].id

            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        return result

    def _get_link_on_channel_message(self, channel_name: str, message_id: int) -> str:
        return f"https://t.me/{channel_name}/{message_id}"

    def _is_part_in_list(self, string: str, words: list) -> bool:
        for word in words:
            if word.lower() in string.lower():
                return True
        return False

    def _get_type_threat_by_description(self, description: str) -> str:
        if self._is_part_in_list(description, VULNERABILITIES_KEYWORDS):
            return "Уязвимость"
        elif self._is_part_in_list(description, ATTACKS_KEYWORDS):
            return "Атака"
        elif self._is_part_in_list(description, INCIDENTS_KEYWORDS):
            return "Инцидент"
        elif self._is_part_in_list(description, THREATS_KEYWORDS):
            return "Угроза"
        else:
            return "type undefined"

    def _fix_many_spaces_with_hhtp_clck(self, string: str) -> str:
        return re.sub(' *https://clck', " https://clck", string)
