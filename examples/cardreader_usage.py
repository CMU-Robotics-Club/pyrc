#!/usr/bin/env python3

from rc.clients import APIClient

if __name__ == '__main__':
  """
  Lists all the usernames of Users
  who have used the CardReader project.
  """

  # If the bash variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  cardreader_id = client.projects(name="CardReader")[0]['id']

  api_requests = client.api_requests(endpoint='/magnetic/', updater_is_project=True, updater_id=cardreader_id)

  for api_request in api_requests:
    user_id = api_request['user']

    if user_id:
      user = client.user(id=user_id)
      print("{} used CardReader on {}".format(user['username'], api_request['created_datetime']))
