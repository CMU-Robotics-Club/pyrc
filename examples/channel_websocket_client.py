#!/usr/bin/env python3

from rc.clients import ChannelWebSocketClient
import time

CHANNEL_ID = 1

def callback(value):
  print("New Channel Value: {}".format(value))

if __name__ == '__main__':
  client = ChannelWebSocketClient(CHANNEL_ID, callback)
  client.connect()
  
  while True:
    if client.terminated:
      print("Disconnected")

      client._th.join()
      break

    print("Still connected")
    time.sleep(5)
