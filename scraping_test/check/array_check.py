# 配列の取得チェック

def array_check(array):
    for check in array:
        if check == None:
            return None
    # うまく取得できたら配列を返す
    return array