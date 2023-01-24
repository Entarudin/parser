from translators import ListTranslator, ThreatTranslator
from services import ConfigService
from repositories import ThreatsRepository

threat_translator = ThreatTranslator()
threats_translator = ListTranslator(threat_translator)

threats_repository = ThreatsRepository(threats_translator)

config_service = ConfigService()
