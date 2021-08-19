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

def getDimensions(realm, token):
  limit = 5000 # For some reason breaks with a higher limit
  arrDimensions = []

  #for offset in range(1, 1000):
  offset = 0
  while (1>0):
    print(offset*limit)
    url = "https://api.{}.signalfx.com/v2/dimension?query=key:*&limit={}&offset={}".format(realm, limit, offset*limit)
    headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
    response = requests.get(url, headers=headers)
    responseJSON = json.loads(response.text)
    #print(response.text[0:300])
    try:
      cnt = responseJSON["count"]
    except:
      print("ERROR: Check your token, that's the most likely issue.")
      break
    for result in responseJSON['results']:
      arrDimensions.append(result['key'])
    offset = offset + 1
    if (offset * limit) >= cnt: # The next starting point would be past the last item
      break
  
  arrDimensions = list(set(arrDimensions)) # Remove Duplicates
  arrDimensions.sort()
  print(*arrDimensions, sep = "\n") # Print one per line

def run(realm, token):
  getDimensions(realm, token)

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Metric Metadata')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm

  run(realm, token)

