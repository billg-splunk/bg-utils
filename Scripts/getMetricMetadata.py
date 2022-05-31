#!/usr/bin/env python
#
# This script will get all metric metadata. 
#
# Edit token.yaml.sample to contain valid Access Token and Realm rename to token.yaml
#
# Syntax: python3 getMetricMetadata.py
#
# Alternate Syntax: python3 getMetricMetadata.py -t <token> -r <realm> -m <metric name>

import argparse
import yaml
import requests
import json

def addDimensionsFromDimension(responseJSON, arrDimensions):
  for result in responseJSON['results']:
    arrDimensions.append(result['key'])
  return arrDimensions

def addDimensionsFromMTS(responseJSON, arrDimensions):
  for result in responseJSON['results']:
    dims = result['dimensions']
    for dim in dims:
      arrDimensions.append(dim)
  return arrDimensions

def addCustomProperties(responseJSON, arrCustomProperties):
  for result in responseJSON['results']:
    customProps = result['customProperties']
    for prop in customProps:
      arrCustomProperties.append(prop)
  return arrCustomProperties

def addTags(responseJSON, arrTags):
  for result in responseJSON['results']:
    for tag in result['tags']:
      arrTags.append(tag)
  return arrTags

def processResults(responseJSON, isDimensionsResult):
  arrDimensions = []
  arrCustomProperties = []
  arrTags = []
  try:
    cnt = responseJSON["count"]
  except:
    print("ERROR: Check your token, that's the most likely issue.")
    return

  if (cnt > 10000):
    print('You have more than 10,000 dimensions ({} found).'.format(str(cnt)))
    print('You will need to do this with getMetricMetadataFromReport.py.')
    print('Presenting the results for the first 10,000.')
    #break
  
  if isDimensionsResult:
    arrDimensions = addDimensionsFromDimension(responseJSON, arrDimensions)
  else:
    arrDimensions = addDimensionsFromMTS(responseJSON, arrDimensions)
  arrCustomProperties = addCustomProperties(responseJSON, arrCustomProperties)
  arrTags = addTags(responseJSON, arrTags)
  
  arrDimensions = list(set(arrDimensions)) # Remove Duplicates
  arrDimensions.sort()

  arrCustomProperties = list(set(arrCustomProperties)) # Remove Duplicates
  arrCustomProperties.sort()

  arrTags = list(set(arrTags)) # Remove Duplicates
  arrTags.sort()

  print('********** Dimensions **********')
  print(*arrDimensions, sep = "\n") # Print one per line
  print('********** Custom Properties **********')
  print(*arrCustomProperties, sep = "\n") # Print one per line
  print('********** Tags **********')
  print(*arrTags, sep = "\n") # Print one per line

def callAPI(realm, token, metric):
  limit = 10000 # For some reason breaks with a higher limit
  offset = 0

  if (metric == ""):
    url = "https://api.{}.signalfx.com/v2/dimension?query=key:*&limit={}".format(realm, limit)
  else:
    url = "https://api.{}.signalfx.com/v2/metrictimeseries?query=sf_metric:{}&limit={}".format(realm, metric, limit)
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
  response = requests.get(url, headers=headers)
  responseJSON = json.loads(response.text)
  #print(response.text[0:1000])

  if (metric ==""):
    # Results are from dimension API
    processResults(responseJSON, True)
  else:
    # Results are from MTS API
    processResults(responseJSON, False)

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Metric Metadata')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  parser.add_argument('-m', '--metric', help='Optional: Send metric name', required=False)
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm
  metric = "" if args.metric is None else args.metric

  callAPI(realm, token, metric)

