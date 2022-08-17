# Lineで表示する感染情報のテキスト作成

def infected_info_on_line(infected_info) -> str:
    line_text = infected_info[0] + "\n" + infected_info[1] + "\n" + infected_info[2] + "\n" + infected_info[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    return line_text