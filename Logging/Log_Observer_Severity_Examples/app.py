import logging
from systemd.journal import JournalHandler
import sys
import time
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='Test to show - 1, 2, or 3', default=1)
args = vars(parser.parse_args())

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = JournalHandler()
#handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s {"Logger": "%(name)s", "Level": "%(levelname)s", "Message": "%(message)s"}')
if (args['test'] == 1):
  formatter = logging.Formatter('%(asctime)s {"Logger": "%(name)s", "Level": "%(levelname)s", "Message": "%(message)s"}')
if (args['test'] == 2):
    formatter = logging.Formatter('%(asctime)s {"Logger": "%(name)s", "severity": "%(levelno)s", "Message": "%(message)s"}')

handler.setFormatter(formatter)
root.addHandler(handler)

while 1:
  rnd = random.randint(1,4)
  if rnd == 1:
    root.error('this is an error')
  if rnd == 2:
    root.info('this is an info')
  if rnd == 3:
    root.warning('this is a warning')
  if rnd == 4:
    root.debug('this is a debug')

  time.sleep(2)
