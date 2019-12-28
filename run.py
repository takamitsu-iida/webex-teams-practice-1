#!/usr/bin/env python
# pylint: disable=missing-docstring

import logging

from bot import Bot

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# create Bot class instance with bot name and webhook name
BOT_NAME = 'bot_1'
WEBHOOK_NAME = "MyWonderfulWebHook"
bot = Bot(bot_name=BOT_NAME, webhook_name=WEBHOOK_NAME)

@bot.on_message('あ')
def respond_to_a(room_id=None):
  return bot.send_message_text(room_id=room_id, text='いうえお')


@bot.on_message("*")
def default_response(room_id=None):
  return bot.send_message_text(room_id=room_id, text="Sorry, could not understand that")


if __name__ == '__main__':
  import server
  server.bot = bot
  server.start_ngrok_and_webhook()
  server.run(use_reloader=True, debug=True)
