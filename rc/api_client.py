import requests

class APIClient(object):
  
  def __init__(self, public_key, private_key, base_url="http://roboticsclub.org/api"):
    self._session = requests.Session()
    self._session.headers.update({
      "X_PROJECT_ID": public_key,
      "X_PROJECT_NAME": private_key,
    })
    self._base_url = base_url

  @property
  def users(self):
    return self._get_request("users")

  def _get_request(self, url):
    return self._session.get("{}/{}".format(self._base_url, url)).json()