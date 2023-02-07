import re


class BduFSTECParser:
    def __init__(self):
        self.pattern = re.compile(r'BDU[:-]\d{4}[:-]\d{4,7}', re.IGNORECASE)

    def parse(self, source: str) -> list[str]:
        items = set(self.pattern.findall(source))
        return [item.upper() for item in items]
