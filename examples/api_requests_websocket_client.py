#!/usr/bin/env python3

from rc.clients import WebSocketClient

MODEL = 'api_requests'
MODEL_ID = None

def callback(apiRequest):
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
  client = WebSocketClient(MODEL, MODEL_ID, callback)
  client.connect()
  client.run_forever()
