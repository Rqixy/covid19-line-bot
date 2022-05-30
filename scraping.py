from asyncore import loop
import string
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# スクレイピング部分
def covid19_scraping(iframe_xpath: string, scraping_xpath: string) -> string:
    # 取得出来るまで繰り返す(無限ループ阻止のため最大20回まで)
    loop = 20
    for i in range(loop):
        # iframeに入る
        iframe = driver.find_element(by=By.XPATH, value=iframe_xpath)
        driver.switch_to.frame(iframe)
        # time.sleep(1)
        # スクレイピングする
        result = driver.find_element(by=By.XPATH, value=scraping_xpath)
        print('result.text : ' + result.text)
        if result.text != '':
            # スクレイピング成功したらTextを返す
            break
    return result.text

# 文字列のから数値型に変換する   # エラーが出た場合、処理が成功するまで繰り返す(無限ループを避けるため、最大10回まで)
def remove_comma_and_text_to_int(text: string) -> int:
    # スクレイピングでうまく取れなかったらNoneを返す
    if text == '':
        return None
    # 中身が空でないなら変換する
    text = text.replace(',','')
    text = int(text)
    print('text : ' + str(text))
    return text

def infected_people_scraping():
    try:
        driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
        # ページが読み込まれるまで待機
        wait.until(EC.presence_of_all_elements_located)

        # 更新チェック用の日付を取得する
        infected_day_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[3]/div/iframe'
        infected_day_xpath = '/html/body/main/div/div/div/div/div/h3/span'
        infected_day = covid19_scraping(infected_day_iframe_xpath, infected_day_xpath)
        infected_day = infected_day + "0:00現在"
        # 元のフレームに戻る
        driver.switch_to.default_content()

        # 新規感染者数
        new_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[1]/iframe'   # 新規感染者のiframe
        new_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        new_people = covid19_scraping(new_iframe_xpath, new_xpath)
        # 数値型に変換する
        new_people = remove_comma_and_text_to_int(new_people)
        # 元のフレームに戻る
        driver.switch_to.default_content()

        # 重症者数
        severe_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[4]/iframe'   # 重症者のiframe
        severe_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        severe_people = covid19_scraping(severe_iframe_xpath, severe_xpath)
        # 数値型に変換する
        severe_people = remove_comma_and_text_to_int(severe_people)
        # 元のフレームに戻る
        driver.switch_to.default_content()

        # 死亡者数
        deaths_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[3]/iframe'   # 死亡者のiframe
        deaths_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        deaths = covid19_scraping(deaths_iframe_xpath, deaths_xpath)
        # 数値型に変換する
        deaths = remove_comma_and_text_to_int(deaths)
        # 元のフレームに戻る
        driver.switch_to.default_content()

        # ドライバーを閉じる
        driver.quit()

        # 1つでも中身が空だったらNoneを送る
        if new_people == None or severe_people == None or deaths == None or infected_day == None:
            return None

        # 配列にスクレイピングしたデータを格納する
        infected_people = [new_people, severe_people, deaths, infected_day]
        print(infected_people)
        return infected_people
    except Exception as e:
        # 情報の取得に失敗したら、コンソールにエラーメッセージ表示とNoneを返す
        print("Error : " + e)
        return None