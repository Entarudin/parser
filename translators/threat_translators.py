from models import Threat


class ThreatTranslator:
    def to_dict(self, model: Threat) -> dict:
        return {
            "source": model.source,
            "type": model.type,
            "database_identifiers": model.database_identifiers,
            "description": model.description,
            "date_publication": model.date_publication
        }
