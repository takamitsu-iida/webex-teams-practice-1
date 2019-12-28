#!/usr/bin/env python
# pylint: disable=missing-docstring
"""Bot for Webex Teams

- Define decorator for bot
- Show/Create/Delete webhook for Webex Teams

Links:
  - user account: https://developer.webex.com/
  - webhook api: https://developer.webex.com/docs/api/v1/webhooks
"""

import json
import logging
import os
import sys

import requests

logger = logging.getLogger(__name__)

class Bot:

  def __init__(self, bot_name=None, webhook_name=None):

    self.bot_name = bot_name
    self.webhook_name = webhook_name

    self._bot_id = None  # get_bot_id() set this value and returns it

    self.auth_token = self.get_auth_token(bot_name=bot_name)
    if self.auth_token is None:
      sys.exit("failed to get authentication token for {}".format(bot_name))

    self.headers = {
      'Authorization': "Bearer {}".format(self.auth_token),
      'content-type': "application/json"
    }

    # functions with decorator will be stored in this dict object
    self.on_message_functions = {}


  def on_message(self, message_text):
    """on_message decorator

    Arguments:
        message_text {str} -- the message found

    Returns:
        [func] -- decorator function
    """
    def decorator(func):
      self.on_message_functions[message_text] = func
    return decorator


  @staticmethod
  def get_auth_token(bot_name=None):
    """get authentication token by bot name.

    first, try to get token from environment variable,
    then read from file with ~/.{bot name}

    Keyword Arguments:
        bot_name {str} -- name of the bot (default: {None})

    Returns:
        str -- authentication token if found else None
    """

    # 1st get token from environment
    token = os.getenv('{}'.format(bot_name))
    if token:
      return token

    token = os.getenv('bot_token')
    if token:
      return token

    # 2nd get from ~/.bot_name
    file_name = '~/.{}'.format(bot_name)
    file_path = os.path.expanduser(file_name)
    if not os.path.isfile(file_path):
      logger.info('%s is not found', file_name)
      return None
    try:
      with open(file_path, mode='r') as f:
        return f.read().strip()
    except IOError as e:
      logger.exception(e)

    return None


  def get_me(self):
    """get bot info

    {
      "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YTg5NDI0Mi03YjExLTRjNmEtYmZkMi0yNDRlYmI4ZTk5NjM",
      "emails": [
        "iida_bot_1@webex.bot"
      ],
      "phoneNumbers": [],
      "displayName": "bot_1",
      "nickName": "bot_1",
      "avatar": "https://avatar-prod-us-east-2.webexcontent.com/Avtr~V1~f5...
      "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9mNWI0ZDk2Mi1mYzM4LTQzYTMtYWI5MS1hMDY4MzM1NWFiNjY",
      "created": "2019-12-23T04:50:43.279Z",
      "status": "unknown",
      "type": "bot"
    }

    Returns:
        dict -- information about this bot obtained from rest api, or None
    """
    api_path = 'https://api.ciscospark.com/v1/people/me'

    get_result = requests.get(api_path, headers=self.headers)
    if get_result and get_result.ok:
      return get_result.json()
    return None


  def get_bot_id(self):
    if self._bot_id:
      return self._bot_id

    me = self.get_me()
    if not me:
      return None

    self._bot_id = me.get('id')

    return self._bot_id


  def get_message_detail(self, message_id=None):
    api_path = 'https://api.ciscospark.com/v1/messages/{}'.format(message_id)
    get_result = requests.get(api_path, headers=self.headers, verify=False)
    if get_result and get_result.ok:
      return get_result.json()
    return None


  def get_message_text(self, message_id=None):
    json_data = self.get_message_detail(message_id=message_id)
    if json_data is None:
      return None
    return json_data.get('text')


  def send_message_text(self, text=None, room_id=None, to_person_id=None, to_person_email=None):
    """
    send text message to room_id or person_id or person_email
    see, https://developer.webex.com/docs/api/v1/messages/create-a-message
    """
    if not any([room_id, to_person_id, to_person_email]):
      return None

    payload = {
      'text': text
    }

    if room_id is not None:
      payload.update({'roomId': room_id})

    if to_person_id is not None:
      payload.update({'toPersonId': to_person_id})

    if to_person_email is not None:
      payload.update({'toPersonEmail': to_person_email})

    api_path = 'https://api.ciscospark.com/v1/messages/'
    post_result = requests.post(api_path, headers=self.headers, data=json.dumps(payload))

    if post_result and post_result.ok:
      json_data = post_result.json()
      print(json.dumps(json_data, ensure_ascii=False, indent=2))
      return json_data
      # {
      #   "id": "Y2lzY29zcGFyazovL3VzL01FU1NBR0UvNTAwZjQ5NzAtMjk5MC0xMWVhLWEwYzctOWQ5Mzk0MjEzODcw",
      #   "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vNDQ4NWM5ZmUtMDNkYy0zNWVjLTlhZTctNmY4MThiZGM3NGQw",
      #   "toPersonEmail": "takamitsu.iida@gmail.com",
      #   "roomType": "direct",
      #   "text": "はい！",
      #   "personId": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YTg5NDI0Mi03YjExLTRjNmEtYmZkMi0yNDRlYmI4ZTk5NjM",
      #   "personEmail": "iida_bot_1@webex.bot",
      #   "created": "2019-12-28T16:37:18.343Z"
      # }

    return None


  def get_webhooks(self, webhook_name=None):
    name = webhook_name
    if name is None:
      name = self.webhook_name

    api_path = 'https://api.ciscospark.com/v1/webhooks'
    get_result = requests.get(api_path, headers=self.headers)
    data = get_result.json()
    webhooks = data.get('items') if data else []
    if name is None:
      return webhooks
    return list(filter(lambda  x: x.get('name') == name, webhooks))


  def show_webhooks(self, webhook_name=None):
    name = webhook_name
    if name is None:
      name = self.webhook_name
    webhooks = self.get_webhooks(webhook_name=name)
    for w in webhooks:
      print(json.dumps(w, ensure_ascii=False, indent=2))


  def delete_webhook(self, webhook_id=None):
    if not id:
      return False
    api_path = 'https://api.ciscospark.com/v1/webhooks/{}'.format(webhook_id)
    delete_result = requests.delete(api_path, headers=self.headers)
    return delete_result.ok


  def _delete_webhooks_by_name(self, webhook_name):
    webhooks = self.get_webhooks(webhook_name)
    for webhook_id in [w.get('id') for w in webhooks]:
      self.delete_webhook(webhook_id=webhook_id)


  def register_webhook(self, webhook_name=None, target_url=None):
    name = webhook_name
    if name is None:
      name = self.webhook_name

    # delete same name webhooks, if any
    self._delete_webhooks_by_name(webhook_name)

    api_path = "https://api.ciscospark.com/v1/webhooks"

    payload = {
      "resource": "messages",
      "event": "all",
      "targetUrl": target_url,
      "name": name
    }

    post_result = requests.post(api_path, json=payload, headers=self.headers, verify=False)

    if not post_result.ok:
      logger.error('Webhook registration failed!')
      sys.exit(-1)


if __name__ == '__main__':

  import argparse

  logging.basicConfig(level=logging.INFO)

  def test_decorator():
    # pylint: disable=unused-variable

    bot = Bot()

    @bot.on_message('hi')
    def on_message_hi(room_id=None):
      print('My room_id is {}'.format(room_id))

    @bot.on_message('*')
    def on_message_default(room_id=None):
      print(room_id)

    # Python起動時にデコレータが付与されている関数は回収されて辞書型に格納される
    # 上の２つの関数は辞書型に格納されているはず
    print(bot.on_message_functions.keys())

    # その辞書型を使えば任意のタイミングでデコレータの付いた関数を実行できる
    message = 'hi'
    if message in bot.on_message_functions:
      func = bot.on_message_functions.get('hi')
      func(room_id="1")
    return 0

  def test_send():
    bot = Bot(bot_name='bot_1')
    bot.send_message_text(text='はい！', to_person_email='takamitsu.iida@gmail.com')

  def main():
    parser = argparse.ArgumentParser(description='webex teams bot related operations.')
    parser.add_argument('bot_name', help='name of the bot')
    parser.add_argument('-d', '--delete', action='store_true', default=False, help='Delete all webhooks')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='List all webhooks')
    args = parser.parse_args()

    bot = Bot(bot_name=args.bot_name)

    if args.list:
      bot.show_webhooks()
      return 0

    if args.delete:
      webhooks = bot.get_webhooks()
      for webhook_id in [w.get('id') for w in webhooks]:
        result = bot.delete_webhook(webhook_id=webhook_id)
        print('{} : {}'.format(webhook_id, str(result)))
      return 0

    me = bot.get_me()
    print(json.dumps(me, ensure_ascii=False, indent=2))

    return 0

  # sys.exit(test_send())
  sys.exit(main())
