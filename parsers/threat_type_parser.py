class ThreatTypeParser:
    def __init__(self, keyword_to_sign_pairs: list[tuple[set[str], str]]):
        self.__keyword_to_sign_pairs = keyword_to_sign_pairs

    def parse(self, source: str) -> str | None | list[str]:
        for keywords, sign in self.__keyword_to_sign_pairs:
            if not self.__is_part_in_list(source, keywords):
                continue
            return sign

    def __is_part_in_list(self, source: str, words: set[str]) -> bool:
        lower_source = source.lower()
        for word in words:
            if word.lower() in lower_source:
                return True
        return False
