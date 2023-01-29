from typing import Optional


class StatisticsThreats:
    def __init__(self):
        self.summary: Optional[int] = 0
        self.count_vulnerabilities: Optional[int] = 0
        self.count_attacks: Optional[int] = 0
        self.count_threats: Optional[int] = 0
        self.count_incidents: Optional[int] = 0