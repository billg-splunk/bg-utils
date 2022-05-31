#!/usr/bin/env python
#
# This script will get user logins in last one hour. You can edit the script for longer time ranges. 
#
# Edit token.yaml.sample to contain valid Access Token and Realm rename to token.yaml
#
# Syntax: python3 getLogins.py

import argparse
from asyncio import current_task
import yaml
import requests
import json
import time

def callAPI(realm, token):
  limit = 10000 # For some reason breaks with a higher limit
  offset = 0
  current_time = int(time.time() * 1000)
  start_time = current_time - (24 * 60 * 60 * 1000)
  # Not sure if there is a difference between these
  #url = "https://api.{}.signalfx.com/v2/event/find?query=sf_eventCategory:AUDIT&start_time={}&limit={}".format(realm, start_time, limit)
  url = "https://api.{}.signalfx.com/v2/event/find?query=sf_eventType:SessionLog&start_time={}&limit={}".format(realm, start_time, limit)
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
  response = requests.get(url, headers=headers)
  print(response.text)

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Logins')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm

  callAPI(realm, token)

