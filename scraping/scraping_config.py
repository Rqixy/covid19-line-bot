from selenium import webdriver

# WebDriverの設定
def setting_web_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    return driver

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