class DatabaseIdentifiersParser:
    def __init__(self, parsers: list):
        self.parsers = parsers

    def parse(self, source: str) -> None | list[str]:
        result = self.__get_database_identifiers(source)
        return result

    def __get_database_identifiers(self, source: str) -> list[str]:
        database_identifiers = []
        for parser in self.parsers:
            result_parser = parser.parse(source)
            database_identifiers += result_parser

        return database_identifiers
