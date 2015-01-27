#!/usr/bin/env python3

from rc.clients import APIClient

if __name__ == '__main__':
  """
  Given a valid RFID attempts to lookup
  the User's ID.  Then using that User ID,
  if it exists, get more information about the User.
  The User will only be granted access to our imaginary
  service if their first_name is 'Brent'.
  """

  # If the bash variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  rfid = input("RFID: ")

  # Ask the API who this RFID corresponds to
  (user_id, api_request_id) = client.rfid(rfid, "Some Meta String")

  # Can modify the APIRequest to give more information
  # to the User(and Officers) about what this operation
  # was for
  print("APIRequest ID: {}".format(api_request_id))

  if user_id is None:
    print("No such User")
  else:
    # Get more information about the user
    user = client.user(user_id)

    print("Username: {}".format(user['username']))

    if user['first_name'] == "Brent":
      # Access Granted
      print("Welcome " + user['first_name'])

      client.api_request_write(api_request_id, meta="You are a Brent", success=True)
    else:
      # Access Denied 
      print("Goodbye" + user['first_name'])

      client.api_request_write(api_request_id, meta="You are not a Brent", success=False)
