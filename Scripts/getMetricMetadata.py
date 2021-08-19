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



def addDimensions(responseJSON, arrDimensions):
  for result in responseJSON['results']:
    arrDimensions.append(result['key'])
  return arrDimensions

def addCustomProperties(responseJSON, arrCustomProperties):
  for result in responseJSON['results']:
    customProps = result['customProperties']
    for prop in customProps:
      arrCustomProperties.append(prop)
  return arrCustomProperties

def addTags(responseJSON, arrTags):
  return

def callAPI(realm, token):
  arrDimensions = []
  arrCustomProperties = []
  arrTags = []
  limit = 5000 # For some reason breaks with a higher limit
  offset = 0
  while (1>0):
    url = "https://api.{}.signalfx.com/v2/dimension?query=key:*&limit={}&offset={}".format(realm, limit, offset*limit)
    headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
    response = requests.get(url, headers=headers)
    responseJSON = json.loads(response.text)
    #print(response.text[0:1000])
    try:
      cnt = responseJSON["count"]
    except:
      print("ERROR: Check your token, that's the most likely issue.")
      break
    
    arrDimensions = addDimensions(responseJSON, arrDimensions)
    arrCustomProperties = addCustomProperties(responseJSON, arrCustomProperties)

    offset = offset + 1
    if (offset * limit) >= cnt: # The next starting point would be past the last item
      break
  
  arrDimensions = list(set(arrDimensions)) # Remove Duplicates
  arrDimensions.sort()

  arrCustomProperties = list(set(arrCustomProperties)) # Remove Duplicates
  arrCustomProperties.sort()

  print('********** Dimensions **********')
  print(*arrDimensions, sep = "\n") # Print one per line
  print('********** Custom Properties **********')
  print(*arrCustomProperties, sep = "\n") # Print one per line

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Metric Metadata')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm

  callAPI(realm, token)

