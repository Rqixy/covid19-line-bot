# 要素の取得チェック
def check_get_info(info_array) -> bool:
    for info in info_array:
        if info == None:
            return False
            
    return True