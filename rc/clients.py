import logging
import json
import os
import collections

import requests
from ws4py.client.threadedclient import WebSocketClient

from . import __client__, __version__


__all__ = ['APIClient', 'ChannelWebSocketClient', 'APIRequestsWebSocketClient']


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
      base_url = "https://roboticsclub.org"

    # Delay import of __client__ and __version__ 
    # otherwise causes circular import
    from . import __client__, __version__

    self._session = requests.Session()
    self._session.headers.update({
      "PUBLIC_KEY": public_key,
      "PRIVATE_KEY": private_key,
      "API_CLIENT": "{} v{}".format(__client__, __version__),
    })

    self._logger.debug("session created")

    self._base_url = base_url

  def api_requests(self, **kwargs):
    """
    Returns the list of APIRequests that
    match the specified search criteria.
    """

    return self._api_query_get_request("api_requests", **kwargs)

  def api_request(self, id, **kwargs):
    """
    Returns the APIRequest with the specified id.
    """

    return self._api_query_get_request("api_requests/{}/".format(id), **kwargs)

  def api_request_write(self, id, **kwargs):
    """
    Sets the fields provided of the specified APIRequest.
    """

    return self._put_request("api_requests/{}/".format(id), kwargs)

  def calendar(self):
    """
    Returns the list of events that are currently occuring
    in the club.  Each event has a 'name', 'location', 'start', and 'end'
    field.
    """

    return self._api_get_request("calendar")

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

    return self._api_query_get_request("channels/{}/".format(id), **kwargs)

  def channel_write(self, id, value):
    """
    Writes the value to the specified channel.
    """

    return self._put_request("channels/{}/".format(id), {'value': value})

  def datetime(self, **kwargs):
    """
    Returns the a String of the current datetime object.
    Can pass strftime 'form' query parameter to set format.
    NOTE: useful for systems without RTC
    or no WIFI/Ethernet connection.
    """

    response = self._api_query_get_request("datetime", **kwargs)
    return response['datetime']

  def faqs(self, **kwargs):
    """
    Returns the list of FAQ categories that
    match the specified search criteria.
    """

    return self._api_query_get_request("faq", **kwargs)

  def faq(self, id, **kwargs):
    """
    Returns the FAQ category with the specified id.
    """

    return self._api_query_get_request("faq/{}".format(id), **kwargs)

  def machines(self, **kwargs):
    """
    Returns the list of Machines that
    match the specified search criteria.
    """

    return self._api_query_get_request("machines/", **kwargs)

  def machine(self, id, **kwargs):
    """
    Returns the Machine with the specified id.
    """

    return self._api_query_get_request("machines/{}".format(id), **kwargs)

  def magnetic(self, _id, meta=""):
    """
    Returns a tuple of the corresponding User ID
    to the Magnetic ID provided (if it exists) and the
    APIRequest ID for this request.
    """

    response = self._post_request("magnetic", {
      "magnetic": _id,
      "meta": meta
    })

    return (response['user'], response['api_request'])


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

  def posters(self, **kwargs):
    """
    Returns the list of posters that
    match the specified search criteria.
    """

    return self._api_query_get_request("posters", **kwargs)

  def poster(self, id, **kwargs):
    """
    Returns the poster with the specified id.
    """

    return self._api_query_get_request("posters/{}".format(id), **kwargs)

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

  def rfid(self, _id, meta=""):
    """
    Returns a tuple of the corresponding User ID
    to the RFID provided (if it exists) and the
    APIRequest ID for this request.
    """

    response = self._post_request("rfid", {
      "rfid": _id,
      "meta": meta,
    })

    return (response['user'], response['api_request'])

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

  def sponsors(self, **kwargs):
    """
    Returns the list of sponsors that
    match the specified search criteria.
    """

    return self._api_query_get_request("sponsors", **kwargs)

  def sponsor(self, id, **kwargs):
    """
    Returns the sponsor with the specified id.
    """

    return self._api_query_get_request("sponsors/{}".format(id), **kwargs)

  def tshirts(self, **kwargs):
    """
    Returns the list of tshirts that
    match the specified search criteria.
    """

    return self._api_query_get_request("tshirts", **kwargs)

  def tshirt(self, id, **kwargs):
    """
    Returns the tshirt with the specified id.
    """

    return self._api_query_get_request("tshirts/{}".format(id), **kwargs)


  def users(self, **kwargs):
    """
    Returns the list of users that
    match the specified search criteria.
    """
    
    return self._api_query_get_request("users/", **kwargs)

  def user(self, id, **kwargs):
    """
    Returns the user with the specified id.
    """

    return self._api_query_get_request("users/{}/".format(id), **kwargs)

  def user_balance(self, user_id, amount, meta=""):
    """
    Changes the User's balance by the specified amount.
    This is a priveleged option and you likely
    do not have permission.
    """

    self._logger.debug("balance of {} ${}".format(user_id, amount))

    return self._post_request("users/{}/balance/".format(user_id), {
      'amount': content,
      'meta': meta,
    })

  def user_email(self, user_id, subject, content, meta=""):
    """
    Sends an email to the specified user.
    This is a priveleged option and you likely
    do not have permission.
    """

    self._logger.debug("Sending email to {} - {} | {}".format(user_id, subject, content))

    return self._post_request("users/{}/email/".format(user_id), {
      'subject': subject,
      'content': content,
      'meta': meta,
    })

  def user_rfid(self, user_id, rfid, meta=""):
    """
    Set the RFID for the specified user.
    This is a priveleged option and you likely
    do not have permission.
    """

    return self._post_request("users/{}/rfid/".format(user_id), {
      'rfid': rfid,
      'meta': meta,
    })

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

  def upcs(self, **kwargs):
    """
    Returns the list of UPCs that
    match the specified search criteria.
    """

    return self._api_query_get_request("upcs", **kwargs)

  def upc(self, id, **kwargs):
    """
    Returns the UPC with the specified id.
    """

    return self._api_query_get_request("upcs/{}".format(id), **kwargs)

  def get(self, url):
    """
    Request a resource using GET with authentication keys.
    """

    return self._get(url)


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
    return self._request(path, message, self._session.post)

  def _put_request(self, path, message):
    return self._request(path, message, self._session.put)

  def _request(self, path, message, request_method):
    self._logger.debug("request to {}".format(path))

    url = "{}/api/{}/".format(self._base_url, path)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    try:
      data = json.dumps(message)
    # Not JSON so just send it as is
    except ValueError:
      data = message

    response = request_method(url, data=data, headers=headers)

    self._check_response(response)

    return response.json(object_pairs_hook=collections.OrderedDict)

  def _check_response(self, response):
    if response.status_code != requests.codes.ok:
      raise requests.exceptions.HTTPError(response.json(), response=response)



class ChannelWebSocketClient(WebSocketClient):

  def __init__(self, channel_id, callback, public_key=None, private_key=None, base_url=None, *args, **kwargs):
    """
    WebSocketClient that calls the provided callback
    whenever the Channel object is saved.
    """

    if not base_url:
      base_url = "ws://roboticsclub.org:1984"

    url = "{}/channels/{}/".format(base_url, channel_id)

    if not public_key:
      public_key = os.environ.get('RC_PUBLIC_KEY')

    if not private_key:
      private_key = os.environ.get('RC_PRIVATE_KEY')

    headers = [
      ('PUBLIC_KEY', public_key),
      ('PRIVATE_KEY', private_key),
      ('API_CLIENT', '{} v{}'.format(__client__, __version__)),
    ]

    super().__init__(url, headers=headers, *args, **kwargs)

    self.received_message = callback



class APIRequestsWebSocketClient(WebSocketClient):

  def __init__(self, callback, public_key=None, private_key=None, base_url=None, *args, **kwargs):
    """
    WebSocketClient that calls the provided callback
    whenever an APIRequest object is saved.
    """

    if not base_url:
      base_url = "ws://roboticsclub.org:1984"

    url = "{}/api_requests/".format(base_url)

    if not public_key:
      public_key = os.environ.get('RC_PUBLIC_KEY')

    if not private_key:
      private_key = os.environ.get('RC_PRIVATE_KEY')

    headers = [
      ('PUBLIC_KEY', public_key),
      ('PRIVATE_KEY', private_key),
      ('API_CLIENT', '{} v{}'.format(__client__, __version__)),
    ]

    super().__init__(url, headers=headers, *args, **kwargs)

    self.received_message = callback
