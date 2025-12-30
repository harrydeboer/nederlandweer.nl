import unittest
from django.test import Client


class TropicalTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/tropisch")

        self.assertEqual(response.status_code, 200)
