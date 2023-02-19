from models import Exposure


class ExposureTranslator:
    def to_dict(self, model: Exposure) -> dict:
        return {
            "source": model.source,
            "type": model.type,
            "database_identifiers": model.database_identifiers,
            "title": model.title,
            "description": model.description,
            "date_publication": model.date_publication
        }
