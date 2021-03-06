#!/usr/bin/env python3

from rc.clients import APIClient

if __name__ == '__main__':
  """
  Lists all the usernames of Users
  who have used the Drill Press.
  """

  # If the bash variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  tooltron_id = client.projects(name="Tooltron")[0]['id']

  api_requests = client.api_requests(endpoint='/rfid/', updater_is_project=True, updater_id=tooltron_id, meta="Drill Press")

  for api_request in api_requests:
    user_id = api_request['user']

    if user_id:
      user = client.user(id=user_id)
      print("{} was {} access on Drill Press from {} until {}".format(user['username'], "Granted" if api_request['success'] else "Denied", api_request['created_datetime'], api_request['updated_datetime']))
