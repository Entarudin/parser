from structure import structure
from constants import OUTPUT_FILE, CHANNELS_NAMES, RIA_NEWS_KEYWORDS


def scrape():
    telegram_scraper = structure.telegram_scraper
    exposures_statistics_service = structure.exposures_statistics_service
    ria_news_scraper = structure.ria_news_scraper
    exposures_repository = structure.exposures_repository

    exposures_from_telegram_channels = telegram_scraper.scrape_channels(CHANNELS_NAMES)
    exposures_from_ria_news = ria_news_scraper.scrape(RIA_NEWS_KEYWORDS)
    exposures = exposures_from_telegram_channels + exposures_from_ria_news
    statistics = exposures_statistics_service.get_statistics_by_type(exposures)

    exposures_repository.save_on_json_file(OUTPUT_FILE, exposures, statistics)


if __name__ == '__main__':
    scrape()
