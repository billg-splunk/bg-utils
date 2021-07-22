#!/usr/bin/env python
#
# Find first 100 metrics and their mts count

import requests
import json
import argparse
import csv

parser = argparse.ArgumentParser(description='SignalFx MTS Categories')
parser.add_argument('-t', '--token', help='Access Token', required=True)
parser.add_argument('-r', '--realm', help='Realm (us0,us1,us2, eu0)', required=True)
parser.add_argument('-a', '--active', help='Active (true/false)', default='true')
args = vars(parser.parse_args())

headers = {"Content-Type": "application/json", "X-SF-TOKEN": "{}".format(args['token']) }
url = "https://app.{}.signalfx.com/v2/metric/_/metricfinder?activeOnly={}&filters=sf_mtsCategoryType:3&query=".format(args['realm'], args['active'])
response = requests.get(url, headers=headers)
responseJSON = json.loads(response.text)
total = 0

print("{:<90} {:>10}".format("\nSignalFx Metrics", "MTS"))
print("{:<90} {:>10}".format("---------------------------------", "----"))
for item in responseJSON['metrics']['metricResults']:
    print("{:<90} {:>10}".format(item['value'], item['count']))
    total = total + 1
print("{:<90} {: >10}".format("---------------------------------", "---"))
print("{:<90} {: >10}".format("", total))
