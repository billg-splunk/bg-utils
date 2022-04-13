#!/usr/bin/env python

# Syntax: python3 getContainerList.py
#         or
#         python3 getContainerList.py -m container_cpu_utilization
#
# For convenience can store org_access_token in token.yaml file

import os
import signalfx
from signalfx.signalflow import messages
import argparse
import yaml
import time
import datetime

clear = lambda: os.system("cls" if os.name == "nt" else "clear")
clear()

def write(toFile, f, msg):
  if toFile == "screen":
    print(msg)
  else:
    print(msg)
    f.write("%s\n" % msg)

def run(metricName, realm, token, toFile, f):
  now = int(time.time()) * 1000
  start = now - 15 * 60 * 1000
  stop = now - 1 * 60 * 1000
  program = (
    "data('%s', extrapolation='last_value', maxExtrapolations=2).publish(label='A')"
    % (metricName)
  )
  url = (
    "https://stream.%s.signalfx.com" % realm
  )
  client = signalfx.SignalFx(stream_endpoint=url)
  flow = client.signalflow(token)
  # c = flow.execute(program, start=start, stop=stop, resolution=86400000, immediate=True)
  c = flow.execute(program, start, stop)

  for msg in c.stream():
    if isinstance(msg, messages.MetadataMessage):
      container_name = "Unknown"
      try:
        container_name = msg.properties["k8s.container.name"]
      except:
        try:
          container_name = msg.properties["container_name"]
        except:
          pass

      host_name = "Unknown"
      try:
        host_name = msg.properties["k8s.node.name"]
      except:
        try:
          host_name = msg.properties["kubernetes_node"]
        except:
          pass

      if (container_name != 'Unknown' or host_name != 'Unknown'):
        write(toFile, f, f"{container_name}, {host_name}")            

if __name__ == "__main__":
  with open("token.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

  if "access_token" in cfg:
    token = cfg["access_token"]
    requireToken = False
  else:
    token = ""
    requireToken = True

  parser = argparse.ArgumentParser(description="Splunk O11y Cloud - GetContainerList")
  parser.add_argument("-m", "--metricName", help="Metric Name", required=False, default="container_cpu_utilization")
  parser.add_argument("-r", "--realm", help="Realm", required=False, default="us1")
  parser.add_argument("-t", "--token", help="Token", required=requireToken, default=token)
  parser.add_argument("-f", "--toFile", help="Output file (screen otherwise)", required=False, default="screen")
  args = parser.parse_args()

  if args.toFile != 'screen':
    f = open(args.toFile, "a")
  else:
    f = ''

  run(args.metricName, args.realm, args.token, args.toFile, f)

  if args.toFile != 'screen':
    f.close()
