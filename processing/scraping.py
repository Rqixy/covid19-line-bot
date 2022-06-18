import re
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# WebDriverの設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# 待機時間
def sleeping():
    wait.until(EC.presence_of_all_elements_located)

# 文字列のから数値型に変換する
def remove_comma_and_text_to_int(text: string) -> int:
    # スクレイピングでうまく取れなかったらNoneを返す
    if text == '':
        return None
    # 中身が空でないなら変換する
    text = text.replace(',','')
    text = int(text)
    return text

# スクレイピング部分
def covid19_scraping(iframe_xpath: string, scraping_xpath: string) -> any:
    try:
        # 戻り値のテキスト初期化
        text = ''
        # 取得出来るまで繰り返す(無限ループ阻止のため最大20回まで)
        for i in range(20):
            sleeping()
            # iframeに入る
            iframe = wait.until(lambda x: x.find_element(By.XPATH, iframe_xpath))
            driver.switch_to.frame(iframe)
            sleeping()
            # スクレイピングする
            result = wait.until(lambda x: x.find_element(By.XPATH, scraping_xpath))
            if result.text != '':
                # 文字列型の数字が送られた場合数値型に変換する
                if re.compile('^[0-9,]+$').search(result.text):
                    text = remove_comma_and_text_to_int(result.text)
                else:
                    text = result.text + "0:00現在"
                break
        # iframeから元のフレームに戻る
        driver.switch_to.default_content()
        return text
    except Exception as e:
        print(e)
        return None

# 感染者情報をスクレイピングする
def infected_people_scraping():
    try:
        # 更新チェック用の日付のxpath
        infected_day_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[3]/div/iframe'   # 更新日付のiframe
        infected_day_xpath = '/html/body/main/div/div/div/div/div/h3/span'
        # 新規感染者数のxpath
        new_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[1]/iframe'   # 新規感染者のiframe
        new_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        # 重症者数のxpath
        severe_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[4]/iframe'   # 重症者のiframe
        severe_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        # 死亡者数のxpath
        deaths_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[3]/iframe'   # 死亡者のiframe
        deaths_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'

        # 各xpathを二次元配列に格納する
        xpaths = [
            [   # 更新チェック用の日付
                infected_day_iframe_xpath,
                infected_day_xpath
            ],
            [   # 新規感染者数
                new_iframe_xpath,
                new_xpath
            ],
            [   # 重症者数
                severe_iframe_xpath,
                severe_xpath
            ],
            [   # 死亡者数
                deaths_iframe_xpath,
                deaths_xpath
            ]
        ]


        # 指定したURLに遷移
        driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
        # ページが読み込まれるまで待機
        sleeping()

        # 配列の初期化
        infected_people = []

        # xpathを配列から取得してスクレピングし、
        # 新規感染者数配列に結果を格納する
        for xpath in xpaths:
            result = covid19_scraping(xpath[0], xpath[1])
            infected_people.append(result)

        # ウィンドウを全て閉じる
        driver.quit()

        # スクレイピングでうまく情報が受け取ることができず
        # NoneがあったらNoneを返す
        for check in infected_people:
            if check == None:
                return None
        # うまく取得できたら配列を返す
        return infected_people
    
    # 何かエラーが出てしまった場合はNoneを返す
    except Exception as e:
        print(e)
        return None