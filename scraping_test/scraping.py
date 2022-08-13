from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# スクレピング実行部分
def scraping(driver: webdriver, xpaths: dict) -> str:
    scraped_text = ''

    # 取得したい要素が非同期で表示されるため、取得できないことがある。
    # そのため、取得できなかった時はページを更新し再度取得できるか試す。(ただし、無限ループを避けるため、10回までの制限をかけておく)
    for i in range(10):
        time.sleep(2)   # 明示的にページの読み込みを待機する

        # iframeに入る
        iframe_element = driver.find_element(By.XPATH, xpaths['iframe'])
        driver.switch_to.frame(iframe_element)
        time.sleep(2)   # 明示的にページの読み込みを待機する

        element = driver.find_element(By.XPATH, xpaths['xpath'])
        scraped_text = element.text

        # iframeから元のフレームに戻る
        driver.switch_to.default_content()

        # 取得できたらループを抜ける
        if scraped_text != '':
            break

        # Webページを更新する
        driver.refresh()

    return scraped_text