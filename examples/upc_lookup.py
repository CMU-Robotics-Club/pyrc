#!/usr/bin/env python3

from rc.clients import APIClient

if __name__ == '__main__':
  """
  Get information about the item with the specified UPC.
  """

  # If the bash variables RC_PUBLIC_KEY and RC_PRIVATE_KEY 
  # are not set you need to pass the public and private key
  # values into this constructor
  client = APIClient()

  while True:
    upc = input("UPC: ")

    item = client.upcs(upc=upc)

    if len(item):
      item = item[0]

      print("{} (${})".format(item['name'], item['cost']))
    else:
      print("No such item")
