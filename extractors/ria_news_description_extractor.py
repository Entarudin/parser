from bs4 import BeautifulSoup


class RiaNewsDescriptionExtractor:
    def extract(self, soup: BeautifulSoup) -> str | None:
        article_text_chunks = []
        list_article_blocks = soup.findAll("div", class_="article__block")
        for item in list_article_blocks:
            article_text = item.find("div", class_="article__text")
            article_quote = item.find("div", class_="article__quote-text m-small")
            if article_text:
                article_text_chunks.append(article_text.getText(strip=True))
            if article_quote:
                article_text_chunks.append(article_quote.getText(strip=True))
        return " ".join(article_text_chunks)
