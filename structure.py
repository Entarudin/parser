from functools import cached_property
from translators import ListTranslator, ThreatTranslator, StatisticsThreatsTranslator
from services import ConfigService
from repositories import ThreatsRepository
from wrappers import MatplotlibWrapper

threat_translator = ThreatTranslator()
threats_translator = ListTranslator(threat_translator)

statistics_threats_translator = StatisticsThreatsTranslator()
threats_repository = ThreatsRepository(threats_translator, statistics_threats_translator)

config_service = ConfigService()

matplotlib_wrapper = MatplotlibWrapper()


class Structure:
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
    def config_service(self):
        return ConfigService()

    @cached_property
    def matplotlib_wrapper(self):
        return MatplotlibWrapper()


structure = Structure()
