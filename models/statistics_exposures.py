from constants import TypeExposuresEnum


class StatisticsExposures:
    def __init__(self):
        self.summary = 0
        self.count_vulnerabilities = 0
        self.count_attacks = 0
        self.count_threats = 0
        self.count_incidents = 0

    def assign_type_to_number(self, type_to_number: dict[TypeExposuresEnum, int]) -> None:
        self.count_threats = type_to_number[TypeExposuresEnum.THREAT.value]
        self.count_attacks = type_to_number[TypeExposuresEnum.ATTACK.value]
        self.count_incidents = type_to_number[TypeExposuresEnum.INCIDENT.value]
        self.count_vulnerabilities = type_to_number[TypeExposuresEnum.VULNERABILITY.value]
