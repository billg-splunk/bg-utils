#!/usr/bin/env python
#
# This script will make users admins.
#
# Syntax: python3 makeUsersAdmins.py

import argparse
import yaml
import requests
import json
from os.path import exists
import datetime

def appendEmailToFile(email):
  theLog.write(f"{email}\n")

def makeAdmin(userId):
  url = f"https://api.{realm}.signalfx.com/v2/organization/member/{userId}"
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": f"{token}" }
  data = "{ admin:true }"
  response = requests.put(url, headers=headers, data=data)
  #print(userId)

def callAPI():
  limit = 10000 # For some reason breaks with a higher limit
  url = f"https://api.{realm}.signalfx.com/v2/organization/member?limit={limit}&query=(!sf_role:admin)"
  #url = f"https://api.{realm}.signalfx.com/v2/organization/member?limit={limit}&query=(email:billg@splunk.com)"
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": f"{token}" }
  response = requests.get(url, headers=headers)
  #print(response.text)
  for result in response.json()["results"]:
    makeAdmin(result["id"])
    appendEmailToFile(result["email"])


  #if output != "":
  #  with open(args.output, 'w') as outfile:
  #    json.dump(response.json(), outfile, indent=2, sort_keys=True)
  #  print(f"Results saved to file: {output}")

if __name__ == '__main__':
  if ( exists('token.yaml') ):
    with open('token.yaml', 'r') as ymlfile:
      cfg = yaml.safe_load(ymlfile)
  
  global theLog
  theLog = open("admins.log", "a")

  parser = argparse.ArgumentParser(description='Splunk - Make all users admins')
  parser.add_argument('-r', '--realm', help='Realm', required=False)
  parser.add_argument('-t', '--token', help='Token', required=False)
  args = parser.parse_args()

  try:
    global token
    token = cfg['access_token'] if args.token is None else args.token
    global realm
    realm = cfg['realm'] if args.realm is None else args.realm
  except:
    print('ERROR: Need to define either config file or arguments')
    exit()

  currentTS = datetime.datetime.now()
  theLog.write(f"Running @ {currentTS}\n")  
  callAPI()

