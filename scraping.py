import time
from unittest import result
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


#スクレイピング部分
def covid19_scraping(iframe_xpath, scraping_xpath):
    #中身が空の場合、取ってこれるまで繰り返す
    result = None
    while result == None:
        # iframeに入る
        iframe = driver.find_element(by=By.XPATH, value=iframe_xpath)
        driver.switch_to.frame(iframe)
        time.sleep(1)
        # スクレイピングする
        result = driver.find_element(by=By.XPATH, value=scraping_xpath)
    return result.text

# 文字列のから数値型に変換する
def remove_comma_and_text_to_int(text):
    text = text.replace(',','')
    text = int(text)
    return text

def infected_people_scraping():
    driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
    # ページが読み込まれるまで待機
    wait.until(EC.presence_of_all_elements_located)

    #更新チェック用の日付を取得する
    infected_day_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[3]/div/iframe'
    infected_day_xpath = '//*[@id="currentDate"]'
    infected_day = covid19_scraping(infected_day_iframe_xpath, infected_day_xpath)
    infected_day = infected_day + "0:00現在"
    # 元のフレームに戻る
    driver.switch_to.default_content()

    #新規感染者数
    new_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[1]/iframe'   # 新規感染者のiframe
    new_xpath = '//*[@id="newInfectedKPI"]'
    new_people = covid19_scraping(new_iframe_xpath, new_xpath)
    #数値型に変換する
    new_people = remove_comma_and_text_to_int(new_people)
    # 元のフレームに戻る
    driver.switch_to.default_content()

    #重症者数
    severe_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[4]/iframe'   # 重症者のiframe
    severe_xpath = '//*[@id="GrPh14SevereKPI"]'
    severe_people = covid19_scraping(severe_iframe_xpath, severe_xpath)
    #数値型に変換する
    severe_people = remove_comma_and_text_to_int(severe_people)
    # 元のフレームに戻る
    driver.switch_to.default_content()

    #死亡者数
    deaths_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[3]/iframe'   # 死亡者のiframe
    deaths_xpath = '//*[@id="GrPh13TotalDeadKPI"]'
    deaths = covid19_scraping(deaths_iframe_xpath, deaths_xpath)
    #数値型に変換する
    deaths = remove_comma_and_text_to_int(deaths)
    # 元のフレームに戻る
    driver.switch_to.default_content()

    driver.quit()

    # 配列にスクレイピングしたデータを格納する
    infected_people = [new_people, severe_people, deaths, infected_day]
    return infected_people