from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime, timedelta
import re

from parsers import ExposureTypeParser, DatabaseIdentifiersParser, ExposureTitleParser
from constants import UNIQUE_KEYWORDS, TypeExposuresEnum
from models import Exposure, StatisticsExposures


class TelegramScraper:
    def __init__(
            self,
            client: TelegramClient,
            database_identifiers_parser: DatabaseIdentifiersParser,
            exposure_type_parser: ExposureTypeParser,
            exposure_title_parser: ExposureTitleParser
    ):
        self.client = client
        self.min_count_coincidences_with_unique_keywords = 2
        self.database_identifiers_parser = database_identifiers_parser
        self.exposure_type_parser = exposure_type_parser
        self.exposure_title_parser = exposure_title_parser

    def scrape_channels(self, channels_names: list[str]) -> list[Exposure]:
        result = []
        for channel_name in channels_names:
            result += self.scrape_channel(channel_name)
        return result

    def scrape_channel(self, channel_name: str) -> list[Exposure]:
        print(f'[{datetime.utcnow().isoformat()}][TelegramScraper] - {channel_name} scraping started')
        channel_entity = self.client.get_entity(channel_name)
        offset_id = 0
        limit = 100
        exposures = []
        while True:
            history_posts_page = self.__get_history_posts_page(
                channel_entity,
                offset_id,
                limit
            )
            if not history_posts_page.messages:
                break
            messages = history_posts_page.messages
            exposures += self.__build_exposures_from_messages(messages, channel_name)
            offset_id = messages[len(messages) - 1].id
        return exposures

    def get_statistics_by_type(self, exposures: list[Exposure]) -> StatisticsExposures:
        statistics_exposures = StatisticsExposures()
        statistics_exposures.summary = len(exposures)
        type_to_number = {
            TypeExposuresEnum.THREAT.value: 0,
            TypeExposuresEnum.ATTACK.value: 0,
            TypeExposuresEnum.INCIDENT.value: 0,
            TypeExposuresEnum.VULNERABILITY.value: 0
        }
        for item in exposures:
            if item.type not in type_to_number.keys():
                continue
            type_to_number[item.type] += 1
        statistics_exposures.assign_type_to_number(type_to_number)
        return statistics_exposures

    def __build_exposures_from_messages(self, messages: list, channel_name: str) -> list[Exposure]:
        exposures = []
        for message in messages:
            text = str(message.message)
            half_of_year_days = 180
            if self.__get_difference_in_days(message.date.isoformat()) > half_of_year_days:
                continue
            if not self.__is_part_in_list_by_unique_keywords(text, UNIQUE_KEYWORDS):
                continue
            exposure = self.__build_exposure(channel_name, message.id, message.message, message.date)
            if not exposure:
                continue
            exposures.append(exposure)
        return exposures

    def __build_exposure(self, channel_name, message_id, message_text, message_date) -> Exposure | None:
        exposure = Exposure()
        exposure.type = self.exposure_type_parser.parse(message_text)
        if not exposure.type:
            return None
        exposure.database_identifiers = self.database_identifiers_parser.parse(message_text)
        exposure.title = self.exposure_title_parser.parse(message_text)
        exposure.source = self.__build_message_url(channel_name, message_id)
        exposure.description = self.__fix_many_spaces_with_http_clck(message_text)
        exposure.date_publication = message_date.isoformat()
        return exposure

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
