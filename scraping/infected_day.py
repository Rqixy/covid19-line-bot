from dis import dis
from selenium import webdriver
from scraping.scraping import scraping

# 感染日時を取得するスクレイピング
def infected_day_scraping(driver: webdriver, xpaths: dict) -> (str | None):
    try:
        infected_day = scraping(driver, xpaths) + "0:00現在"
        return infected_day
    except Exception as e:
        print("str_scraping error : " + e)
        return None