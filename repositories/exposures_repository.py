from models import Exposure, StatisticsExposures
from utils import uuid_generate
import json


class ExposuresRepository:
    def __init__(self, exposure_translator, statistics_exposures_translator):
        self.exposure_translator = exposure_translator
        self.statistics_exposures_translator = statistics_exposures_translator

    def save_on_json_file(
            self,
            filename: str,
            exposures: list[Exposure],
            statistics_exposures: StatisticsExposures
    ):
        exposures_dict = {}
        for exposure in exposures:
            uuid_exposure = str(uuid_generate(exposure.source))
            exposures_dict[uuid_exposure] = self.exposure_translator.to_dict(exposure)

        with open(filename, 'w', encoding='utf8') as json_file:
            presented = {
                "exposures": exposures_dict,
                "statistics": self.statistics_exposures_translator.to_dict(statistics_exposures)
            }
            json.dump(presented, json_file, ensure_ascii=False, indent=2)
