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

### APIを使ってbotに関する情報を取得する

トークンさえあればAPIを使ってbotの情報を取れる。

こんな感じのスクリプトを保存しておく。ここではme.pyで保存。

```python
#!/usr/bin/env python
# pylint: disable=missing-docstring
"""
get bot info by token
"""

import argparse
import json
import logging
import sys

logger = logging.getLogger(__name__)

try:
  import requests
  requests.packages.urllib3.disable_warnings()
except ImportError as e:
  logger.exception('failed to import requests: %s', e)
  sys.exit(-1)


if __name__ == '__main__':

  logging.basicConfig(level=logging.INFO)

  def get_me(token):
    api_path = 'https://api.ciscospark.com/v1/people/me'
    header = {
      'Authorization': "Bearer {}".format(token),
      'content-type': "application/json"
    }

    get_result = requests.get(api_path, headers=header)
    if get_result and get_result.ok:
      return get_result.json()
    return None


  def main():
    parser = argparse.ArgumentParser(description='show account info from bot token.')
    parser.add_argument('-i', '--inline', type=argparse.FileType('r'), default=sys.stdin, help='bot token file')
    args = parser.parse_args(args=sys.argv[1:])

    with args.inline as f:
      token = f.read()
      token = token.strip()

    me = get_me(token)
    print(json.dumps(me, ensure_ascii=False, indent=2))

    return 0

  sys.exit(main())
```

これを実行すると、

```bash
iida-macbook-pro:webex-teams-practice-1 iida$ ./me.py -i ~/.bot_1
```

このような結果（↓）が得られる。

```json
{
  "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YTg5NDI0Mi03YjExLTRjNmEtYmZkMi0yNDRlYmI4ZTk5NjM",
  "emails": [
    "iida_bot_1@webex.bot"
  ],
  "phoneNumbers": [],
  "displayName": "bot_1",
  "nickName": "bot_1",
  "avatar": "https://avatar-prod-us-east-2.webexcontent.com/Avtr~V1~f5b4d962-fc38-43a3-ab91-a0683355ab66/V1~9a894242-7b11-4c6a-bfd2-244ebb8e9963~2b1e7ca7414146e8b56081398db3fa2d~80",
  "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mNWI0ZDk2Mi1mYzM4LTQzYTMtYWI5MS1hMDY4MzM1NWFiNjY",
  "created": "2019-12-23T04:50:43.279Z",
  "status": "unknown",
  "type": "bot"
}
```

## botを招待する

招待するときはメールアドレスを使うので、Teamsのアプリで iida_bot_1@webex.bot を招待する。

## 簡単なアプリで試す

ファイル構造

```bash
.
├── LICENSE
├── README.md
├── bot.py
├── me.py
├── ngrok.py
├── run.py
├── server.py
└── vscode.code-workspace
```

### botの情報を取得する

`bot.py [bot名]`

```bash
webex-teams-practice-1 iida$ ./bot.py bot_1
{
  "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YTg5NDI0Mi03YjExLTRjNmEtYmZkMi0yNDRlYmI4ZTk5NjM",
  "emails": [
    "iida_bot_1@webex.bot"
  ],
  "phoneNumbers": [],
  "displayName": "bot_1",
  "nickName": "bot_1",
  "avatar": "https://avatar-prod-u...
  "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mNWI0ZDk2Mi1mYzM4LTQzYTMtYWI5MS1hMDY4MzM1NWFiNjY",
  "created": "2019-12-23T04:50:43.279Z",
  "status": "unknown",
  "type": "bot"
}
```

### webhookの一覧を取得する

`bot.py [bot名] --list`

```bash
webex-teams-practice-1 iida$ ./bot.py bot_1 -l
{
  "id": "Y2lzY29zcGFyazovL3VzL1dFQkhPT0svMTI4MWNjNGYtZWVkMi00MDlhLWE1MDktNTEyOWZmNzI5OGJl",
  "name": "MyWonderfulWebHook",
  "targetUrl": "https://cc1df7bf.ngrok.io",
  "resource": "messages",
  "event": "all",
  "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mNWI0ZDk2Mi1mYzM4LTQzYTMtYWI5MS1hMDY4MzM1NWFiNjY",
  "createdBy": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YTg5NDI0Mi03YjExLTRjNmEtYmZkMi0yNDRlYmI4ZTk5NjM",
  "appId": "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL0MzMmM4MDc3NDBjNmU3ZGYxMWRhZjE2ZjIyOGRmNjI4YmJjYTQ5YmE1MmZlY2JiMmM3ZDUxNWNiNGEwY2M5MWFh",
  "ownedBy": "creator",
  "status": "active",
  "created": "2019-12-28T17:02:03.873Z"
}
```

### webhookを削除する

`bot.py [bot名] --delete`

```bash
(base) iida-macbook-pro:webex-teams-practice-1 iida$ ./bot.py bot_1 -d
Y2lzY29zcGFyazovL3VzL1dFQkhPT0svMTI4MWNjNGYtZWVkMi00MDlhLWE1MDktNTEyOWZmNzI5OGJl : True
```

### ngrokを起動する

`ngrok.py --start`

```bash
webex-teams-practice-1 iida$ ./ngrok.py -s
INFO:__main__:start ngrok
INFO:__main__:ngrok is running successfuly
ngrok is running with public url: https://7edbcd78.ngrok.io

:webex-teams-practice-1 iida$ ps ax | grep ngrok
39891 s002  S      0:00.23 ngrok http 5000 -log=stdout
39899 s002  S+     0:00.00 grep ngrok
:webex-teams-practice-1 iida$
```

### ngrokのプロセスを停止する

開発中はngrokのプロセスが残りっぱなしになりがち。
pythonスクリプトの中で停止する必要もあるのでラップしておく。

`ngrok.py --stop`

```bash
webex-teams-practice-1 iida$ ps ax | grep ngrok
39953 s002  S      0:00.23 ngrok http 5000 -log=stdout
39961 s002  S+     0:00.00 grep ngrok

webex-teams-practice-1 iida$ ./ngrok.py -k
webex-teams-practice-1 iida$ ps ax | grep ngrok
39971 s002  S+     0:00.00 grep ngrok
webex-teams-practice-1 iida$
```

### botを走らせる

`run.py` で走り出す。

## 参考文献

開発者向けのページ。
Bot用のアカウントを作ったり、APIのマニュアルを参照したり、何をするにしてもここがスタート地点。

<https://developer.webex.com/>

WebhookのAPIマニュアル

<https://developer.webex.com/docs/api/guides/webhooks>

Pythonでのwebhookの例

<https://community.cisco.com/t5/collaboration-documents/a-simple-webex-teams-webhook-in-python/ta-p/3691304>

<https://community.cisco.com/t5/collaboration-documents/a-simple-webex-teams-webhook-in-python/ta-p/3691304>
