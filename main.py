import scraping

# スクレイピングし、結果を配列で取得する
array = scraping.infected_people_scraping()
print(array)

# 配列で受け取った結果をDBに保存する
# 7個まで保存し8個目が登録されたとき、古い情報を削除する

# LineBot作成
# Lineの自動送信で最新のスクレイピング結果と前日との人数差の結果とスクレイピングしているサイトのURLを送信する
# Lineで「昨日の感染状況」と送ると前日の結果を表示する
# Lineで「1週間の感染状況」と送ると1週間分の結果と1週間分の新規感染者数、重症者数、死亡者数の平均を表示する