#!/usr/bin/env python
#
# This script will make users admins.
#
# Syntax: python3 makeUsersAdmins.py

import yaml
import requests
import json
from os.path import exists
import datetime

def appendErrorToFile(theError):
  theLog.write(f"ERROR: {theError}\n")

def appendEmailToFile(email):
  theLog.write(f"- {email}\n")

def makeAdmin(userId):
  try:
    url = f"https://api.{realm}.signalfx.com/v2/organization/member/{userId}"
    headers = { "Content-Type": "application/json", "X-SF-TOKEN": f"{token}" }
    data = "{ admin:true }"
    response = requests.put(url, headers=headers, data=data)
    emailUpdated = response.json()["email"]
    appendEmailToFile(emailUpdated)
  except Exception as e:
    appendErrorToFile(e)

def findUsersAndMakeAdmin():
  limit = 10000 # Breaks with a higher limit
  url = f"https://api.{realm}.signalfx.com/v2/organization/member?limit={limit}&query=(!sf_role:admin)"
  headers = {"Content-Type": "application/json", "X-SF-TOKEN": f"{token}" }
  response = requests.get(url, headers=headers)
  for result in response.json()["results"]:
    makeAdmin(result["id"])

def login(email, password, orgId):
  url = f"https://api.{realm}.signalfx.com/v2/session"
  headers = { "Content-Type": "application/json" }
  data = f'{{ "email": "{email}", "password": "{password}", "organizationId": "{orgId}" }}'
  response = requests.post(url, headers=headers, data=data)
  return response.json()["accessToken"]

if __name__ == '__main__':
  global theLog
  theLog = open("/home/ubuntu/show-makeadmins/admins.log", "a")

  if ( exists('/home/ubuntu/show-makeadmins/creds.yaml') ):
    with open('/home/ubuntu/show-makeadmins/creds.yaml', 'r') as ymlfile:
      cfg = yaml.safe_load(ymlfile)

  try:
    global realm
    realm = cfg['realm']
    global token
    email = cfg['email']
    password = cfg['password']
    orgId = cfg['orgId']
    potentialToken = login(email, password, orgId)
    if len(potentialToken) > 0:
      token = potentialToken
  except Exception as e:
    appendErrorToFile(e)
    exit()

  currentTS = datetime.datetime.now()
  theLog.write(f"Running @ {currentTS}\n")  
  findUsersAndMakeAdmin()