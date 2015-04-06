#!/usr/bin/env python3

from rc.clients import WebSocketClient
import time

MODEL = 'channels'
# Can be None to listen to changes on all Channels
MODEL_ID = 1

def callback(instance):
  print("New Channel Value: {}".format(instance['value']))

if __name__ == '__main__':
  client = WebSocketClient(MODEL, MODEL_ID, callback, base_url="ws://127.0.0.1:1984")
  client.connect()
  
  while True:
    if client.terminated:
      print("Disconnected")

      client._th.join()
      break

    print("Still connected")
    time.sleep(5)
