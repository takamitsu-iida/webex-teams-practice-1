#!/usr/bin/env python
# pylint: disable=missing-docstring

import logging
import os
import sys

from flask import Flask, request

# import local library
from ngrok import Ngrok

logger = logging.getLogger(__name__)

# the bot object MUST be attached before app.run()
bot = None

# http port
PORT = 5000

# flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():

  # get the json data from request
  json_data = request.get_json()
  data = json_data.get('data')

  # import json
  # print(json.dumps(data, ensure_ascii=False, indent=2))
  # this is something like this
  # {
  #   "id": "Y2lzY29zcGFyazovL3VzL01FU1NBR0UvM2YxMDk5ZjAtMjk3MC0xMWVhLWIwNzktYjk5NDQzYThkODJj",
  #   "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vNDQ4NWM5ZmUtMDNkYy0zNWVjLTlhZTctNmY4MThiZGM3NGQw",
  #   "roomType": "direct",
  #   "personId": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80MjgyYjBmNC03NGMxLTRjMTctYmZhYS1jYWM4ZTU4MGY1MDE",
  #   "personEmail": "takamitsu.iida@gmail.com",
  #   "created": "2019-12-28T12:47:45.935Z"
  # }

  message_id = data.get('id')
  room_id = data.get('roomId')
  person_id = data.get('personId')
  # email = data.get('personEmail')

  if person_id == bot.get_bot_id():
    return "this message is my own ... ignoring it"

  # retreive the message contents
  message = bot.get_message_text(message_id=message_id)
  if message is None:
    return 'failed to retreive message: {}'.format(message_id)

  # debug
  print(message)
  print('*'*10)

  if message.strip() != '' and message in bot.on_message_functions:
    func = bot.on_message_functions.get(message)
    func(room_id=room_id)

  elif message.strip() != '' and message not in bot.on_message_functions:
    func = bot.on_message_functions.get('*')
    func(room_id=room_id)

  return "successfully responded"


def start_ngrok_and_webhook():
  # solution to avoid multiple initialization
  # see, https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode
  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logger.info("skip initialization")
  else:
    logger.info("initialize first time")

    # create Ngrok class instance
    ngrok = Ngrok(port=PORT)

    # run ngrok background
    ngrok_result = ngrok.run_background()
    if ngrok_result is False:
      logger.error("failed to run ngrok")
      sys.exit(-1)

    # get public_url opened by ngrok
    public_url = ngrok.get_public_url()

    # register webhook with the public url
    bot.register_webhook(target_url=public_url)


def run(port=None, use_reloader=False, debug=False):
  if port is None:
    port = PORT
  app.run(host='127.0.0.1', port=port, use_reloader=use_reloader, debug=debug)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=PORT, use_reloader=True, debug=True)
