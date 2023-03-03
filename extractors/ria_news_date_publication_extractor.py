from bs4 import BeautifulSoup
from datetime import datetime


class RiaNewsDatePublicationExtractor:
    def extract(self, soup: BeautifulSoup) -> str:
        article_date = soup\
            .find("div", class_="article__info-date").find("a").getText()
        article_date_datetime = datetime.strptime(article_date, "%H:%M %d.%m.%Y")
        return datetime.isoformat(article_date_datetime)
