from selenium import webdriver
import scraping.scraping as SC
import scraping.unit.remove_comma as RC
import scraping.unit.str_to_int as STI

# 感染、重症、死亡の人数を取得するスクレピング
def people_scraping(driver: webdriver, xpaths: dict) -> (int | None):
    try:
        str_people = SC.scraping(driver, xpaths)
        removed_comma_people = RC.remove_comma(str_people)
        people = STI.str_to_int(removed_comma_people)
        
        return people
    except Exception as e:
        print("num_scraping error : " + e)
        return None