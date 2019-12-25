<!-- markdownlint-disable MD001 -->

# Cisco Webex Teamsの練習・その１

Cisco Webex Teamsを操作する練習です。
いろんなところにある情報をメモしておきます。

## ボットのアカウントを作成する

開発者用のページに行く。

[Webex for Developers](<https://developer.webex.com/>)

メニューから、

"My Webex Teams Apps"

を選択する。

#### Bot Name

> Name of your bot in 100 characters or less.

ボットを識別する名前。ここでは `bot_1` にする。

Teamの画面上にはこれが表示される。

#### Bot Username

> The username users will use to add your bot to a space. Cannot be changed later.

後から変更できない、と書いてある。
他の人からみたときにスペースに招待するときの名前。@webex.botが後ろにつく。

ここでは `iida_bot_1` @webex.botにする。

#### Icon

> Upload your own or select from our defaults. Must be 512x512px in JPEG or PNG format.

デフォルトで用意されている画像か、自分でアップロードするか。アップロードするなら512x512pxでなければならない。

#### Description

> Provide some details about what your bot does,
> how it benefits users, and how an end user can get started in 1000 characters or less.
> Bullets and links Markdown supported.
> If your app is listed on the Webex App Hub,
> this field will be used as the listing’s description.

Webex App Hubに登録するならちゃんと書いたほうが良さそう。

Add Botボタンを押すとBot用のアカウントが生成される。

#### Bot's Access Token

> Non-expiring (good for 100 years) access token for your bot.

このトークンはブラウザを閉じてしまうと二度と表示されないので、この時点でコピーして保存しなければならない。
`~/.bot_1` あたりに保存しておく。

Teamsのアプリで iida_bot_1@webex.bot を招待する。

## Pythonで試す

<https://github.com/Paul-weqe/python_webex_bot>

```bash
iida-macbook-pro:~ iida$ pip install python_webex_bot
```

ngrokでローカルのポートを公開する。

```bash
ngrok http 5000
```

## 参考文献

WebhookのAPIマニュアル

<https://developer.webex.com/docs/api/guides/webhooks>

Pythonでのwebhookの例

<https://community.cisco.com/t5/collaboration-documents/a-simple-webex-teams-webhook-in-python/ta-p/3691304>
