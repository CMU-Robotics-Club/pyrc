import logging
import requests
import json
import os
import dateutil.parser
import collections

class APIClient(object):
  """
  Client that can be used to make calls in Python to Roboclub API.
  """

  def __init__(self, public_key=None, private_key=None, base_url=None):
    """
    Creates a API session with the provided public and private keys.
    The URL that is used to connect to the API can be overwritten by setting
    base_url.
    """

    self._logger = logging.getLogger(__name__)
    self._public_key = public_key

    if not public_key:
      public_key = os.environ.get('RC_PUBLIC_KEY')

    if not private_key:
      private_key = os.environ.get('RC_PRIVATE_KEY')

    if not base_url:
      base_url = "http://roboticsclub.org/crm"

    self._session = requests.Session()
    self._session.headers.update({
      "PUBLIC_KEY": public_key,
      "PRIVATE_KEY": private_key,
      "API_CLIENT": "pyrc v1.0",
    })

    self._logger.debug("session created")

    self._base_url = base_url

  def users(self, **kwargs):
    """
    Returns the list of users that
    match the specified search criteria.
    """
    
    return self._api_query_get_request("users", **kwargs)

  def user(self, id, **kwargs):
    """
    Returns the user with the specified id.
    """

    return self._api_query_get_request("users/{}".format(id), **kwargs)

  def projects(self, **kwargs):
    """
    Returns the list of projects that
    match the specified search criteria.
    """

    return self._api_query_get_request("projects", **kwargs)

  def project(self, id, **kwargs):
    """
    Returns the project with the specified id.
    """

    return self._api_query_get_request("projects/{}".format(id), **kwargs)

  def officers(self, **kwargs):
    """
    Returns the list of officers that
    match the specified search criteria.
    """

    return self._api_query_get_request("officers", **kwargs)

  def officer(self, id, **kwargs):
    """
    Returns the officer with the specified id.
    """

    return self._api_query_get_request("officers/{}".format(id), **kwargs)

  def webcams(self, **kwargs):
    """
    Returns the list of webcams that
    match the specified search criteria.
    """

    return self._api_query_get_request("webcams", **kwargs)

  def webcam(self, id, **kwargs):
    """
    Returns the webcam with the specified id.
    """

    return self._api_query_get_request("webcams/{}".format(id), **kwargs)

  def social_medias(self, **kwargs):
    """
    Returns the list of social medias that
    match the specified search criteria.
    """

    return self._api_query_get_request("social_medias", **kwargs)

  def social_media(self, id, **kwargs):
    """
    Returns the social media with the specified id.
    """

    return self._api_query_get_request("social_medias/{}".format(id), **kwargs)

  def channels(self, **kwargs):
    """
    Returns the list of channels that
    match the specified search criteria.
    """

    return self._api_query_get_request("channels", **kwargs)

  def channel(self, id, **kwargs):
    """
    Returns the channel with the specified id.
    """

    return self._api_query_get_request("channels/{}".format(id), **kwargs)

  def calendar(self):
    """
    Returns the list of events that are currently occuring
    in the club.  Each event has a 'name', 'location', 'start', and 'end'
    field.
    """

    return self._api_get_request("calendar")

  def login(self, username, password):
    """
    Returns True the provided authentication credentials
    are valid, False otherwise.
    """

    response = self._post_request("login", {
      'username': username,
      'password': password
    })

    return bool(response)

  def datetime(self):
    """
    Returns the current datetime object.
    NOTE: useful for systems without RTC
    or no WIFI/Ethernet connection.
    """

    response = self._api_get_request("datetime")
    return dateutil.parser.parse(response)

  def magnetic(self, _id):
    """
    Returns the ID of the user with the specified Magnetic ID.
    If no such user exists returns None.
    """

    try:
      return self._post_request("magnetic", _id)
    except requests.exceptions.HTTPError as e:
      if e.status_code == 400:
        return None
      else:
        raise

  def rfid(self, _id):
    """
    Returns the ID of the user with the specified RFID.
    If no such user exists returns None.
    """

    try:
      return self._post_request("rfid", _id)
    except requests.exceptions.HTTPError as e:
      if e.status_code == 400:
        return None
      else:
        raise

  def create_channel(self, name):
    return self._post_request("channels", {'name': name})

  # TODO: ability to create and write to channels

  def get(self, url):
    """
    Request a resource using GET with authentication keys.
    """

    return self._get(url)


  def set_user_rfid(self, user_id, rfid):
    """
    Set the RFID for the specified user.
    This is a priveleged option and you likely
    do not have permission.
    """

    return self._post_request("users/{}/rfid".format(user_id), rfid)

  def send_email(self, user_id, subject, body):
    """
    Sends an email to the specified user.
    This is a priveleged option and you likely
    do not have permission.
    """

    self._logger.debug("Sending email to {} - {} | {}".format(user_id, subject, body))

    return self._post_request("users/{}/email".format(user_id), {
      'subject': subject,
      'body': body,
    })


  # Private Methods

  def _get(self, url):
    self._logger.debug("GET to {}".format(url))

    response = self._session.get(url)
    self._check_response(response)

    self._logger.debug("GET response {}".format(response.text))
    return response

  def _get_request(self, path):
    return self._get("{}/{}".format(self._base_url, path))

  def _api_get_request(self, path):
    return self._get_request("api/{}".format(path)).json(object_pairs_hook=collections.OrderedDict)

  def _api_query_get_request(self, path, **kwargs):
    self._logger.debug("GET to {} with query parameters {}".format(path, kwargs))

    url = path

    for i,(key, value) in enumerate(kwargs.items()):
      token = '?' if i == 0 else '&'
      url += "{}{}={}".format(token, key, value)

    return self._api_get_request(url)

  def _post_request(self, path, message):
    self._logger.debug("POST to {}".format(path))

    url = "{}/api/{}/".format(self._base_url, path)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    try:
      data = json.dumps(message)
    # Not JSON so just send it as is
    except ValueError:
      data = message

    response = self._session.post(url, data=data, headers=headers)
    self._check_response(response)

    return response.json(object_pairs_hook=collections.OrderedDict)

  def _check_response(self, response):
    # Don't call raise_for_status since the HTTPException fields
    # status_code, errno, and detail should be set.
    if response.status_code != requests.codes.ok:      
      status_code = response.status_code
      response_body = response.json(object_pairs_hook=collections.OrderedDict)
      errno = response_body['errno']
      detail = response_body['detail']

      e = requests.exceptions.HTTPError("{} {}({})".format(status_code, errno, detail))
      
      e.status_code = status_code
      e.errno = errno
      e.detail = detail

      raise e
