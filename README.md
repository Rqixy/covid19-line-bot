# LineBotの概要
***

毎日午後1時に最新の感染者情報が自動送信されるLineBotです。

チャットから最新情報と3日前までと一週間の感染情報が確認出来ます。

開発言語は、**Python PostgreSQL**
フレームワークは、**Flask**
クラウドは、**Heroku**を利用しています。

感染情報は[厚生労働省](https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html "covid-19 kokunainohasseijoukyou")こちらからスクレイピングして取ってきております。
スクレイピングは毎日午後1時と、再送信用に午後6時の2回のみ行うようにし、Lineから最新情報を取ってくる時は保存したデータベースから取ってくるようにすることで、サイトに負荷を掛けないようにしました。  

スクレピングしているので、サイトからの取得が出来なくなったら、サービス終了とします。

こちらがLineBotのQRコードになります。良かったら使ってみてください。
![LineBot](https://raw.githubusercontent.com/Rqixy/covid19-line-bot/master/covid19-linebot-QRimage.jpg "Covid-19LineBot")

# 環境構築

## Lineの新規チャネルを作成する

[LINE Developers](https://developers.line.biz/ja/)に移動し、ログインしてください。

[コンソール（ホーム）](https://developers.line.biz/console/)に移動し、Adminの自分のアカウント名を選択してください。
チャネル設定から、**新規チャネル**作成を選択し、**Messaging API**を選択してください。

### 新規チャネル作成
|設定|記入内容|
|:--|:--|
|**チャネルの種類**|Messaging API|
|**プロバイダー**|自分のプロバイダー名(ex: 佐藤)|
|**会社・事業者の所在国・地域** |日本|
|**チャネルアイコン**|好きなアイコン(任意)|
|**チャネル名**|動作にあったチャネル名(ex: コロナ感染者Bot)|
|**チャネル説明**|チャネルの動作を説明する(ex: 感染情報を自動送信するBotです)|
|**大業種**|個人|
|**小業種**|自分の情報(ex: 個人（学生）)|
|**メールアドレス**|使用できるメールアドレス(ex: test@test.com)|
|**プライバシーポリシーURL**|(任意)|
|**サービス利用規約URL**|(任意)|

上記を記入し、利用規約に同意して作成します。
***
![](https://user-images.githubusercontent.com/67447178/185031147-8c080895-f018-4631-9857-4cfaa8c745f8.png)
上記のようなページが表示されていたら完成です。

作成に成功したら、チャネル基本設定とMessaging API設定を見ていきます。
### チャネル基本設定
このページの下の方にあるチャネルシークレットを発行し、メモしておきます。(Herokuの環境変数に保存するために使用します。)
![](https://user-images.githubusercontent.com/67447178/185031353-65e10557-a3ce-46ae-89df-07fabb31e7a1.png)
(画像内のチャネルシークレットは再発行済みです。)


### Messaging API設定
このページでは、LINE公式アカウント機能、チャネルアクセストークンの設定をします。(Webhook設定はHerokuの設定完了後に設定します。)

#### LINE公式アカウント機能

![スクリーンショット 2022-08-17 13 20 40](https://user-images.githubusercontent.com/67447178/185034036-42cde2a2-3344-4460-bbac-358e4a1d0094.png)

応答メッセージの右側の編集をクリックし、応答設定ページに移動します。

![スクリーンショット 2022-08-17 13 21 10](https://user-images.githubusercontent.com/67447178/185034256-56c2105b-958c-46c1-beee-7382ab0f700a.png)

- **基本設定**
  - 応答モード
    -  Bot
  - あいさつメッセージ
    - オフ

- **詳細設定**
  - 応答メッセージ
    - オフ
  - Webhook
    - オン

このように設定しておきます。

#### チャネルアクセストークン

チャネルシークレット同様に発行して、メモしておきます。

***

## ディレクトリのダウンロード
任意のディレクトリに移動したら、下記のコマンドを入力してダウンロードして、移動しておきます。
```
git clone https://github.com/Rqixy/covid19-line-bot.git
cd covid19-line-bot
```

***

## Herokuの設定

前提として、Herokuのアカウントを作成とスケジューラーを使用するため、クレジットカード登録をしておきます。

Windowsの方は、こちらのリンクからHeroku CLIのインストーラーをダウンロードします。
[Heroku CLIのダウンロードリンク](https://devcenter.heroku.com/ja/articles/heroku-cli)

Macの方は、下記のコマンドでインストールします。
```
​brew tap heroku/brew && brew install heroku
```

インストールが完了したらTerminal上でログインします。

```
heroku login
```

### アプリ作成
アプリを作成していきます。
```
git init
heroku apps:create 他と被らない名前(ex: rqixy-covid19bot)
git add .
git commit -m "make it better"
git push heroku master
```
(今後の説明において、**rqixy-covid19bot**というアプリ名を使用していきます。)

### スケジューラー作成
スリープ対策と午後1時と午後6時に送信するためのスケジューラーを設定していきます。

```
heroku addons:create scheduler:standard
```

作成できたら、[Herokuダッシュボードページ](https://dashboard.heroku.com/apps)に移動し、作成したアプリを選択します。

アプリのページから、**Heroku Scheduler**を選択します。

移動できたら、**Create job**を選択し、スリープ対策コマンドを追加します。

- **Schedule**
  - Every 10 minutes
- **Run Command**
  - curl https://rqixy-covid19bot.herokuapp.com/

追加できたら、**Add job**から午後1時と午後6時に自動送信するコマンドを追加します。
- **午後1時**
  - **Schedule**
    - Every day at...
    - 04:00AM
  - **Run Command**
    - python auto_send.py

- **午後6時**
  - **Schedule**
    - Every day at...
    - 09:00AM
  - **Run Command**
    - python auto_resend.py

### DB作成
このbotでは、PostgreSQLを使用しているので、Herokuに追加していきます。

まず、HerokuにPostgreSQLを追加します。
```
heroku addons:create heroku-postgresql:hobby-dev --app rqixy-covid19bot
```

追加できたら、[Herokuダッシュボードページ](https://dashboard.heroku.com/apps)に移動し、作成したアプリを選択します。

アプリのページから、**Heroku Postgres**を選択します。

Settingページに移動し、View Credentialsを選択します。
![](https://user-images.githubusercontent.com/67447178/185060285-de755b63-7049-4b7c-8e4c-32a431fd3964.png)

Heroku CLIのコマンドをコピーし、Terminalに貼り付け、DB内に入ります。
```
heroku pg:psql postgresql-rectangular-77122 --app rqixy-covid19bot
```

#### テーブル作成
感染情報を保存する**infected_info**テーブルとユーザーIDを保存する**users_id**テーブルを作成します。

infected_infoテーブル作成
```
rqixy-covid19bot::DATABASE=> create table infected_info (id SERIAL NOT NULL PRIMARY KEY, infected_day VARCHAR(255) NOT NULL, new_infected_people int NOT NULL, severe_people int NOT NULL, deaths int NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

users_idテーブル作成
```
rqixy-covid19bot::DATABASE=> create table users_id(id SERIAL NOT NULL PRIMARY KEY, user_id VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

仮の感染情報データを入れる
```
rqixy-covid19bot::DATABASE=> INSERT INTO infected_info (infected_day, new_infected_people, severe_people, deaths) VALUES ('令和4年8月10日0:00現在', 100000, 100, 10000),('令和4年8月11日0:00現在', 111111, 111, 11111),('令和4年8月12日0:00現在', 222222, 222, 22222),('令和4年8月13日0:00現在', 333333, 333, 33333),('令和4年8月14日0:00現在', 444444, 444, 44444),('令和4年8月15日0:00現在', 555555, 555, 55555),('令和4年8月16日0:00現在', 666666, 666, 66666);
```

### 環境変数の設定

Heroku上に環境変数として、**DATABASE_URL、LINE_CHANNEL_SECRET、LINE_CHANNEL_ACCESS_TOKEN**
の3つ登録します。

Terminal上で設定していきます。

環境変数の確認
```
heroku config
```
この時点で、DATABASE_URLは設定いるかと思われます。

設定されてない場合、Heroku PostgresのSettingページのView Credentialsから、URIをコピーしてきます。

コピーしてきたURIを**DATABASE_URL**という変数名で設定します。
```
heroku config:set DATABASE_URL=コピーしてきたURI
```

LINEのチャネル作成時にメモしておいた、**チャネルシークレットをLINE_CHANNEL_SECRET**、**チャネルアクセストークンをLINE_CHANNEL_ACCESS_TOKEN**という変数名で設定します。

```
heroku config:set LINE_CHANNEL_SECRET=メモしたチャネルシークレット
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=メモしたチャネルアクセストークン
```

***

## 最後に

また、[LINE Developers](https://developers.line.biz/ja/)に移動し、Webhookの設定をします。
#### Webhook設定
Webhook URLにURLを入力し、Webhookの利用をオンにしてください。
![](https://user-images.githubusercontent.com/67447178/185094354-52fbc7a1-a7b6-4bab-afee-14951324f69a.png)

その後、検証を押し、成功と表示されたら完成です。
![](https://user-images.githubusercontent.com/67447178/185094684-3fc86760-08b5-4617-b3c5-5c2b7dc4ff9b.png)

