from db.infection.print_day import print_infected_day
from messages.quick_reply import quick_reply_for_reply

# 1日分のコロナ感染者情報の送信の処理
def infected_info_reply(event: any, day: int):
    infected_info = print_infected_day(day)
    # もし1週間の範囲外の数値が与えられたら範囲外のメッセージを送信する
    if type(infected_info) is str:
        quick_reply_for_reply(event.reply_token, text=infected_info)
        return
    line_text_new_data = infected_info[0] + "\n" + infected_info[1] + "\n" + infected_info[2] + "\n" + infected_info[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    quick_reply_for_reply(event.reply_token, text=line_text_new_data)