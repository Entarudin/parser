import re

from constants import (
    FIELD_TYPE,
    FIELD_DATABASE_IDENTIFIERS
)


class SignParser:
    def __init__(
            self,
            keyword_to_sign_pairs: list[tuple[set[str], str]],
            field: str,
            parsers: list
    ):
        self.__keyword_to_sign_pairs = keyword_to_sign_pairs
        self.__field = field
        self.parsers = parsers

    def parse(self, source: str) -> str | None | list[str]:
        if self.__field == FIELD_TYPE:
            for keywords, sign in self.__keyword_to_sign_pairs:
                if not self.__is_part_in_list(source, keywords):
                    continue
                return sign

        elif self.__field == FIELD_DATABASE_IDENTIFIERS:
            result = self.__get_database_identifiers(source)
            return result

        return None

    def __is_part_in_list(self, source: str, words: set[str]) -> bool:
        lower_source = source.lower()
        for word in words:
            if word.lower() in lower_source:
                return True
        return False

    def __get_database_identifiers(self, source: str) -> list[str]:
        database_identifiers = []
        for parser in self.parsers:
            result_parser = parser.parse(source)
            database_identifiers += result_parser

        return database_identifiers
