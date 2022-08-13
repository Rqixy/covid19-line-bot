from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# スクレピング実行部分
def scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> str:
    result_text = ''

    # 非同期でWebページが表示されるため、取得できないことがあるため、
    # Webページを更新し再度取得できるか試す。
    for i in range(10):
        time.sleep(2)   # 
        # iframeに入る
        iframe = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe)
        time.sleep(2)
        result = driver.find_element(By.XPATH, scraping_xpath)
        result_text = result.text

        # iframeから元のフレームに戻る
        driver.switch_to.default_content()

        # 取得できたらループを抜ける
        if result_text != '':
            break

        # Webページを更新する
        driver.refresh()

    return result_text