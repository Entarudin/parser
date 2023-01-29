from models import StatisticsThreats


class StatisticsThreatsTranslator:
    def to_dict(self, model: StatisticsThreats) -> dict:
        return {
            "summary": model.summary,
            "count_vulnerabilities": model.count_vulnerabilities,
            "count_threats": model.count_threats,
            "count_attacks": model.count_attacks,
            "count_incidents": model.count_incidents
        }
