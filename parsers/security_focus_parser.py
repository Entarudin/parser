import re


class SecurityFocusParser:
    def __init__(self):
        self.pattern = re.compile(
            r'DSA-\d{4,7}-\d{1,7}|'
            r'TZO-\d{1,7}-\d{4}|'
            r'WSA-\d{4}-\d{4,7}|'
            r'SSA[:-]\d{4}[:-]\d{2,7}[:-]\d{2,7}',
            re.IGNORECASE
        )

    def parse(self, source: str) -> list[str]:
        items = set(self.pattern.findall(source))
        return [item.upper() for item in items]