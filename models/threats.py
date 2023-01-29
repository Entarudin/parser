from typing import Optional


class Threat:
    def __init__(self):
        self.source: Optional[str] = None
        self.type: Optional[str] = None
        self.date_publication: Optional[str] = None
        self.description: Optional[str] = None
        self.feature: Optional[str] = None


Threats = list[Threat]
