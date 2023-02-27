import re


class CapecParser:
    def __init__(self):
        self.pattern = re.compile(r'CAPEC-\d{2,7}', re.IGNORECASE)

    def parse(self, source: str) -> list[str]:
        items = set(self.pattern.findall(source))
        return [item.upper() for item in items]
