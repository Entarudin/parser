from functools import cached_property
from translators import ListTranslator, ThreatTranslator, StatisticsThreatsTranslator
from services import ConfigService
from repositories import ThreatsRepository
from wrappers import MatplotlibWrapper
from telegram_scraper import TelegramScraper

# Todo: make wrapper
from telethon.sync import TelegramClient


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
        # maybe start inside scraper
        return TelegramClient(
            self.telegram_phone,
            self.telegram_api_id,
            self.telegram_api_hash
        )

    @cached_property
    def telegram_scraper(self):
        return TelegramScraper(self.telegram_client)

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
