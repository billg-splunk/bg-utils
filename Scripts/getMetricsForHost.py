#!/usr/bin/env python
#
# This script will get all unique metrics for a given host. 
#
# Edit token.yaml.sample to contain valid Access Token and rename to token.yaml
#
# Syntax: python3 getMetricsForHost.py -h <HOST_NAME>
#
# HOST_NAME should be an exact match

import argparse
import yaml
import requests
import json

def run(hostname, realm, token):
  limit = 1000
  url = "https://api.{}.signalfx.com/v2/metrictimeseries?limit={}&query=host.name:{}".format(realm, limit, hostname)
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(token) }
  response = requests.get(url, headers=headers)
  responseJSON = json.loads(response.text)
  
  # If the result count is > limit, say so and exit
  try:
    cnt = responseJSON["count"]
  except:
    print("ERROR: Check your token, that's the most likely issue.")
    return

  if (cnt > limit):
    print("Need to increase limit, this host has > {} mts's.".format(limit))
    return

  # Add metrics to a list
  arr = []
  for result in responseJSON['results']:
    arr.append(result['metric'])

  arr = list(set(arr)) # Remove Duplicates
  arr.sort()
  print(*arr, sep = "\n") # Print one per line

if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Host Metrics')
  parser.add_argument('-n', '--hostName', help='HostName', required=True)
  parser.add_argument('-r', '--realm', help='Realm', required=True)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  if (args.token is None):
    run(args.hostName, args.realm, cfg['access_token'])
  else:
    run(args.hostName, args.realm, args.token)