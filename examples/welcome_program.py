#!/usr/bin/env python

"""
Waits for a user to badge in at Front Door
and says their name, displays their name on the clock,
and changes both the rls-logo and rls-strip channels
to the user's color pattern.
"""

from rc.clients import APIClient, WebSocketClient

api_client = APIClient()

def callback(value):
    # 19 is the Project ID of the Front Door project
    if value['endpoint'] != '/rfid/' or value['updater_is_project'] != True or value['updater_id'] != 19:
        return

    value = value['user']

    if value:
        u = api_client.user(value)

        m = "Hello " + u['first_name']
        c = u['color']
        api_client.channel_write(11, c) # rls-logo
        api_client.channel_write(12, c) # rls-strip
    else:
        m = "Please sign up using Card Reader."

    print(m)

    api_client.channel_write(5, m) # Clock
    api_client.channel_write(9, m) # Speaker


if __name__ == '__main__':
    while True:
        client = WebSocketClient(model='api_requests', model_id=None, callback=callback);
        client.connect()
        client.run_forever()