#!/usr/bin/env python
import json
import requests 
import yaml 

def removeTest(realm, apiToken, testType, testId):
  url = f"https://api.{realm}.signalfx.com/v2/synthetics/tests/{testType}/{testId}"
  headers = { "Content-Type": "application/json", "X-SF-TOKEN": f"{apiToken}" }
  response = requests.delete(url, headers=headers)

def removeSynthetics(realm, apiToken):
  url = f"https://api.{realm}.signalfx.com/v2/synthetics/tests?limit=10000"
  headers = { "Content-Type": "application/json", "X-SF-TOKEN": f"{apiToken}" }
  response = requests.get(url, headers=headers)
  if response.status_code == 401:
    print('Access denied: Check token.')
  else:
    for test in response.json()["tests"]:
      testType = test["type"]
      testId = test["id"]
      testName = test["name"]
      removeTest(realm, apiToken, testType, testId)
      print(f'Deleted test {testType}-{testId}-{testName}')
  
if __name__ == '__main__':
  realm = 'us1'
  apiToken = 'xxx'
  removeSynthetics(realm, apiToken)
  print('Done.')
