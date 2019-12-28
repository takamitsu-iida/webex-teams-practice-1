#!/usr/bin/env python
# pylint: disable=missing-docstring

import logging
import subprocess
import sys
import time

from distutils.spawn import find_executable

import requests
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

class Ngrok:

  # delay time in sec
  delay = 3

  # Popen object
  popen = None

  # pubilic url
  public_url = None


  def __init__(self, port=5000):
    """constructor for Ngrok class

    Keyword Arguments:
        port {int} -- internal port number (default: {5000})
    """
    self.port = port

    # check if ngrok is installed
    assert find_executable("ngrok"), "ngrok command must be installed, see https://ngrok.com/"

    self.ngrok_cmds = ["ngrok", "http", str(port), "-log=stdout"]

    self.pkill_cmds = ["pkill"]
    self.pkill_cmds.extend(self.ngrok_cmds)


  def pkill(self):
    """kill previous sessions of ngrok (if any)"""
    subprocess.Popen(self.pkill_cmds, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()


  def run_background(self):
    """run ngrok in background, using subprocess.Popen()"""

    # kill same port process, if any
    self.pkill()

    logger.info("start ngrok")

    # spawn ngrok in background
    # subprocess.call("ngrok http 5000 -log=stdout > /dev/null &", shell=True)
    self.popen = subprocess.Popen(self.ngrok_cmds, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Leaving some time to ngrok to open
    time.sleep(self.delay)

    result_code = self.popen.poll()
    if result_code is None:
      logger.info("ngrok is running successfuly")
      return True

    logger.error("ngrok terminated abruptly with code: %s", str(result_code))
    return False


  def get_public_url(self):
    """getter for public_url

    Returns:
        str -- public_url handled by ngrok
    """
    if self.popen is None:
      # ngronk is not running yet
      return None

    if self.public_url:
      # already exist
      return self.public_url

    # use ngrok management api
    get_result = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = get_result.json()
    self.public_url = data['tunnels'][0]['public_url']

    return self.public_url


if __name__ == '__main__':

  import argparse

  logging.basicConfig(level=logging.INFO)

  def main():
    parser = argparse.ArgumentParser(description='operate ngrok.')
    parser.add_argument('-s', '--start', action='store_true', default=False, help='Start ngrok')
    parser.add_argument('-k', '--kill', action='store_true', default=False, help='Kill ngrok process')
    args = parser.parse_args()

    ngrok = Ngrok()

    if args.start:
      ngrok.run_background()
      print("ngrok is running with public url: {}".format(ngrok.get_public_url()))

    if args.kill:
      ngrok.pkill()

    return 0

  sys.exit(main())
