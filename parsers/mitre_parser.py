import re


class MitreParser:
    def __init__(self):
        self.pattern = re.compile(
            r'TA\d{4,7}|'
            r'T\d{4,7}|'
            r'DS\d{4,7}|'
            r'M\d{4,7}|'
            r'G\d{4,7}',
            re.IGNORECASE
        )

    def parse(self, source: str) -> list[str]:
        items = set(self.pattern.findall(source))
        return [item.upper() for item in items]
