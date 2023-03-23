import requests
from bs4 import BeautifulSoup
from datetime import datetime

from models import Exposure
from parsers import (
    DatabaseIdentifiersParser,
    ExposureTypeParser
)
from extractors import (
    RiaNewsDatePublicationExtractor,
    RiaNewsTitleExtractor,
    RiaNewsDescriptionExtractor
)


class RiaNewsScraper:
    def __init__(
            self,
            base_url: str,
            database_identifiers_parser: DatabaseIdentifiersParser,
            exposure_type_parser: ExposureTypeParser,
            ria_news_date_publication_extractor: RiaNewsDatePublicationExtractor,
            ria_news_title_extractor: RiaNewsTitleExtractor,
            ria_news_description_extractor: RiaNewsDescriptionExtractor
    ):
        self.base_url = base_url
        self.database_identifiers_parser = database_identifiers_parser
        self.exposure_type_parser = exposure_type_parser
        self.ria_news_date_publication_extractor = ria_news_date_publication_extractor
        self.ria_news_title_extractor = ria_news_title_extractor
        self.ria_news_description_extractor = ria_news_description_extractor

    def scrape(self, keyword: str):
        url = f"{self.base_url}/{keyword}/"
        return self.__build_exposures_from_news(url)

    def __build_exposures_from_news(self, url: str) -> list[Exposure]:
        exposures = []
        next_pages_urls = self.__get_next_pages_urls(url)
        news_urls = self.__get_news_urls(next_pages_urls)
        for news_url in news_urls:
            print(f'[{datetime.utcnow().isoformat()}][RiaNewsScraper] - {news_url} scraping started')
            soup = self.__get_soup_by_request(news_url)
            date_publication_news = self.ria_news_date_publication_extractor.extract(soup)
            if not date_publication_news:
                continue
            description_news = self.ria_news_description_extractor.extract(soup)
            if not description_news:
                continue
            title_news = self.ria_news_title_extractor.extract(soup)
            if not title_news:
                continue
            exposure = self.__build_exposure(
                news_url,
                date_publication_news,
                description_news,
                title_news
            )
            if not exposure:
                continue
            exposures.append(exposure)
        return exposures

    def __build_exposure(
            self,
            url: str,
            date_publication: str,
            description: str,
            title: str
    ) -> Exposure | None:
        exposure = Exposure()
        exposure.type = self.exposure_type_parser.parse(description)
        if not exposure.type:
            return None
        exposure.database_identifiers = self.database_identifiers_parser.parse(description)
        exposure.title = title
        exposure.source = url
        exposure.description = description
        exposure.date_publication = date_publication
        return exposure

    def __get_news_urls(self, next_pages_urls: list[str]) -> list[str]:
        result = []
        for next_page_url in next_pages_urls:
            news_urls = self.__get_news_urls_in_next_page_url(next_page_url)
            result += news_urls
        return result

    def __get_news_urls_in_next_page_url(self, url: str) -> list[str]:
        news_url = []
        soup = self.__get_soup_by_request(url)
        list_news = soup.findAll("div", class_="list-item__content")
        for item in list_news:
            url_news = item.find("a", class_="list-item__image").get("href")
            if url_news:
                news_url.append(url_news)
            continue
        return news_url

    def __get_next_pages_urls(self, url: str) -> list[str]:
        next_pages_urls = []
        for _ in range(10):
            soup = self.__get_soup_by_request(url)
            next_url_chunk = self.__parse_next_page_url(soup)
            if not next_url_chunk:
                break
            next_page_url = self.base_url + self.__parse_next_page_url(soup)
            next_pages_urls.append(next_page_url)
        return next_pages_urls

    def __parse_next_page_url(self, soup) -> str | None:
        load_more_button = soup.select_one(".list-more.color-btn-second-hover")
        url_chunk = None
        if load_more_button:
            url_chunk = load_more_button.get('data-url')
        loaded_div = soup.select_one(".list-items-loaded")
        if loaded_div:
            url_chunk = loaded_div.get("data-next-url")
        return url_chunk

    def __get_soup_by_request(self, url: str) -> BeautifulSoup:
        with requests.Session() as session:
            response = session.get(url)
            page_source = response.text
            soup = BeautifulSoup(page_source, "lxml")
            return soup
