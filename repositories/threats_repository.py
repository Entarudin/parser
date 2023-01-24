from models import Threats
from utils import DateTimeEncoder
import json

class ThreatsRepository:
    def __init__(self, threats_translator):
        self.threats_translator = threats_translator

    def save_on_json_file(self, filename: str, threats: Threats):
        with open(filename, 'w', encoding='utf8') as json_file:
            presented = {
                "threats": self.threats_translator.to_dict(threats)
            }
            json.dump(presented, json_file, ensure_ascii=False, cls=DateTimeEncoder, indent=2)
