from constants import TypeExposuresEnum
from models import Exposure, StatisticsExposures


class ExposuresStatisticsService:
    def get_statistics_by_type(self, exposures: list[Exposure]) -> StatisticsExposures:
        statistics_exposures = StatisticsExposures()
        statistics_exposures.summary = len(exposures)
        type_to_number = {
            TypeExposuresEnum.THREAT.value: 0,
            TypeExposuresEnum.ATTACK.value: 0,
            TypeExposuresEnum.INCIDENT.value: 0,
            TypeExposuresEnum.VULNERABILITY.value: 0
        }
        for item in exposures:
            if item.type not in type_to_number.keys():
                continue
            type_to_number[item.type] += 1
        statistics_exposures.assign_type_to_number(type_to_number)
        return statistics_exposures
