from db.infection.oneday_infected_info import oneday_infected_info
from db.infection.oneweek_infected_info import oneweek_infected_info

from messages.messages import reply_message
from messages.text_on_line import infected_info_on_line


# 1日分のコロナ感染者情報の送信の処理
def reply_oneday_infected_info(event, num: int):
    infected_info = oneday_infected_info(num)
    # もし1週間の範囲外の数値が与えられたら範囲外のメッセージを送信する
    if type(infected_info) is str:
        reply_message(event.reply_token, infected_info)
        return

    line_text_new_info = infected_info_on_line(infected_info)
    reply_message(event.reply_token, line_text_new_info)

# 1週間分のコロナ感染者情報の送信の処理
def reply_oneweek_infected_info(event):
    oneweek_infected_info_array = oneweek_infected_info()
    line_text_week_info = oneweek_infected_info_array[0] + oneweek_infected_info_array[1] + oneweek_infected_info_array[2] + oneweek_infected_info_array[3] + oneweek_infected_info_array[4] + oneweek_infected_info_array[5] + oneweek_infected_info_array[6] + "\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    reply_message(event.reply_token, text=line_text_week_info)