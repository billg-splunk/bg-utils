import logging
import sys
import time

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s {\n "Logger": "%(name)s",\n "Level": "%(levelname)s",\n "Message": "%(message)s"\n}')
handler.setFormatter(formatter)
root.addHandler(handler)

while 1:
  root.error('this is an error')
  time.sleep(2)
