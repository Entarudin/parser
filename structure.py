from functools import cached_property

from translators import ListTranslator, ThreatTranslator, StatisticsThreatsTranslator
from services import ConfigService
from repositories import ThreatsRepository
from wrappers import MatplotlibWrapper, TelethonWrapper
from telegram_scraper import TelegramScraper
from sign_parser import SignParser
from constants import KEYWORD_FEATURE_PAIRS, KEYWORD_THREAT_TYPE_PAIRS


class Structure:
    @cached_property
    def telegram_api_id(self):
        return self.config_service.telegram_api_id

    @cached_property
    def telegram_api_hash(self):
        return self.config_service.telegram_api_hash

    @cached_property
    def telegram_phone(self):
        return self.config_service.telegram_phone

    @cached_property
    def telegram_client(self):
        return TelethonWrapper(
            self.telegram_phone,
            self.telegram_api_id,
            self.telegram_api_hash
        ).get_client()

    @cached_property
    def telegram_scraper(self):
        return TelegramScraper(
            self.telegram_client,
            self.feature_parser,
            self.threat_type_parser
        )

    @cached_property
    def feature_parser(self):
        return SignParser(KEYWORD_FEATURE_PAIRS)

    @cached_property
    def threat_type_parser(self):
        return SignParser(KEYWORD_THREAT_TYPE_PAIRS)

    @cached_property
    def config_service(self):
        return ConfigService()

    @cached_property
    def threat_translator(self):
        return ThreatTranslator()

    @cached_property
    def threats_translator(self):
        return ListTranslator(self.threat_translator)

    @cached_property
    def statistics_threats_translator(self):
        return StatisticsThreatsTranslator()

    @cached_property
    def threats_repository(self):
        return ThreatsRepository(
            self.threats_translator,
            self.statistics_threats_translator
        )

    @cached_property
    def matplotlib_wrapper(self):
        return MatplotlibWrapper()


structure = Structure()
