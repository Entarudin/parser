from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime, timedelta
import re

from parsers.sign_parser import SignParser
from constants import UNIQUE_KEYWORDS, TypeThreatsEnum
from models import Threat, StatisticsThreats


class TelegramScraper:
    def __init__(
            self,
            client: TelegramClient,
            database_identifiers_parser: SignParser,
            threat_type_parser: SignParser,
    ):
        self.client = client
        self.min_count_coincidences_with_unique_keywords = 2
        self.database_identifiers_parser = database_identifiers_parser
        self.threat_type_parser = threat_type_parser

    def scrape_channels(self, channels_names: list[str]) -> list[Threat]:
        result = []
        for channel_name in channels_names:
            result += self.scrape_channel(channel_name)
        return result

    def scrape_channel(self, channel_name: str) -> list[Threat]:
        print(f'[{datetime.utcnow().isoformat()}][TelegramScraper] - {channel_name} scraping started')
        channel_entity = self.client.get_entity(channel_name)
        offset_id = 0
        limit = 100
        threats = []
        while True:
            history_posts_page = self.__get_history_posts_page(
                channel_entity,
                offset_id,
                limit
            )
            if not history_posts_page.messages:
                break
            messages = history_posts_page.messages
            threats += self.__build_threats_from_messages(messages, channel_name)
            offset_id = messages[len(messages) - 1].id
        return threats

    def get_statistics_by_type(self, list_threats: list[Threat]) -> StatisticsThreats:
        statistics_threats = StatisticsThreats()
        statistics_threats.summary = len(list_threats)
        type_to_number = {
            TypeThreatsEnum.THREAT.value: 0,
            TypeThreatsEnum.ATTACK.value: 0,
            TypeThreatsEnum.INCIDENT.value: 0,
            TypeThreatsEnum.VULNERABILITY.value: 0
        }
        for item in list_threats:
            if item.type not in type_to_number.keys():
                continue
            type_to_number[item.type] += 1
        statistics_threats.assign_type_to_number(type_to_number)
        return statistics_threats

    def __build_threats_from_messages(self, messages: list, channel_name: str) -> list[Threat]:
        threats = []
        for message in messages:
            text = str(message.message)
            half_of_year_days = 180
            if self.__get_difference_in_days(message.date.isoformat()) > half_of_year_days:
                continue
            if not self.__is_part_in_list_by_unique_keywords(text, UNIQUE_KEYWORDS):
                continue
            threat = self.__build_threat(channel_name, message.id, message.message, message.date)
            if not threat:
                continue
            threats.append(threat)
        return threats

    def __build_threat(self, channel_name, message_id, message_text, message_date) -> Threat | None:
        threat = Threat()
        threat.type = self.threat_type_parser.parse(message_text)
        if not threat.type:
            return None
        threat.database_identifiers = self.database_identifiers_parser.parse(message_text)
        threat.source = self.__build_message_url(channel_name, message_id)
        threat.description = self.__fix_many_spaces_with_http_clck(message_text)
        threat.date_publication = message_date.isoformat()
        return threat

    def __build_message_url(self, channel_name: str, message_id: int) -> str:
        return f"https://t.me/{channel_name}/{message_id}"

    def __is_part_in_list_by_unique_keywords(self, string: str, words: list) -> bool:
        count_coincidences = 0
        for word in words:
            if word.lower() in string.lower():
                count_coincidences += 1
        return count_coincidences >= self.min_count_coincidences_with_unique_keywords

    def __fix_many_spaces_with_http_clck(self, string: str) -> str:
        return re.sub(' *https://clck', " https://clck", string)

    def __get_difference_in_days(self, iso_date: str) -> int:
        datetime_now = datetime.now()
        event_datetime = datetime.fromisoformat(iso_date)
        delta_seconds = (datetime_now.timestamp() - event_datetime.timestamp())
        return timedelta(seconds=delta_seconds).days

    def __get_history_posts_page(self, channel_entity, offset_id, limit):
        try:
            return self.client(
                GetHistoryRequest(
                    peer=channel_entity,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                )
            )
        except Exception as ex:
            print(str(ex))
