from inspect import isframe
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

driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
# ページが読み込まれるまで待機
wait.until(EC.presence_of_all_elements_located)

scraping_xpath = '/html/body/main/div/div/div/div/div/h3'
iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[3]/div/iframe'

def covid19_scraping(iframe_xpath, scraping_xpath):
    # iframeに入る
    iframe = driver.find_element(by=By.XPATH, value=iframe_xpath)
    driver.switch_to.frame(iframe)
    time.sleep(5)
    # スクレイピングする
    result = driver.find_element(by=By.XPATH, value=scraping_xpath)
    return result.text

print(covid19_scraping(iframe_xpath, scraping_xpath))
# 元のフレームに戻る
driver.switch_to.default_content()
time.sleep(1)