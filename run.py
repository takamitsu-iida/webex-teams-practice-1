#!/usr/bin/env python
# pylint: disable=missing-docstring

from __future__ import print_function  # Needed if you want to have console output using Flask

import json
import sys
import os
import time

import requests
from flask import Flask, request

token = 'Enter your bot access_token here !'
with open('~/.bot_1', mode='r') as f:
  TOKEN = f.read().strip()

def get_header():
  return {
    'Authorization': "Bearer {}".format(TOKEN)
  }

app = Flask(__name__)

@app.route("/", methods=['POST'])  # all request for localhost:5000/  will reach this method
def webhook():

  # Get the json data
  j = request.json

  # Retrieving message ID, person ID, email and room ID from message received

  message_id = j["data"]["id"]
  user_id = j["data"]["personId"]
  email = j["data"]["personEmail"]
  room_id = j["data"]["roomId"]

  print(message_id, file=sys.stdout)
  print(user_id, file=sys.stdout)
  print(email, file=sys.stdout)
  print(room_id, file=sys.stdout)

  if user_id != 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS85M2ViYTZlMi01ZDk2LTRhMmUtYjEyNy1hNzA5YWJjY2NlMDM':

    # Loading the message with the message ID

    get_rooms_url = "https://api.ciscospark.com/v1/messages/" + message_id
    get_response = requests.get(get_rooms_url, headers=get_header(), verify=False)
    response_json = get_response.json()
    message = response_json["text"]
    print(message, file=sys.stdout)

    print('******************', file=sys.stdout)

    # You can do whatever you want with the message,person_id,room_id over here !

    return "Success!"

  else:

    return "It's my own messages ... ignoring it"


os.popen("pkill ngrok")  # clearing previous sessions of ngrok (if any)

os.popen("ngrok http 5000 &")  # Opening Ngrok in background

time.sleep(5)  #Leaving some time to Ngrok to open

term_output_json = os.popen('curl http://127.0.0.1:4040/api/tunnels').read()  # Getting public URL on which NGROK is listening to
tunnel_info = json.loads(term_output_json)
public_url = tunnel_info['tunnels'][0]['public_url']

# Registering Webhook
header = {"Authorization": "Bearer %s" % token, "content-type": "application/json"}
requests.packages.urllib3.disable_warnings()  #removing SSL warnings
post_message_url = "https://api.ciscospark.com/v1/webhooks"

# Preparing the payload to register. We are only interested in messages here, but feel free to change it
payload = {"resource": "messages", "event": "all", "targetUrl": public_url, "name": "MyWonderfulWebHook"}

api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)  #Registering webhook

if api_response.status_code != 200:
  print('Webhook registration Error !')
  exit(0)

if __name__ == '__main__':
  app.run(host='localhost', use_reloader=True, debug=True)
