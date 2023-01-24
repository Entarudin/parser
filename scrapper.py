from structure import config_service, threats_repository
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
threats_repository.save_on_json_file(OUTPUT_FILE, list_threats)
