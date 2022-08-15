from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraping.config import setting_web_driver
from scraping.people import people_scraping
from scraping.infected_day import infected_day_scraping
from scraping.check.get_info import get_info

# 取得したい情報の要素までのxpathを連想配列に格納する
# 取得したい情報がiframeを使用して表示されているのでirame内に入るためのxpathも用意しておく

# 感染日のxpath
infected_day_xpaths = {
    'iframe': '/html/body/div[1]/main/div[2]/div/div/div[3]/div/iframe',
    'xpath': '/html/body/main/div/div/div/div/div/h3/span'
}
# 新規感染者数のxpath
new_infected_xpaths = {
    'iframe': '/html/body/div[1]/main/div[2]/div/div/div[4]/div[1]/iframe',
    'xpath': '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
}
# 重症者数のxpath
severe_xpaths = {
    'iframe': '/html/body/div[1]/main/div[2]/div/div/div[4]/div[4]/iframe',
    'xpath': '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
}
# 死亡者数のxpath
deaths_xpaths = {
    'iframe': '/html/body/div[1]/main/div[2]/div/div/div[4]/div[3]/iframe',
    'xpath': '/html/body/main/div/div/div[3]/div[1]/p[2]/span[1]'
}

# 感染者情報をスクレイピングする
def infected_people_scraping() -> (list | None):
    try:
        # WebDriverの設定
        driver = config.setting_web_driver()
        # 指定したURLに遷移
        driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
        # ページが読み込まれるまで待機
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located)

        infected_info = []

        infected_day = ID.infected_day_scraping(driver, infected_day_xpaths)
        infected_info.append(infected_day)
        
        new_infected_people = PP.people_scraping(driver, new_infected_xpaths)
        infected_info.append(new_infected_people)
        
        severe_people = PP.people_scraping(driver, severe_xpaths)
        infected_info.append(severe_people)
        
        deaths = PP.people_scraping(driver, deaths_xpaths)
        infected_info.append(deaths)
        
        # ウィンドウを全て閉じる
        driver.quit()
        
        # 一つでも情報が取得出来ていなかったら、Noneを返す
        if not GI.get_info(infected_info):
            return None

        return infected_info
    
    # 何かエラーが出てしまった場合はNoneを返す
    except Exception as e:
        print(e)
        return None