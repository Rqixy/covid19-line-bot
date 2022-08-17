from dis import dis
from selenium import webdriver
import scraping_test.scraping as SC

# 感染日時を取得するスクレイピング
def infected_day_scraping(driver: webdriver, xpaths: dict) -> str:
    try:
        infected_day = SC.scraping(driver, xpaths) + "0:00現在"
        return infected_day
    except Exception as e:
        print("str_scraping error : " + e)
        return None