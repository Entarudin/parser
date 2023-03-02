import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

from models import Exposure
from parsers import DatabaseIdentifiersParser, ExposureTypeParser, ExposureTitleParser


class RiaNewsScraper:
    def __init__(
            self,
            base_url: str,
            database_identifiers_parser: DatabaseIdentifiersParser,
            exposure_type_parser: ExposureTypeParser,
            exposure_title_parser: ExposureTitleParser
    ):
        self.base_url = base_url
        self.database_identifiers_parser = database_identifiers_parser
        self.exposure_type_parser = exposure_type_parser
        self.exposure_title_parser = exposure_title_parser

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
            date_publication_news = self.__get_date_publication(soup)
            if not date_publication_news:
                continue
            description_news = self.__get_description_news(soup)
            if not description_news:
                continue
            title_news = self.__get_title_news(soup)
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

    def __get_date_publication(self, soup: BeautifulSoup) -> str:
        article_date = soup.find("div", class_="article__info-date").find("a").getText()
        article_date_datetime = datetime.strptime(article_date, "%H:%M %d.%m.%Y")
        return datetime.isoformat(article_date_datetime)

    def __get_description_news(self, soup: BeautifulSoup) -> str:
        article_text_chunks = []
        list_article_blocks = soup.findAll("div", class_="article__block")
        for item in list_article_blocks:
            article_text = item.find("div", class_="article__text")
            article_quote = item.findNext("div", class_="article__quote-text m-small")
            if article_text:
                article_text_chunks.append(article_text.getText(strip=True))
            if article_quote:
                article_text_chunks.append(article_quote.getText(strip=True))
        return " ".join(article_text_chunks)

    def __get_title_news(self, soup: BeautifulSoup) -> str:
        article_header = soup.find("div", class_="article__header")
        if article_header:
            article_title_div = article_header.find("div", class_="article__title")
            if article_title_div:
                return article_title_div.getText(strip=True)
            article_title_h1 = article_header.find("h1", class_="article__title")
            if article_title_h1:
                return article_title_h1.getText(strip=True)

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
            sleep(3)
            response = session.get(url)
            page_source = response.text
            soup = BeautifulSoup(page_source, "lxml")
            return soup
