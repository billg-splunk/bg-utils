#!/usr/bin/env python
#
# This script will get all metric metadata. 
#
# Edit token.yaml.sample to contain valid Access Token and rename to token.yaml
#
# Syntax: python3 getMetricMetadata.py

import argparse
import yaml
import requests
import json

def run(realm, token):
  limit = 5000
  url = "https://api.{}.signalfx.com/v2/dimension?query=key:a*&limit={}".format(realm, limit)
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
  response = requests.get(url, headers=headers)
  responseJSON = json.loads(response.text)
  print(response.text)

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Metric Metadata')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  if (args.token is None):
    token = cfg['access_token']
  else:
    token = args.token

  if (args.realm is None):
    realm = cfg['realm']
  else:
    realm = args.realm

  run(realm, token)

