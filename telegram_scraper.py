from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from constants import (
    UNIQUE_KEYWORDS,
    VULNERABILITIES_KEYWORDS,
    ATTACKS_KEYWORDS,
    INCIDENTS_KEYWORDS,
    THREATS_KEYWORDS,
    TypeThreatsEnum,
    FeatureThreatsEnum,
    FEATURE_DATA_KEYWORDS,
    FEATURE_CYBER_KEYWORDS,
    FEATURE_VIRUS_KEYWORDS,
    FEATURE_ATTACKS_KEYWORDS,
    FEATURE_HACKING_KEYWORDS,
    FEATURE_SNIFFER_KEYWORDS,
    FEATURE_THREATS_KEYWORDS,
    FEATURE_ENCRYPTION_KEYWORDS,
    FEATURE_INTERCEPTION_KEYWORDS,
    FEATURE_INTRUDER_KEYWORDS,
    FEATURE_MONITORING_KEYWORDS,
    FEATURE_SECURITY_KEYWORDS,
    FEATURE_VULNERABILITIES_KEYWORDS,
    FEATURE_LEAK_INFORMATION_KEYWORDS,
)
from models import Threat, StatisticsThreats
import re
from datetime import datetime, timedelta


class TelegramScraper:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.min_count_coincidences_with_unique_keywords = 2

    def scrape_channels(self, channels_names: list[str]) -> list[Threat]:
        result = []
        for channel_name in channels_names:
            result += self.scrape_channel(channel_name)
        return result

    def scrape_channel(self, channel_name: str) -> list[Threat]:
        print(f'[{datetime.utcnow().isoformat()}][TelegramScraper] - {channel_name} scraping started')
        threats = []

        channel_entity = self.client.get_entity(channel_name)

        offset_id = 0
        limit = 100

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
    
    def __build_threats_from_messages(self, messages: list, channel_name: str) -> list[Threat]:
        threats = []
        for message in messages:
            text = str(message.message)
            half_of_year_days = 180
            if self._get_difference_in_days(message.date.isoformat()) > half_of_year_days:
                continue
            if not self._is_part_in_list_by_unique_keywords(text, UNIQUE_KEYWORDS):
                continue
            threat = self.__build_threat(channel_name, message.id, message.message, message.date)
            if not threat:
                continue
            threats.append(threat)
        return threats

    def __build_threat(self, channel_name, message_id, message_text, message_date) -> Threat | None:
        threat = Threat()
        threat.source = self._get_link_on_channel_message(channel_name, message_id)
        threat.type = self._get_type_threat_by_description(message_text)
        threat.feature = self._get_feature_threats_by_description(message_text)
        if not threat.type or not threat.feature:
            return None
        threat.description = self._fix_many_spaces_with_http_clck(message_text)
        threat.date_publication = message_date.isoformat()
        return threat

    def __get_history_posts_page(self, channel_entity,  offset_id, limit):
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

    def _get_link_on_channel_message(self, channel_name: str, message_id: int) -> str:
        return f"https://t.me/{channel_name}/{message_id}"

    def _is_part_in_list_by_unique_keywords(self, string: str, words: list) -> bool:
        count_coincidences = 0
        for word in words:
            if word.lower() in string.lower():
                count_coincidences += 1
        return count_coincidences >= self.min_count_coincidences_with_unique_keywords

    def _is_part_in_list(self, string: str, words: list) -> bool:
        for word in words:
            if word.lower() in string.lower():
                return True
        return False

    def _get_type_threat_by_description(self, description: str) -> str:
        if self._is_part_in_list(description, VULNERABILITIES_KEYWORDS):
            return TypeThreatsEnum.VULNERABILITY.value
        elif self._is_part_in_list(description, ATTACKS_KEYWORDS):
            return TypeThreatsEnum.ATTACK.value
        elif self._is_part_in_list(description, INCIDENTS_KEYWORDS):
            return TypeThreatsEnum.INCIDENT.value
        elif self._is_part_in_list(description, THREATS_KEYWORDS):
            return TypeThreatsEnum.THREAT.value

    def _get_feature_threats_by_description(self, description: str) -> str:
        if self._is_part_in_list(description, FEATURE_THREATS_KEYWORDS):
            return FeatureThreatsEnum.THREAT.value

        elif self._is_part_in_list(description, FEATURE_LEAK_INFORMATION_KEYWORDS):
            return FeatureThreatsEnum.LEAK_INFORMATION.value

        elif self._is_part_in_list(description, FEATURE_VULNERABILITIES_KEYWORDS):
            return FeatureThreatsEnum.VULNERABILITY.value

        elif self._is_part_in_list(description, FEATURE_SECURITY_KEYWORDS):
            return FeatureThreatsEnum.SECURITY.value

        elif self._is_part_in_list(description, FEATURE_MONITORING_KEYWORDS):
            return FeatureThreatsEnum.MONITORING.value

        elif self._is_part_in_list(description, FEATURE_INTRUDER_KEYWORDS):
            return FeatureThreatsEnum.INTRUDER.value

        elif self._is_part_in_list(description, FEATURE_INTERCEPTION_KEYWORDS):
            return FeatureThreatsEnum.INTERCEPTION.value

        elif self._is_part_in_list(description, FEATURE_ENCRYPTION_KEYWORDS):
            return FeatureThreatsEnum.ENCRYPTION.value

        elif self._is_part_in_list(description, FEATURE_SNIFFER_KEYWORDS):
            return FeatureThreatsEnum.SNIFFER.value

        elif self._is_part_in_list(description, FEATURE_HACKING_KEYWORDS):
            return FeatureThreatsEnum.HACKING.value

        elif self._is_part_in_list(description, FEATURE_ATTACKS_KEYWORDS):
            return FeatureThreatsEnum.ATTACK.value

        elif self._is_part_in_list(description, FEATURE_VIRUS_KEYWORDS):
            return FeatureThreatsEnum.VIRUS.value

        elif self._is_part_in_list(description, FEATURE_CYBER_KEYWORDS):
            return FeatureThreatsEnum.CYBER.value

        elif self._is_part_in_list(description, FEATURE_DATA_KEYWORDS):
            return FeatureThreatsEnum.DATA.value

    def _fix_many_spaces_with_http_clck(self, string: str) -> str:
        return re.sub(' *https://clck', " https://clck", string)

    def _get_difference_in_days(self, iso_date: str) -> int:
        datetime_now = datetime.now()
        event_datetime = datetime.fromisoformat(iso_date)
        delta_seconds = (datetime_now.timestamp() - event_datetime.timestamp())
        return timedelta(seconds=delta_seconds).days

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
