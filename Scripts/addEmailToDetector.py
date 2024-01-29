#!/usr/bin/env python
#
# This script will find a detector by name and add the email to the notirications
#
# Edit token.yaml.sample to contain valid Access Token and Realm rename to token.yaml
#
# Syntax: python3 addEmailToDetector.py -d "<detector name>" -e "<email address>"

import argparse
import yaml
import requests
import json

def addEmail(realm, accessToken, detectorName, emailAddress):
  headers = { "Content-Type": "application/json", "X-SF-TOKEN": f"{accessToken}" }
  url = f"https://app.{realm}.signalfx.com/v2/detector?name={detectorName}"
  response = requests.get(url, headers=headers)
  try:
    responseJSON = json.loads(response.text)
  except:
    print("ERROR: API call failed. Check token")
    return

  try:
    cnt = responseJSON["count"]
    if cnt == 1:
      # Found one detector, let's get the detector contents
      for result in responseJSON['results']:
        detectorId = result['id']      
      url = f"https://app.{realm}.signalfx.com/v2/detector/{detectorId}"
      response = requests.get(url, headers=headers)
      responseJSON = json.loads(response.text)
      toAdd = { 'type': 'Email', 'email': f'{emailAddress}' }
      for rule in responseJSON['rules']:
        rule['notifications'].append(toAdd)
      url = f"https://app.{realm}.signalfx.com/v2/detector/{detectorId}"
      response = requests.put(url, headers=headers, json=responseJSON)
      if response.status_code == 200:
        print("Successfully updated.")
      else:
        print("Error: Not updated.")
    else:
      print("ERROR: Found more than 1 detector. No updated.")
      return
  except:
    print("ERROR: Found detector, but unsuccessful updating.")
    return


if __name__ == '__main__':
  with open('token.yaml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
  
  parser = argparse.ArgumentParser(description='Splunk - Get Recent Detectors')
  parser.add_argument('-d', '--detectorName', help='detectorName', required=True)
  parser.add_argument('-e', '--emailAddress', help='email address', required=True)
  parser.add_argument('-r', '--realm', help='realm', required=False, default='us1')
  parser.add_argument('-t', '--token', help='token', required=False)
  args = parser.parse_args()

  token = cfg['access_token'] if args.token is None else args.token
  realm = cfg['realm'] if args.realm is None else args.realm
  detectorName = args.detectorName
  emailAddress = args.emailAddress

  addEmail(realm, token, detectorName, emailAddress)