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
