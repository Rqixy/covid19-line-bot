from selenium import webdriver
import scraping as SC

# 感染日時を取得するスクレイピング
def infected_day_scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> str:
    try:
        text = SC.scraping(driver, iframe_xpath, scraping_xpath)
        text += "0:00現在"
        print("infected_day_scraping : " + text)
        return text
    except Exception as e:
        print("str_scraping error : " + e)
        return None