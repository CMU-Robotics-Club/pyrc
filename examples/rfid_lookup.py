#!/usr/bin/env python3

from rc import APIClient
import requests
import sys

if __name__ == '__main__':
  # If the base variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  rfid = input("RFID: ")

  try:
    user_id = client.rfid(rfid)
  except requests.exceptions.HTTPError as e:
    print("HTTP {}: {}({})".format(e.status_code, e.detail, e.errno))
    sys.exit(1)

  user = client.user(user_id)

  print("This user is {}".format(user['username']))
