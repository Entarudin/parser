from models import Threat, StatisticsThreats
import json


class ThreatsRepository:
    def __init__(self, threats_translator, statistics_threats_translator):
        self.threats_translator = threats_translator
        self.statistics_threats_translator = statistics_threats_translator

    def save_on_json_file(self, filename: str, threats: list[Threat], statistics_threats: StatisticsThreats):
        with open(filename, 'w', encoding='utf8') as json_file:
            presented = {
                "threats": self.threats_translator.to_dict(threats),
                "statistics": self.statistics_threats_translator.to_dict(statistics_threats)
            }
            json.dump(presented, json_file, ensure_ascii=False, indent=2)
