from selenium import webdriver
import scraping as SC
import unit.remove_comma as RC
import unit.str_to_int as STI

# 感染、重症、死亡の人数を取得するスクレピング
def people_scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> int:
    try:
        num = SC.scraping(driver, iframe_xpath, scraping_xpath)
        num = RC.remove_comma(num)
        num = STI.str_to_int(num)
        print("people_scraping : " + str(num))
        return num
    except Exception as e:
        print("num_scraping error : " + e)
        return None