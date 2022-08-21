from tkinter import E
from selenium import webdriver

from scraping.scraping import scraping
from scraping.unit.remove_comma import remove_comma
from scraping.unit.str_to_int import str_to_int


# スクレピングで感染者、重症者、死亡者の人数を取得して整数型に変換して返す
def people_scraping(driver: webdriver, xpaths: dict) -> (int | None):
    try:
        str_people = scraping(driver, xpaths)

        # もしスクレピングができていなかったら、例外を発生させる
        if str_people == '':
            raise Exception("人数の取得ができませんでした。")

        removed_comma_people = remove_comma(str_people)
        people = str_to_int(removed_comma_people)
        
        return people
    except Exception as e:
        print("str_people error : " + str(e))
        return None
