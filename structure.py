from functools import cached_property

from translators import (
    ListTranslator,
    ExposureTranslator,
    StatisticsExposuresTranslator
)
from services import ConfigService
from repositories import ExposuresRepository
from wrappers import (
    MatplotlibWrapper,
    TelethonWrapper
)
from telegram_scraper import TelegramScraper
from constants import KEYWORD_EXPOSURE_TYPE_PAIRS
from parsers import (
    CWEParser,
    CVEParser,
    BduFSTECParser,
    DatabaseIdentifiersParser,
    ExposureTypeParser,
    ExposureTitleParser
)


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
            self.database_identifiers_parser,
            self.exposure_type_parser,
            self.exposure_title_parser
        )

    @cached_property
    def database_identifiers_parser(self):
        return DatabaseIdentifiersParser(
            [
                self.bdu_fsctec_parser,
                self.cve_parser,
                self.cwe_parser
            ]
        )

    @cached_property
    def exposure_type_parser(self):
        return ExposureTypeParser(KEYWORD_EXPOSURE_TYPE_PAIRS)

    @cached_property
    def exposure_title_parser(self):
        return ExposureTitleParser()

    @cached_property
    def config_service(self):
        return ConfigService()

    @cached_property
    def exposure_translator(self):
        return ExposureTranslator()

    @cached_property
    def exposures_translator(self):
        return ListTranslator(self.exposure_translator)

    @cached_property
    def statistics_exposures_translator(self):
        return StatisticsExposuresTranslator()

    @cached_property
    def exposures_repository(self):
        return ExposuresRepository(
            self.exposures_translator,
            self.statistics_exposures_translator
        )

    @cached_property
    def matplotlib_wrapper(self):
        return MatplotlibWrapper()

    @cached_property
    def cve_parser(self):
        return CVEParser()

    @cached_property
    def cwe_parser(self):
        return CWEParser()

    @cached_property
    def bdu_fsctec_parser(self):
        return BduFSTECParser()


structure = Structure()
