from enum import Enum

CHANNELS_NAMES = [
    "New_Vulnerability",
    "itsecforutel",
    "searchinform",
    "dataleak",
    "EchelonEyes",
    "haccking",
    "manual_pentesting",
    "RUSCADASEC",
    "crypto_security_lab"
]

OUTPUT_FILE = "channel_threats.json"


class TypeThreatsEnum(str, Enum):
    VULNERABILITY_TYPE = 'Уязвимость'
    ATTACK_TYPE = 'Атака'
    INCIDENT_TYPE = 'Инцидент'
    THREAT_TYPE = 'Угроза'


class FeatureThreatsEnum(str, Enum):
    VULNERABILITY = 'Уязвимость'
    ATTACK = 'Атака'
    THREAT = 'Угроза'
    CYBER = 'Кибер'
    SECURITY = "Безопасность"
    INTRUDER = "Злоумышленник"
    LEAK_INFORMATION = "Утечка"
    HACKING = "Взлом"
    DATA = "Данные"
    ENCRYPTION = "Шифрование"
    MONITORING = "Мониторинг"
    SNIFFER = "Снифер"
    INTERCEPTION = "Перехват"
    VIRUS = "Вирус"


FEATURE_ATTACKS_KEYWORDS = ["Атаки", "атака", "атаку", "атаками", "атакой"]
FEATURE_VULNERABILITIES_KEYWORDS = ["Уязвимости", "уязвимость", "уязвимостью"]
FEATURE_THREATS_KEYWORDS = ["Угрозы", "угроза", "угрозы", "угрозами"]
FEATURE_CYBER_KEYWORDS = [
    "Кибер",
    "киберсистема",
    "киберфизическая",
    "киберпреступник",
    "кибератака",
    "киберпространоство",
    "киберсталкинг"
]
FEATURE_SECURITY_KEYWORDS = ["Безопасность", "безопасности"]
FEATURE_INTRUDER_KEYWORDS = ["Злоумышленник", "злоумышленники", "злоумышленником"]
FEATURE_LEAK_INFORMATION_KEYWORDS = ["Утечка", "утечки", "утечками"]
FEATURE_HACKING_KEYWORDS = ["Взлом"]
FEATURE_DATA_KEYWORDS = ["Данные", "данных"]
FEATURE_ENCRYPTION_KEYWORDS = ["Шифрование", "шифр", "шифровальщик"]
FEATURE_MONITORING_KEYWORDS = ["Мониторинг", "мониторить", "мониторят"]
FEATURE_SNIFFER_KEYWORDS = ["Снифер", "сниферы", "сниферами"]
FEATURE_INTERCEPTION_KEYWORDS = ["Перехват", "перехватывают", "перехватили", "перехватить"]
FEATURE_VIRUS_KEYWORDS = ["Вирус", "вирусы"]

VULNERABILITIES_KEYWORDS = [
                               "слабое место",
                               "слабость",
                               "недостаток",
                               "CVE",
                               "NVD",
                               "ФСТЭК",
                               "NIST",
                               "CVSS",
                               "уязвимости нулевого дня",
                               "переполнение буфера",
                               "эксплойт",
                               "подделка запросов",
                               "межсайтовый скриптинг",
                               "удаленное выполнение кода",
                               "обратный инжиниринг",
                               "python",
                               "XSS-уязвимость",
                               "IDOR-уязвимость",
                               "SQL-инъекция",
                               "брандмауэр",
                               "эксплуатация"
                           ] + FEATURE_VULNERABILITIES_KEYWORDS

ATTACKS_KEYWORDS = [
                       "CAPEC",
                       "MITRE",
                       "ATT&CK",
                       "ФСТЭК",
                       "злоумышленник",
                       "нарушитель",
                       "хакер",
                       "жертва",
                       "пользователь",
                       "фишинг",
                       "DDoS",
                       "DoS",
                       "Brute-force",
                       "SQL-инъекция",
                       "таргетированная атака",
                       "целевая атака",
                       "APT",
                       "сетевая атака",
                       "шпионское ПО",
                       "касперский",
                       "код безопасности",
                       "InfoWatch",
                   ] + FEATURE_ATTACKS_KEYWORDS

INCIDENTS_KEYWORDS = [
    "информационная безопасность",
    "касперский",
    "реагирование",
    "последствия",
    "ущерб",
    "нежелательное событие",
    "атака",
    "нарушение",
    "потеря",
    "причины",
    "следствие",
    "мошенник",
]

THREATS_KEYWORDS = [
                       "ФСТЭК",
                       "CWE",
                       "CWSS",
                       "внутренняя угроза",
                       "внешняя угроза",
                       "опасность",
                       "информационная система",
                       "автоматизированная система",
                       "информационные ресурсы",
                       "искажение",
                       "несанкционированный",
                       "модификация",
                       "разрушение",
                       "дестабилизация",
                       "нарушение",
                       "реализация"
                   ] + FEATURE_THREATS_KEYWORDS

KEYWORDS = FEATURE_ATTACKS_KEYWORDS + FEATURE_VULNERABILITIES_KEYWORDS + FEATURE_THREATS_KEYWORDS
KEYWORDS += FEATURE_SECURITY_KEYWORDS + FEATURE_INTRUDER_KEYWORDS + FEATURE_LEAK_INFORMATION_KEYWORDS
KEYWORDS += FEATURE_HACKING_KEYWORDS + FEATURE_DATA_KEYWORDS + FEATURE_ENCRYPTION_KEYWORDS
KEYWORDS += FEATURE_MONITORING_KEYWORDS + FEATURE_SNIFFER_KEYWORDS + FEATURE_INTERCEPTION_KEYWORDS
KEYWORDS += FEATURE_VIRUS_KEYWORDS + VULNERABILITIES_KEYWORDS + ATTACKS_KEYWORDS + INCIDENTS_KEYWORDS
KEYWORDS += THREATS_KEYWORDS + FEATURE_CYBER_KEYWORDS

UNIQUE_KEYWORDS = list(set(KEYWORDS))
