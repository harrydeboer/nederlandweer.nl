import unittest
from django.test import Client


class RainTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/regen")

        self.assertEqual(response.status_code, 200)
