import unittest
from django.test import Client


class SunshineTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/zon")

        self.assertEqual(response.status_code, 200)
