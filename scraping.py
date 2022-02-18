import time
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
    # iframeに入る
    iframe = driver.find_element_by_xpath(iframe_xpath)
    driver.switch_to.frame(iframe)

    wait.until(EC.visibility_of_element_located((By.XPATH, scraping_xpath)))

    # スクレイピングする
    result = driver.find_element_by_xpath(scraping_xpath)

    return result

def infected_people_scraping():
    driver.get('https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html')
    # ページが読み込まれるまで待機
    wait.until(EC.presence_of_all_elements_located)

    #合計感染者数   上手くスクレイピングでき次第復活！
    # total_infected_people_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[3]/div/iframe'   # 新規感染者のiframe
    # total_infected_people_xpath = '//*[@id="currentSituationTb"]/tbody/tr[1]/td[2]'
    # result = covid19_scraping(total_infected_people_iframe_xpath, total_infected_people_xpath)
    # print("新規感染者の数：" + result.text + "人")
    # # 元のフレームに戻る
    # driver.switch_to.default_content()
    # time.sleep(1)


    #新規感染者数
    new_infected_people_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[1]/iframe'   # 新規感染者のiframe
    new_infected_people_xpath = '//*[@id="newInfectedKPI"]'
    new_infected_people_result = covid19_scraping(new_infected_people_iframe_xpath, new_infected_people_xpath).text

    #数値型に変換する
    new_infected_people_result = new_infected_people_result.replace(',','')
    new_infected_people_result = int(new_infected_people_result)
    # print("新規感染者の数：" + str(new_infected_people_result) + "人")

    # 元のフレームに戻る
    driver.switch_to.default_content()
    time.sleep(1)


    #重症者数
    total_severe_people_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[4]/iframe'   # 　重症者のiframe
    total_severe_people_xpath = '//*[@id="GrPh14SevereKPI"]'
    total_severe_people_result = covid19_scraping(total_severe_people_iframe_xpath, total_severe_people_xpath).text

    #数値型に変換する
    total_severe_people_result = total_severe_people_result.replace(',','')
    total_severe_people_result = int(total_severe_people_result)
    # print("重症者の数の合計：" + str(total_severe_people_result) + "人")

    # 元のフレームに戻る
    driver.switch_to.default_content()
    time.sleep(1)


    #死亡者数
    total_number_of_deaths_iframe_xpath = '//*[@id="content"]/div[2]/div/div/div[4]/div[3]/iframe'   # 死亡者のiframe
    total_number_of_deaths_xpath = '//*[@id="GrPh13TotalDeadKPI"]'
    total_number_of_deaths_result = covid19_scraping(total_number_of_deaths_iframe_xpath, total_number_of_deaths_xpath).text

    #数値型に変換する
    total_number_of_deaths_result = total_number_of_deaths_result.replace(',','')
    total_number_of_deaths_result = int(total_number_of_deaths_result)
    # print("死亡者の数の合計：" + str(total_number_of_deaths_result) + "人")
    
    # 元のフレームに戻る
    driver.switch_to.default_content()
    time.sleep(1)

    driver.quit()

    infected_people_array = [new_infected_people_result, total_severe_people_result, total_number_of_deaths_result]
    
    return infected_people_array

# print(infected_people_scraping())