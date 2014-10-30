#!/usr/bin/env python3

from rc import APIClient
import sys

if __name__ == '__main__':
  # If the base variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  username = input("username: ")

  users = client.users(username=username)
  
  if len(users) == 0:
    print("Invalid username")
    sys.exit(1)
  else:
    user = users[0]
    
    user_id = user['id']
    projects = client.projects(leaders=user_id)

    for project in projects:
      print(project['name'])
