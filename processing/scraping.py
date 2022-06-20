from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# WebDriverの設定
def setting_web_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

# 待機時間
def waiting_open_website():
    driver = setting_web_driver()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located)

# 文字列に含まれるカンマを取り除く
def remove_comma(text: str) -> str:
    text = text.replace(',','')
    return text

# 文字列型の数字列を整数型に変換する
def str_to_int(text: str) -> int:
    text = int(text)
    return text

# 配列がちゃんと取得できているかチェック
def check_array(array):
    for check in array:
        if check == None:
            return None
    # うまく取得できたら配列を返す
    return array

# スクレピング部分
def scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> str:
    wait = WebDriverWait(driver, 10)

    # iframeに入る
    iframe = wait.until(lambda x: x.find_element(By.XPATH, iframe_xpath))
    driver.switch_to.frame(iframe)

    # スクレイピングする
    result = wait.until(lambda x: x.find_element(By.XPATH, scraping_xpath))
    result_text = result.text

    # iframeから元のフレームに戻る
    driver.switch_to.default_content()

    return result_text

# 文字列を取得するスクレイピング
def infected_day_scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> str:
    try:
        text = scraping(driver, iframe_xpath, scraping_xpath)
        text += "0:00現在"
        return text
    except Exception as e:
        print("str_scraping error : " + e)
        return None

# 整数を取得するスクレピング
def people_scraping(driver: webdriver, iframe_xpath: str, scraping_xpath: str) -> int:
    try:
        num = scraping(driver, iframe_xpath, scraping_xpath)
        num = remove_comma(num)
        num = str_to_int(num)

        return num
    except Exception as e:
        print("num_scraping error : " + e)
        return None


# 感染者情報をスクレイピングする
def infected_people_scraping():
    try:
        # 更新チェック用の日付のxpath
        infected_day_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[3]/div/iframe'   # 更新日付のiframe
        infected_day_xpath = '/html/body/main/div/div/div/div/div/h3/span'
        # 新規感染者数のxpath
        new_infected_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[1]/iframe'   # 新規感染者のiframe
        new_infected_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        # 重症者数のxpath
        severe_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[4]/iframe'   # 重症者のiframe
        severe_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
        # 死亡者数のxpath
        deaths_iframe_xpath = '/html/body/div[1]/main/div[2]/div/div/div[4]/div[3]/iframe'   # 死亡者のiframe
        deaths_xpath = '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'

        driver = setting_web_driver()
        # 指定したURLに遷移
        driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
        # ページが読み込まれるまで待機
        waiting_open_website()

        # 配列の初期化
        infected_people = []

        infected_day = infected_day_scraping(driver, infected_day_iframe_xpath, infected_day_xpath)
        infected_people.append(infected_day)

        new_infected_people = people_scraping(driver, new_infected_iframe_xpath, new_infected_xpath)
        infected_people.append(new_infected_people)

        severe_people = people_scraping(driver, severe_iframe_xpath, severe_xpath)
        infected_people.append(severe_people)

        deaths = people_scraping(driver, deaths_iframe_xpath, deaths_xpath)
        infected_people.append(deaths)

        # ウィンドウを全て閉じる
        driver.quit()
        
        infected_people = check_array(infected_people)
        return infected_people
    
    # 何かエラーが出てしまった場合はNoneを返す
    except Exception as e:
        print(e)
        return None
