from structure import structure
from constants import OUTPUT_FILE, CHANNELS_NAMES

telegram_scraper = structure.telegram_scraper
matplotlib_wrapper = structure.matplotlib_wrapper
threats_repository = structure.threats_repository

list_threats = telegram_scraper.scrape_channels(CHANNELS_NAMES)
statistics = telegram_scraper.get_statistics_by_type(list_threats)

matplotlib_wrapper.get_statisctics_chart(statistics)
threats_repository.save_on_json_file(OUTPUT_FILE, list_threats, statistics)