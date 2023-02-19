from models import Exposure, StatisticsExposures
import json


class ExposuresRepository:
    def __init__(self, exposures_translator, statistics_exposures_translator):
        self.exposures_translator = exposures_translator
        self.statistics_exposures_translator = statistics_exposures_translator

    def save_on_json_file(self, filename: str, exposures: list[Exposure], statistics_exposures: StatisticsExposures):
        with open(filename, 'w', encoding='utf8') as json_file:
            presented = {
                "exposures": self.exposures_translator.to_dict(exposures),
                "statistics": self.statistics_exposures_translator.to_dict(statistics_exposures)
            }
            json.dump(presented, json_file, ensure_ascii=False, indent=2)
