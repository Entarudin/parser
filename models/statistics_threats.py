from constants import TypeThreatsEnum


class StatisticsThreats:
    def __init__(self):
        self.summary = 0
        self.count_vulnerabilities = 0
        self.count_attacks = 0
        self.count_threats = 0
        self.count_incidents = 0

    def assign_type_to_number(self, type_to_number: dict[TypeThreatsEnum, int]) -> None:
        self.count_threats = type_to_number[TypeThreatsEnum.THREAT.value]
        self.count_attacks = type_to_number[TypeThreatsEnum.ATTACK.value]
        self.count_incidents = type_to_number[TypeThreatsEnum.INCIDENT.value]
        self.count_vulnerabilities = type_to_number[TypeThreatsEnum.VULNERABILITY.value]
