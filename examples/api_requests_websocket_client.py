#!/usr/bin/env python3

from rc.clients import APIRequestsWebSocketClient
import json

def callback(apiRequest):
  apiRequest = str(apiRequest)
  apiRequest = json.loads(apiRequest)

  print("APIRequest: {} {} {} {} {} {} {} {} {} {}".format(
    apiRequest['id'],
    apiRequest['endpoint'],
    apiRequest['extra'],
    apiRequest['user'],
    apiRequest['updater_is_project'],
    apiRequest['updater_id'],
    apiRequest['updated_datetime'],
    apiRequest['created_datetime'],
    apiRequest['success'],
    apiRequest['meta']
  ))


if __name__ == '__main__':
  client = APIRequestsWebSocketClient(callback, base_url="ws://127.0.0.1:1984")
  client.connect()
  client.run_forever()
