from selenium import webdriver

# WebDriverの設定
def setting_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    return driver