#!/usr/bin/env python3

import unittest
from rc.clients import APIClient

class APIClientTestCase(unittest.TestCase):
  """Tests for APIClient."""

  def test_users(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.users()), 1)

  def test_projects(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.projects()), 1)

  def test_webcams(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.webcams()), 1)

  def test_officers(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.officers()), 1)

  def test_sponsors(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.sponsors()), 1)

  def test_channels(self):
    client = APIClient()

    self.assertGreaterEqual(len(client.channels()), 1)

  def test_faqs(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.faqs()), 1)

  def test_tshirts(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.tshirts()), 1)

  def test_social_medias(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.social_medias()), 1)

  def test_posters(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.posters()), 1)


if __name__ == '__main__':
  unittest.main()