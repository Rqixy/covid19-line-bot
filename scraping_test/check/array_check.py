# 配列の取得チェック

def array_check(array) -> bool:
    for check in array:
        if check == None:
            return False
            
    return True