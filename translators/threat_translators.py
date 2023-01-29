from models import Threat


class ThreatTranslator:
    def to_dict(self, model: Threat) -> dict:
        return {
            "source": model.source,
            "type": model.type,
            "feature": model.feature,
            "description": model.description,
            "date_publication": model.date_publication
        }
