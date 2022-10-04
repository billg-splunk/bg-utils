import logging
from systemd.journal import JournalHandler
import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='Test to show - 1, 2, or 3', default=1)
args = vars(parser.parse_args())

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = JournalHandler()
//handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s {"Logger": "%(name)s", "Level": "%(levelname)s", "Message": "%(message)s"}')
if (args['test'] == 1):
  formatter = logging.Formatter('%(asctime)s {"Logger": "%(name)s", "Level": "%(levelname)s", "Message": "%(message)s"}')

handler.setFormatter(formatter)
root.addHandler(handler)

while 1:
  root.error('this is an error')
  time.sleep(2)
