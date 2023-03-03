from structure import structure
import json


def main():
    ria_news_scraper = structure.ria_news_scraper
    exposures_translator = structure.exposures_translator
    exposures = ria_news_scraper.scrape("keyword_khakery")
    with open("ria_news.json", 'w', encoding='utf8') as json_file:
        presented = {
            "exposures": exposures_translator.to_dict(exposures),
        }
        json.dump(presented, json_file, ensure_ascii=False, indent=2)


main()
