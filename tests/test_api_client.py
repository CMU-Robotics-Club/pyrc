#!/usr/bin/env python3

import unittest
from rc import APIClient

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

    # Might be 0 channels
    self.assertGreaterEqual(len(client.channels()), 0)

  def test_social_medias(self):
    client = APIClient()
    self.assertGreaterEqual(len(client.social_medias()), 1)

  def test_rfid_none(self):
    client = APIClient()
    
    # 1 is an invalid RFID so this should
    # be a result of None
    self.assertEqual(client.rfid(1), None)

  def test_magnetic_none(self):
    client = APIClient()

    # 1 is an invalid Magnetic ID so
    # this should return a result of None
    self.assertEqual(client.magnetic(1), None)

if __name__ == '__main__':
  unittest.main()