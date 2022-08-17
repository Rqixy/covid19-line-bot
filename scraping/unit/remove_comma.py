# 文字列に含まれるカンマを取り除く
def remove_comma(text: str) -> str:
    text = text.replace(',','')
    return text