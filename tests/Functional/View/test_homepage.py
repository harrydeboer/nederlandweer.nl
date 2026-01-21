import unittest
from django.test import Client


class HomepageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            "/?station=260&begin_year=1906&end_year=2025&type=temperature-day",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode("utf-8").find('zomerdag'), -1)
