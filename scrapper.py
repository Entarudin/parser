from structure import config_service, threats_repository, matplotlib_wrapper
from telethon.sync import TelegramClient
from telegram_scraper import TelegramScraper
from constants import OUTPUT_FILE, CHANNELS_NAMES

API_ID = config_service.get_telegram_api_id()
API_HASH = config_service.get_telegram_api_hash()
PHONE = config_service.get_telegram_phone()

client = TelegramClient(PHONE, API_ID, API_HASH)
client.start()

telegram_scraper = TelegramScraper(client)
list_threats = telegram_scraper.scrape_channels(CHANNELS_NAMES)
statistics = telegram_scraper.get_statistics_by_type(list_threats)

matplotlib_wrapper.get_statisctics_chart(statistics)
threats_repository.save_on_json_file(OUTPUT_FILE, list_threats, statistics)