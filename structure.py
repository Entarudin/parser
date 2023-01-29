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