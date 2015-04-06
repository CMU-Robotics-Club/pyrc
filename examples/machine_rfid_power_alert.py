#!/usr/bin/env python

from rc.clients import WebSocketClient, APIClient
from threading import Timer

AUTHORIZED_POWERED_OFF_TIMEOUT = 5  # 5 seconds
api = APIClient()

timers = {}


def forgot_id(tool_name, user_id):
  """
  Called after User left ID in tool after AUTHORIZED_POWERED_OFF_TIMEOUT
  """

  user = api.user(user_id)
  m = "{} {} did you forget your ID on the {}?".format(user['first_name'], user['last_name'], tool_name)

  print(m)

  api.channel_write(5, m) # Clock Channel
  api.channel_write(9, m) # Speaker Channel


def callback(machine):
  id = machine['id']
  type = machine['type']
  user_id = machine['user']
  powered = machine['powered']

  if not id in timers:
    timers[id] = Timer(AUTHORIZED_POWERED_OFF_TIMEOUT, forgot_id, args=(type, user_id, ))

  print("{} | user: {}, powered: {}".format(type, user_id, powered))

  if powered:
    print("Canceling timeout for {}".format(type))
    timers[id].cancel()
    timers[id] = Timer(AUTHORIZED_POWERED_OFF_TIMEOUT, forgot_id, args=(type, user_id, ))
  elif user_id:
    print("Scheduling timeout for {}".format(type))
    timers[id].cancel()
    timers[id] = Timer(AUTHORIZED_POWERED_OFF_TIMEOUT, forgot_id, args=(type, user_id, ))
    timers[id].start()


if __name__ == '__main__':
  client = WebSocketClient('machines', None, callback)
  client.connect()
  client.run_forever()
