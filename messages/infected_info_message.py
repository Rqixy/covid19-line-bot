from db.infection.print_oneday import oneday_infected_info

from messages.messages import reply_message
from messages.text_on_line import infected_info_on_line


# 1日分のコロナ感染者情報の送信の処理
def oneday_infected_info_message(event, num: int):
    infected_info = oneday_infected_info(num)
    # もし1週間の範囲外の数値が与えられたら範囲外のメッセージを送信する
    if type(infected_info) is str:
        reply_message(event.reply_token, infected_info)
        return

    line_text_new_info = infected_info_on_line(infected_info)
    reply_message(event.reply_token, line_text_new_info)
