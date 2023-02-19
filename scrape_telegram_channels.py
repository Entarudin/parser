from structure import structure
from constants import OUTPUT_FILE, CHANNELS_NAMES


def scrape_telegram_channels():
    telegram_scraper = structure.telegram_scraper
    matplotlib_wrapper = structure.matplotlib_wrapper
    exposures_repository = structure.exposures_repository

    exposures = telegram_scraper.scrape_channels(CHANNELS_NAMES)
    statistics = telegram_scraper.get_statistics_by_type(exposures)

    matplotlib_wrapper.get_statisctics_chart(statistics)
    exposures_repository.save_on_json_file(OUTPUT_FILE, exposures, statistics)


if __name__ == '__main__':
    scrape_telegram_channels()
