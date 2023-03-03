from bs4 import BeautifulSoup


class RiaNewsTitleExtractor:
    def extract(self, soup: BeautifulSoup) -> str | None:
        article_header = soup.find("div", class_="article__header")
        if not article_header:
            return None
        article_title_div = article_header.find("div", class_="article__title")
        if article_title_div:
            return article_title_div.getText(strip=True)
        article_title_h1 = article_header.find("h1", class_="article__title")
        if article_title_h1:
            return article_title_h1.getText(strip=True)
