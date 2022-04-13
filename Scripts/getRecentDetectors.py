#!/usr/bin/env python
#
# This script will get all detectors created in the last x days. 
#
# Edit token.yaml.sample to contain valid Access Token and Realm rename to token.yaml
#
# Syntax: python3 getRecentDetectors.py

import argparse
import yaml
import requests
import json
import time

def getDetectors(responseJSON, arrDetectors, days):
  ms = int(time.time() * 1000)
  ms = ms - (int(days) * 24 * 60 * 1000)
  for result in responseJSON['results']:
    if result['created'] > ms:
      arrDetectors.append(result['name'] + ',' + str(result['created']))
  return arrDetectors

def callAPI(realm, token, days):
  arrDetectors = []
  limit = 10000
  offset = 0

  url = f"https://api.{realm}.signalfx.com/v2/detector"
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": f"{token}" }
  response = requests.get(url, headers=headers)
  responseJSON = json.loads(response.text)
  try:
    cnt = responseJSON["count"]
  except:
    print("ERROR: Check your token, that's the most likely issue.")
    print(response.text)
    return

  if (cnt > 10000):
    print(f'You have more than 10,000 detectors ({cnt} found).')
    print('You will need to do this with getMetricMetadataFromReport.py.')
    print('Presneting the results for the first 10,000.')
    #break

  arrDetectors = getDetectors(responseJSON, arrDetectors, days)
  print(arrDetectors)

  #arrDimensions = addDimensions(responseJSON, arrDimensions)
  #arrCustomProperties = addCustomProperties(responseJSON, arrCustomProperties)
  #arrTags = addTags(responseJSON, arrTags)
  
  #arrDimensions = list(set(arrDimensions)) # Remove Duplicates
  #arrDimensions.sort()

  #arrCustomProperties = list(set(arrCustomProperties)) # Remove Duplicates
  #arrCustomProperties.sort()

  #arrTags = list(set(arrTags)) # Remove Duplicates
  #arrTags.sort()

  #print(*arrDimensions, sep = "\n") # Print one per line
  #print('********** Custom Properties **********')
  #print(*arrCustomProperties, sep = "\n") # Print one per line
  #print('********** Tags **********')
  #print(*arrTags, sep = "\n") # Print one per line

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Recent Detectors')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  parser.add_argument('-d', '--days', help='Days old', required=False, default='1')
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm
  days = args.days

  callAPI(realm, token, days)