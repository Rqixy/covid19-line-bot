from selenium import webdriver

# WebDriverの設定
def setting_web_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    return driver