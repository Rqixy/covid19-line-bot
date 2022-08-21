from selenium import webdriver
from scraping.scraping import scraping

# 感染日時を取得するスクレイピング
def infected_day_scraping(driver: webdriver, xpaths: dict) -> (str | None):
    try:
        scraped_text = scraping(driver, xpaths)

        # もしスクレピングができていなかったら、例外を発生させる
        if scraped_text == '':
            raise Exception("感染日時情報が取得できませんでした。")

        infected_day = scraped_text + "0:00現在"
        return infected_day
    except Exception as e:
        print("str_scraping error : " + str(e))
        return None