from django.test import TestCase
from django.test import Client


class HomepageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
